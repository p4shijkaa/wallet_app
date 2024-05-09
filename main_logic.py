import json
import sqlite3


class Wallet:

    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()
        self.create_table()
        self.notations = []

    '''Функция для создания таблицы базы данных'''

    def create_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS wallet 
                         (id INTEGER PRIMARY KEY, date TEXT, category TEXT, amount INT, description TEXT)''')
        return self.conn.commit()

    '''Функция для добавления записи о доходах и расходах в базу данных'''

    def add_notation(self, date, category, amount, description):
        new_notation = self.c.execute("INSERT INTO wallet (date, category, amount, description) VALUES (?, ?, ?, ?)",
                                      (date, category, amount, description))
        self.conn.commit()
        return new_notation

    '''Функция для просмотра всех записей в базе данных'''

    def view_all_notations(self) -> list:
        self.c.execute("SELECT * FROM wallet")
        notations = self.c.fetchall()
        notations_list = []
        for notation in notations:
            values_dict = {
                'Дата': f"{notation[1]}",
                'Категория': f"{notation[2]}",
                'Сумма': notation[3],
                'Описание': f"{notation[4]}",
            }
            notations_list.append(values_dict)

        self.notations = notations_list
        return self.notations

    '''Функция для поиска записей о расходах и доходах в базе данных по любым критериям, например по дате'''

    def search_notation(self, search_param):
        self.c.execute(
            "SELECT * FROM wallet WHERE category LIKE ? OR amount LIKE ? OR description LIKE ? OR date LIKE ?",
            ('%' + search_param + '%', '%' + search_param + '%',
             '%' + search_param + '%', '%' + search_param + '%'))
        searched_notations = self.c.fetchall()
        notations_list = []
        for index, notation in enumerate(searched_notations):
            values_dict = {
                'Дата': f"{notation[1]}",
                'Категория': f"{notation[2]}",
                'Сумма': notation[3],
                'Описание': f"{notation[4]}",
            }
            notations_list.append(values_dict)

        self.notations = notations_list
        return self.notations

    '''Функция для просмотра текущего баланса, а также всех расходов и доходов'''

    def show_balance(self):
        self.view_all_notations()
        total_income = sum(notation['Сумма'] for notation in self.notations
                           if notation['Категория'] == 'Доход')
        total_expenses = sum(notation['Сумма'] for notation in self.notations
                             if notation['Категория'] == 'Расход')
        balance = total_income - total_expenses
        self.conn.commit()
        return f"Текущий баланс {balance} р., Доход составил {total_income} р., Расход составил {total_expenses} р."

    '''Функция для редактирования записи в базе данных. Обращаться к записи нужно по индексу'''

    def edit_notation(self, notation_index, new_date, new_category, new_amount, new_description):
        self.view_all_notations()
        add_list = self.notations
        print(add_list)
        for index, notation in enumerate(add_list):
            if index == notation_index:
                notation['Дата'] = new_date
                notation['Категория'] = new_category
                notation['Сумма'] = new_amount
                notation['Описание'] = new_description

        self.notations = add_list
        self.conn.commit()
        return self.notations

    '''Функция сохранения всех записей в формате JSON'''

    def file_to_txt(self, filename):
        with open(filename, 'w', encoding="utf-8") as file:
            self.c.execute("SELECT * FROM wallet")
            notations = self.c.fetchall()
            self.conn.commit()
            json.dump(notations, file, ensure_ascii=False, indent=4)
