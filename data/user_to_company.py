import sqlalchemy
from .db_session import SqlAlchemyBase


class UserCompany(SqlAlchemyBase):
    __tablename__ = 'user_company'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer)
    company = sqlalchemy.Column(sqlalchemy.String)

    def __repr__(self):
        return f'<UC> {self.id} {self.user_id} {self.company}'
