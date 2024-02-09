import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Company(SqlAlchemyBase):
    __tablename__ = 'companies'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    short_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    full_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    pic_url = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    land_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("lands.id"))
    land = orm.relationship("Land", lazy='subquery')

    def __repr__(self):
        return (f'<Company> {self.id} {self.land} {self.short_name} {self.full_name} '
                f'{self.description} {self.pic_url}')
