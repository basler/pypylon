# Helper scripts
| Script File                     | Description                                                      |
|---------------------------------|------------------------------------------------------------------|
| synch_programmers_guide.py      | Synchronize pypylon docs and bpd.                                |
| synch_programmers_guide_test.py | Unit test for the sync'ing script.                               |

## Synchronizing the Programmer's Guide

Use the standalone, standard-library script to transfer the guide between
`../../docs/programmers_guide` and the BPD Markdown folder (default `docs/bpd`):

```console
python scripts/sync_programmers_guide.py export --dry-run
python scripts/sync_programmers_guide.py export --overwrite
python scripts/sync_programmers_guide.py import --overwrite
python scripts/sync_programmers_guide.py check
python scripts/sync_programmers_guide.py check --layout bpd
```

Both directory defaults are relative to the repository, not the working
directory. All commands accept `--local-dir PATH` and `--bpd-dir PATH`.
Transfers refuse existing destination chapters unless `--overwrite` is given;
`--dry-run` performs the same preflight without writing. Unrelated files are
left alone. Existing alternative numbered names for transferred chapters are
removed only with `--overwrite`.

Export removes chapter-number prefixes and the local TOC/header/footer
navigation. Import restores them using the existing local `../../README.md` TOC order,
or the current 17-chapter order if there is no local README. Add new chapters to
the local TOC before importing them; missing or ambiguous chapters are errors.
Chapter links and fragments are adapted in both directions. BPD-only topic links
become absolute `https://docs.baslerweb.com/` URLs locally and relative `.md`
links on export; API documentation and other websites remain external. A body
link to the local README cannot be exported because BPD has no contents page.

`check` validates chapter filenames, TOC/navigation, file targets, Markdown
heading fragments, explicit HTML anchors, and reference-style links. Transfers
also check the converted guide before writing. Errors include file/line
diagnostics and return a nonzero exit status. Checking is offline: external URLs
(including unavailable non-guide BPD topics) are reported as unchecked, not
fetched. The current mixed numbered/unnumbered BPD input can be imported, but
`check --layout bpd` requires canonical unnumbered chapter filenames.

Run the script's SDK-independent tests with:

```console
python -m unittest discover -s tests/scripts -p '*_test.py'
```

