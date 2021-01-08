import os
import io
import pygame
from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
from gtts import gTTS
from googletrans import Translator
from currency_converter import CurrencyConverter

class Translation(object):
    
    def __init__(self, master):
        frame = Frame(master)
        frame.grid()
        tabControl = ttk.Notebook(root)
        tabControl.configure(width=500, heigh=260)

        self.phrase_tab = ttk.Frame(tabControl)
        tabControl.add(self.phrase_tab, text="Language")
        tabControl.grid()
        self.phrase_tab.grid_propagate(0)

        self.currency_tab = ttk.Frame(tabControl)
        tabControl.add(self.currency_tab, text="Currency")
        tabControl.grid()

        self.languages = {
            'Arabic':'ar','Belarusian':'br','Bengali':'bn','Bosnian':'bs','Bulgarian':'bg','Chinese':'zh-cn',
            'Croatian':'hr','Czech':'cs','Danish':'da','English':'en','Finnish':'fi','French':'fr','German':'de',
            'Gujarati':'gu','Greek':'el','Haitian':'ht','Hebew':'he','Hindi':'hi','Irish':'ga','Italian':'it',
            'Japanese':'ja','Korean':'ko','Malayalam':'ml','Marathi':'mr','Nepali':'ne','Persian':'fa','Punjabi':'pa',
            'Romanian':'ro', 'Russian':'ru','Sindhi':'sd','Spanish':'es','Swedish':'sv','Tamil':'ta',
            'Telugu':'te','Thai':'th','Turkish':'tr','Urdu':'ur'
        }

        self.currency = CurrencyConverter()
        self.options = ["AUD","CAD","CNY","DKK","EUR","GBP","INR","JPY","NZD","USD"]
        
        self.language_page()
        self.currency_page()

    def language_page(self):
        self.top_label = Label(self.phrase_tab, text="Enter Sentence: ",font=("Courier", 14))
        self.top_label.grid(column=0, row=0)
        self.word_entry = Entry(self.phrase_tab, width=68)
        self.word_entry.grid(column=0, row=1, columnspan=3, padx=2, pady=5)

        self.language_label = Label(self.phrase_tab, text="Language: ",font=("Courier", 14))
        self.language_label.grid(column=0, row=2, pady=5)
        self.language_menu = ttk.Combobox(self.phrase_tab, values=[*self.languages.keys()])
        self.language_menu.grid(column=0, row=3)
        self.language_menu.current(0)

        self.translate_btn = Button(self.phrase_tab, text="Translate", command=self.lang_translation)
        self.translate_btn.grid(row=4, column=0, pady=15)
        

        self.word_frame= LabelFrame(self.phrase_tab, text="Translation: ", width=490, height=50)
        self.word_frame.grid(column=0, row=5, columnspan=3, rowspan=3, padx=2)
        self.word_frame.grid_propagate(0)
        self.word_result = Label(self.word_frame, text="")
        self.word_result.grid()

        self.speak_check = Button(self.phrase_tab, text="Say it!", command=self.speak_it)
        self.speak_check.grid(column=0, row=11, pady=5)
        

    def currency_page(self):
        self.amount_label = Label(self.currency_tab, text="Enter Amount", font=("Courier", 14))
        self.amount_label.grid(column=0, row=0, padx=10, pady=10)
        self.amount_entry = Entry(self.currency_tab,font=("Courier", 14))
        self.amount_entry.grid(column=1, row=0)

        self.selection_frame = LabelFrame(self.currency_tab, text="Currencies")
        self.selection_frame.grid(column=0, row=1, columnspan=2, padx=10, pady=10)
        self.from_label = Label(self.selection_frame, text="From: ", font=("Courier", 14))
        self.from_label.grid(column=0,row=0)
        self.to_label = Label(self.selection_frame, text="To: ", font=("Courier", 14))
        self.to_label.grid(column=1,row=0)

        self.from_menu = ttk.Combobox(self.selection_frame, values=self.options)
        self.from_menu.grid(column=0, row=1)
        self.from_menu.current(0)
        self.to_menu = ttk.Combobox(self.selection_frame, values=self.options)
        self.to_menu.grid(column=1, row=1)
        self.to_menu.current(1)

        self.result_label = Label(self.currency_tab, text="",font=("Courier", 20))
        self.result_label.grid(column=0, row=2, columnspan=2)
        self.convert_btn = Button(self.currency_tab, text="Convert!",command=self.curr_convert)
        self.convert_btn.grid(column=0, row=3, columnspan=2)



    def lang_translation(self):
        trans = Translator()
        word = self.word_entry.get()
        lang = str(self.languages.get(self.language_menu.get()))
        result = str(trans.translate(word,dest=lang).text)
        self.word_result.configure(text=result)


    def speak_it(self):
        trans = Translator()
        word = self.word_entry.get()
        lang = str(self.languages.get(self.language_menu.get()))
        result = str(trans.translate(word,dest=lang).text)
        myobj = gTTS(text=result, lang=lang, slow=False)
        myobj.save("text.mp3")
        os.system("text.mp3")

    def curr_convert(self):
        try:
            currency_result = round(self.currency.convert(float(self.amount_entry.get()),
            self.from_menu.get(), self.to_menu.get()), 2)

            self.result_label.configure(text=f"{currency_result} {self.to_menu.get()}")

        except ValueError:
            self.result_label.configure(text="Valuerror")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    root = Tk()
    root.title('Morpher- lets translate!')
    root.geometry("510x270")
    Translation(root)
    root.mainloop()

