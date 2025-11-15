import sys
from ui.Menu import Menu


def main():
    main_menu = Menu()
    if len(sys.argv) > 1:
        if "-c" in sys.argv:
            main_menu.create_table()
        if "-p" in sys.argv:
            main_menu.import_panels()
        if "-a" in sys.argv:
            main_menu.import_portions()
    else:
        main_menu.show()


if __name__ == "__main__":
    main()
