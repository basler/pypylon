"""Select matching SDK control files by version segment, then download them."""

import json
import os
from pathlib import Path
import re
import subprocess
import sys


def parse_version(value, release_tag=False):
    """Return decimal year/month/patch; pypylon patches do not select SDK patches."""
    suffix = r"(?:rc[0-9]+)?" if release_tag else ""
    match = re.fullmatch(r"([0-9]+)\.([0-9]+)(?:\.([0-9]+))?" + suffix, value)
    if match is None:
        raise ValueError(f"Invalid {'release tag' if release_tag else 'SDK version'}: {value!r}")
    year, month, patch = (int(part, 10) if part else 0 for part in match.groups())
    if not 1 <= month <= 12:
        raise ValueError(f"Invalid month in version: {value!r}")
    return year, month, patch


def select_control_files(paths, platforms, tag=None):
    """Select latest SDK patch/build per platform, with licenses in the same folder.

    Branch builds keep using the globally latest production SDK version.
    Release tags constrain year/month only, independently of the pypylon patch.
    """
    release_month = parse_version(tag, release_tag=True)[:2] if tag is not None else None
    paths = set(paths)
    reports = []
    for path in sorted(paths):
        parts = path.split("/")
        if len(parts) != 5 or parts[1] != "setup":
            continue
        repository, _, version_text, build_text, filename = parts
        if not repository.startswith("pylon-artifacts-generic-"):
            continue
        if tag is None and repository != "pylon-artifacts-generic-prod":
            continue
        if not filename.startswith("report_") or not filename.endswith(".json"):
            continue
        version = parse_version(version_text)
        if release_month is not None and version[:2] != release_month:
            continue
        if re.fullmatch(r"[0-9]{8}\.[0-9]+", build_text) is None:
            raise ValueError(f"Invalid SDK build directory: {path}")
        build = tuple(int(part, 10) for part in build_text.split("."))
        reports.append((version, build, path))

    if not reports:
        raise ValueError(f"No SDK reports found for {tag or 'latest production SDK'}")
    if tag is None:
        latest_version = max(report[0] for report in reports)
        reports = [report for report in reports if report[0] == latest_version]

    selections = {}
    for platform in platforms:
        candidates = []
        for version, build, path in reports:
            report_name = path.rsplit("/", 1)[1]
            stem = report_name[len("report_"):-len(".json")]
            if stem == platform or stem.startswith(platform + "_"):
                candidates.append((version, build, path))
        if not candidates:
            raise ValueError(f"No SDK report for {platform} ({tag or 'latest production SDK'})")
        latest = max((version, build) for version, build, _ in candidates)
        matches = [path for version, build, path in candidates if (version, build) == latest]
        if len(matches) != 1:
            raise ValueError(f"Ambiguous SDK reports for {platform}: {matches}")
        report = matches[0]
        directory, report_name = report.rsplit("/", 1)
        license_path = directory + "/oso_" + report_name[len("report_"):-len(".json")] + ".txt"
        if license_path not in paths:
            raise ValueError(f"Missing third-party license: {license_path}")
        selections[platform] = (report, license_path)
    return selections


def download_file(source, destination):
    """Fail on CLI errors, missing files and empty files, including no-op downloads."""
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        destination.unlink()
    subprocess.run(
        ["jf", "rt", "dl", "--flat=true", "--fail-no-op=true", source, str(destination)],
        check=True,
    )
    if not destination.is_file() or destination.stat().st_size == 0:
        raise ValueError(f"Download did not produce a nonempty file: {destination}")


def main():
    with open(".github/workflows/build_config.json", encoding="utf-8") as config_file:
        platforms = json.load(config_file)
    tag = os.environ.get("TAG_NAME")
    if tag is not None:
        parse_version(tag, release_tag=True)
    result = subprocess.run(
        ["jf", "rt", "s", "pylon-artifacts-generic-*/setup/*"],
        check=True, capture_output=True, text=True,
    )
    if result.stderr:
        print(result.stderr, file=sys.stderr, end="")
    artifacts = json.loads(result.stdout)
    selections = select_control_files([artifact["path"] for artifact in artifacts], platforms, tag)
    for platform, (report, license_path) in selections.items():
        version, build = report.split("/")[2:4]
        print(f"Downloading control files for {platform} using pylon {version}, build {build}", flush=True)
        download_file(report, Path(platform) / f"report_{platform}.json")
        download_file(license_path, Path(platform) / "pylon_Third-Party_Licenses.txt")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as error:
        print(f"Control file preparation failed: {error}", file=sys.stderr)
        sys.exit(1)
