from View import Card, Syndicate, Company, Pouch


def menu():
    option = ' '
    while option != '0':
        print(''' Select the option Register
        1 - Card
        2 - Syndicate
        3 - Company
        4 - Pouch
        0 - Exit ''')
        option = input('option: ').strip()
        if option == '0':
            continue
        elif option == '1':
            Card.menu()
        elif option == '2':
            Syndicate.menu()
        elif option == '3':
            Company.menu()
        elif option == '4':
            Pouch.menu()
        else:
            print('\33[1;31mInvalid option\33[m')
    print('-' * 40)
