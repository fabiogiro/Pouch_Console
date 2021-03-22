from Models.Card import Card
from Utils.util import inform_code, inform_name
from pandas import DataFrame


def search_name_card(dfCard: DataFrame) -> object:
    codeCard: int = inform_code('Card')

    if codeCard == 0:
        return Card(0, '')
    # Check if have the card exist
    regcard: Card = Card(codeCard, Card.findcode(dfCard, codeCard).strip())

    return regcard


def validcard(option: int, dfcard: DataFrame) -> object:
    regok: bool = False
    while not regok:
        regcard: Card = search_name_card(dfcard)
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


def insert(option: int, dfcard: DataFrame) -> None:
    resp = 'Y'
    while resp.upper() == 'Y':
        regcard: Card = validcard(option, dfcard)
        if int(regcard.codeCard) > 0:
            # the code informed is ok
                regcard.nameCard = inform_name('Card')

                dfcard.loc[len(dfcard) + 1] = [regcard.codeCard, regcard.nameCard]
                Card.insertdb(regcard)

        resp = ' '
        while resp.upper() not in 'YN':
            resp = input('Do you want continue [Y/N]? ')


def update(option: int, dfcard: DataFrame) -> None:
    resp = 'Y'
    while resp.upper() == 'Y':
        regcard: Card = validcard(option, dfcard)
        if int(regcard.codeCard) > 0:
            regcard.nameCard = inform_name('Card')

            nameAnt = dfcard.Name
            dfcard['Name'].replace(to_replace=[nameAnt], value=regcard.nameCard, inplace=True)

            Card.updatedb(regcard)

        resp = ' '
        while resp.upper() not in 'YN':
            resp = input('Do you want continue [Y/N}? ')


def delete(option: int, dfcard: DataFrame) -> None:
    resp = 'Y'
    while resp.upper() == 'Y':
        regcard: Card = validcard(option, dfcard)
        if int(regcard.codeCard) > 0:
            resp = ' '
            while resp.upper() not in 'YN':
                resp = input(f'Confirm the delete the {regcard.codeCard} - '
                             f'{regcard.nameCard} [Y/N]? ')
            if resp.upper() == 'Y':
                dfcard = dfcard.drop(dfcard[(dfcard.Code == regcard.codeCard)].index)

                Card.deletedb(regcard)

        resp = ' '
        while resp.upper() not in 'YN':
            resp = input('Do you want continue [Y/N}? ')


def list(dfcard: DataFrame):
    # List all cards
    Card.findall(dfcard)


def menu():
    option = ' '
    dfcard = Card.upload_dataframe(self=object)
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
            insert(int(option), dfcard)
        elif option == '2':
            update(int(option), dfcard)
        elif option == '3':
            delete(int(option), dfcard)
        elif option == '4':
            list(dfcard)
        else:
            print('-' * 40)
            print('\33[1;31mInvalid option\33[m')
            print('-' * 40)
    print('-' * 40)
