import psycopg2 as dbapi2
from moderator import Moderator
from flask import current_app as app
from _sqlite3 import Row
from flask_login import UserMixin


class ModeratorList:
    def __init__(self):
            self.last_mod_id = None

    def add_moderator(self, moderator):
        with dbapi2.connect(app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """INSERT INTO MODERATORS (NICKNAME, PASSWORD) VALUES (%s, %s)"""
                cursor.execute(query, (moderator.nickname, moderator.password))
                connection.commit()

    def delete_moderator(self, mod_id):
        with dbapi2.connect(app.config['dsn']) as connection:
                cursor = connection.cursor()
                statement ="""DELETE FROM IMGPOSTS WHERE (MODID = (%s))"""
                cursor.execute(statement, (mod_id,))
                connection.commit()
                statement ="""DELETE FROM MODERATORS WHERE (ID = (%s))"""
                cursor.execute(statement, (mod_id,))
                connection.commit()
                cursor.close()

    def update_moderator(self, mod_id, newName):
        with dbapi2.connect(app.config['dsn']) as connection:
                cursor = connection.cursor()
                statement ="""UPDATE MODERATORS
                SET NICKNAME = (%s)
                WHERE (ID = (%s))"""
                cursor.execute(statement, (newName, mod_id))
                connection.commit()
                cursor.close()

    def get_moderator(self, modName):
            with dbapi2.connect(app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """SELECT ID FROM MODERATORS WHERE (NICKNAME = (%s))"""
                cursor.execute(query, (modName, ))
                mod_id = cursor.fetchone()  # the possibility of having two or more mods with the same name!!!
                #imgid, imgname, modid
                connection.commit()
                cursor.close()
            return mod_id

    def get_moderatorName(self, modid):
            with dbapi2.connect(app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """SELECT NICKNAME FROM MODERATORS WHERE (ID = (%s))"""
                cursor.execute(query, (modid, ))
                modName = cursor.fetchone()  # the possibility of having two or more mods with the same name!!!
                #imgid, imgname, modid
                connection.commit()
                cursor.close()
            return modName

    def get_moderators(self):
            with dbapi2.connect(app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """SELECT ID, NICKNAME, PASSWORD FROM MODERATORS
                ORDER BY ID"""
                cursor.execute(query)
                modTable = [(id, Moderator(nickname, password))
                          for id, nickname, password in cursor]
                connection.commit()
                cursor.close()
            return modTable

    def get_moderatorObj(self, mod_name):   # def get_user
            empty = 'Empty'
            with dbapi2.connect(app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """SELECT PASSWORD FROM MODERATORS WHERE (NICKNAME = (%s))"""
                cursor.execute(query, (mod_name,))
                mod_pass = cursor.fetchone()
                connection.commit()
                if mod_pass is None:
                    mod = None
                else:
                    mod = Moderator(mod_name, mod_pass[0])  #[0]
                cursor.close()
                return mod
