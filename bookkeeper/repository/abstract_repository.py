"""
Модуль содержит описание абстрактного репозитория

Репозиторий реализует хранение объектов, присваивая каждому объекту уникальный
идентификатор в атрибуте pk (primary key). Объекты, которые могут быть сохранены
в репозитории, должны поддерживать добавление атрибута pk и не должны
использовать его для иных целей.
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Protocol, Any, List


class Model(Protocol):  # pylint: disable=too-few-public-methods
    """
    Модель должна содержать атрибут pk
    """
    pk: int


T = TypeVar('T', bound=Model)


class AbstractRepository(ABC, Generic[T]):
    """
    Абстрактный репозиторий.
    Абстрактные методы:
    add
    get
    get_all
    update
    delete
    """

    def __init__(self):
        self._data: List[T] = []

    def add(self, obj: T) -> int:
        """
        Добавить объект в репозиторий, вернуть id объекта,
        также записать id в атрибут pk.
        """
        # Предполагаем, что объекты имеют атрибут pk
        if hasattr(obj, 'pk'):
            obj.pk = len(self._data)  # Простой способ генерации id
            self._data.append(obj)
            return obj.pk
        else:
            raise AttributeError("Объект должен иметь атрибут 'pk'")

    def get(self, pk: int) -> T | None:
        """ Получить объект по id """
        for obj in self._data:
            #есть ли такой атрибут
            if hasattr(obj, 'pk') and obj.pk == pk:
                return obj
        return None

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        """
        Получить все записи по некоторому условию
        where - условие в виде словаря {'название_поля': значение}
        если условие не задано (по умолчанию), вернуть все записи
        """
        if where is None:
            return self._data
        else:
            return [obj for obj in self._data if all(getattr(obj, field) == value for field, value in where.items())]

    def update(self, obj: T) -> None:
        """ Обновить данные об объекте. Объект должен содержать поле pk. """
        if hasattr(obj, 'pk'):
            for i, item in enumerate(self._data):
                if hasattr(item, 'pk') and item.pk == obj.pk:
                    self._data[i] = obj
                    break
        else:
            raise AttributeError("Объект должен иметь атрибут 'pk'")

    def delete(self, pk: int) -> None:
        """ Удалить запись """
        self._data = [obj for obj in self._data if not hasattr(obj, 'pk') or obj.pk != pk]
