import os, random, keyboard, re
import logging
from enum import Enum
from create_database import CreateDatabase
from vocabulary_lite import VocabularyBook
from my_exception import OutOfRangeExecption, InvalidInputExecption


def not_Chinese(word):
    for ch in word:
        if not ('\u4e00' <= ch <= '\u9fff' or ch in ('，', '、', ' ', '(', ')', ';')):
            return True
    return False


def clean():
    os.system('cls')


"""
The valid_funcs_dict should put a dictionary that
put tuples insides. The first parameter is the restriction
function of the input and the second is the corresponding 
function.
If the action() return False, it will jump out
the while-loop to terminate the selecting.
The input_hint is the string to print out before inputting.
And the should_put is the string to print when inputting 
something invalid.
"""


def get_mode_choice(input_hint: str, mode_dict, should_put: str | None = "Invalid Input."):
    while True:
        inp = input(input_hint).lower()
        if inp in mode_dict:
            return mode_dict[inp]()
        print(f"Invalid input. Please enter {should_put}")


def print_word(word_list):
    print(word_list[1], end='  \t')
    for typ in word_list[2].split(';'):
        print(f'({typ}.)', end='')
    print(f'  {word_list[3]}\nE.g. ', end='')
    if word_list[4] == '':
        print('-- No example sentence --')
    else:
        for sent in word_list[4].split(';'):
            print(sent, end='\n     ')
    print()


class Mode(Enum):
    MAIN = 1
    STUDY = 2
    WRITE = 3
    DELETE = 4
    TEST = 5
    STUDY_FLASH = 21
    STUDY_NEW = 22
    STUDY_SHOW = 23
    TEST_ETC = 51
    TEST_CTE = 52


