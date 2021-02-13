import argparse
import os
import sys
from datetime import date
from colorama import Fore
from database import ExpenseRecord, BudgetRecord, Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import func, extract, and_, or_
from data import *

parser = argparse.ArgumentParser()
parser.add_argument('command', nargs='?', default='wait')
args = vars(parser.parse_args())


def getQueryTime(*, get_today=False):
    if not get_today:
        try:
            year = int(input('[year] '))
            month = int(input('[month] '))
        except:
            query_time = None
        else:
            query_time = {'year': year, 'month': month}

    else:
        query_time = f"{today.year}-{today.month:02}"

    return query_time


def initialize():
    global today
    today = date.today()
    setMessage("...")
    

def func_wait(*args) -> CommandCode:
    clearScreen()
    setMessage("---- HOME SCREEN ----")
    showMessage()
    showMenu(menu_wait)

    choice = input(">> ")
    check_value = menu_wait.get(choice, None)

    if check_value is None:
        setMessage(f"{choice}: Invalid choice!")
        return CommandCode.WAIT
    else:
        return execFunc(menu_wait, choice)


def func_back(*args) -> CommandCode:
    return CommandCode.WAIT


def func_quit(*args):
    clearScreen()
    sys.exit(0)

#----------------- functions for ADD ---------------------#

def func_add(*args) -> CommandCode:
    clearScreen()
    showMessage()
    showMenu(menu_add)
    
    choice = input('>> ')
    check_value = menu_add.get(choice, None)

    if check_value is None:
        setMessage(f"{choice}: Invalid choice!")
        return CommandCode.ADD
    else:
        return execFunc(menu_add, choice, choice)


def updateDatabase(choice: str) -> CommandCode:
    new_record = addExpenseRecord(choice)
    updateBudgetRecord()

    setMessage(f"Added {new_record}")

    return CommandCode.ADD


def addExpenseRecord(category: str):
    if category in menu_add.keys():
        new_expense_record = getExpense(category)

        if new_expense_record:
            session.add(new_expense_record)
            session.commit()
    else:
        print(Fore.RED + 'Invalid category!' + Fore.RESET)
    
    return new_expense_record


def updateBudgetRecord():
    total_expense = session.query(func.sum(ExpenseRecord.amount))\
                    .filter(and_(extract('month', ExpenseRecord.date)==today.month,
                                extract('year', ExpenseRecord.date)==today.year))\
                    .scalar()
    
    total_saving = session.query(func.sum(ExpenseRecord.amount))\
                            .filter(and_(extract('month', ExpenseRecord.date)==today.month,
                                        extract('year', ExpenseRecord.date)==today.year,
                                                 ExpenseRecord.category=='saving'))\
                            .scalar()

    query_time = getQueryTime(get_today=True)
    result = session.query(BudgetRecord).filter_by(month=query_time).first()

    if result is None:
        new_budget_record = BudgetRecord(month=query_time, outcome=total_expense, saving=total_saving)
        session.add(new_budget_record)
    else:
        result.outcome = total_expense
        result.saving = total_saving
    session.commit()


def getExpense(category: str):
    clearScreen()

    print(Fore.BLUE + "---- " + menu_add[category]['command'] + " ----" + Fore.RESET)
    print(Fore.RED + '(nhap 0 vao muc [so tien] de huy)' + Fore.RESET)

    try:
        amount = int(input(Fore.GREEN + '[so tien] ' + Fore.RESET))
    except:
        amount = 0

    if amount == 0:
        return None

    content = input(Fore.GREEN + '[noi dung] ' + Fore.RESET)

    return ExpenseRecord(date=date.today(), category=menu_add[category]['category'], 
                        amount=amount, content=content)


def deleteLastExpense(*args) -> CommandCode:
    last_id = session.query(func.max(ExpenseRecord.id_num)).scalar()
    result = session.query(ExpenseRecord).filter(ExpenseRecord.id_num == last_id)

    # or use subquery
    #
    # subquery = session.query(func.max(ExpenseRecord.id_num)).subquery()
    # result = session.query(ExpenseRecord).filter(ExpenseRecord.id_num.in_(subquery))

    result.delete(synchronize_session=False)
    session.commit()

    setMessage(f'{last_id} -> result {result}')
    return CommandCode.ADD


#------------------ functions for CHECK -----------------------#

def func_check(*args):
    clearScreen()
    showMessage()
    showMenu(menu_check)

    choice = input('>> ')
    check_value = menu_check.get(choice, None)

    if check_value is None:
        setMessage(f"{choice}: Invalid choice!")
        return CommandCode.CHECK

    else:
        return execFunc(menu_check, choice)


def checkExpenseRecord():
    clearScreen()
    query_time = getQueryTime()

    if not query_time:
        return CommandCode.CHECK

    result = session.query(ExpenseRecord.category, 
                            ExpenseRecord.amount, 
                            ExpenseRecord.content) \
                    .filter(and_(extract('month', ExpenseRecord.date)==query_time['month'],
                                extract('year', ExpenseRecord.date)==query_time['year'])) \
                    .order_by(ExpenseRecord.category)

    setMessage(formatResultTable(result, "category", "amount", "content"))

    return CommandCode.CHECK


def checkBudgetRecord():
    clearScreen()
    result = session.query(BudgetRecord.month, BudgetRecord.income, 
                            BudgetRecord.outcome, BudgetRecord.saving)

    setMessage(formatResultTable(result, "month", "income", "outcome"))

    return CommandCode.CHECK

#-----------------------------------------#

def func_update(*args):
    clearScreen()
    setMessage("---- [UPDATE] ----")
    showMessage()

    query_time = getQueryTime(get_today=True)

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

    return CommandCode.WAIT


def showMenu(menu):
    for (k, v) in menu.items():
        print(Fore.GREEN + f"[{k}] {v['command']}" + Fore.RESET)


def showMessage():
    print(Fore.BLUE + ">> " + system_message + Fore.RESET)
    setMessage("...")


def setMessage(message: str):
    global system_message
    system_message = message


def clearScreen():
    os.system("clear")


def formatResultTable(data, *fields):
    result = table_header_template.format('+', fields=fields)

    for d in data:
        result += table_row_template.format(values=d)
    return result


def runCommand(code: CommandCode) -> CommandCode:
    return eval(command_map[code]['action'])()


def execFunc(menu, choice: str, *args) -> CommandCode:
    return eval(menu[choice]['action'])(*args)


def event_loop():
    command = command_code_map.get(args['command'].lower(), CommandCode.WAIT)

    while True:
        command = runCommand(command)


if __name__ == '__main__':
    engine = create_engine('sqlite:///record.db', echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    initialize()

    event_loop()