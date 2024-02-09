import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Land(SqlAlchemyBase):
    __tablename__ = 'lands'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def __repr__(self):
        return f'<Land> {self.id} {self.name}'
