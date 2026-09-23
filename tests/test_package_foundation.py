"""Foundation checks for the public package boundary."""

import importlib.metadata

import abaqus_file_creator


def test_package_imports() -> None:
    assert abaqus_file_creator.__name__ == "abaqus_file_creator"


def test_package_has_no_modelling_api_yet() -> None:
    public_names = {
        name for name in vars(abaqus_file_creator) if not name.startswith("_")
    }

    assert public_names == set()


def test_distribution_metadata_is_source_of_version() -> None:
    assert importlib.metadata.version("abaqus-file-creator") == "0.1.0"
