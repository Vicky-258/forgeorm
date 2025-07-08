from typing import ClassVar

from forgeorm.core.db_manager import (
    delete_instance,
    fetch_all,
    fetch_filtered,
    save_instance,
)

from .fields import Field


class MetaInfo:
    def __init__(self, table_name, fields, primary_key):
        self.table_name = table_name
        self.fields = fields
        self.primary_key = primary_key

    def debug_print(self):
        print("Meta Info:")
        print(f"Table: {self.table_name}")
        print(f"Fields: {list(self.fields.keys())}")
        print(f"Primary Key: {self.primary_key}")


class ModelMeta(type):
    def __new__(cls, name, bases, attrs):
        fields = {}
        primary_key = None

        for attr_name, attr_value in list(attrs.items()):
            if isinstance(attr_value, Field):
                attr_value.name = attr_name
                if not attr_value.db_column:
                    attr_value.db_column = attr_name
                fields[attr_name] = attr_value

                if attr_value.primary_key:
                    if primary_key:
                        raise ValueError(f"Multiple primary keys in {name}")
                    primary_key = attr_name

        attrs["_meta"] = MetaInfo(
            table_name=name.lower(), fields=fields, primary_key=primary_key
        )

        return super().__new__(cls, name, bases, attrs)


class BaseModel(metaclass=ModelMeta):

    _meta: ClassVar[MetaInfo]

    def __init__(self, **kwargs):
        fields = self._meta.fields

        for field_name in fields:
            value = kwargs.get(field_name, fields[field_name].default)
            setattr(self, field_name, value)

    def __repr__(self):
        field_strings = [
            f"{name}={getattr(self, name)!r}" for name in self._meta.fields
        ]
        return f"<{self.__class__.__name__} {', '.join(field_strings)}>"

    def save(self):
        save_instance(self)

    @classmethod
    def all(cls):
        return fetch_all(cls)

    @classmethod
    def filter(cls, **kwargs):
        return fetch_filtered(cls, **kwargs)

    def delete(self):
        delete_instance(self)
