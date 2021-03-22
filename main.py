import menuRegister, Report, DataAnalysis


def main() -> None:
    option = ' '
    while option != '0':
        print(''' Select the option:
        1 - Register
        2 - Report
        3 - Data Analysis
        0 - Exit ''')
        option = input('option: ').strip()
        if option == '0':
            continue
        elif option == '1':
            menuRegister.menu()
        elif option == '2':
            Report.menu()
        elif option == '3':
            DataAnalysis.menu()
        else:
            print('\33[1;31mInvalid option\33[m')
    print('Thanks')


if __name__ == '__main__':
    main()
