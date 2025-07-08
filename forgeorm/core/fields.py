class Field:
    def __init__(
        self,
        *,
        primary_key=False,
        nullable=True,
        default=None,
        unique=False,
        db_column=None,
    ):
        self.primary_key = primary_key
        self.nullable = nullable
        self.default = default
        self.unique = unique
        self.db_column = db_column
        self.name = None

    def get_sql_type(self, db_engine="sqlite"):
        raise NotImplementedError("Subclasses must implement get_sql_type()")

    def __repr__(self):
        return (
            f"<{self.__class__.__name__} (column={self.db_column},"
            f"pk={self.primary_key})>"
        )


class IntegerField(Field):
    def get_sql_type(self, db_engine="sqlite"):
        return "INTEGER"


class CharField(Field):
    def __init__(self, *, max_length=255, **kwargs):
        super().__init__(**kwargs)
        self.max_length = max_length

    def get_sql_type(self, db_engine="sqlite"):
        return f"VARCHAR({self.max_length})"


class BooleanField(Field):
    def get_sql_type(self, db_engine="sqlite") -> str:
        return "BOOLEAN"


class FloatField(Field):
    def get_sql_type(self, db_engine="sqlite") -> str:
        return "REAL"  # For SQLite; PostgreSQL adapter can override later


class TextField(Field):
    def get_sql_type(self, db_engine="sqlite") -> str:
        return "TEXT"


class DateField(Field):
    def get_sql_type(self, db_engine="sqlite") -> str:
        return "DATE"


class DateTimeField(Field):
    def get_sql_type(self, db_engine="sqlite") -> str:
        return "DATETIME"
