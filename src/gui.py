from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from scrap import *
import time

class LoginScreen(GridLayout):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 1
        self.add_widget(Label(text='web page'))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)
        
        self.password = Button(text='scrap!')
        self.password.bind(on_press = lambda a:self.onclick())
        self.add_widget(self.password)
        self.output = TextInput(multiline=True)
        self.add_widget(self.output)
        
    def onclick(self):
        self.output.text = "working..."
        run(self.username.text, self.output)
        self.output.text = "done!"

class MyApp(App):

    def build(self):
        
        return LoginScreen()
    


if __name__ == '__main__':
    MyApp().run()