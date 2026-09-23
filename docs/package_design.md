## Target package design

Use a normal Python package structure. Follows a `src/` layout with package name:

abaqus_file_creator

Do not rename the repository unless explicitly requested.

Keep these concerns separate:

- user/domain input models;
- I-section geometry;
- perforation geometry;
- meshing;
- materials;
- loads and boundary conditions;
- analysis-step definitions;
- Abaqus keyword/input-file serialization;
- optional execution/batch helpers.

Avoid global mutable state and module-level interactive `input()` calls.

Core functions should accept explicit arguments or typed configuration objects.

Use `pathlib` for filesystem paths. Never hard-code user-specific paths.

Do not require pandas/Excel in the core modelling API. If legacy spreadsheet
support is retained, keep it in an optional adapter layer.

Generated node numbering, element numbering, set ordering, and `.inp` output
must be deterministic.

The public API should eventually be exported deliberately from `__init__.py`.
Do not expose implementation internals accidentally.


## Documentation

Update README.md when a change affects:

- installation;
- public API;
- supported geometry;
- supported analysis types;
- user-visible defaults;
- required inputs; or
- generated output behaviour.

Keep detailed finite-element modelling requirements in a dedicated document
such as `docs/fea_requirements.md` rather than expanding AGENTS.md indefinitely.

Keep durable architectural decisions in `docs/` if they are important enough
that a future contributor must understand them.