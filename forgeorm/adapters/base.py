from abc import ABC, abstractmethod


class BaseAdapter(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def create_table(self, model_cls):
        pass

    @abstractmethod
    def drop_table(self, model_cls):
        pass

    @abstractmethod
    def create_table_sql(self, model_cls) -> str:
        pass

    @abstractmethod
    def _format_default(self, value):
        pass
