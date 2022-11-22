# pip install pyperclip

import pyperclip as pc 
import flet
from flet import Text,Page,FloatingActionButton,icons,Row,SnackBar

def main(page : Page):
    page.theme_mode = "light"
    page.window_width = 400
    page.window_height = 200
    
    def copiar(e):
        pc.copy(text1.value)

        page.snack_bar = SnackBar(Text("Copiado para área de transferência!"))
        page.snack_bar.open = True
        page.update()

    text1 = Text(value = "GeeksforGeeks")
    botao = FloatingActionButton(icon=icons.COPY,scale=0.7,on_click=copiar)
    
    page.add(Row([text1,botao]))

flet.app(target=main)
