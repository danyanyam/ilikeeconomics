import argparse

# Скрипт должен по конфигу создавать предписанную структуру папок.
# Создаваемые папки могут содержать файлы из ./rcs

def bash_args_handler():
    parser = argparse.ArgumentParser(description='My script')
    parser.add_argument('-path_to', action="store", help="Folder address",
                        dest="path_to", required=True, type=str)

    args = parser.parse_args()
    return print(args)

def main():
    parser = bash_args_handler()
    return None

if __name__ == '__main__':
    main()
