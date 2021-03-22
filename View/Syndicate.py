from Models.Syndicate import Syndicate
from Models.Pouch import Pouch
from Utils.util import inform_code, inform_name


def search_name_synd() -> object:
    codeSynd: int = inform_code('Syndicate')

    if codeSynd == 0:
        return Syndicate(0, '')
    # Check if the syndicate exist
    regsynd: Syndicate = Syndicate(codeSynd, Syndicate.findcode(codeSynd).strip())
    return regsynd


def validsyndicate(option: int) -> Syndicate:
    regok = False
    while not regok:
        regsynd: Syndicate = search_name_synd()
        # the code informed is ok
        if int(regsynd.codeSynd) == 0:
            regsynd: Syndicate = Syndicate(0, '')
            break
        if option == 1:   # INSERT
            if regsynd.nameSynd == '':
                # the syndicate not exist
                regok = True
            else:
                print(f'\33[1;31mSyndicate Code exist\33[m')
        else:   # UPDATE / DELETE / SEARCH
            if regsynd.nameSynd != '':
                # the syndicate exist
                regok = True
            else:
                print(f'\33[1;31mSyndicate Code not exist\33[m')

    return regsynd


def insert(option: int) -> None:
    resp = 'Y'
    while resp.upper() == 'Y':
        regsynd: Syndicate = validsyndicate(option)
        if int(regsynd.codeSynd) > 0:
            regsynd.nameSynd = inform_name('Syndicate')
            Syndicate.insertdb(regsynd)

        resp = ' '
        while resp.upper() not in 'YN':
            resp = input('Do you want continue [Y/N]? ')


def update(option: int) -> None:
    resp = 'Y'
    while resp.upper() == 'Y':
        regsynd: Syndicate = validsyndicate(option)
        # the code informed is ok
        if int(regsynd.codeSynd) > 0:
            regsynd.nameSynd = inform_name('Syndicate')
            Syndicate.updatedb(regsynd)

        resp = ' '
        while resp.upper() not in 'YN':
            resp = input('Do you want continue [Y/N}? ')


def delete(option: int) -> None:
    resp = 'Y'
    while resp.upper() == 'Y':
        regsynd: Syndicate = validsyndicate(option)
        if int(regsynd.codeSynd) > 0:
            countcodepouch = Pouch.countcodepouchsynd(regsynd.codeSynd)

            if countcodepouch == 0:
                resp = ' '
                while resp.upper() not in 'YN':
                    resp = input(f'Confirm the delete the {regsynd.codeSynd} - '
                                 f'{regsynd.nameSynd} [Y/N]? ')
                if resp.upper() == 'Y':
                   Syndicate.deletedb(regsynd)
            else:
                print(f'\33[1;31mHave Pouch registered\33[m')

        resp = ' '
        while resp.upper() not in 'YN':
            resp = input('Do you want continue [Y/N}? ')


def list():
    # list all syndicate
    Syndicate.findall(self=object)


def menu():
    option = ' '
    while option != '0':
        print('''Select the option Card
        1 - Insert
        2 - Update
        3 - Delete
        4 - List
        0 - Exit''')
        option = input('option: ').strip()
        if option == '0':
            continue
        elif option == '1':
            insert(int(option))
        elif option == '2':
            update(int(option))
        elif option == '3':
            delete(int(option))
        elif option == '4':
            list()
        else:
            print('-' * 40)
            print('\33[1;31mInvalid option\33[m')
            print('-' * 40)
    print('-' * 40)
