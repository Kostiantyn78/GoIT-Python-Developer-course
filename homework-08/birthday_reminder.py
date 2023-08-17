import datetime
import random

users = [{'Олег': datetime.date(2023, 8, 24)}, {'Катерина': datetime.date(2023, 9, 6)},
         {'Олександр': datetime.date(2023, 9, 3)}, {'Тетяна': datetime.date(2023, 8, 29)},
         {'Дмитро': datetime.date(2023, 8, 18)}, {'Антон': datetime.date(2023, 8, 19)},
         {'Віктор': datetime.date(2023, 8, 20)}, {'Марія': datetime.date(2023, 8, 17)},
         {'Генадій': datetime.date(2023, 9, 3)}, {'Олена': datetime.date(2023, 9, 8)},
         {'Андрій': datetime.date(2023, 8, 21)}, {'Зоя': datetime.date(2023, 8, 14)},
         {'Людмила': datetime.date(2023, 8, 19)}, {'Анна': datetime.date(2023, 8, 15)},
         {'Володимир': datetime.date(2023, 8, 22)}, {'Ігор': datetime.date(2023, 8, 16)},
         {'Мілана': datetime.date(2023, 8, 18)}]


# def create_users_birthdays(users_names):
#
#     users_names = ['Олег', 'Катерина', 'Олександр', 'Тетяна', 'Дмитро', 'Антон', 'Віктор', 'Марія', 'Генадій', 'Олена',
#                    'Андрій', 'Зоя', 'Людмила', 'Анна', 'Володимир', 'Ігор', 'Мілана']
#
#     users = []
#
#     for user in users_names:
#         users.append({user: datetime.date.today() + datetime.timedelta(random.randint(1, 30))})
#
#     return users


def get_birthdays_per_week(users):
    current_date = datetime.date.today()
    # current_date = datetime.date(year=2023, month=8, day=14) # start the search from Monday
    lucky_names = []

    for shift_day in range(0, 7): # through 7 days, starting with the current day
        for user in users:
            for name, birthday in user.items():
                if birthday == current_date + datetime.timedelta(shift_day):
                    lucky_names.append(name)

        # if the current day is Saturday or Sunday, accumulate the names and move to the next day
        if (current_date + datetime.timedelta(shift_day)).weekday() > 4:
            continue

        if lucky_names:
            print(f'{(current_date + datetime.timedelta(shift_day)).strftime("%A")}: ', end='')
            print(*lucky_names, sep=', ')
            lucky_names = []

    # output names for Saturday and Sunday, if the search started on Monday
    if lucky_names:
        print(f'{datetime.date(year=2023, month=1, day=2).strftime("%A")}: ', end='')
        print(*lucky_names, sep=', ')

def main():
    get_birthdays_per_week(users)


if __name__ == '__main__':
    main()
