from main_logic import *

"""Основной блок выполнения команд в меню. Следуйте инструкциям, описанным в консоли, если таковые имеются"""


def main():
    wallet = Wallet('wallet.db')
    wallet.file_to_txt('wallet.json')

    def first_choice():
        date = input("Введите дату (ГГГГ-ММ-ДД): ")
        category = input("Введите тип (Доход или "
                         "Расход): ")
        amount = int(input("Введите сумму: "))
        description = input("Введите описание операции : ")
        wallet.add_notation(date, category, amount, description)
        return f"Запись успешно добавлена"

    def second_choice():
        return wallet.view_all_notations()

    def third_choice():
        search_param = input("Введите ключевое слово для поиска: ")
        return wallet.search_notation(search_param)

    def fourth_choice():
        return wallet.show_balance()

    def fifth_choice():
        index = int(input("Введите индекс : "))
        new_date = input("Введите новую дату (ГГГГ-ММ-ДД): ")
        new_category = input("Введите новый тип (Доход или "
                             "Расход): ")
        new_amount = int(input("Введите сумму: "))
        new_description = input("Введите описание операции : ")
        return wallet.edit_notation(index, new_date, new_category, new_amount, new_description)

    def six_choice():
        while True:
            break

    while True:
        print("1. Добавить запись")
        print("2. Просмотреть все записи")
        print("3. Поиск записей")
        print("4. Проверить баланс")
        print("5. Редактировать запись")
        print("6. Выход")
        choice = input("Выберите действие: ")

        choices_dict = {
            "1": first_choice,
            "2": second_choice,
            "3": third_choice,
            "4": fourth_choice,
            "5": fifth_choice,
            "6": six_choice
        }
        if choice == '6':
            break
        elif choice in choices_dict:
            print(choices_dict[choice]())
        else:
            print("Неверный выбор")
            break


if __name__ == "__main__":
    main()
