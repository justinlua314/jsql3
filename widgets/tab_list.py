from curses import A_REVERSE as highlight


class TabList:
    # TODO: Make sure rendering safely scrolls if there's
    # too many tables
    def render(screen, tabs:list[str], line:int, selected:int):
        width:int = screen.getmaxyx()[1]
        x:int = 0

        for index, tab in enumerate(tabs):
            if index == selected:
                screen.addstr(line, x, f"{tab}", highlight)
            else:
                screen.addstr(line, x, f"{tab}")
            x += len(tab) + 1

            if x >= width:
                break

            if index != len(tabs) - 1:
                screen.addstr(line, x, " | ")
                x += 3

