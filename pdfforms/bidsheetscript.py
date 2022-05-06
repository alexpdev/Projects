import time
from fpdf import FPDF
from fpdf.enums import Align

lines = open("next.csv").read().split('\n')




class PDF(FPDF):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.imgs = {
            "carl": "assets/carl.png",
            "socal": "assets/socalpit.jpg",
            "handpaw": "assets/handpaw.png"
        }
        self.font = "helvetica"
        self.title = "Silent Auction Bid Sheet"
        self.fields = ["Description", "Min Bid", "Min Raise", "Value"]
        self.table_columns = ["Name", "Phone", "Bid Amount"]
        self.line = None
        self.out = None


    def run(self):
        self.add_page()
        self.set_font(self.font, "b", 16)
        self.head()
        self.titlefunc()
        self.improved_table(self.table_columns)
        self.fieldsfunc()
        # self.set_table()
        self.output(self.out)

    def accept_entry(self, line, out):
        self.line = line
        self.out = out

    def head(self):
        self.image(self.imgs['carl'], w=40, x=15, y=36)
        self.image(self.imgs['handpaw'], w=45, x=(self.epw*2)/5 + 6, y=5)
        self.image(self.imgs['socal'], w=35, x=self.epw - 30, y=20)

    def titlefunc(self):
        self.set_font(self.font, "b", 24)
        self.set_text_color(25,55,200)
        self.set_x(self.epw/2)
        self.set_y(60)
        self.cell(txt=self.title, align=Align.C, w=self.epw)
        self.set_text_color(0)

    def improved_table(self, headings, rows=9, col_widths=(60, 60, 60)):
        self.set_y(140)
        self.set_x(self.get_x() + 10)
        self.set_font(self.font, "b", 15)
        for col_width, heading in zip(col_widths, headings):
            self.cell(col_width, 7, heading, 1, 0, "C")
        self.ln()
        for row in range(rows):
            self.set_x(self.get_x() + 10)
            self.cell(col_widths[0], 12, '', 1)
            self.cell(col_widths[1], 12, '', 1)
            self.cell(col_widths[2], 12, '', 1)
            # self.cell(col_widths[3], 6, 'row[3]', "LR", 0, "R")
            self.ln()
        # Closure line:
        # self.cell(sum(col_widths), 0, "", "T")

    def fieldsfunc(self):
        self.set_y(75)
        self.set_x(30)
        self.set_font(self.font, "b", 12)
        self.cell(txt=f"Description: ", w=30, align=Align.L)
        self.set_font(self.font, "bi", 15)
        self.multi_cell(txt=self.line[0], w=self.epw*.65, align=Align.L)
        self.ln()
        self.ln()
        self.set_font(self.font, "b", 12)
        self.set_x(30)
        self.cell(txt=f"Donated by: ", w=30, align=Align.L)
        self.set_font(self.font, "bi", 14)
        self.multi_cell(txt=self.line[-1], w=self.epw*.6, align=Align.L)
        self.ln()
        self.ln()
        self.ln()
        self.ln()
        self.set_x(40)
        self.set_font(self.font, "b", 12)
        self.cell(w=self.epw/8, txt="Value: ", align=Align.R)
        self.set_font(self.font, "i", 15)
        if self.line[1] == "priceless":
            self.cell(w=self.epw/7, txt=f"priceless", align=Align.L)
        else:
            self.cell(w=self.epw/7, txt=f"${self.line[1]}", align=Align.L)
        self.set_font(self.font, "b", 12)
        self.cell(w=self.epw/8, txt="Min Bid: ", align=Align.R)
        self.set_font(self.font, "i", 15)
        self.cell(w=self.epw/8, txt=f"${self.line[2]}", align=Align.L)
        self.set_font(self.font, "b", 12)
        self.cell(w=self.epw/8, txt="Min Raise: ", align=Align.R)
        self.set_font(self.font, "i", 15)
        self.cell(w=self.epw/8, txt=f"${self.line[3]}", align=Align.L)
        # self.cell()


    # def set_table(self):
    #     y = (2 * self.eph)/3
    #     x = self.eph/3
    #     self.set_x(x)
    #     self.set_y(y)
    #     print(self.get_x(), self.get_y())
    #     line_height = self.font_size * 2.5
    #     col_width = self.epw / 4
    #     for item in self.table_columns:
    #         self.cell(col_width, line_height, item, border=1)
    #         print(self.get_x(), self.get_y())
    #     self.ln()
    #     print(self.get_x(), self.get_y())
    #     for i in range(5):
    #         for _ in range(len(self.table_columns)):
    #             print(self.get_x(), self.get_y())
    #             self.cell(col_width, line_height, "", border=1)
    #             print(self.get_x(), self.get_y())
    #         self.ln()


def basic_table(self, headings, rows):
        for heading in headings:
            self.cell(40, 7, heading, 1)
        self.ln()
        for row in rows:
            for col in row:
                self.cell(40, 6, col, 1)
            self.ln()



for i, line in enumerate(lines[:-1]):
    entries = line.split(",")
    pdf  = PDF(format="letter")
    pdf.accept_entry(entries, "bid_sheet %2d.pdf" % i)
    pdf.run()
    time.sleep(.3)
    del pdf
