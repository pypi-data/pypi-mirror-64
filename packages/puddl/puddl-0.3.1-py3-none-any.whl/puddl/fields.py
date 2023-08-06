from pathlib import Path
from django.db import models


class PathField(models.TextField):
    """
    Pathlib FTW! Saves absolute paths to DB.

    >>> class MyModel(models.Model):
            path = PathField()
    >>> x = MyModel()
    >>> type(x.path)
    pathlib.Path
    """

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return Path(value)

    def to_python(self, value):
        if isinstance(value, str) or value is None:
            return value
        abspath = value.resolve()
        return str(abspath)
