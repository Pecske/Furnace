import sys
from ui.Menu import Menu


def main():
    main_menu = Menu()
    if len(sys.argv) > 1:
        table_creation_arg = sys.argv[1]
        if table_creation_arg == "-c":
            main_menu.create_table()
            main_menu.import_panels()
    else:
        main_menu.show()


if __name__ == "__main__":
    main()
