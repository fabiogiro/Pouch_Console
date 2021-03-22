from Models.Card import Card
from Models.Pouch import Pouch
from Utils.util import inform_code, inform_name


def search_name_card() -> object:
    codeCard: int = inform_code('Card')

    if codeCard == 0:
        return Card(0, '')
    # Check if have the card exist
    regcard: Card = Card(codeCard, Card.findcode(codeCard).strip())

    return regcard


def validcard(option: int) -> Card:
    regok: bool = False
    while not regok:
        regcard: Card = search_name_card()
        # the code informed is ok
        if int(regcard.codeCard) == 0:
            regcard: Card = Card(0, '')
            break
        if option == 1:   # INSERT
            if regcard.nameCard == '':
                # the card not exist
                regok = True
            else:
                print(f'\33[1;31mCard Code exist\33[m')
        else:   # UPDATE / DELETE
            if regcard.nameCard != '':
                # the card exist
                regok = True
            else:
                print(f'\33[1;31mCard Code not exist\33[m')
    return regcard


def insert(option: int) -> None:
    resp = 'Y'
    while resp.upper() == 'Y':
        regcard: Card = validcard(option)
        if int(regcard.codeCard) > 0:
            # the code informed is ok
                regcard.nameCard = inform_name('Card')
                Card.insertdb(regcard)

        resp = ' '
        while resp.upper() not in 'YN':
            resp = input('Do you want continue [Y/N]? ')


def update(option: int) -> None:
    resp = 'Y'
    while resp.upper() == 'Y':
        regcard: Card = validcard(option)
        if int(regcard.codeCard) > 0:
            regcard.nameCard = inform_name('Card')
            Card.updatedb(regcard)

        resp = ' '
        while resp.upper() not in 'YN':
            resp = input('Do you want continue [Y/N}? ')


def delete(option: int) -> None:
    resp = 'Y'
    while resp.upper() == 'Y':
        regcard: Card = validcard(option)
        if int(regcard.codeCard) > 0:
            countcodepouch = Pouch.countcodepouchcard(regcard.codeCard)

            if countcodepouch == 0:
                resp = ' '
                while resp.upper() not in 'YN':
                    resp = input(f'Confirm the delete the {regcard.codeCard} - '
                                 f'{regcard.nameCard} [Y/N]? ')
                    if resp.upper() == 'Y':
                        Card.deletedb(regcard)
            else:
                print(f'\33[1;31mHave Pouch registered\33[m')
        resp = ' '
        while resp.upper() not in 'YN':
            resp = input('Do you want continue [Y/N}? ')


def list():
    # List all cards
    Card.findall(self=object)


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
