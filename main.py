import argparse
import os
from datetime import date
from colorama import Fore
from enum import IntEnum
from database import ExpenseRecord, BudgetRecord, Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import func, extract, and_, or_

class CommandCode(IntEnum):
    WAIT = 0
    ADD = 1
    CHECK = 2
    UPDATE = 3
    BACK = 4
    QUIT = 5

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

command_map = {'wait': CommandCode.WAIT, 
                'add': CommandCode.ADD, 'a': CommandCode.ADD, 
                'check': CommandCode.CHECK, 'c': CommandCode.CHECK, 
                'update': CommandCode.UPDATE, 'u': CommandCode.UPDATE,
                'b': CommandCode.BACK, 
                'q': CommandCode.QUIT}

check_prompt_text = '''\
[1] expense
[2] budget
[b] back
[q] quit
'''


def getExpense(category):
    # /usr/bin/clear screen
    # os.system('/usr/bin/clear')
    print(Fore.BLUE + category_map[category][0] + Fore.RESET)
    print(Fore.RED + 'nhap 0 vao muc [so tien] de huy' + Fore.RESET)

    try:
        amount = int(input(Fore.GREEN + '[so tien] ' + Fore.RESET))
    except:
        amount = 0

    if amount == 0:
        return None

    content = input(Fore.GREEN + '[noi dung] ' + Fore.RESET)

    return ExpenseRecord(date=date.today(), category=category_map[category][1], 
                        amount=amount, content=content)


def addExpenseRecord(category):
    if category in category_map.keys():
        new_expense_record = getExpense(category)
        print(new_expense_record)
        if new_expense_record:
            session.add(new_expense_record)
            session.commit()
    else:
        print(Fore.RED + 'Invalid category!' + Fore.RESET)


def updateBudgetRecord(query_time):
    total_expense = session.query(func.sum(ExpenseRecord.amount)).filter(and_(extract('month', ExpenseRecord.date)==today.month,
                                                 extract('year', ExpenseRecord.date)==today.year)).scalar()
    result = session.query(BudgetRecord).filter_by(month=query_time).first()

    if result is None:
        new_budget_record = BudgetRecord(month=query_time, outcome=total_expense)
        session.add(new_budget_record)
    else:
        result.outcome = total_expense
    session.commit()


def updateIncome(query_time):
    try:
        income = int(input('[income] '))
    except:
        income = 0

    result = session.query(BudgetRecord).filter_by(month=query_time).first()

    if result is None:
        new_budget_record = BudgetRecord(month=query_time, income=income)
        session.add(new_budget_record)
    else:
        result.income += income
    session.commit()


def getQueryTime():
    try:
        year = int(input('[year] '))
        month = int(input('[month] '))
    except:
        year = today.year
        month = today.month

    query_time = f"{year}-{month:02}"

    return query_time


def checkRecord(option):
    result = session.query(ExpenseRecord.category, ExpenseRecord.amount, ExpenseRecord.content).all()
    print(result)
    return CommandCode.WAIT


def initialize():
    global today
    today = date.today()

    global command_prompt_text
    command_prompt_text = ''
    global add_prompt_text
    add_prompt_text = ''

    for (k, v) in option_map.items():
        command_prompt_text += f'[{k}] {v}\n'

    
    for (k, v) in category_map.items():
        add_prompt_text += f'[{k}] {v[0]}\n'
    add_prompt_text += '[b] back\n[q] quit'


def add():
    os.system('/usr/bin/clear')
    print(Fore.GREEN + add_prompt_text + Fore.RESET)

    option = input('>> ')
    if option == 'b':
        return CommandCode.WAIT
    elif option == 'q': 
        return CommandCode.QUIT
    else:
        addExpenseRecord(option)
        
        query_time = f"{today.year}-{today.month:02}"
        updateBudgetRecord(query_time)
    return CommandCode.ADD


def check():
    os.system('/usr/bin/clear')
    print(Fore.GREEN + check_prompt_text + Fore.RESET)

    option = input('>> ')

    if option == 'b':
        return CommandCode.WAIT
    elif option == 'q':
        return CommandCode.QUIT
    else:
        return checkRecord(option)


def main():
    command = command_map.get(args['command'].lower(), CommandCode.WAIT)

    while True:
        if command == CommandCode.WAIT:
            #os.system('/usr/bin/clear')
            print(Fore.GREEN + command_prompt_text + Fore.RESET)

            command = command_map.get(input('>> '), CommandCode.WAIT)

        if command == CommandCode.ADD:
            command = add()

        elif command == CommandCode.CHECK:
            command = check()

        elif command == CommandCode.UPDATE:
            query_time = getQueryTime()
            updateIncome(query_time)
            command = CommandCode.WAIT

        elif command == CommandCode.QUIT:
            os.system('/usr/bin/clear')
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