import flet
from flet import Page

def main(page: Page):
    page.title = "Password Manager"
    page.theme_mode = "light"
    page.window_min_width = 600
    page.window_width = 600
    page.window_min_height = 600
    page.window_height = 600

    



flet.app(target=main)