class Interface():

    def __init__(self):
        clean()
        print("Welcome to vocabularier!")
        databaselist = [f for f in os.listdir('.\\data') if f.endswith('.db')]
        books = {}
        num = 1
        for db in databaselist:
            print(num, '.  ', db, sep='')
            books[num] = db
            num += 1
        print('(c) Create a new voacabulary book')
        while True:
            self.database_name = input('Please choose vocabulary book: ')
            if self.database_name == 'c':
                CreateDatabase.create()
                clean()
                databaselist = [f for f in os.listdir('.\\data') if f.endswith('.db')]
                books = {}
                num = 1
                for db in databaselist:
                    print(num, '.   ', db, sep='')
                    books[num] = db
                    num += 1
            elif self.database_name.isdigit():
                self.database_name = int(self.database_name)
                if self.database_name in books:
                    self.database_name = '.\\data\\' + books[self.database_name]
                    break
                else:
                    print('Invalid number')
            else:
                print('Please enter a number')
        self.set_mode(Mode.MAIN)
        clean()

    def main_menu(self):
        print(f'Your now in {self.database_name}')
        while self.mode == Mode.MAIN:
            clean()
            print("-------------------------")
            print("Main Menu")
            print("Mode: (s) Studying Mode")
            print("      (w) Writing Mode")
            print("      (d) Deleting Mode")
            print("      (t) Testing Mode")
            print("      (e) Exit\n")
            modes = {
                's': self.studying_mode,
                'w': self.writing_mode,
                'd': self.deleting_mode,
                't': self.testing_mode,
                'e': self.main_menu_exit,
            }
            get_mode_choice("Select a Mode: ", modes)

    def studying_mode(self):
        self.set_mode(Mode.STUDY)
        while self.mode == Mode.STUDY:
            clean()
            print("-------------------------")
            print("Studying Mode")
            print("Mode: (1) Flash Card Mode")
            print("      (2) New word Mode")
            print("      (3) View all words Mode")
            print("      (e) Exit\n")
            modes = {
                '1': self.flash_card_mode,
                '2': self.new_word_mode,
                '3': self.show_all_mode,
                'e': self.exit_to_main_menu
            }
            get_mode_choice("Select a studying mode: ", modes, "'1' or '2' or '3' or 'e'")

    def flash_card_mode(self):
        clean()
        print("----------Start----------")
        print("(space) switch (←) last (→) next")
        print("(esc) leave\n")
        with VocabularyBook(self.database_name) as vocb:
            self.set_mode(Mode.STUDY_FLASH)
            count = 1
            switch_side = False
            while self.mode == Mode.STUDY_FLASH:
                if vocb.count_amo() == 0:
                    print("Your vocabulary book is empty.")
                    self.set_mode(Mode.MAIN)
                    break
                word = vocb.sel_by_seq(count)
                if switch_side is False:
                    print(word[1])
                else:
                    for typ in word[2].split(';'):
                        print('(' + typ + '.) ', end='')
                    print(word[3] + '\n' + word[4])
                while True:
                    keyboard.read_event()  # to read the surplus event
                    event = keyboard.read_event()
                    if event.name == 'left' and count > 1:
                        count -= 1
                        switch_side = False
                        clean()
                        print("----------Start----------")
                        print("(space) switch (←) last (→) next")
                        print("(esc) leave\n")
                        break
                    elif event.name == 'right' and count < vocb.count_amo():
                        count += 1
                        switch_side = False
                        clean()
                        print("----------Start----------")
                        print("(space) switch (←) last (→) next")
                        print("(esc) leave\n")
                        break
                    elif event.name == 'esc':
                        self.set_mode(Mode.STUDY)
                        break
                    elif event.name == 'space':
                        switch_side = not switch_side
                        clean()
                        print("----------Start----------")
                        print("(space) switch (←) last (→) next")
                        print("(esc) leave\n")
                        break
        print("Flash card mode ended.")

    def new_word_mode(self):
        clean()
        print("----------Start----------")
        print("(←) last (→) next")
        print("(esc) leave")
        with VocabularyBook(self.database_name) as vocb:
            self.set_mode(Mode.STUDY_NEW)
            count = 1
            while self.mode == Mode.STUDY_NEW:
                if vocb.count_amo() == 0:
                    print("Your vocabulary book is empty.")
                    self.set_mode(Mode.MAIN)
                    break
                word = vocb.sel_by_seq(count)
                print()
                print_word(word)
                while True:
                    keyboard.read_event()  # to read the surplus event
                    event = keyboard.read_event()
                    if event.name == 'left' and count > 1:
                        count -= 1
                        clean()
                        print("----------Start----------")
                        print("(←) last (→) next")
                        print("(esc) leave")
                        break
                    elif event.name == 'right' and count < vocb.count_amo():
                        count += 1
                        clean()
                        print("----------Start----------")
                        print("(←) last (→) next")
                        print("(esc) leave")
                        break
                    elif event.name == 'esc':
                        self.mode = Mode.STUDY
                        break
        print("New word mode ended.")

    def show_all_mode(self):
        clean()
        print("(esc) leave\n")
        with VocabularyBook(self.database_name) as vocb:
            self.set_mode(Mode.STUDY_SHOW)
            while self.mode == Mode.STUDY_SHOW:
                for i in range(1, vocb.count_amo() + 1):
                    print_word(vocb.show_a_ind(i))
                while True:
                    keyboard.read_event()  # to read the surplus event
                    event = keyboard.read_event()
                    if event.name == 'esc':
                        self.set_mode(Mode.STUDY)
                        break

    def writing_mode(self):
        clean()
        print("-------------------------")
        print("Writing Mode")
        print("Enter (q) to quit")
        with VocabularyBook(self.database_name) as vocb:
            self.set_mode(Mode.WRITE)
            while self.mode == Mode.WRITE:
                inputting = True  # turn False when a valid input entered
                while inputting:
                    voc = input("Please enter a new vocabulary: ").strip()
                    # check the constrain of voc
                    if voc == 'q':
                        self.set_mode(Mode.MAIN)
                        inputting = False
                        break
                    elif len(voc) > 50:
                        print("Too long~")
                    elif voc in vocb.check_voc():  # duplicated word
                        word_dup = vocb.show_a_voc(voc)
                        print("This word has been writed:")
                        print(f"{word_dup[1]}  ({word_dup[2]})  {word_dup[3]}\n{word_dup[4]}")
                        while True:
                            check = input("Do you want to overwrite this word? [Y/N] ").lower()
                            if check == 'y':
                                inputting = False
                                break
                            elif check == 'n':
                                break
                            else:
                                print("Invalid input. Please enter 'Y' or 'N'.")
                    elif voc == '':
                        print("Input shouldn't be blank.")
                    else:
                        inputting = False
                if voc == 'q':
                    break
                inputting = True

                while inputting:
                    typ = input("What is the part of speech? (seperate with ';' if many) ").strip()
                    if typ == 'q':
                        self.set_mode(Mode.MAIN)
                        break
                    typ_list = typ.split(';')
                    # check the constrain of typ
                    types = []
                    for t in typ_list:
                        typ_corr = True
                        if t == 'a':  # valid type, keep on checking other types
                            t = 'adj'
                            types.append(t)
                        elif t not in ('n', 'adj', 'adv', 'phr', 'v', 'prep', 'conj'):
                            typ_corr = False
                            print('Invalid part of speech')
                            break
                        elif t in types:
                            typ_corr = False
                            print('Duplicated part of speech')
                            break
                        else:  # fit the constrain
                            types.append(t)
                    typ = ';'.join(types)
                    if typ_corr is True:
                        inputting = False
                if typ == 'q':
                    break
                inputting = True

                while inputting:
                    chi = input(
                        "What is the meaning in Chinese? (seperate with ';' if many) ").strip()
                    if chi == 'q':
                        self.set_mode(Mode.MAIN)
                        break
                    chi_list = chi.split(';')
                    # check the constrain of chi
                    chis = []
                    for c in chi_list:
                        chi_corr = True
                        if len(c) > 20:
                            chi_corr = False
                            print("Too long~")
                            break
                        elif not_Chinese(c):
                            chi_corr = False
                            print('Please enter Chinese!')
                            break
                        else:  # fit the constrain
                            chis.append(t)
                    if chi_corr is True:
                        inputting = False
                if chi == 'q':
                    break
                inputting = True

                while inputting:
                    sent = input("Enter an example sentence! (seperate with ';' if many) ").strip()
                    if sent == 'q':
                        self.set_mode(Mode.MAIN)
                        break
                    sent_list = sent.split(';')
                    # check the constrain of sent
                    sents = []
                    for s in sent_list:
                        sent_corr = True
                        if s == '':  # valid sentence, keep on tracking others
                            sents.append(s)
                        elif len(s) > 120:
                            sent_corr = False
                            print("Too long~")
                            break
                        elif not s.endswith('.'):
                            sent_corr = False
                            print('Please enter a sentence ended with a period!')
                            break
                        else:  # fit the constrain
                            sents.append(s)
                    if sent_corr is True:
                        inputting = False
                if sent == 'q':
                    break
                inputting = True

                #  confirm the inputted vocabulary
                vocabulary = [None, voc, typ, chi, sent]
                print_word(vocabulary)
                while True:
                    check = input("Confirm to add this word? [Y/N] ").lower()
                    if check == 'y':
                        if voc in vocb.check_voc():
                            vocb.add_voc(voc, typ, chi, sent, dup=True)
                        else:
                            vocb.add_voc(voc, typ, chi, sent)
                        break
                    elif check == 'n':
                        print("Adding fail.")
                        break
                    else:
                        print("Invalid input. Please enter 'Y' or 'N'.")

    def deleting_mode(self):
        self.set_mode(Mode.DELETE)
        clean()
        print("-------------------------")
        print("Writing Mode")
        print("Enter (q) to quit\n")
        with VocabularyBook(self.database_name) as vocb:
            vocb.show_data()
            while self.mode == Mode.DELETE:
                try:
                    ind = input("Select an index to delete: ").lower()
                    if ind == 'q':
                        self.set_mode(Mode.MAIN)
                        break
                    ind = int(ind)  # may raise ValueError
                    if vocb.show_a_ind(ind) is None:
                        raise OutOfRangeExecption("Not a valid index")
                    while True:
                        try:
                            check = input(
                                f"Confirm to delete this word? \n{print_word(vocb.show_a_ind(ind))}[Y/N] "
                            ).lower()
                            if check == 'y':
                                vocb.del_voc(ind)
                                break
                            elif check == 'n':
                                break
                            else:
                                raise InvalidInputExecption(
                                    "Invalid input. Please enter 'Y' or 'N'.")
                        except InvalidInputExecption as e:
                            print(e)
                    # if successfully delete a word
                    clean()
                    print("-------------------------")
                    print("Writing Mode")
                    print("Enter (q) to quit\n")
                    vocb.show_data()
                except ValueError:
                    print("Please enter an index")
                except OutOfRangeExecption as e:
                    print(e.message)

    def english_to_chinese(self, vocb):
        self.set_mode(Mode.TEST_ETC)
        correct = 0
        rounds = 0
        clean()
        print("----------Start----------")
        print("Enter (q) to quit")
        while self.mode == Mode.TEST_ETC:
            test_vocb = vocb.sel_one_voc()
            ans = input(f"What is {test_vocb[1]} in Chinese? ")
            if ans == 'q':
                self.set_mode(Mode.TEST)
                break
            elif ans == test_vocb[3]:
                rounds += 1
                print("You're right!")
                correct += 1
            else:
                rounds += 1
                print("Your wrong!\n\nReview this vocabulary :")
                print_word(test_vocb)
                os.system('pause')  # print("press any botton to continue")
                clean()
                print("Enter (q) to quit")
        if rounds != 0:
            print(f"Your correct rate is {int(correct / rounds * 100)}%")

    def chinese_to_english(self, vocb):
        self.set_mode(Mode.TEST_CTE)
        correct = 0
        rounds = 0
        clean()
        print("----------Start----------")
        print("Enter (q) to quit")
        while self.mode == Mode.TEST_CTE:
            test_vocbs = vocb.make_mult()
            print(f"What is {test_vocbs[0][3]} in English? ")
            num = vocb.count_amo()
            if num < 4:
                choices_list = random.sample(test_vocbs, vocb.count_amo())
                correct_choice = 0
                for i in range(vocb.count_amo()):
                    if choices_list[i][1] == test_vocbs[0][1]:
                        correct_choice = i
                correct_choice += 1  # to fit the 1234 choice
                print("Options:")
                for i in range(vocb.count_amo()):
                    print(f"({i+1}) {choices_list[i][1]}")
            else:
                choices_list = random.sample(test_vocbs, 4)
                correct_choice = 0
                for i in range(4):
                    if choices_list[i][1] == test_vocbs[0][1]:
                        correct_choice = i
                correct_choice += 1  # to fit the 1234 choice
                print("Options:")
                for i in range(4):
                    print(f"({i+1}) {choices_list[i][1]}")

            ans = input("\nAnswer: ")
            if ans == 'q':
                self.set_mode(Mode.TEST)
                break
            elif ans == str(correct_choice):
                rounds += 1
                print("You're right!\n")
                correct += 1
            else:
                rounds += 1
                print("Your wrong!\n\nReview this vocabulary :")
                print_word(test_vocbs[0])
                os.system('pause')  # print("press any botton to continue")
                clean()
                print("Enter (q) to quit")
        if rounds != 0:
            print(f"Your correct rate is {int(correct / rounds * 100)}%")

    def testing_mode(self):
        with VocabularyBook(self.database_name) as vocb:
            self.set_mode(Mode.TEST)
            clean()
            while self.mode == Mode.TEST:
                print("-------------------------")
                print("Testing Mode")
                print("Mode: (1) English to Chinese")
                print("      (2) Chinese to English")
                print("      (e) Exit\n")
                if vocb.count_amo() == 0:
                    print("Your vocabulary book is empty.")
                    self.set_mode(Mode.MAIN)
                    break
                modes = {
                    '1': lambda: self.english_to_chinese(vocb),
                    '2': lambda: self.chinese_to_english(vocb),
                    'e': lambda: self.exit_to_main_menu()
                }
                get_mode_choice('select a testing mode: ', modes, "'1' or '2' or 'e'")

    def exit_to_main_menu(self):
        self.set_mode(Mode.MAIN)

    def main_menu_exit(self):  # exit the program
        self.mode = None
        self.running = False

    def set_mode(self, given_mode: Mode):
        self.mode = given_mode


if __name__ == '__main__':
    os.system("title Vocabularier.exe")
    logging.basicConfig(filename='app.log',
                        filemode='w',
                        format='%(name)s - %(levelname)s - %(message)s')
    try:
        user_interface = Interface()
        user_interface.main_menu()
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
