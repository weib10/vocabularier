import sqlite3
from sqlite3 import Error
import os


class CreateDatabase:

    def create():
        database_name = input('Please enter a name of your new vocabulary book: ')
        try:
            # have to change future when construct a new environment
            if not os.path.exists('.\\data\\' + database_name + '.db.'):
                connection = sqlite3.connect('.\\data\\' + database_name + '.db.')
            else:
                inp = input('this vocabulary book has existed, confirn to reset? [y/n] ')
                while True:
                    if inp == 'y':
                        connection = sqlite3.connect('.\\data\\' + database_name + '.db.')
                        break
                    if inp == 'n':
                        print('Bye~')
                        exit()
                    else:
                        inp = input('Invalid input. ')
            cursor = connection.cursor()

            cursor.execute("DROP TABLE IF EXISTS `vocabulary`;")
            cursor.execute("""
                        CREATE TABLE IF NOT EXISTS `vocabulary`(
                        `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                        `vocabulary` TEXT NOT NULL UNIQUE,
                        `type` TEXT,
                        `chinese` TEXT,
                        `sentence` TEXT
                        );
                        """)
            cursor.execute("CREATE INDEX idx_vocabulary ON vocabulary (vocabulary);")
            cursor.execute("PRAGMA table_info(vocabulary);")
            # result = cursor.fetchall()
            # for res in result:
            #     print(res)
            print('Create successfully')

        except Error as e:
            raise Error("Could not connect to: %s" % '.\\data\\' + database_name + '.db.') from e

        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None:
                connection.close()


if __name__ == '__main__':
    CreateDatabase.create()
