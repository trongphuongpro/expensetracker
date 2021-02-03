import argparse
import os
from datetime import date
from colorama import Fore, init
from database import ExpenseRecord, Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


parser = argparse.ArgumentParser()
parser.add_argument('command', nargs='?', default='wait')
args = vars(parser.parse_args())

category_map = {'1': ['Quy chi tieu can thiet', 'living'], 
                '2': ['Quy tiet kiem dai han', 'saving'],
                '3': ['Quy giao duc', 'education'],
                '4': ['Quy huong thu', 'playing'],
                '5': ['Quy tu do tai chinh', 'free'],
                '6': ['Quy tu thien', 'giving']
                }

option_map = {'a': 'add', 'c': 'check', 'u': 'update', 'q': 'quit'}


def getExpense(category):
    # clear screen
    os.system('cls')
    print(Fore.BLUE + category_map[category][0] + Fore.RESET)
    print(Fore.RED + 'nhap 0 vao muc [so tien] de huy' + Fore.RESET)

    amount = int(input(Fore.GREEN + '[so tien] ' + Fore.RESET))

    if amount == 0:
        return None

    content = input(Fore.GREEN + '[noi dung] ' + Fore.RESET)

    return ExpenseRecord(date=date.today(), category=category_map[category][1], 
                        amount=amount, content=content)


def addNewRecord(category):
    if category in category_map.keys():
        new_record = getExpense(category)
        print(new_record)
        if new_record:
            session.add(new_record)
            session.commit()
    else:
        print(Fore.RED + 'Invalid category!' + Fore.RESET)


def initialize():
    global command_prompt_text
    command_prompt_text = ''
    global add_prompt_text
    add_prompt_text = ''

    for (k, v) in option_map.items():
        command_prompt_text += f'[{k}] {v}\n'

    
    for (k, v) in category_map.items():
        add_prompt_text += f'[{k}] {v[0]}\n'
    add_prompt_text += '[b] back\n[q] quit'

    init()


def main():
    command = args['command'].lower()

    while True:
        if command == 'wait':
            os.system('cls')
            print(Fore.GREEN + command_prompt_text + Fore.RESET)

            try:
                command = option_map[input('>> ')]
            except Exception as e:
                command == 'wait'

        if command in ['add', 'a']:
            # clear screen
            os.system('cls')
            print(Fore.GREEN + add_prompt_text + Fore.RESET)

            option = input('>> ')
            if option == 'b':
                command = 'wait'
            elif option == 'q':
                os.system('cls')
                break
            else:
                addNewRecord(option)
            

        elif command in ['check', 'c']:
            print(Fore.GREEN + "CHECK" + Fore.RESET)


        elif command in ['show', 's']:
            print(Fore.GREEN + "SHOW" + Fore.RESET)


        elif command == 'quit':
            os.system('cls')
            break

        else:
            print(Fore.RED + "Error: {} -> Invalid command!".format(command)
                    + Fore.RESET)


if __name__ == '__main__':
    engine = create_engine('sqlite:///record.db', echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    initialize()
    main()