"""Тестовый модуль для unit_of_work"""

import pytest
from my_hm.domain.unit_of_work import UnitOfWork


def test_unit_of_work_is_abstract():
    """Попытка реализовать абстрактный класс UnitOfWork"""
    with pytest.raises(TypeError):
        UnitOfWork()

    assert hasattr(UnitOfWork, "__enter__")
    assert hasattr(UnitOfWork, "__exit__")
    assert hasattr(UnitOfWork, "commit")
    assert hasattr(UnitOfWork, "rollback")
