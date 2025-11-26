from forgeorm.core.base_model import BaseModel
from forgeorm.core.fields import *


class Book(BaseModel):
    id = IntegerField(primary_key=True)
    title = CharField(max_length=100, nullable=False)
    description = TextField()
    published = BooleanField(default=False)
    rating = FloatField(default=4.5)
    release_date = DateField()
    last_updated = DateTimeField()

