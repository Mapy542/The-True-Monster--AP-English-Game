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
                temp = text[i].split('\n')
                print(temp[0])
                numdial = temp[0]
                if str(num) == numdial:
                    val = text[i][(len(numdial)+1):]
                    return val

    except FileNotFoundError:
        print("Dialouge.txt not found. Please make sure it is in the same folder as this program.")
        exit()


def continuegame():
    global Level, Living, options
    if Level == 0:
        if "Creator" in options.value:
            Level = 1
            Living.append(Character(name="Victor", health=10,
                          enthusiasm=0, education=0, ability=0))
            user_options = ['Enthusiasm', 'Education', 'Ability', 'Health']
            text = "You are Frankenstein. Please choose a stat or two to specialize in. \nCTRL select for multiple."
        elif "Random" in options.value:
            Level = 2
            Living.append(Character(name="Victor"))
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
    elif Level == 2:
        Level = 3
        Living.append(Character(name='Earnest'))
        Living.append(Character(name='William'))
        Living[1].Make_Random()
        Living[2].Make_Random()
        user_options = ['Vacation', 'Recover at home']
        text = TextFile(3)
    elif Level == 3:
        if 'Vacation' in options.value:
            Level = 4
            user_options = ['Adopt the baby', 'Nah, it\'s too dirty.']
            text = TextFile(4)
        if 'Recover at home' in options.value:
            Level = 6
            Living[0].education += 1
            Living[0].enthusiasm += 2
            user_options = ['Try to make friends', 'Stay with your family']
            text = TextFile(6)
    elif Level == 4:
        if 'Adopt the baby' in options.value:
            Level = 5
            user_options = ['Next']
            Living.append(Character(name='Elizabeth'))
            text = TextFile(5)
        if 'Nah, it\'s too dirty.' in options.value:
            Level = 6
            Living[0].education += 1
            Living[0].enthusiasm += 2
            user_options = ['Try to make friends', 'Stay with your family']
            text = 'The family blood line can\'t be spoiled anyways. The family returns and you enter school. \n'
            text += TextFile(6)
    elif Level == 5:
        Level = 6
        Living[0].education += 1
        Living[0].enthusiasm += 2
        user_options = ['Try to make friends', 'Stay with your family']
        text = TextFile(6)
    elif Level == 6:
        if 'Try to make friends' in options.value:
            Level = 7
            user_options = ['Next']
            text = TextFile(7)
        if 'Stay with your family' in options.value:
            Level = 9
            user_options = ['Next']
            text = TextFile(9)
    elif Level == 7:
        Level = 8
        user_options = ['Next']
        Living[0].enthusiasm -= 1
        text = TextFile(8)
        Living.pop(1)
    elif Level == 8:
        Level = 10
        text = TextFile(10)
        user_options = ['Science Book', 'Pick another shelf']
    elif Level == 9:
        Level = 10
        text = TextFile(10)
        user_options = ['Science Book', 'Pick another shelf']
    elif Level == 10:
        if 'Science Book' in options.value:
            Level = 12
            text = TextFile(12)
            user_options = ['Next']
            Living[0].education += 1
            Living[0].enthusiasm += 1
        if 'Pick another shelf' in options.value:
            Level = 11
            text = TextFile(11)
            user_options = ['Restart', 'Quit']
    elif Level == 11:
        if 'Restart' in options.value:
            Level = 0
            text = 'You have restarted the game. \n Use the character creator or randomize your stats.'
            user_options = ['Creator', 'Random']
            Living = []
        if 'Quit' in options.value:
            exit()
    elif Level == 12:
        Level = 13
        text = TextFile(13)
        user_options = ['Next']
        Living[0].enthusiasm += 1
        Living[0].education += 1
    elif Level == 13:
        Level = 14
        text = TextFile(14)
        user_options = ['Attend Birdgepour University',
                        'Attend the University of Ingolstadt', 'Work for your father']
    elif Level == 14:
        if 'Work for your father' in options.value:
            Level = 15
            text = TextFile(15)
            user_options = ['Restart', 'Quit']

    elif Level == 15:
        if 'Restart' in options.value:
            Level = 0
            text = 'You have restarted the game. \n Use the character creator or randomize your stats.'
            user_options = ['Creator', 'Random']
            Living = []
        if 'Quit' in options.value:
            exit()

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
                  'options'], width=450, height=300, multiselect=True)
options.font = "Courier"
characters_text = Text(app, grid=[0, 7, 2, 1], text="Characters")
characters = ListBox(app, grid=[0, 8, 2, 3],
                     scrollbar=True, items=['characters'], width=450, height=300)
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
