__author__ = 'ramin'
from flask import json
from peewee import Model, MySQLDatabase, Field, SQL
import env

__author__ = 'ramin'

mysql_db = MySQLDatabase(env.DB_DATABASE, user=env.DB_USERNAME, password=env.DB_PASSWORD,
                         host=env.DB_HOST, port=env.DB_PORT)


class BaseModel(Model):
    class Meta:
        database = mysql_db

    # def __str__(self):
    #     r = {}
    #     for k in self._data.keys():
    #         try:
    #             r[k] = str(getattr(self, k))
    #         except:
    #             r[k] = json.dumps(getattr(self, k))
    #     return str(r)


class EnumField(Field):
    db_field = "enum"

    def pre_field_create(self, model):
        field = "e_%s" % self.name

        self.get_database().get_conn().cursor().execute(
            "DROP TYPE IF EXISTS %s;" % field
        )

        query = self.get_database().get_conn().cursor()

        tail = ', '.join(["'%s'"] * len(self.choices)) % tuple(self.choices)
        q = "CREATE TYPE %s AS ENUM (%s);" % (field, tail)
        query.execute(q)

    def post_field_create(self, model):
        self.db_field = "e_%s" % self.name

    def coerce(self, value):
        if value not in self.choices:
            raise Exception("Invalid Enum Value `%s`", value)
        return str(value)

    def get_column_type(self):
        return "enum"

    def __ddl_column__(self, ctype):
        return SQL("e_%s" % self.name)
