from lib.helpers import Helpers


class TableValues:
    def render(
        screen, table_values:dict[str,list[str]],
        line:int, line_limit:int, top_line:int
    ):
        width:int = screen.getmaxyx()[1]

        # Measure max size of all fields
        field_partitions:list[int] = []
        row_count:int = 0

        for field in table_values:
            field_partitions.append(max(
                len(field),
                max([len(val) for val in table_values[field]])
            ) + 1)

            row_count = max(row_count, len(table_values[field]))

        # Partition width of each field so largest fields shrink first
        render_width:int
        shrink_index:int
        spacer:int = len("|  |")

        while True:
            render_width = sum(field_partitions)
            render_width += (spacer * len(field_partitions))

            if render_width >= width:
                shrink_index = field_partitions.index(
                    max(field_partitions)
                )

                field_partitions[shrink_index] -= 1
                continue

            break

        # Render Headers
        y:int = line
        x:int = 0

        for index, header in enumerate(table_values):
            border = '-' * (
                field_partitions[index] + len("|  |")
            )

            screen.addstr(y, x, border)
            x += len(border)

        y += 1
        x = 0

        if y == line_limit:
            return

        text:str

        for index, header in enumerate(table_values):
            text = Helpers.center_text(
                header, field_partitions[index]
            )

            screen.addstr(y, x, f"| {text} |")
            x += len(f"| {text} |")

        y += 1

        if y == line_limit:
            return

        x = 0
        border:str

        for index, header in enumerate(table_values):
            border = '-' * (
                field_partitions[index] + len("|  |")
            )

            screen.addstr(y, x, border)
            x += len(border)

        y += 1

        if y == line_limit:
            return

        x = 0

        # Render Values
        line_index:int = 0

        for row_index in range(row_count):
            if line_index < top_line:
                line_index += 1
                continue

            for field_index, field in enumerate(table_values):
                text = table_values[field][row_index]

                text = Helpers.center_text(
                    text, field_partitions[field_index]
                )

                screen.addstr(y, x, f"| {text} |")
                x += len(f"| {text} |")

            y += 1

            if y == line_limit:
                return

            x = 0

            for field_index in range(len(table_values)):
                border = '-' * (
                    field_partitions[field_index] + len("|  |")
                )

                screen.addstr(y, x, border)
                x += len(border)

            y += 1

            if y == line_limit:
                return

            x = 0
            line_index += 1

