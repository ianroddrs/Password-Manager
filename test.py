import flet
from flet import Page,Row,Container,colors,Text,border,Column,TextField,icons,FloatingActionButton, FilledButton,ButtonStyle,RoundedRectangleBorder

def main(page: Page):
    page.title = "Password Manager"
    page.theme_mode = "light"
    page.window_min_width = 600
    page.window_width = 600
    page.window_min_height = 600
    page.window_height = 600

    page.add(
        Container(
            content=Column(
                [
                    Row([Text("Ian Rodrigues",size=40,weight="bold")],alignment="center"),
                    Container(bgcolor=colors.BLACK45,height=1,margin=20),
                    Row(
                        [
                            TextField(scale=0.8,label='Username',prefix_icon=icons.ACCOUNT_CIRCLE,value="Ian Rodrigues"),
                            FloatingActionButton(scale=0.7,icon=icons.CHECK)
                        ],alignment="center"
                    ),
                    Row(
                        [
                            TextField(scale=0.8,label='E-mail',prefix_icon=icons.ACCOUNT_CIRCLE,value="ian@gmail.com"),
                            FloatingActionButton(scale=0.7,icon=icons.CHECK)
                        ],alignment="center"
                    ),

                    FilledButton(text='Mudar Senha',width=310,style=ButtonStyle(shape={"hovered": RoundedRectangleBorder(radius=20),"": RoundedRectangleBorder(radius=5)},))

                    
                    
                ],horizontal_alignment="center"
            ),border=border.all(1),border_radius=20,padding=15,
        ),
    )



flet.app(target=main)