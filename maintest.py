import flet
from flet import IconButton, Page, Row, TextField, icons
from flet.ref import Ref
from controle import Controle

class Main:    

    def __init__(self, page):        
        self.txt_number = Ref[TextField]()
        self.components = {
            'txt_number' : self.txt_number 
        }
        
        self.page = page
        self.controle = Controle(self.page, self.components)

    def mount(self):    
        self.page.title = "Flet counter example"
        self.page.vertical_alignment = "center" 
        # self.page.theme_mode = "light"               
        self.page.add(
            Row(
                [
                    IconButton(icons.REMOVE, on_click=self.controle.minus_click),
                    TextField(ref=self.components['txt_number'], value="0", text_align="right", width=100),
                    IconButton(icons.ADD, on_click=self.controle.plus_click),
                ],
                alignment="center",
            )
        )


def main(page: Page):
    m = Main(page)
    m.mount()        

flet.app(target=main)