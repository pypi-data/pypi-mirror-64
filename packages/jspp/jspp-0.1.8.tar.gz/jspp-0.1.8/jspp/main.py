"""Main Module"""

def display_sstjs_logo():
    print("                                                                                         ")
    print("                                                                                         ")
    print("     ,--.,--.     ,--.             ,---.               ,--.         ,--.                 ")
    print("     |  ||  ,---. `--',--,--,     '   .-'  ,---.,--.--.`--' ,---. ,-'  '-. ,---. ,--.--. ")
    print(",--. |  ||  .-.  |,--.|      \\    `.  `-. | .--'|  .--',--.| .-. |'-.  .-'| .-. :|  .--' ")
    print("|  '-'  /|  | |  ||  ||  ||  |    .-'    |\\ `--.|  |   |  || '-' '  |  |  \\   --.|  |    ")
    print(" `-----' `--' `--'`--'`--''--'    `-----'  `---'`--'   `--'|  |-'   `--'   `----'`--'    ")
    print("                                                           `--'                          ")
    print("                                                                                         ")

def display_windows_logo():
    print('                                                                                         ')
    print('                /|  /|  ---------------------------   ,--------------------------===---. ')
    print('                ||__||  |                         |   | Jhin Scripter#0922              |')
    print('               /   O O\\__  I have a horny little  |   | ,----------------------------.  |')
    print('              /          \\   operating system     |   | |                             | |')
    print('             /      \\     \\                       |   | |                             | |')
    print('            /   _    \\     \\ ----------------------   | |                             | |')
    print('           /    |\\____\\     \\      ||                 | |     _       _--""--_        | |')
    print('          /     | | | |\\____/      ||                 | |       " --""   |    |       | |')
    print('         /       \\| | | |/ |     __||                 | |     " . _|     |    |       | |')
    print('        /  /  \\   -------  |_____| ||                 | |     _    |  _--""--_|       | |')
    print('       /   |   |           |       --|                | |       " --""   |    |       | |')
    print('       |   |   |           |_____  --|                | |    "  . _|     |    |       | |')
    print('       |  |_|_|_|          |     \\----                | |     _    |  _--""--_|       | |')
    print('       /\\                  |                          | |       " --""                | |')
    print('      / /\\        |        /                          | |                             | |')
    print('     / /  |       |       |                           | |.............................| |')
    print(' ___/ /   |       |       |                           | |  _  :          ´      :  _  | |')
    print('|____/    c_c_c_C/ \\C_c_c_c                           | | |_| :                 : |_| | |')
    print('                                                      | |  _  :_               _:  _  | |')
    print('                                                      | | |_| :.)        .    (.: |_| | |')
    print('                                                      | ´-----....._________.....-----´ |')
    print('                                                      |     _    _     O     _    _     |')
    print('                                                      |    |_|  |_|    |    |_|  |_|    |')
    print('                                                      "------......____O____......------"')
    print('                                                                                         ')

def get_multiplication_table(num):
    return [(f"{x} X {num} = {x*num}\n") for x in list(range(0,11))]

def rot_string_left(string, rot):
    return string[rot:] + string[:rot]

def rot_string_right(string, rot):
    x1 = len(string)
    return string[x1-rot:] + string[:x1-rot]