'''
Widget animation
================

This example demonstrates creating and applying a multi-part animation to
a button widget. You should see a button labelled 'plop' that will move with
an animation when clicked.
'''

import kivy
kivy.require('1.0.7')

from kivy.animation import Animation
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

import datetime
from bs4 import BeautifulSoup
import requests

class TestApp(App):


    def build(self):
        # create a button, and  attach animate() method as a on_press handler
        button = Button(size_hint=(None, None), text='plop',
                        on_press=self.parsing)
        return button


    def parsing(self, instance):
        today = datetime.date.today()

        url = 'http://rgkript.ru/raspisanie-zanyatiy/'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')

        #Парсинг ссылки расписания занятий {
        schedule = soup.find_all('tbody')
        for i in schedule:
            schedule = i.find('a')
        schedule = schedule.attrs['href']
        #                                  }

        #Парсинг ссылки замен занятий      {
        changes = soup.find_all('div', class_='page-content')
        for i in changes:
            h3 = i.find_all('h3')
            for n in h3:
                changes = n.find('a')
        changes = changes.attrs['href']
        #                                  }

        resp = requests.get(schedule)
        resp2 = requests.get(changes)


        output = open('/storage/emulated/0/РГКРИПТ_Расписание/расписание_скачано-'+str(today)+'.xls', 'wb')
        output.write(resp.content)
        output.close()

        output2 = open('/storage/emulated/0/РГКРИПТ_Расписание/замены_скачано-'+str(today)+'.doc', 'wb')
        output2.write(resp2.content)
        output2.close()


if __name__ == '__main__':
    TestApp().run()
