import datetime

# users = [{'name': 'Олег', 'birthday': datetime.date(2023, 8, 24)},
#          {'name': 'Катерина', 'birthday': datetime.date(2023, 9, 6)},
#          {'name': 'Олександр', 'birthday': datetime.date(2023, 9, 3)},
#          {'name': 'Тетяна', 'birthday': datetime.date(2023, 8, 21)},
#          {'name': 'Дмитро', 'birthday': datetime.date(2023, 8, 22)},
#          {'name': 'Антон', 'birthday': datetime.date(2023, 8, 27)},
#          {'name': 'Віктор', 'birthday': datetime.date(2023, 8, 26)},
#          {'name': 'Марія', 'birthday': datetime.date(2023, 8, 17)},
#          {'name': 'Генадій', 'birthday': datetime.date(2023, 9, 3)},
#          {'name': 'Олена', 'birthday': datetime.date(2023, 9, 8)},
#          {'name': 'Андрій', 'birthday': datetime.date(2023, 8, 25)},
#          {'name': 'Зоя', 'birthday': datetime.date(2023, 8, 14)},
#          {'name': 'Людмила', 'birthday': datetime.date(2023, 8, 19)},
#          {'name': 'Анна', 'birthday': datetime.date(2023, 8, 15)},
#          {'name': 'Володимир', 'birthday': datetime.date(2023, 8, 22)},
#          {'name': 'Ігор', 'birthday': datetime.date(2023, 8, 16)},
#          {'name': 'Мілана', 'birthday': datetime.date(2023, 8, 28)}]

def get_birthdays_per_week(users):

    current_date = datetime.date.today()
    # current_date = datetime.date(year=2023, month=8, day=21)  # start the search from Monday
    lucky_names = []

    for shift_day in range(0, 7):  # through 7 days, starting with the current day
        for user in users:
            if user['birthday'] == current_date + datetime.timedelta(shift_day):
                    lucky_names.append(user['name'])

        # if the current day is Saturday or Sunday, accumulate the names and move to the next day
        if (current_date + datetime.timedelta(shift_day)).weekday() > 4:
            continue

        if lucky_names:
            print(f'{(current_date + datetime.timedelta(shift_day)).strftime("%A")}: ', end='')
            print(*lucky_names, sep=', ')
            lucky_names = []

    # output names for Saturday and Sunday, if the search started on Monday
    if lucky_names:
        print(f'{datetime.date(year=2023, month=1, day=2).strftime("%A")}: ', end='') # just word Monday on all languages
        print(*lucky_names, sep=', ')

# def main():
#     get_birthdays_per_week(users)
#
# if __name__ == '__main__':
#     main()
