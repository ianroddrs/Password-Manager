import flet as ft
from flet import AppBar, Page, Text, View ,ElevatedButton, colors,Container, PopupMenuButton,PopupMenuItem,Row, Icon,icons, NavigationRail,NavigationRailDestination,IconButton,FloatingActionButton,VerticalDivider,Column, ButtonStyle,TextField,FilledButton,margin, TextButton, alignment, AlertDialog


def main(page: ft.Page):
    page.title = "AlertDialog examples"

    dlg = ft.AlertDialog(
        title=ft.Text("Hello, you!"), on_dismiss=lambda e: print("Dialog dismissed!")
    )

    def close_dlg(e):
        dlg_modal.open = False
        page.update()

    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Please confirm"),
        content=Container(content=Row(
                            [
                                Column(controls=[
                                        Container(content=Text("123123"),width=500,alignment=alignment.center_left,margin=margin.only(bottom=15)),
                                        Row([TextField(label="oioi"),TextField(label="alkh"),]),
                                        FilledButton(text="lasihd")
                                    ],scroll="hidden",expand=True,alignment="center",horizontal_alignment="center"
                                )
                            ],expand=True,
                        ),expand=True),
        on_dismiss=lambda e: print("Modal dialog dismissed!"),
    )

    def open_dlg(e):
        page.dialog = dlg
        dlg.open = True
        page.update()

    def open_dlg_modal(e):
        page.dialog = dlg_modal
        dlg_modal.open = True
        page.update()

    page.add(
        ft.ElevatedButton("Open dialog", on_click=open_dlg),
        ft.ElevatedButton("Open modal dialog", on_click=open_dlg_modal),
    )

ft.app(target=main)