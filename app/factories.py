import factory
from factory import LazyAttribute
from factory.fuzzy import FuzzyText

from app.database import SessionLocal
from app.models import ModelUser


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = ModelUser
        sqlalchemy_session = SessionLocal()
        sqlalchemy_get_or_create = ("name",)
        sqlalchemy_session_persistence = "commit"

    name = FuzzyText(length=6)
    password = FuzzyText(length=256)