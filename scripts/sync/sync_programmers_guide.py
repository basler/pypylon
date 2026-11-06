"""Transfer the Programmer's Guide between local and BPD Markdown layouts."""

import argparse
from dataclasses import dataclass
import html
from pathlib import Path
import posixpath
import re
import sys
from urllib.parse import quote, unquote, urlsplit, urlunsplit


ROOT = Path(__file__).resolve().parents[1]
BPD_URL = "https://docs.baslerweb.com/"
CHAPTERS = (
    "pypylon-introduction",
    "pypylon-installation-and-environment-setup",
    "pypylon-quick-start",
    "pypylon-core-concepts",
    "pypylon-discovering-and-selecting-cameras",
    "pypylon-image-acquisition",
    "pypylon-working-with-images",
    "pypylon-configuring-camera-parameters",
    "pypylon-triggered-image-acquisition",
    "pypylon-performance-optimization",
    "pypylon-error-handling-and-recovery",
    "pypylon-threading-and-concurrency",
    "pypylon-integration-with-opencv",
    "pypylon-multi-camera-systems",
    "pypylon-best-practices",
    "pypylon-troubleshooting",
    "pypylon-sample-code",
)
CHAPTER_NAME = re.compile(r"(?:\d+-)?(pypylon-[\w-]+)\.md$")
DEFINITION = re.compile(
    r"^ {0,3}\[([^\]\n]+)\]:[ \t]*(?:<([^>\n]+)>|(\S+))", re.MULTILINE
)
INLINE_LINK = re.compile(
    r"(?<!\\)!?\[(?:\\.|[^\[\]\\\n]|\[[^\[\]\n]*\])*\]"
    r"\([ \t]*(?:<([^>\n]+)>|((?:\\.|[^\s()\\]|\((?:\\.|[^()\\])*\))*))"
    r"(?=[ \t]*(?:\)|[\"']))"
)
HTML_LINK = re.compile(
    r"<[A-Za-z][^>]*?\b(?:href|src)\s*=\s*([\"'])(.*?)\1", re.IGNORECASE
)
TOC_ENTRY = re.compile(
    r"^\s*(\d+)\.\s+\[([^\]\n]+)\]\(([^)\n]+)\)\s*$", re.MULTILINE
)


class GuideError(ValueError):
    """An invalid guide or unsafe transfer request."""


@dataclass(frozen=True)
class Link:
    start: int
    end: int
    target: str
    line: int


def mask_code(text, inline=True):
    """Hide code without changing offsets or line numbers."""
    lines = []
    fence = None
    for line in text.splitlines(keepends=True):
        marker = re.match(r" {0,3}(`{3,}|~{3,})(.*)", line)
        if fence:
            lines.append(re.sub(r"[^\n]", " ", line))
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence):
                if not marker[2].strip():
                    fence = None
        elif marker:
            fence = marker[1]
            lines.append(re.sub(r"[^\n]", " ", line))
        elif line.startswith(("    ", "\t")):
            lines.append(re.sub(r"[^\n]", " ", line))
        else:
            lines.append(line)
    masked = "".join(lines)
    if inline:
        masked = re.sub(
            r"(`+)(?!`)(.*?)(?<!`)\1(?!`)",
            lambda match: re.sub(r"[^\n]", " ", match[0]),
            masked,
            flags=re.DOTALL,
        )
    return masked


def links(text):
    """Locate Markdown destinations and HTML href/src attributes outside code."""
    masked = mask_code(text)
    spans = []
    for pattern, groups in (
        (INLINE_LINK, (1, 2)),
        (DEFINITION, (2, 3)),
        (HTML_LINK, (2,)),
    ):
        for match in pattern.finditer(masked):
            group = next(group for group in groups if match[group] is not None)
            start, end = match.span(group)
            spans.append(Link(start, end, text[start:end], text.count("\n", 0, start) + 1))
    return sorted(spans, key=lambda link: link.start)


def identity(filename):
    match = CHAPTER_NAME.fullmatch(filename)
    return match[1] if match else None


def split_target(target):
    try:
        return urlsplit(html.unescape(target))
    except ValueError as error:
        raise GuideError(f"Invalid URL {target!r}: {error}") from error


def discover(directory):
    if not directory.is_dir():
        raise GuideError(f"Guide directory does not exist: {directory}")
    chapters = {}
    for path in sorted(directory.glob("*.md")):
        chapter = identity(path.name)
        if chapter:
            if chapter in chapters:
                raise GuideError(f"Duplicate chapter {chapter}: {chapters[chapter]} and {path.name}")
            chapters[chapter] = path.name
    if not chapters:
        raise GuideError(f"No pypylon chapters found in {directory}")
    return chapters


