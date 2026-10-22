"""Check SDK version selection and fail-fast control file downloads without a network."""

from prepare_control_files import download_file, main, parse_version, select_control_files

from contextlib import redirect_stdout
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch


def artifact_pair(version="26.09.2", build="20261001.4", platform="linux_aarch64",
                  repository="pylon-artifacts-generic-prod"):
    directory = f"{repository}/setup/{version}/{build}"
    return [f"{directory}/report_{platform}.json", f"{directory}/oso_{platform}.txt"]


class PrepareControlFilesTestSuite(unittest.TestCase):
    # ------------------------------------------------------------------
    # Version and build selection
    # ------------------------------------------------------------------

    def test_release_tag_normalization(self):
        """Unpadded months, pypylon patches and RC tags select the same SDK month."""
        paths = artifact_pair()
        for tag in ("26.9", "26.09", "26.9.1", "26.9rc1", "26.9.1rc2"):
            with self.subTest(tag=tag):
                self.assertEqual(select_control_files(paths, ["linux_aarch64"], tag),
                                 {"linux_aarch64": tuple(paths)})

    def test_invalid_versions(self):
        """Malformed versions and invalid months fail instead of becoming patterns."""
        for value in ("26x9", "26.0", "26.13", "", "26.9.*", "26.9rc", "v26.9"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                parse_version(value, release_tag=True)

    def test_build_date_does_not_match_tag(self):
        """An August build cannot make an unrelated SDK version match tag 26.8."""
        with self.assertRaisesRegex(ValueError, "No SDK reports"):
            select_control_files(artifact_pair("26.07.1", "20260819.1"), ["linux_aarch64"], "26.8")

    def test_august_version_matches_numerically(self):
        """Tag 26.8 matches SDK 26.08.1 even when its build is in October."""
        paths = artifact_pair("26.08.1")
        self.assertEqual(select_control_files(paths, ["linux_aarch64"], "26.8")["linux_aarch64"],
                         tuple(paths))

    def test_highest_patch_then_highest_build(self):
        """SDK patch and build counters are ordered numerically, not lexically."""
        expected = artifact_pair("26.09.10", "20261001.10")
        paths = (artifact_pair("26.09.2", "20261231.99")
                 + artifact_pair("26.09.10", "20261001.9") + expected
                 + artifact_pair("26.10.1", "20261002.1"))
        self.assertEqual(select_control_files(paths, ["linux_aarch64"], "26.9")["linux_aarch64"],
                         tuple(expected))

    def test_platforms_select_their_own_latest_patch(self):
        """Each platform selects its highest available patch in the release month."""
        linux = artifact_pair()
        macos = artifact_pair("26.09.1", platform="macos_arm64")
        windows = artifact_pair(platform="windows_AMD64")
        self.assertEqual(select_control_files(linux + macos + windows,
                                             ["linux_aarch64", "macos", "windows"], "26.9"),
                         {"linux_aarch64": tuple(linux), "macos": tuple(macos),
                          "windows": tuple(windows)})

    def test_branch_uses_latest_production_version(self):
        """Branch builds ignore non-production repositories and select latest version."""
        expected = artifact_pair("26.10.1")
        paths = artifact_pair() + expected + artifact_pair(
            "26.11.1", repository="pylon-artifacts-generic-test")
        self.assertEqual(select_control_files(paths, ["linux_aarch64"])["linux_aarch64"],
                         tuple(expected))

    def test_missing_platform_does_not_fall_back_on_branch(self):
        """A missing platform in the latest production SDK fails explicitly."""
        paths = artifact_pair() + artifact_pair("26.10.1", platform="windows_AMD64")
        with self.assertRaisesRegex(ValueError, "No SDK report for linux_aarch64"):
            select_control_files(paths, ["linux_aarch64"])

    def test_no_reports(self):
        """An empty search result fails immediately."""
        with self.assertRaisesRegex(ValueError, "No SDK reports"):
            select_control_files([], ["linux_aarch64"], "26.9")

    def test_license_must_share_report_directory(self):
        """A license from an older build cannot complete the selected report."""
        paths = artifact_pair("26.09.2", "20261001.3") + artifact_pair()[:1]
        with self.assertRaisesRegex(ValueError, "Missing third-party license"):
            select_control_files(paths, ["linux_aarch64"], "26.9")

    def test_ambiguous_reports_fail(self):
        """Multiple matching reports cannot silently overwrite the control file."""
        paths = artifact_pair(platform="macos_arm64") + artifact_pair(platform="macos_x64")
        with self.assertRaisesRegex(ValueError, "Ambiguous SDK reports"):
            select_control_files(paths, ["macos"], "26.9")

    def test_invalid_build_fails(self):
        """Malformed build directories are rejected explicitly."""
        with self.assertRaisesRegex(ValueError, "Invalid SDK build"):
            select_control_files(artifact_pair(build="latest"), ["linux_aarch64"], "26.9")

    # ------------------------------------------------------------------
    # Downloads and CLI integration
    # ------------------------------------------------------------------

    def test_missing_or_empty_download_fails(self):
        """A successful CLI exit alone is insufficient, even with stale local files."""
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "report.json"
            destination.write_text("stale", encoding="utf-8")
            with patch("prepare_control_files.subprocess.run"):
                with self.assertRaisesRegex(ValueError, "nonempty file"):
                    download_file("source", destination)
            with patch("prepare_control_files.subprocess.run",
                       side_effect=lambda *args, **kwargs: destination.touch()):
                with self.assertRaisesRegex(ValueError, "nonempty file"):
                    download_file("source", destination)

    def test_successful_download(self):
        """The downloader requires a nonempty file and enables JFrog no-op errors."""
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "report.json"
            with patch("prepare_control_files.subprocess.run",
                       side_effect=lambda *args, **kwargs: destination.write_text("{}")) as run:
                download_file("source", destination)
            self.assertIn("--fail-no-op=true", run.call_args.args[0])
            self.assertTrue(run.call_args.kwargs["check"])

    def test_cli_failure_propagates(self):
        """JFrog download failures are not swallowed."""
        with tempfile.TemporaryDirectory() as directory:
            with patch("prepare_control_files.subprocess.run",
                       side_effect=subprocess.CalledProcessError(1, "jf")):
                with self.assertRaises(subprocess.CalledProcessError):
                    download_file("source", Path(directory) / "report.json")

    def test_main_searches_and_downloads_selected_pair(self):
        """The entry point wires the tag, artifact search and normalized output paths."""
        paths = artifact_pair()
        result = subprocess.CompletedProcess([], 0, json.dumps([{"path": p} for p in paths]), "")
        with patch.dict(os.environ, {"TAG_NAME": "26.9"}):
            with patch("prepare_control_files.open", unittest.mock.mock_open(
                    read_data='{"linux_aarch64": {}}')):
                with patch("prepare_control_files.subprocess.run", return_value=result):
                    with patch("prepare_control_files.download_file") as download:
                        with redirect_stdout(io.StringIO()) as output:
                            main()
        self.assertEqual(download.call_args_list, [
            unittest.mock.call(paths[0], Path("linux_aarch64/report_linux_aarch64.json")),
            unittest.mock.call(paths[1], Path("linux_aarch64/pylon_Third-Party_Licenses.txt")),
        ])
        self.assertIn("pylon 26.09.2, build 20261001.4", output.getvalue())


if __name__ == "__main__":
    unittest.main()
