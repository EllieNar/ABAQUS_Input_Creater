# Abaqus File Creator

Python package for generating deterministic Abaqus/Standard input files for
perforated thin-walled I-beams. The core package does not require Abaqus/CAE
or Excel.

The project currently contains the package foundation only. Geometry,
meshing, input-file generation, and analysis logic will be added in later
phases.

## Development environment

The supported Python version is 3.12. Create the development environment with:

```text
conda env create -f environment.yml
conda activate abaqus-file-creator
```

Run the foundation tests with:

```text
pytest
```
