from enum import IntEnum

class CommandCode(IntEnum):
    WAIT = 0
    ADD = 1
    CHECK = 2
    UPDATE = 3
    BACK = 4
    QUIT = 5

# dict {command key: [command, callback]}
command_map = {
                CommandCode.ADD: {'command': 'add', 'action': 'func_add'}, 
                CommandCode.CHECK: {'command': 'check', 'action': 'func_check'},
                CommandCode.UPDATE: {'command': 'update', 'action': 'func_update'},
                CommandCode.WAIT: {'command': 'wait', 'action': 'func_wait'},
                CommandCode.BACK: {'command': 'back', 'action': 'func_back'},
                CommandCode.QUIT: {'command': 'quit', 'action': 'func_quit'}
            }

command_code_map = {
                    'wait': CommandCode.WAIT, 
                    'add': CommandCode.ADD, 'a': CommandCode.ADD, 
                    'check': CommandCode.CHECK, 'c': CommandCode.CHECK, 
                    'update': CommandCode.UPDATE, 'u': CommandCode.UPDATE,
                    'back': CommandCode.BACK, 
                    'quit': CommandCode.QUIT
                    }

menu_wait = {
                'a': {'command': 'add', 'action': 'func_add'}, 
                'c': {'command': 'check', 'action': 'func_check'}, 
                'u': {'command': 'update', 'action': 'func_update'},
                'q': {'command': 'quit', 'action': 'func_quit'}
            }

# dict {category index: [detail, category]}
menu_add = {
                '1': {'command': 'Quy chi tieu can thiet', 'category': 'living', 'action': 'updateDatabase'}, 
                '2': {'command': 'Quy tiet kiem dai han', 'category': 'saving', 'action': 'updateDatabase'},
                '3': {'command': 'Quy giao duc', 'category': 'education', 'action': 'updateDatabase'},
                '4': {'command': 'Quy huong thu', 'category': 'playing', 'action': 'updateDatabase'},
                '5': {'command': 'Quy tu do tai chinh', 'category': 'free', 'action': 'updateDatabase'},
                '6': {'command': 'Quy tu thien', 'category': 'giving', 'action': 'updateDatabase'},
                'b': {'command': 'back', 'action': 'func_back'},
                'q': {'command': 'quit', 'action': 'func_quit'}
                }

menu_check = {
                '1': {'command': 'expense', 'action': 'checkExpenseRecord'},
                '2': {'command': 'budget', 'action': 'checkBudgetRecord'},
                'b': {'command': 'back', 'action': 'func_back'},
                'q': {'command': 'quit', 'action': 'func_quit'}
}


menu_check_expense = {
                    '1': {'command': 'by time', 'action': 'checkExpenseRecordByTime'},
                    '2': {'command': 'N most recent expense', 'action': 'checkExpenseRecordRecent'},
                    'b': {'command': 'back', 'action': 'func_back'},
                    'q': {'command': 'quit', 'action': 'func_quit'}
                }


table_header_template = '''
{0:+<60}
+{fields[0]:^16}+{fields[1]:^10}+{fields[2]:^30}+
{0:+<60}
'''

table_row_template = "+{values[0]:^16}+{values[1]:^10}+{values[2]:^30}+\n"