def read_order(local_dir):
    readme = local_dir / "README.md"
    if not readme.exists():
        return list(CHAPTERS)
    entries = list(TOC_ENTRY.finditer(mask_code(readme.read_text(encoding="utf-8"))))
    if not entries:
        raise GuideError(f"{readme}: no numbered chapter TOC found")
    order = []
    for index, entry in enumerate(entries, 1):
        target = split_target(entry[3])
        chapter = identity(unquote(target.path))
        if (
            int(entry[1]) != index
            or not chapter
            or target.path != f"{index:02d}-{chapter}.md"
            or target.scheme
            or target.netloc
            or target.fragment
            or target.query
            or chapter in order
        ):
            raise GuideError(f"{readme}: invalid or duplicate TOC entry: {entry[0].strip()}")
        order.append(chapter)
    return order


def require_chapters(chapters, order):
    missing = set(order) - set(chapters)
    unknown = set(chapters) - set(order)
    if missing or unknown:
        details = []
        if missing:
            details.append("missing chapters: " + ", ".join(sorted(missing)))
        if unknown:
            details.append("unknown chapters (add them to the local TOC): " + ", ".join(sorted(unknown)))
        raise GuideError("; ".join(details))


def navigation(names, index):
    previous = names[index - 1] if index else "README.md"
    following = f"[Next]({names[index + 1]})" if index + 1 < len(names) else ""
    return f"[Previous]({previous}) | [Contents](README.md) | {following}".rstrip()


def is_navigation(line):
    return bool(re.fullmatch(
        r"\s*(?:\[Previous\]\([^)]+\))?\s*\|\s*"
        r"(?:\[Contents\]\([^)]+\))?\s*\|\s*(?:\[Next\]\([^)]+\))?\s*",
        line,
    ))


def chapter_body(text):
    lines = text.strip("\n").splitlines(keepends=True)
    if lines and is_navigation(lines[0]):
        lines.pop(0)
        while lines and not lines[0].strip():
            lines.pop(0)
        if lines and lines[0].strip() == "---":
            lines.pop(0)
    while lines and not lines[0].strip():
        lines.pop(0)
    if lines and is_navigation(lines[-1]):
        lines.pop()
        while lines and not lines[-1].strip():
            lines.pop()
        if lines and lines[-1].strip() == "---":
            lines.pop()
    return "".join(lines).strip("\n") + "\n"


