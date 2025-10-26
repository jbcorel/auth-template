from server.core.repository import BaseRepository, UuidRepositoryMixin
from .entities import Department


class DepartmentRepository(UuidRepositoryMixin[Department], BaseRepository[Department]):
    model = Department
