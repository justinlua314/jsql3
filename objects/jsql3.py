from objects.db_parser import DBParser

from windows.w_viewport import W_Viewport


class JSQL3:
    def __init__(self, screen, db_path:str):
        self.screen = screen
        self.running:bool = False
        self.db = DBParser(db_path)
        self.viewport = W_Viewport(self)


    def run(self):
        self.running = True

        while self.running:
            self.screen.erase()
            self.viewport.render(self.screen)
            self.screen.refresh()

            key = self.screen.getkey()
            self.viewport.handle_input(key)

