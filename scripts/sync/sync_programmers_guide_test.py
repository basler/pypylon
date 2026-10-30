"""Check SDK-independent guide conversion, CLI safety, and cross-references."""

from scripts import sync_programmers_guide as sync
from contextlib import redirect_stdout, redirect_stderr
import io
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


class GuideTransferTestSuite(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.local = self.root / "local"
        self.bpd = self.root / "bpd"
        self.bpd.mkdir()
        for index, chapter in enumerate(sync.CHAPTERS):
            body = f"# Chapter {index + 1}\n\n## Details\n\nText.\n"
            (self.bpd / f"{chapter}.md").write_text(body, encoding="utf-8")

    def run_cli(self, command, *arguments):
        with redirect_stdout(io.StringIO()) as output, redirect_stderr(io.StringIO()) as errors:
            status = sync.main([
                command, "--local-dir", str(self.local), "--bpd-dir", str(self.bpd),
                *arguments,
            ])
        return status, output.getvalue(), errors.getvalue()

    def assert_success(self, command, *arguments):
        status, output, errors = self.run_cli(command, *arguments)
        self.assertEqual(status, 0, errors)
        return output

    def test_import_export_round_trip(self):
        """Import restores local structure and export preserves BPD chapter bodies."""
        originals = {path.name: path.read_bytes() for path in self.bpd.iterdir()}
        self.assert_success("import")
        self.assert_success("check")
        first = self.local / "01-pypylon-introduction.md"
        last = self.local / "17-pypylon-sample-code.md"
        self.assertTrue(first.read_text().startswith("[Previous](README.md)"))
        self.assertTrue(last.read_text().endswith("[Contents](README.md) |\n"))
        self.assert_success("export", "--overwrite")
        self.assertEqual(originals, {path.name: path.read_bytes() for path in self.bpd.iterdir()})
        self.assert_success("check", "--layout", "bpd")
        self.assert_success("import", "--overwrite")
        self.assert_success("export", "--overwrite")
        self.assertEqual(originals, {path.name: path.read_bytes() for path in self.bpd.iterdir()})

    def test_links_code_anchors_and_external_topics(self):
        """Destinations are adapted while labels, titles, code, and API URLs survive."""
        chapter = self.bpd / f"{sync.CHAPTERS[0]}.md"
        body = """# Intro

[Inline](pypylon-core-concepts.md?view=full#details "Title")
[Reference][target]
![Image][target]
[target]: <pypylon-core-concepts.md#details> 'Title'
<a href="pypylon-core-concepts.md#details">HTML</a>
[Camera](cameras.md#models)
[API](https://docs.baslerweb.com/pylonapi/cpp)
[Website](https://example.com/a_(b)?x=1&y=2)
[Duplicate](#repeated-1)
[Explicit](#custom)
[HTML anchor](#named)
[Encoded](#some-heading)
[Short]
[Short]: #intro

## Repeated
## Repeated
## With ID {#custom}
## Some `heading`
<a name="named"></a>

---

`[Not a link](missing.md)`
```python
# Fake heading
[Not a link](missing.md#invalid)
```
"""
        chapter.write_text(body, encoding="utf-8")
        self.assert_success("import")
        self.assert_success("check")
        imported = (self.local / "01-pypylon-introduction.md").read_text()
        self.assertIn('04-pypylon-core-concepts.md?view=full#details "Title"', imported)
        self.assertIn('href="04-pypylon-core-concepts.md#details"', imported)
        self.assertIn("<04-pypylon-core-concepts.md#details> 'Title'", imported)
        self.assertIn("https://docs.baslerweb.com/cameras#models", imported)
        self.assertIn("[Not a link](missing.md#invalid)", imported)
        self.assert_success("export", "--overwrite")
        self.assertEqual(chapter.read_text(), body)

    def test_custom_toc_order(self):
        """An existing TOC controls import numbering and navigation."""
        self.assert_success("import")
        order = list(sync.CHAPTERS)
        order[0], order[1] = order[1], order[0]
        toc = "# Programmer's Guide\n\n" + "\n".join(
            f"{index}. [Title]({index:02d}-{chapter}.md)"
            for index, chapter in enumerate(order, 1)
        )
        (self.local / "README.md").write_text(toc)
        self.assert_success("import", "--overwrite")
        self.assertFalse((self.local / "01-pypylon-introduction.md").exists())
        self.assertTrue((self.local / "02-pypylon-introduction.md").exists())
        self.assert_success("check")

    def test_mixed_bpd_input_and_unrelated_files(self):
        """Mixed BPD names import successfully and unrelated product files remain intact."""
        first = self.bpd / "pypylon-introduction.md"
        first.rename(self.bpd / "01-pypylon-introduction.md")
        unrelated = self.bpd / "cameras.md"
        unrelated.write_text("# Camera\n")
        status, _, errors = self.run_cli("check", "--layout", "bpd")
        self.assertEqual(status, 1)
        self.assertIn("noncanonical", errors)
        self.assert_success("import")
        self.assert_success("export", "--overwrite")
        self.assertFalse((self.bpd / "01-pypylon-introduction.md").exists())
        self.assertTrue(first.exists())
        self.assertEqual(unrelated.read_text(), "# Camera\n")

    def test_overwrite_refusal_and_dry_run(self):
        """Overwrite is explicit and dry run never changes or creates destination files."""
        self.assert_success("import", "--dry-run")
        self.assertFalse(self.local.exists())
        self.assert_success("import")
        original = {path.name: path.read_bytes() for path in self.local.iterdir()}
        status, _, errors = self.run_cli("import")
        self.assertEqual(status, 1)
        self.assertIn("--overwrite", errors)
        self.assert_success("import", "--overwrite", "--dry-run")
        self.assertEqual(original, {path.name: path.read_bytes() for path in self.local.iterdir()})

    def test_invalid_output_blocks_all_writes(self):
        """Broken chapter targets and fragments block the whole transfer with line diagnostics."""
        path = self.bpd / "pypylon-introduction.md"
        for target in ("pypylon-absent.md", "pypylon-core-concepts.md#absent", "missing.png"):
            with self.subTest(target=target):
                path.write_text(f"# Intro\n\n[Broken]({target})\n")
                status, _, errors = self.run_cli("import")
                self.assertEqual(status, 1)
                self.assertIn(target, errors)
                self.assertFalse(self.local.exists())

    def test_duplicate_missing_and_unknown_chapters(self):
        """Chapter discovery rejects ambiguity and incomplete or unknown chapter sets."""
        duplicate = self.bpd / "01-pypylon-introduction.md"
        duplicate.write_text("# Duplicate\n")
        status, _, errors = self.run_cli("import")
        self.assertEqual(status, 1)
        self.assertIn("Duplicate chapter", errors)
        duplicate.unlink()
        unknown = self.bpd / "pypylon-unknown.md"
        unknown.write_text("# Unknown\n")
        status, _, errors = self.run_cli("import")
        self.assertEqual(status, 1)
        self.assertIn("unknown chapters", errors)
        unknown.unlink()
        (self.bpd / "pypylon-introduction.md").unlink()
        status, _, errors = self.run_cli("import")
        self.assertEqual(status, 1)
        self.assertIn("missing chapters", errors)

    def test_contents_body_link_blocks_export(self):
        """A body reference to README is rejected rather than silently removed."""
        self.assert_success("import")
        path = self.local / "01-pypylon-introduction.md"
        path.write_text(path.read_text().replace("Text.", "[TOC](README.md)."))
        status, _, errors = self.run_cli("export", "--overwrite")
        self.assertEqual(status, 1)
        self.assertIn("No BPD equivalent", errors)
        self.assertEqual((self.bpd / "pypylon-introduction.md").read_text(), "# Chapter 1\n\n## Details\n\nText.\n")

    def test_checker_navigation_toc_and_reference_failures(self):
        """Check detects bad navigation, broken references, duplicate IDs, and TOC targets."""
        self.assert_success("import")
        path = self.local / "01-pypylon-introduction.md"
        path.write_text(path.read_text().replace(
            "[Previous](README.md)", "[Previous](02-pypylon-installation-and-environment-setup.md)", 1
        ).replace("Text.", "[Broken][missing]\n\n[id]: #details\n[id]: #details"))
        status, _, errors = self.run_cli("check")
        self.assertEqual(status, 1)
        self.assertIn("incorrect header/footer", errors)
        self.assertIn("undefined reference", errors)
        self.assertIn("duplicate reference", errors)
        readme = self.local / "README.md"
        readme.write_text(readme.read_text().replace("1. [", "2. [", 1))
        status, _, errors = self.run_cli("check")
        self.assertEqual(status, 1)
        self.assertIn("invalid or duplicate TOC", errors)

    def test_external_reporting_and_available_bpd_topic(self):
        """Offline checks report external topics but validate available product-page anchors."""
        path = self.bpd / "pypylon-introduction.md"
        path.write_text("# Intro\n\n[Camera](cameras.md#models)\n")
        output = self.assert_success("check", "--layout", "bpd")
        self.assertIn("Unchecked external URL: https://docs.baslerweb.com/cameras#models", output)
        (self.bpd / "cameras.md").write_text("# Camera\n")
        status, _, errors = self.run_cli("check", "--layout", "bpd")
        self.assertEqual(status, 1)
        self.assertIn("missing anchor", errors)

    def test_overlap_and_symlinks(self):
        """Transfers reject overlapping directories and destination symlinks."""
        with self.assertRaisesRegex(sync.GuideError, "must not overlap"):
            sync.transfer(self.bpd, self.bpd / "nested", True)
        self.local.mkdir()
        target = self.root / "unrelated.md"
        target.write_text("# Unrelated\n")
        (self.local / "01-pypylon-introduction.md").symlink_to(target)
        status, _, errors = self.run_cli("import", "--overwrite")
        self.assertEqual(status, 1)
        self.assertIn("regular file", errors)
        self.assertEqual(target.read_text(), "# Unrelated\n")

    def test_script_from_another_working_directory(self):
        """Explicit directories work when the script is launched outside the repository."""
        result = subprocess.run(
            [sys.executable, str(sync.ROOT / "scripts/sync_programmers_guide.py"),
             "import", "--local-dir", str(self.local), "--bpd-dir", str(self.bpd)],
            cwd=self.root, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_absolute_chapter_links_and_escaped_markdown(self):
        """Absolute guide URLs are localized and escaped Markdown is left untouched."""
        path = self.bpd / "pypylon-introduction.md"
        path.write_text(
            "# Intro\n\n"
            "[Chapter](https://docs.baslerweb.com/pypylon-core-concepts#details)\n"
            "\\[Not a link](absent.md)\n"
            "![Nested [label]](pypylon-core-concepts.md#details)\n"
        )
        self.assert_success("import")
        imported = (self.local / "01-pypylon-introduction.md").read_text()
        self.assertIn("[Chapter](04-pypylon-core-concepts.md#details)", imported)
        self.assertIn("\\[Not a link](absent.md)", imported)
        self.assertIn("![Nested [label]](04-pypylon-core-concepts.md#details)", imported)

    def test_malformed_url_and_undefined_image_reference(self):
        """Malformed URLs and missing image references produce explicit diagnostics."""
        path = self.bpd / "pypylon-introduction.md"
        path.write_text("# Intro\n\n[Invalid](https://[broken)\n![Image][missing]\n")
        status, _, errors = self.run_cli("check", "--layout", "bpd")
        self.assertEqual(status, 1)
        self.assertIn("Invalid URL", errors)
        self.assertIn("undefined reference [missing]", errors)
        status, _, errors = self.run_cli("import")
        self.assertEqual(status, 1)
        self.assertIn("Invalid URL", errors)
        self.assertFalse(self.local.exists())

    def test_nonregular_obsolete_destination_blocks_writes(self):
        """Preflight rejects obsolete chapter directories before any chapters are written."""
        self.local.mkdir()
        (self.local / "pypylon-introduction.md").mkdir()
        status, _, errors = self.run_cli("import", "--overwrite")
        self.assertEqual(status, 1)
        self.assertIn("non-regular file", errors)
        self.assertEqual(len(list(self.local.iterdir())), 1)


if __name__ == "__main__":
    unittest.main()
