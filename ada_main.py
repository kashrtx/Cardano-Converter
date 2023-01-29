from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from kivy.clock import Clock
import sys

sys.setrecursionlimit(5000)


class Cardano_Converter_By_Kaushal_Bhingaradia(App):
    logo = 'ada_logo.png'
    count = 0
    red = [1, 0, 0, 1]
    green = [0, 1, 0, 1]
    blue = [0, 0, 1, 1]
    purple = [1, 0, 1, 1]
    white = [0, 0, 0, 0]

    def build(self):
        self.window = GridLayout()
        self.window.cols = 1

        # Widgets
        self.window.add_widget(Image(source="ada_logo.png"))

        intro = 'Welcome to Simple Cardano Converter!\n By: Kaushal ' \
                'Bhingaradia 2022\n\n' \
                'NOTE: This program works off the internet for real time\n ' \
                'ADA prices and is still in beta!'

        instructions = 'Just enter only numbers for CAD or ADA in the ' \
                       'text box, then the program will output ADA or CAD\n' \
                       'depending on which conversion button you press!'

        # The top message
        self.greeting = Label(text=intro)
        self.window.add_widget(self.greeting)

        # Output instructions in console
        print(instructions)

        # The clickable start Button
        self.start_button = Button(text="Let's get started!")
        self.start_button.bind(on_press=self.convert_page)
        self.start_button.bind(on_press=self.refresh)
        self.start_button.bind(on_press=self.delete)
        self.window.add_widget(self.start_button)

        # Display the widgets
        return self.window

    def refresh(self, instance):
        print('Now running refresher!')
        # refresh date and currency price every 10 seconds
        Clock.schedule_interval(self.refresh_conversion_page, 10)

    def refresh_conversion_page(self, dt):

        self.price.text = f"""
        The current price of ADA is ${self.get_realtime_cardano_price()} CAD
        @ {self.date_time()}
        """

    def date_time(self):
        now = datetime.now()
        return now.strftime('%Y/%m/%d %I:%M:%S')

    def delete(self, instance):
        # Function to delete the button on click
        self.window.remove_widget(self.start_button)
        self.window.remove_widget(self.greeting)

    def convert_page(self, instance):
        # New page UI to show conversion buttons

        self.window.cols = 1

        price_status = f"""
        The current price of ADA is ${self.get_realtime_cardano_price()} CAD
        @ {self.date_time()}
        """

        # Market Price
        self.price = Label(text=price_status)
        self.price.color = self.red
        self.window.add_widget(self.price)

        # Text input instructions
        self.message = Label(text='Enter CAD or ADA in text box below!')
        self.window.add_widget(self.message)

        # Input Lines for entering values of either ADA  or CAD
        self.input = TextInput(multiline=False, input_filter='float',
                               write_tab=False)
        if self.input.text == '':
            self.input.text = '0'
        self.window.add_widget(self.input)

        # Button shows the conversion result and clears on click
        self.result = Button(text='Output')
        self.result.bind(on_press=self.clear)
        self.window.add_widget(self.result)

        # Top button to convert the inputted text CAD to ADA
        self.button = Button(text='Convert CAD to ADA')
        self.button.color = self.blue
        self.button.bind(on_press=self.CAD_to_ADA)
        self.window.add_widget(self.button)

        # Bottom button to convert the inputted text ADA to CAD
        self.button2 = Button(text='Convert ADA to CAD')
        self.button2.color = self.purple
        self.button2.bind(on_press=self.ADA_to_CAD)
        self.window.add_widget(self.button2)

        # Display widgets
        return self.window

    def clear(self, instance):
        self.result.color = self.red
        self.count = 0
        self.input.text = '0'
        self.result.text = 'CLEAR!'

    def get_realtime_cardano_price(self):
        # Get the URL
        url = "https://www.google.ca/search?q=" + 'ADA' + "+price"

        # Make a request to the website
        HTML = requests.get(url)

        # Parse the HTML
        soup = BeautifulSoup(HTML.text, 'html.parser')

        # Find the current price
        # text = soup.find("div", attrs={'class':'BNeawe iBp4i AP7Wnd'}).text
        text = soup.find("div", attrs={'class': 'BNeawe iBp4i AP7Wnd'}).find(
            "div", attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
        # Return the text
        edit = str(text)[:4]
        return edit

    def CAD_to_ADA(self, instance):
        # Count number of conversions
        self.count += 1

        # Get real time cardano prices
        cardano_price = float(self.get_realtime_cardano_price())

        # CAD variable converted to float
        if self.input.text == '':
            self.input.text = '0'
        CAD = float(self.input.text)

        # Conversion formula to get ADA value from CAD
        convert = CAD / cardano_price

        # ADA rounded 2 decimal places after conversion
        rounded_calc = round(convert, 2)

        work = '{} CAD  --------->  {} ADA! ' \
               '\nYou converted {} time(s)!'.format(str(round(float(CAD), 2)),
                                                    str(rounded_calc),
                                                    str(self.count))
        # Update the button to show the conversion
        self.result.color = self.green
        self.result.text = work

    def ADA_to_CAD(self, instance):
        # Count number of conversions
        self.count += 1

        # Get real time cardano prices
        cardano_price = float(self.get_realtime_cardano_price())

        # ADA variable
        if self.input.text == '':
            self.input.text = '0'
        ADA = float(self.input.text)

        # Conversion formula to get CAD value from Cardano
        convert = ADA * cardano_price

        # ADA rounded 2 decimal places after conversion
        rounded_calc = round(convert, 2)

        work = '{} ADA  --------->  {} CAD! ' \
               '\nYou converted {} time(s)!'.format(str(round(float(ADA), 2)),
                                                    str(rounded_calc),
                                                    str(self.count))
        # Update the button to show the conversion
        self.result.color = self.green
        self.result.text = work


if __name__ == "__main__":
    Cardano_Converter_By_Kaushal_Bhingaradia().run()
