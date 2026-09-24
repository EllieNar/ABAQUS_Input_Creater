# AGENTS.md

## Scope

This file applies to the entire repository:

/home/eleno/projects/abaqus_file_creater/

## File modification policy

Do not modify, delete, move, or rename existing repository files without
explicit user approval.

Codex may create and remove temporary files/directories required for its own
work (for example under `/tmp`) provided they are created by Codex for the
current task, are not pre-existing files, and are cleaned up afterwards.

Existing repository files must remain unchanged unless the user has explicitly approved changes.

Read-only inspection outside the repository is permitted when required,
including consulting external documentation.

Do not commit, push, rename the repository, or add production dependencies
unless explicitly requested.

Do not use CONTEXT.md as a transcript or reasoning log. Follow the guidance
at the start of CONTEXT.md for correct formatting.

## Project purpose

Develop a Python package in:

/home/eleno/projects/abaqus_file_creator/src/abaqus_file_creator/

that generates Abaqus/Standard `.inp` files without requiring Abaqus/CAE.

The target structures are perforated I-beams subjected to:

- buckling;
- three-point bending;
- four-point bending; or
- explicitly defined combined loading.

Web perforations may be:

- circular;
- rectangular; or
- rectangular with rounded corners.

Perforations are permitted only in the web.

The core package must not require Excel files or Abaqus GUI/Python modules.

It should generate deterministic Abaqus input text using ordinary Python.

## Sources of truth

Use sources in this order:

1. The user's requirements for the current task.
2. Current official Abaqus documentation for Abaqus syntax, element
   capabilities, analysis procedures, keyword behaviour, and version
   compatibility.
3. `moen_yao_rasmussen_selected_sections.pdf` for applicable finite-element
   modelling methodology.
4. Repository documentation in `docs/`.
5. Tests for implementation validation.

If changing an engineering modelling assumption, state the relevant source
and section/page in the implementation plan and request approval.

Do not silently extend conclusions from the reference PDF to problems it does
not address. In particular, bending-specific modelling assumptions must be
supported by appropriate literature and Abaqus documentation.

If sources disagree or a required modelling assumption is unspecified,
report the conflict or uncertainty before implementing it.

## Definition of done

A change is complete only when:

- it stays within the approved scope;
- relevant tests have been added or updated;
- all applicable tests pass;
- generated output is deterministic;
- engineering assumptions are documented;
- user-specific paths and hidden interactive inputs have not been introduced;
- public documentation is updated when required; and
- no unrelated refactoring has been included.

## Development environment

Use the Conda environment defined by `environment.yml`.

Create:

`conda env create -f environment.yml`

Activate:

`conda activate abaqus-file-creator`

Run tests:

`pytest`
