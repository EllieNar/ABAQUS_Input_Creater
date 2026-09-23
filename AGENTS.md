# AGENTS.md

## Scope

This file applies to the entire repository:

/home/eleno/projects/abaqus_file_creater/

Do not write, delete, move, or create files outside this repository.
Read-only access to external documentation and reference material is allowed
when required for the task.

For every new modification task:
1. Inspect the relevant code and references.
2. Produce an implementation and validation plan.
3. That plan must list which files will changed (full path).
4. Do not modify repository files until the user explicitly approves that plan.
5. Once approved, execute the approved plan without requesting permission for
   each individual file.

Do not commit, push, rename the repository, or add production dependencies
unless explicitly requested.

Do not use CONTEXT.md as a transcript or reasoning log. See heading ## in CONTEXT.md for guidance.

## Project purpose

Develop a Python package in /home/eleno/projects/abaqus_file_creater/src/abaqus_file_creater
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
3. The reference pdf `moen_yao_rasmussen_selected_sections.pdf` for finite-element modelling
   methodology applicable to this project.
4. Repository documentation (all .md files in docs folder)
5. Any applicable tests.

If changing an engineering modelling assumption, state the relevant source
and section/page in the implementation plan. Ask for approval.

Do not silently extend conclusions from the reference PDF to problems it does
not address. In particular, bending-specific modelling assumptions must be
supported by appropriate literature and Abaqus documentation.

If the sources disagree or a required modelling assumption is not specified,
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

## Development and environment

Use the Conda environment defined by 'environment.yml'.
Create:     'conda env create -f environment.yml'
Activate:   'conda activate abaqus-file-creator'
Run tests:  'pytest'