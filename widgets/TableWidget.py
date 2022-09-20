from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import BorderImage
from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty
from kivy.properties import ListProperty
from kivy.properties import NumericProperty

primary_color = StringProperty('ffffcc')
secondary_color = StringProperty('ffffcc')
header_color = StringProperty('ffffcc')

class MyLabelPrimary(Label):
    primary_color = ListProperty([0, 0, 1, .5])
    def on_size(self, *_):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0, 0, 1, .5)
            Rectangle(pos=self.pos, size=self.size)
            BorderImage(pos=(self.x, self.y + 1), size=(self.width, self.height - 2), border=(0, 0, 0, 50),
                        Color=Table.primary_color)

class MyLabelSecondary(Label):
    secondary_color = ListProperty([0, 7, 0, .5])
    def on_size(self, *_):
        self.canvas.before.clear()
        with self.canvas.before:
            c = (0, 2, 0, 1)
            Color(0, 7, 0, .5)
            Rectangle(pos=self.pos, size=self.size)
            BorderImage(pos=(self.x, self.y + 1), size=(self.width, self.height - 2), border=(0, 0, 0, 50),
                        Color=Table.secondary_color)

class MyLabelHeader(Label):
    header_color = ListProperty([0, 0, 1, .5])
    def on_size(self, *_):
        self.canvas.before.clear()
        with self.canvas.before:
            print("header color:" + str(self.header_color))
            print("header color:" + str(self.header_color[0]))
            Color(self.header_color[0],self.header_color[1],self.header_color[2], self.header_color[3])
            Rectangle(pos=self.pos, size=self.size)
            BorderImage(pos=(self.x, self.y + 1), size=(self.width, self.height - 2), border=(0, 0, 0, 50),
                        Color=header_color)

class Table(Widget):

    primary_color = ListProperty([0, 0, 1, .5])
    secondary_color = ListProperty([0, 7, 0, .5])
    header_color = ListProperty([1, 0, 1, .5])
    table_height = NumericProperty(3)
    table_width = NumericProperty(3)
    table_columns = NumericProperty(3)
    table_rows = NumericProperty(5)
    table_Information = []
    cols_titles = []

    def addHeader(self,list):
        self.cols_titles=list
        self.Build()

    def addRow(self,list):
        self.table_Information.insert(0,list)
        self.Build()

    def Build(self):
        self.grid.clear_widgets()
        print("Table Information" + str(self.table_Information))
        header = 0
        while self.table_columns > header:
            text=""
            if(len(self.cols_titles)>header):
                text = self.cols_titles[header]
            h = MyLabelHeader(text=text,size_hint=[.15,.15],header_color=self.header_color)
            self.grid.add_widget(h)
            header = header + 1
        primaryorsecondary = 1
        rowCheck = 0
        while rowCheck < self.table_rows-1:
            columnCheck = 0
            while columnCheck < self.table_columns:
                text = ""
                if len(self.table_Information) > rowCheck:
                    print("len col:" + str(self.table_Information))
                    if len(self.table_Information[rowCheck]) > columnCheck:
                        print("len row:" + str(self.table_Information[rowCheck][columnCheck]))
                        text = self.table_Information[rowCheck][columnCheck]
                if primaryorsecondary == 1:
                    label = MyLabelPrimary(text=text,size_hint=[.25,.25])
                else:
                    label = MyLabelSecondary(text=text,size_hint=[.25,.25])
                self.grid.add_widget(label)
                columnCheck = columnCheck + 1
            rowCheck = rowCheck + 1
            primaryorsecondary = primaryorsecondary * -1

    def __init__(self, **kwargs):
        super(Table, self).__init__(**kwargs)
        primaryorsecondary = 1
        with self.canvas:
            self.grid = GridLayout(cols=self.table_columns, rows=self.table_rows,size=[self.table_width,self.table_height])
        print("test:"+str(self.table_columns))
        primaryorsecondary = 1
        rowCheck = 0
        while rowCheck < self.table_rows:
            columnCheck = 0
            while columnCheck < self.table_columns:
                if primaryorsecondary == 1:
                    label = MyLabelPrimary(text="primary")
                else:
                    label = MyLabelSecondary(text="secondary")
                self.grid.add_widget(label)
                columnCheck = columnCheck+1
            rowCheck = rowCheck + 1
            primaryorsecondary = primaryorsecondary*-1

class TestApp(App):

    def build(self):
        self.root = root = Table(table_columns=6,table_rows=6,table_height =500,table_width=300,header_color=[0,1,1,.3])
        root.addRow(["2"])
        root.addRow(
            ["Information","Information2","Information3","Information4","Information5","Information6","Break it"]
            )
        root.addRow(
            ["Information", "Information2", "Information3", "Information4", "Information5", "Information6", "Break it"]
            )
        root.addRow(
            ["Information", "Information2", "Information3", "Information4", "Information5", "Information6", "Break it"]
            )
        root.addRow(
            ["Information", "Information2", "Information3", "Information4", "Information5", "Information6", "Break it"]
            )
        root.addRow(
            ["Information", "Information2", "Information3", "Information4", "Information5", "Information6", "Break it"]
            )
        root.addRow(
            ["Information", "Information2", "Information3", "Information4", "Information5", "Information6", "Break it"]
            )
        root.addRow(
            ["Information", "Information2", "Information3", "Information4", "Information5", "Information6", "Break it"]
            )
        root.addRow(
            ["Information", "Information2", "Information3", "Information4", "Information5", "Information6", "Break it"]
            )
        root.addRow(
            ["Information", "Information2", "Information3", "Yeet", "Information5", "Information6", "Break it"]
            )
        root.addHeader(
            ["a","b","c","asd","c","asd","fucl"]
            )
        return root

if __name__ == '__main__':
    TestApp().run()
