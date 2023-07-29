import logging
import sqlite3
import random


class VocabularyBook:

    def __init__(self, database_name):
        self.conn = sqlite3.connect(database_name)
        self.database = database_name
        self.vocab_amount = self.count_amo()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            logging.error("Exception occurred in the database operation:")
            logging.error("Exception type: %s", exc_type)
            logging.error("Exception value: %s", exc_value)
            logging.error("Traceback: %s", traceback)
            # Here you could add additional code to handle the exception, if needed
        self.conn.close()

    def show_data(self):
        if self.vocab_amount != 0:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM `vocabulary`")
            records = cursor.fetchall()
            for r in records:
                print(str(r[0]) + '. ' + r[1], end='  \t')
                for typ in r[2].split(';'):
                    print('(' + typ + '.)', end='')
                print('\t' + r[3])
                # print(r[4])

    def show_a_voc(self, vocb):
        if self.vocab_amount != 0:
            cursor = self.conn.cursor()
            sql = f"SELECT * FROM `vocabulary` WHERE `vocabulary` = '{vocb}'"
            cursor.execute(sql)
            result = cursor.fetchone()
            return result

    def show_a_ind(self, ind: int) -> list:
        if self.vocab_amount != 0:
            cursor = self.conn.cursor()
            sql = f"SELECT * FROM `vocabulary` WHERE `id` = '{ind}'"
            cursor.execute(sql)
            result = cursor.fetchone()
            return result

    def check_voc(self):
        cursor = self.conn.cursor()
        sql = "SELECT `vocabulary` FROM `vocabulary`"
        cursor.execute(sql)
        result = cursor.fetchall()
        result_list = []
        for i in result:
            result_list.append(i[0])
        return result_list

    def add_voc(self, voc, typ, chi, sent, dup=False):
        cursor = self.conn.cursor()
        if dup is True:
            sql = ("INSERT INSERT OR REPLACE INTO vocabulary "
                    "(vocabulary, type, chinese, sentence) VALUES (?, ?, ?, ?)")
        else:
            sql = ("INSERT INTO vocabulary "
                    "(vocabulary, type, chinese, sentence) VALUES (?, ?, ?, ?)")
        val = (voc, typ, chi, sent)
        cursor.execute(sql, val)
        self.conn.commit()
        self.vocab_amount -= 1

    def del_voc(self, ind):
        if self.vocab_amount != 0:
            cursor = self.conn.cursor()
            del_sql = "DELETE FROM `vocabulary` WHERE `id` = ?"
            cursor.execute(del_sql, (ind, ))
            self.conn.commit()
            self.rearrange_ids()
            self.vocab_amount -= 1

    def rearrange_ids(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS `new_vocabulary`(
                `id` INTEGER PRIMARY KEY,
                `vocabulary` TEXT NOT NULL UNIQUE,
                `type` TEXT,
                `chinese` TEXT,
                `sentence` TEXT
            );
        """)
        cursor.execute(
            "INSERT INTO `new_vocabulary` (`vocabulary`, `type`, `chinese`, `sentence`) SELECT `vocabulary`, `type`, `chinese`, `sentence` FROM `vocabulary` ORDER BY `id`"
        )
        cursor.execute("DROP TABLE `vocabulary`")
        cursor.execute("ALTER TABLE `new_vocabulary` RENAME TO `vocabulary`")
        self.conn.commit()

    def sel_one_voc(self):
        if self.vocab_amount != 0:
            cursor = self.conn.cursor()
            ran_num = random.randint(1, self.count_amo())
            sql = "SELECT * FROM `vocabulary` WHERE `id` = ?"
            cursor.execute(sql, (ran_num, ))
            result = cursor.fetchone()
            return result

    def sel_by_seq(self, number):
        if self.vocab_amount != 0:
            cursor = self.conn.cursor()
            sql = "SELECT * FROM `vocabulary` WHERE `id` = ?"
            #  ORDER BY `vocabulary`
            cursor.execute(sql, (number, ))
            result = cursor.fetchone()
            return result

    def make_mult(self):
        if self.vocab_amount != 0:
            cursor = self.conn.cursor()
            sql = "SELECT * FROM `vocabulary`"
            cursor.execute(sql)
            result = cursor.fetchall()
            random.shuffle(result)
            return result[:4]

    def count_amo(self):
        cursor = self.conn.cursor()
        sql = "SELECT COUNT(`vocabulary`) FROM `vocabulary`"
        cursor.execute(sql)
        result = cursor.fetchone()
        return result[0]


if __name__ == '__main__':
    database_name = '.\\data\\book1.db'
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    sql = "SELECT * FROM `vocabulary`"
    cursor.execute(sql)
    records = cursor.fetchall()
    if records == []:
        print('Your book is empty.')
        exit()
    for r in records:
        print(str(r[0]) + '. ' + r[1], end='  \t')
    for typ in r[2].split(';'):
        print('(' + typ + '.)', end='')
    print('\t' + r[3])
    print(r[4])
    print(records)
    conn.close()