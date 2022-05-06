from fpdf import FPDF

class PDF(FPDF):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        font = 'Arial'
        self.add_page()
        self.set_font(font, "b", 6)
        self.draw_grid()
        self.output("grid.pdf")

    def draw_grid(self):
        x = self.get_x()
        y = self.get_y()
        while x < self.epw:
            self.text(x, y, str(int(x)))
            x += 10
        while y < self.eph:
            self.text(x, y, str(int(y)))
            y += 10

pdf=PDF()
