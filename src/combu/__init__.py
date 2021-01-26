"""Combu."""

from combu.combu import Combu, CombuParallel
from combu.definition import Pack, Unset
from combu.execution import execute
from combu.generator import create_values
from combu.parallel import ParallelExecutor

__version__ = '1.2.0'

Combu = Combu
CombuParallel = CombuParallel
ParallelExecutor = ParallelExecutor

Pack = Pack
Unset = Unset

create_values = create_values
execute = execute
exec = execute  # alias.  # noqa: A001
values = create_values  # alias.
