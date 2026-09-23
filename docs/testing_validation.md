## Testing and validation

The supported development environment uses Python 3.12 as defined in
`environment.yml`. The package can be installed from the repository with:

```text
python -m pip install ".[dev]"
```

Run the automated tests with:

```text
pytest
```

The same installation and test commands are used by the CI workflow.

Every substantive modelling change must include appropriate tests.

Prefer:

- unit tests for geometry and validation;
- mesh topology and mesh-quality tests;
- deterministic/golden `.inp` tests;
- tests for Abaqus keyword generation; and
- small integration models for representative analysis types.

Mesh tests should detect at least:

- duplicate node IDs;
- duplicate element IDs;
- missing connectivity;
- degenerate elements;
- elements crossing perforation boundaries;
- invalid element orientation; and
- unacceptable mesh-quality metrics.

Normal automated tests must not require an Abaqus licence.

Where an Abaqus executable is available, optional smoke tests may submit very
small generated input files. Such tests must be clearly separable from the
normal test suite.

Never report a test as passing unless it was actually run.

Once build/test/lint commands exist, keep their exact commands in this file.
