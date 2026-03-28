import sqlite3


class DBParser:
    def __init__(self, filename:str):
        self.target:str = filename
        self.connection = sqlite3.connect(filename)


    def get_tables(self) -> list[str]:
        self.cursor = self.connection.cursor()
        sql:str = "SELECT name FROM sqlite_master WHERE type='table'"

        self.cursor.execute(sql)
        tables:list[str] = []
        table:str

        for record in self.cursor.fetchall():
            table = record[0]
            if table != "sqlite_sequence":
                tables.append(table)

        return tables


    def value_to_string(self, value) -> str:
        if value is None:
            return ""

        if type(value) == str:
            return value

        if type(value) == int:
            return str(value)

        if type(value) == float:
            return str(value)

        if type(value) == bytes:
            if len(value) > 32:
                return f"<BLOB {len(value)} bytes>"

            try:
                return value.decode("utf-8")
            except:
                return f"<BLOB {len(value)} bytes>"

        # TODO: Add better error handling
        print("ERROR: Could not parse value type", type(value))
        exit()


    # {header : [values]}
    def parse_table(self, table:str) -> dict[str,list[str]]:
        table_values:dict[str,list[str]] = {}
        self.cursor = self.connection.cursor()

        sql:str = f"PRAGMA table_info({table})"
        self.cursor.execute(sql)
        field_name:str
        
        for info in self.cursor.fetchall():
            field_name = info[1]
            table_values[field_name] = []

        sql = f"SELECT * FROM {table}"
        self.cursor.execute(sql)
        field_index:int = 0

        for record in self.cursor.fetchall():
            for field in table_values:
                table_values[field].append(
                    self.value_to_string(record[field_index])
                )
                field_index += 1

            field_index = 0

        return table_values

