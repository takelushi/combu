"""Test __init__.py."""

import toml

import combu
from combu.combu import Combu, CombuParallel
from combu.definition import Pack, Unset
from combu.execution import execute
from combu.generator import create_values
from combu.parallel import ParallelExecutor


def test_version() -> None:
    """Test __version__."""
    pyproject = toml.load(open('pyproject.toml', 'r'))
    assert combu.__version__ == pyproject['tool']['poetry']['version']


def test_import_classes():
    """Test import classes."""
    assert combu.Combu == Combu
    assert combu.CombuParallel == CombuParallel
    assert combu.ParallelExecutor == ParallelExecutor
    assert combu.Unset == Unset
    assert combu.Pack == Pack


def test_import_methods():
    """Test import methods."""
    assert combu.create_values == create_values
    assert combu.execute == execute


def test_import_aliases():
    """Test import aliases."""
    assert combu.values == create_values
    assert combu.exec == execute
