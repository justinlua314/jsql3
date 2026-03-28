import sys

from curses import wrapper

from objects.jsql3 import JSQL3


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: jsql3 <database.sqlite>")
        sys.exit(1)

    db_path:str = sys.argv[1]

    def main(screen):
        app = JSQL3(screen, db_path)
        app.run()

    wrapper(main)

