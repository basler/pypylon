# AGENTS.md

Development guide for contributors and automated assistants working in this
repository.
pypylon is the official Python wrapper for the Basler pylon Camera Software
Suite, built with SWIG on top of the pylon C++ SDK. See [README.md](README.md)
for the project overview, installation, and quick-start examples.

## Repository map

| Path | Contents |
|---|---|
| `src/` | SWIG interface (`.i`) files — the binding definitions for `genicam`, `pylon`, `pylondataprocessing`. |
| `pypylon/` | Generated/packaged Python modules (build output; not edited by hand). |
| `generated/` | SWIG-generated C++/Python (build output). |
| `samples/` | Example scripts under `pylon/` and `pylondataprocessing/` (one folder per sample, `<name>/<name>.py`); shared helper modules in `common/`; shared image/data assets in `images/`. See [context/sample_style.md](context/sample_style.md) for layout and naming. |
| `samples_reference_pypylon/` | Reference ports of the C++ pylon samples. |
| `tests/` | Unit tests: `genicam/`, `pylon/{emulated,usb,gigE}/`, `pylondataprocessing/`. Entry point: `tests/all_tests.py`. |
| `scripts/` | Build/format helper scripts. |
| `context/` | Coding-style reference docs (see below). |
| `setup.py`, `pyproject.toml` | Build configuration. |

## Environment

Run all project Python commands inside the Python environment where pypylon is
built/installed, so they use the correct interpreter and the matching pylon SDK.
This file intentionally does not prescribe a specific environment manager
(venv, conda, uv, …) — activate whichever one you use before running commands.

Building from source additionally requires an installed pylon SDK, a C++
compiler, Python development headers, and SWIG 4.4 (see
[README.md](README.md#installation-from-source)).

## Common commands

Build and install for local development:
```bash
pip install -e .
# or, to (re)build in place after changing bindings:
python setup.py build
```

Run the tests the way CI does — `pytest` over the hardware-free
(Camera Emulation) suites:
```bash
pip install pytest numpy
pytest tests/genicam tests/pylon/emulated tests/pylondataprocessing
```

The tests are written with `unittest`, so `pytest` runs them natively. To run a
single test module or method:
```bash
pytest tests/pylon/emulated/parameter_test.py -v
pytest tests/pylon/emulated/parameter_test.py::ParameterTestSuite::test_parameter_construction_default -v
```

Tests import the **installed** pypylon, so rebuild/reinstall after changing
bindings before testing. The emulated suites above need no hardware. Other
suites do: `tests/pylon/usb` and `tests/pylon/gigE` require real cameras.
Control the Camera Emulation device count with `PYLON_CAMEMU` (e.g.
`PYLON_CAMEMU=1`).

> Without `pytest`, you can run the same `unittest`-based tests with the stdlib
> runner, e.g. `python -m unittest tests.pylon.emulated.parameter_test -v`. Note
> that `python tests/all_tests.py` discovers every `*test.py`, including the
> hardware-only `usb`/`gigE` suites.

## Changing the bindings

pypylon's API is generated from the SWIG interface (`.i`) files in `src/`;
`pypylon/` and `generated/` are build output. The change cycle is:

1. Edit the relevant `src/<module>/<Name>.i` — never the generated output.
2. Rebuild so the installed package reflects the change:
   ```bash
   pip install -e .   # or: python setup.py build
   ```
3. Run the test that covers that `.i` file (tests import the installed pypylon,
   so this must follow the rebuild):
   ```bash
   pytest tests/pylon/emulated/<name>_test.py -v
   ```
4. Add or extend that test to cover the public API the `.i` introduces; see
   [context/test_style.md](context/test_style.md).

## Code style

The authoritative rules are in the linked docs below; this is a quick reference.
Write idiomatic pypylon: prefer properties over getters (`camera.Width.Value`,
not `camera.Width.GetValue()`), use the pylon parameter API over the GenICam
node API, write parameter values through `.Value` (`camera.Gain.Value = 42`,
never `camera.Gain = 42`), guard optional access with `Try*` / `*OrDefault`, and
manage cameras and grab results with `with` blocks. Use `snake_case` /
`UPPER_SNAKE_CASE` and avoid abbreviations.

Read the relevant style doc in full before writing code:

| When you are… | Read |
|---|---|
| writing any pypylon code | [context/common_style.md](context/common_style.md) |
| adding or editing a sample | [context/sample_style.md](context/sample_style.md) |
| adding or editing a unit test | [context/test_style.md](context/test_style.md) |

`sample_style.md` and `test_style.md` build on `common_style.md`.
