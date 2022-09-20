from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder

class Terminal(ScrollView):

    Builder.load_file("./terminal/terminal.kv")

    pallet = {'yellow':'FFFF00', 'white':'FFFFFF','blue':'0099FF',
              'green':'00FF00',  'red':'FF0000',  'purple':'FF00FF',
              'orange':'FFBB00', 'gray':'999999'}

    def __init__(self, **kwargs):
        super(Terminal, self).__init__(**kwargs)
        self.TerminalGrid = TerminalGrid()
        self.TerminalGrid.height = 0
        self.add_widget(self.TerminalGrid)

    def clear(self):
        self.TerminalGrid.clear_widgets()
        self.TerminalGrid.height = 0

    def addText(self, text, color, Terminal, Temp):
        if Terminal:
            for label in self.TerminalGrid.children:
                if label.Temp == True:
                    self.removeLabel(label)

            label = TerminalLabel(Temp, font_size=self.rowHeight - 4)
            label.height = self.rowHeight

            color = color.lower().strip()
            if color in self.pallet:
                color = self.pallet[color]
            else:
                color = self.pallet['white']
            label.text = '[color='+color+']'+str(text)+'[/color]'
            self.addLabel(label)

    def addLabel(self, label):
        self.TerminalGrid.height += self.rowHeight
        self.TerminalGrid.add_widget(label)
        if self.TerminalGrid.height > self.height:
            self.scroll_to(label, padding = 10, animate=False)

    def removeLabel(self, label):
        self.TerminalGrid.height -= self.rowHeight
        self.TerminalGrid.remove_widget(label)

class TerminalLabel(Label):
    def __init__(self, Temp, *args, **kwargs):
        super(TerminalLabel, self).__init__(*args, **kwargs)
        self.Temp = Temp

class TerminalGrid(GridLayout):
    pass
