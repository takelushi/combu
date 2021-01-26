"""Combu."""

from combu import _combu, definition, execution, generator, parallel

__version__ = '1.2.1'

Combu = _combu.Combu
CombuParallel = _combu.CombuParallel
ParallelExecutor = parallel.ParallelExecutor
Pack = definition.Pack
Unset = definition.Unset

execute = execution.execute
create_values = generator.create_values

exec = execute  # alias.  # noqa: A001
values = create_values  # alias.
