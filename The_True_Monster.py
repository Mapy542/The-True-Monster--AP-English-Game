try:
    from guizero import App, ListBox, Text, PushButton

except ImportError:
    print("Guizero is not installed. Please install it.")
    exit()

import random
import math
import time
from tkinter import font
from textwrap import wrap


class Character:
    def __init__(self, health=10, enthusiasm=5, education=0, ability=5, name="Character"):
        self.luck = random.randint(1, 5)
        self.health = health
        self.enthusiasm = enthusiasm
        self.education = education
        self.ability = ability
        self.name = name

        if (self.luck == 5 and random.randint(1, 2) == 1):
            self.ability += random.randint(1, 3)
            self.enthusiasm += random.randint(1, 3)
            self.education += random.randint(1, 3)

    def Make_Random(self):
        self.luck = random.randint(1, 5)
        self.health = random.randint(1, 10)
        self.enthusiasm = random.randint(1, 5)
        self.education = random.randint(1, 5)
        self.ability = random.randint(1, 5)

        if (self.luck == 5 and random.randint(1, 2) == 1):
            self.ability += random.randint(1, 3)
            self.enthusiasm += random.randint(1, 3)
            self.education += random.randint(1, 3)

    def Luck_Check(self):
        if (self.luck == 5 and random.randint(1, 2) == 1):
            self.ability += random.randint(1, 3)
            self.enthusiasm += random.randint(1, 3)
            self.education += random.randint(1, 3)


def Display_Dialogue(text):
    text = text.split("\n")
    display_text = []
    for section in text:
        if len(section) > 120:
            section = wrap(section, 120)
            for i in range(len(section)):
                if i < len(section)-1:
                    section[i] = section[i] + "-"
                display_text.append(section[i])
        else:
            display_text.append(section)

    dialogue.clear()
    for i in range(len(display_text)):
        dialogue.append(display_text[i])


def Display_Options(options_inputs):
    displaytext = []
    for section in options_inputs:
        if len(section) > 40:
            section = wrap(section, 40)
            for i in range(len(section)):
                if i < len(section)-1:
                    section[i] = section[i] + "-"
                displaytext.append(section[i])
        else:
            displaytext.append(section)

    print(displaytext)
    options.clear()
    for i in range(len(displaytext)):
        options.append(displaytext[i])


def Display_Characters(objects):
    displaytext = []
    for person in objects:
        displaytext.append(person.name)
        displaytext.append("    Health: " + str(person.health))
        displaytext.append("    Enthusiasm: " + str(person.enthusiasm))
        displaytext.append("    Education: " + str(person.education))
        displaytext.append("    Ability: " + str(person.ability))
        displaytext.append("    Luck: " + str(person.luck))

    characters.clear()
    for i in range(len(displaytext)):
        characters.append(displaytext[i])


def TextFile(num):
    try:
        with open('Dialouge.txt', "r") as file:
            text = file.read()
            text = text.split('*')
            text = [x for x in text if x]
            for i in range(len(text)):
                if str(num) == text[i][0]:
                    val = text[i][2:]
                    return val

    except FileNotFoundError:
        print("Dialouge.txt not found. Please make sure it is in the same folder as this program.")
        exit()


def continuegame():
    global Level, Living, options
    if Level == 0:
        if "Creator" in options.value:
            Level = 1
            Living.append(Character(name="Frankenstein", health=10,
                          enthusiasm=0, education=0, ability=0))
            user_options = ['Enthusiasm', 'Education', 'Ability', 'Health']
            text = "You are Frankenstein. Please choose a stat or two to specialize in. \nCTRL select for multiple."
        elif "Random" in options.value:
            Level = 2
            Living.append(Character(name="Frankenstein"))
            Living[0].Make_Random()
            text = TextFile(2)
            user_options = ['Next']
    elif Level == 1:
        Living[0].Make_Random()
        if "Enthusiasm" in options.value:
            Living[0].enthusiasm = random.randint(3, 5)
        if "Education" in options.value:
            Living[0].education = random.randint(3, 5)
        if "Ability" in options.value:
            Living[0].ability = random.randint(3, 5)
        if "Health" in options.value:
            Living[0].health = random.randint(5, 10)
        Living[0].Luck_Check()
        Level = 2
        text = TextFile(2)
        user_options = ['Next']

    Display_Dialogue(text)
    Display_Options(user_options)
    Display_Characters(Living)


#-----------------#
app = App(title="The True Monster", width=1200, height=600, layout="grid")
dialogue = ListBox(app, grid=[0, 0, 8, 6], scrollbar=True, items=[
                   'dialogue'], width=900, height=250)
dialogue.font = "Courier"
title = Text(app, text="The    ", grid=[9, 0, 1, 1], size=30)
title.font = 'Lucida Bright'
title2 = Text(app, text='Monster', grid=[9, 1, 1, 2], size=30)
title2.font = 'Lucida Bright'
options_text = Text(app, grid=[3, 7, 8, 1], text="Options")
options = ListBox(app, grid=[3, 8, 2, 3], scrollbar=True, items=[
                  'options'], width=450, height=250, multiselect=True)
options.font = "Courier"
characters_text = Text(app, grid=[0, 7, 2, 1], text="Characters")
characters = ListBox(app, grid=[0, 8, 2, 3],
                     scrollbar=True, items=['characters'], width=450, height=250)
characters.font = "Courier"

submit = PushButton(app, grid=[9, 8, 2, 1],
                    text="Submit", command=continuegame)

# Enter Character Creator?

#-----------------#
Level = 0
Living = []

Display_Dialogue(
    "Before we begin, would you like to enter the character creator, or would you like random characters?")

Display_Options(["Creator", "Random"])
Display_Characters(Living)

app.display()