def product_page(path):
    """Only flat product topics, not API documentation or arbitrary assets."""
    return bool(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*(?:\.md)?", path))


def rewrite_target(target, mapping, exporting):
    parsed = split_target(target)
    path = unquote(parsed.path)
    product_url = (
        parsed.scheme == "https"
        and parsed.netloc == "docs.baslerweb.com"
        and product_page(path.lstrip("/"))
    )
    if parsed.scheme or parsed.netloc:
        if not product_url:
            return target
        path = path.lstrip("/")
        if not path.endswith(".md"):
            path += ".md"
        if not exporting and not identity(path):
            return target
    elif not path:
        return target

    basename = posixpath.basename(path)
    chapter = identity(basename)
    if chapter and path in (basename, "./" + basename):
        if chapter not in mapping:
            raise GuideError(f"Unknown chapter reference: {target}")
        replacement = mapping[chapter]
    elif exporting and basename == "README.md":
        raise GuideError(f"No BPD equivalent for contents-page body link: {target}")
    elif not exporting and path in (basename, "./" + basename) and product_page(basename):
        if basename.endswith(".md"):
            replacement = BPD_URL + basename[:-3]
        else:
            return target
    elif product_url:
        replacement = path
    else:
        return target
    converted = urlsplit(replacement)
    result = urlunsplit((
        converted.scheme,
        converted.netloc,
        quote(converted.path, safe="/-._~"),
        parsed.query,
        parsed.fragment,
    ))
    return result.replace("&", "&amp;") if "&amp;" in target else result


def rewrite_links(text, mapping, exporting):
    for link in reversed(links(text)):
        try:
            target = rewrite_target(link.target, mapping, exporting)
        except GuideError as error:
            raise GuideError(f"line {link.line}: {error}") from error
        text = text[:link.start] + target + text[link.end:]
    return text


def headings(text):
    masked = mask_code(text, inline=False)
    return re.finditer(r"^ {0,3}#{1,6}\s+(.+?)(?:\s+#+)?\s*$", masked, re.MULTILINE)


def title(text):
    heading = next(headings(text), None)
    if not heading:
        raise GuideError("Chapter has no Markdown heading")
    return heading[1]


def anchors(text):
    found = set()
    for heading in headings(text):
        label = html.unescape(heading[1])
        explicit = re.search(r"\s*\{#([^}]+)\}\s*$", label)
        if explicit:
            found.add(explicit[1])
            continue
        label = re.sub(r"!?\[([^\]]+)\]\([^)]+\)", r"\1", label)
        label = re.sub(r"<[^>]*>", "", label)
        slug = re.sub(r"[^\w\- ]", "", label.lower()).replace(" ", "-")
        candidate = slug
        suffix = 0
        while candidate in found:
            suffix += 1
            candidate = f"{slug}-{suffix}"
        found.add(candidate)
    for match in re.finditer(
        r"<[^>]+\b(?:id|name)\s*=\s*['\"]([^'\"]+)['\"]", mask_code(text)
    ):
        found.add(html.unescape(match[1]))
    return found


def reference_errors(text):
    masked = mask_code(text)
    definitions = {}
    errors = []
    for match in DEFINITION.finditer(masked):
        label = " ".join(match[1].lower().split())
        if label in definitions:
            errors.append((text.count("\n", 0, match.start()) + 1, f"duplicate reference [{match[1]}]"))
        definitions[label] = True
    without_definitions = DEFINITION.sub(lambda match: " " * len(match[0]), masked)
    for match in re.finditer(r"(?<!\\)!?\[([^\]\n]+)\]\[([^\]\n]*)\]", without_definitions):
        label = match[2] or match[1]
        if " ".join(label.lower().split()) not in definitions:
            errors.append((text.count("\n", 0, match.start()) + 1, f"undefined reference [{label}]"))
    return errors


def check_documents(documents, directory, layout, order):
    """Check a virtual representation, optionally resolving non-guide disk files."""
    errors = []
    external = set()
    names = [f"{index:02d}-{chapter}.md" for index, chapter in enumerate(order, 1)]
    expected_names = names if layout == "local" else [chapter + ".md" for chapter in order]
    for name in expected_names:
        if name not in documents:
            errors.append(f"{name}:1: missing chapter or noncanonical filename")
    if layout == "local":
        if "README.md" not in documents:
            errors.append("README.md:1: missing contents page")
        else:
            entries = list(TOC_ENTRY.finditer(mask_code(documents["README.md"])))
            if [entry[3] for entry in entries] != names:
                errors.append("README.md:1: TOC does not match chapter order")
            for index, entry in enumerate(entries, 1):
                if int(entry[1]) != index:
                    errors.append("README.md:1: TOC numbering is not sequential")
        for index, name in enumerate(names):
            if name in documents:
                nonempty = [line.strip() for line in documents[name].splitlines() if line.strip()]
                expected = navigation(names, index)
                if not nonempty or nonempty[0] != expected or nonempty[-1] != expected:
                    errors.append(f"{name}:1: incorrect header/footer navigation")
        if "README.md" in documents:
            nonempty = [line.strip() for line in documents["README.md"].splitlines() if line.strip()]
            expected = f"| | [Next]({names[0]})"
            if not nonempty or nonempty[0] != expected or nonempty[-1] != expected:
                errors.append("README.md:1: incorrect header/footer navigation")

    cache = {name: anchors(text) for name, text in documents.items()}
    for name, text in documents.items():
        for line, message in reference_errors(text):
            errors.append(f"{name}:{line}: {message}")
        if layout == "bpd" and any(is_navigation(line) for line in text.splitlines()):
            errors.append(f"{name}:1: local navigation is not allowed in BPD")
        for link in links(text):
            try:
                parsed = split_target(link.target)
            except GuideError as error:
                errors.append(f"{name}:{link.line}: {error}")
                continue
            if parsed.scheme or parsed.netloc:
                external.add(link.target)
                continue
            path = unquote(parsed.path)
            target_name = posixpath.normpath(path) if path else name
            chapter = identity(posixpath.basename(target_name))
            if chapter and target_name not in expected_names:
                errors.append(f"{name}:{link.line}: noncanonical or unknown chapter: {link.target}")
                continue
            if target_name not in cache:
                target_file = directory / target_name
                if target_file.is_file():
                    cache[target_name] = (
                        anchors(target_file.read_text(encoding="utf-8"))
                        if target_file.suffix == ".md" else set()
                    )
                elif layout == "bpd" and not chapter and product_page(target_name):
                    external.add(urlunsplit((
                        "https", "docs.baslerweb.com", "/" + target_name.removesuffix(".md"),
                        parsed.query, parsed.fragment,
                    )))
                    continue
                else:
                    errors.append(f"{name}:{link.line}: missing target: {link.target}")
                    continue
            fragment = unquote(parsed.fragment)
            if fragment and fragment not in cache[target_name]:
                errors.append(f"{name}:{link.line}: missing anchor: {link.target}")
    return errors, external


def build_documents(local_dir, bpd_dir, exporting):
    source = local_dir if exporting else bpd_dir
    order = read_order(local_dir)
    chapters = discover(source)
    require_chapters(chapters, order)
    names = [f"{index:02d}-{chapter}.md" for index, chapter in enumerate(order, 1)]
    mapping = {
        chapter: chapter + ".md" if exporting else names[index]
        for index, chapter in enumerate(order)
    }
    documents = {}
    titles = []
    for index, chapter in enumerate(order):
        body = chapter_body((source / chapters[chapter]).read_text(encoding="utf-8"))
        try:
            body = rewrite_links(body, mapping, exporting)
            titles.append(title(body))
        except GuideError as error:
            raise GuideError(f"{chapters[chapter]}: {error}") from error
        if not exporting:
            header = navigation(names, index)
            body = f"{header}\n\n---\n\n{body}\n---\n\n{header}\n"
        documents[mapping[chapter]] = body
    if not exporting:
        header = f"| | [Next]({names[0]})"
        toc = "\n".join(
            f"{index}. [{heading}]({name})"
            for index, (heading, name) in enumerate(zip(titles, names), 1)
        )
        documents["README.md"] = f"{header}\n\n---\n\n# Programmer's Guide\n\n{toc}\n\n---\n\n{header}\n"
    return documents, order


def transfer(local_dir, bpd_dir, exporting, overwrite=False, dry_run=False):
    if local_dir == bpd_dir or local_dir in bpd_dir.parents or bpd_dir in local_dir.parents:
        raise GuideError("Local and BPD directories must not overlap")
    destination = bpd_dir if exporting else local_dir
    if destination.exists() and not destination.is_dir():
        raise GuideError(f"Destination is not a directory: {destination}")
    documents, order = build_documents(local_dir, bpd_dir, exporting)
    obsolete = []
    if destination.exists():
        for path in destination.glob("*.md"):
            if identity(path.name) in order and path.name not in documents:
                obsolete.append(path)
    conflicts = [destination / name for name in documents if (destination / name).exists()] + obsolete
    if conflicts and not overwrite:
        raise GuideError("Destination files already exist; use --overwrite:\n" + "\n".join(map(str, conflicts)))
    for name in documents:
        path = destination / name
        if path.is_symlink() or (path.exists() and not path.is_file()):
            raise GuideError(f"Destination is not a regular file: {path}")
    for path in obsolete:
        if path.is_symlink() or not path.is_file():
            raise GuideError(f"Refusing to remove a non-regular file: {path}")
    errors, external = check_documents(
        documents, destination, "bpd" if exporting else "local", order
    )
    if errors:
        raise GuideError("Converted guide has invalid cross-references:\n" + "\n".join(errors))
    for name in documents:
        print(f"{'Would write' if dry_run else 'Write'} {destination / name}")
    for path in obsolete:
        print(f"{'Would remove' if dry_run else 'Remove'} {path}")
    report_external(external)
    if not dry_run:
        destination.mkdir(parents=True, exist_ok=True)
        for name, text in documents.items():
            (destination / name).write_text(text, encoding="utf-8")
        for path in obsolete:
            path.unlink()


def report_external(external):
    for target in sorted(external):
        print(f"Unchecked external URL: {target}")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for command in ("export", "import", "check"):
        subparser = commands.add_parser(command)
        subparser.add_argument("--local-dir", type=Path, default=ROOT / "docs/programmers_guide")
        subparser.add_argument("--bpd-dir", type=Path, default=ROOT / "docs/bpd")
        if command == "check":
            subparser.add_argument("--layout", choices=("local", "bpd"), default="local")
        else:
            subparser.add_argument("--overwrite", action="store_true")
            subparser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args(argv)
    local_dir = arguments.local_dir.resolve()
    bpd_dir = arguments.bpd_dir.resolve()
    try:
        if arguments.command == "check":
            directory = local_dir if arguments.layout == "local" else bpd_dir
            order = read_order(local_dir)
            chapters = discover(directory)
            require_chapters(chapters, order)
            documents = {
                name: (directory / name).read_text(encoding="utf-8")
                for name in chapters.values()
            }
            if arguments.layout == "local" and (directory / "README.md").is_file():
                documents["README.md"] = (directory / "README.md").read_text(encoding="utf-8")
            errors, external = check_documents(documents, directory, arguments.layout, order)
            report_external(external)
            if errors:
                raise GuideError("\n".join(errors))
            print(f"Cross-references OK: {len(chapters)} chapters ({arguments.layout})")
        else:
            transfer(
                local_dir, bpd_dir, arguments.command == "export",
                arguments.overwrite, arguments.dry_run,
            )
    except (GuideError, OSError, UnicodeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
