from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ColorProperty

class VBox(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.button1 = Button(text="Button 1", font_size=23, background_color="#127CA2")
        self.button2 = Button(text="Button 2", font_size=23, background_color="#FF7812")
        self.add_widget(self.button1)
        self.add_widget(self.button2)
        self.button1.bind(on_press=self.btn1_press)
        self.button2.bind(on_press=self.btn2_press)


    def btn1_press(self, *args):
        self.button2.text = "Button 1"

    def btn2_press(self, *args):
        self.button1.text = "Button 2"




class MyApp(App):
    def build(self):
        return VBox()


if __name__ == "__main__":
    MyApp().run()
