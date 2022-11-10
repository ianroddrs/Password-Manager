class Controle:

    def __init__(self, page, components):
        self.page = page
        self.components = components

    def minus_click(self, e):
        self.components['txt_number'].current.value = int(self.components['txt_number'].current.value)-1
        self.page.update()

    def plus_click(self, e):
        self.components['txt_number'].current.value = int(self.components['txt_number'].current.value)+1
        self.page.update()

