from enum import Enum

from windows.window import Window

from widgets.tab_list import TabList
from widgets.helper_bar import HelperBar
from widgets.table_values import TableValues
from widgets.text_input import TextInput


class NavMode(Enum):
    TABLES = 0
    VALUES = 1


class W_Viewport(Window):
    def __init__(self, app:'JSQL3'):
        super().__init__(app)

        self.options:dict[str,str] = {
            "space" : "Toggle NavMode",
            't'     : "Navigate Tables",
            'v'     : "Navigate Values",
            'q'     : "Quit"
        }

        self.input_buffer:str = ""
        self.navmode = NavMode.TABLES

        self.tables:list[str] = []
        self.table_selected:int = 0

        # {field : [values]}
        self.values:dict[str,list[str]] = {}

        # {field : top_line}
        self.top_lines:dict[str,int] = {}
        self.load_tables()


    def load_tables(self):
        self.tables = self.app.db.get_tables()
        
        if len(self.tables) != 0:
            for table in self.tables:
                self.top_lines[table] = self.top_lines.get(table, 0)

            self.values = self.app.db.parse_table(
                self.tables[self.table_selected]
            )


    def render_horizontal_divider(self, screen, line:int):
        width:int = screen.getmaxyx()[1]
        divider:str = '=' * (width - 1)

        screen.addstr(line, 0, divider)


    def get_selected_table_name(self) -> str | None:
        if len(self.tables) == 0:
            return None

        return self.tables[self.table_selected]


    def render(self, screen):
        TabList.render(screen, self.tables, 0, self.table_selected)
        self.render_horizontal_divider(screen, 1)

        if len(self.values) > 0:
            height:int = screen.getmaxyx()[0]

            TableValues.render(
                screen, self.values, line = 2,
                line_limit = (height - len(self.options)),
                top_line = self.top_lines[
                    self.get_selected_table_name()
                ]
            )

        HelperBar.render_options(screen, self.options)

        height:int
        width:int
        height, width = screen.getmaxyx()

        y = height - 1
        x = width - len("Navmode: Tables") - 1

        if self.navmode == NavMode.TABLES:
            nav:str = "Tables"
        else:
            nav:str = "Values"

        screen.addstr(y, x, f"Navmode: {nav}")


    def _handle_global_navigate(self, key:str):
        match(key):
            case ' ':
                if self.navmode == NavMode.TABLES:
                    self.navmode = NavMode.VALUES
                else:
                    self.navmode = NavMode.TABLES

            case 't': self.navmode = NavMode.TABLES
            case 'v': self.navmode = NavMode.VALUES
            case 'q': self.app.running = False


    def _handle_table_navigate(self, key:str):
        if key in "hk":
            self.table_selected = max(
                self.table_selected - 1, 0
            )

        elif key in "jl":
            self.table_selected = min(
                self.table_selected + 1, len(self.tables) - 1
            )

        self.load_tables()


    def _handle_value_navigate(self, key:str):
        table:str = self.get_selected_table_name()

        match(key):
            case 'j':
                rows:int = len(self.values[list(self.values)[0]])
                self.top_lines[table] = min(
                    self.top_lines[table] + 1, rows - 1
                )

            case 'k':
                self.top_lines[table] = max(
                    self.top_lines[table] - 1, 0
                )



    def handle_input(self, key:str):
        if len(self.tables) == 0:
            return

        self._handle_global_navigate(key)

        match(self.navmode):
            case NavMode.TABLES: self._handle_table_navigate(key)
            case NavMode.VALUES: self._handle_value_navigate(key)

