import datetime
import random

users_names = ['Олег', 'Катерина', 'Олександр', 'Тетяна', 'Дмитро', 'Антон', 'Віктор', 'Марія', 'Генадій',
               'Олена', 'Андрій', 'Зоя', 'Людмила', 'Анна', 'Володимир', 'Ігор', 'Мілана']

users = [{'Олег': datetime.date(2023, 8, 24)}, {'Катерина': datetime.date(2023, 9, 6)},
         {'Олександр': datetime.date(2023, 9, 3)}, {'Тетяна': datetime.date(2023, 8, 29)},
         {'Дмитро': datetime.date(2023, 8, 18)}, {'Антон': datetime.date(2023, 8, 19)},
         {'Віктор': datetime.date(2023, 8, 31)}, {'Марія': datetime.date(2023, 8, 17)},
         {'Генадій': datetime.date(2023, 9, 3)}, {'Олена': datetime.date(2023, 9, 8)},
         {'Андрій': datetime.date(2023, 9, 12)}, {'Зоя': datetime.date(2023, 9, 13)},
         {'Людмила': datetime.date(2023, 8, 19)}, {'Анна': datetime.date(2023, 9, 13)},
         {'Володимир': datetime.date(2023, 8, 22)}, {'Ігор': datetime.date(2023, 9, 8)},
         {'Мілана': datetime.date(2023, 8, 18)}]


def create_users_birthdays(users_names):
    users = []

    for user in users_names:
        users.append({user: datetime.date.today() + datetime.timedelta(random.randint(1, 30))})
    return users

# print(create_users_birthdays(users_names))