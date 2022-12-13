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
        self.sick = False

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
                print(temp)
                numdial = temp[0]
                if str(num) == numdial:
                    val = text[i][(len(numdial)+1):]
                    print(val)
                    return val

    except FileNotFoundError:
        print("Dialouge.txt not found. Please make sure it is in the same folder as this program.")
        exit()


def IsAlive(Living, name):
    for person in Living:
        if person.name == name:
            return True
    return False


def GetBadLuck(Living):
    peeps = []
    for person in Living:
        if random.randint(0, 5) - person.luck > 0:
            peeps.append(person.name)
    return peeps


def GetGoodLuck(Living):
    peeps = []
    for person in Living:
        if random.randint(0, 5) + person.luck > 5:
            peeps.append(person.name)
    return peeps


def Kill(Living, name):
    for person in Living:
        if person.name == name:
            Living.remove(person)
    return Living


def MarkSick(Living, name):
    for person in Living:
        if person.name == name:
            person.sick = True
    return Living


def IsSick(Living, name):
    for person in Living:
        if person.name == name:
            return person.sick
    return False


def SicknessCheck(Living):
    for person in Living:
        if person.sick == True:
            person.sick = False
            if random.randint(0, 5) - person.luck > 0:
                name = person.name
                Living.remove(person)
                return Living, name
    return Living, None


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
        user_options = ['Attend Bridgepour University',
                        'Attend the University of Ingolstadt', 'Work for your father']
    elif Level == 14:
        if 'Work for your father' in options.value:
            Level = 15
            text = TextFile(15)
            user_options = ['Restart', 'Quit']
        if 'Attend Bridgepour University' in options.value:
            Level = 16
            text = TextFile(16)
            user_options = ['Ford River', 'Float River']
        if 'Attend the University of Ingolstadt' in options.value:
            Level = 25
            text = TextFile(25)
            user_options = ['Next']
    elif Level == 15:
        if 'Restart' in options.value:
            Level = 0
            text = 'You have restarted the game. \n Use the character creator or randomize your stats.'
            user_options = ['Creator', 'Random']
            Living = []
        if 'Quit' in options.value:
            exit()
    elif Level == 16:
        Level = 17
        text = TextFile(17)
        # check for elizabeth gets sick
        if IsAlive(Living, 'Elizabeth') and 'Elizabeth' in GetBadLuck(Living):
            text += '\n However, over the rest of the journey, Elizabeth gets sick with the Scarlet Fever.'
            Living = MarkSick(Living, 'Elizabeth')
        user_options = ['Next']
    elif Level == 17:
        Level = 18
        text = TextFile(18)
        if IsSick(Living, 'Elizabeth'):
            text += '\n The family promises to send a letter about Elizabeth\'s health when she recovers.'
        user_options = ['Next']
    elif Level == 18:
        if IsSick(Living, 'Elizabeth'):
            Living, name = SicknessCheck(Living)
            if name != None:
                Level = 19
                text = TextFile(19)
                user_options = ['Restart', 'Quit']
            else:
                Level = 20
                text = TextFile(20)
                text += '\n You receive a letter from your family... Elizabeth has recovered! Good news!'
        else:
            Level = 20
            text = TextFile(20)
        user_options = ['Next']
    elif Level == 19:
        if 'Restart' in options.value:
            Level = 0
            text = 'You have restarted the game. \n Use the character creator or randomize your stats.'
            user_options = ['Creator', 'Random']
            Living = []
        if 'Quit' in options.value:
            exit()
    elif Level == 20:
        Level = 21
        text = TextFile(21)
        user_options = ['Next']
    elif Level == 21:
        Level = 22
        text = TextFile(22)
        user_options = ['Chemistry Major', 'Physics Major']
    elif Level == 22:
        if 'Chemistry Major' in options.value:
            Level = 23
            text = TextFile(23)
            user_options = ['Restart', 'Quit']
        if 'Physics Major' in options.value:
            Level = 24
            text = TextFile(24)
            user_options = ['Restart', 'Quit']
    elif Level == 23:
        if 'Restart' in options.value:
            Level = 0
            text = 'You have restarted the game. \n Use the character creator or randomize your stats.'
            user_options = ['Creator', 'Random']
            Living = []
        if 'Quit' in options.value:
            exit()
    elif Level == 24:
        if 'Restart' in options.value:
            Level = 0
            text = 'You have restarted the game. \n Use the character creator or randomize your stats.'
            user_options = ['Creator', 'Random']
            Living = []
        if 'Quit' in options.value:
            exit()
    elif Level == 25:
        if Living[0].ability < 3:
            Level = 26
            text = TextFile(26)
            user_options = ['Restart', 'Quit']
        else:
            Level = 27
            text = TextFile(27)
            user_options = ['Next']
    elif Level == 26:
        if 'Restart' in options.value:
            Level = 0
            text = 'You have restarted the game. \n Use the character creator or randomize your stats.'
            user_options = ['Creator', 'Random']
            Living = []
        if 'Quit' in options.value:
            exit()
    elif Level == 27:
        Level = 28
        text = TextFile(28)
        user_options = ['Next']
    elif Level == 28:
        Level = 29
        text = TextFile(29)
        user_options = ['Next']
    elif Level == 29:
        Level = 30
        text = TextFile(30)
        user_options = ['Next']
    elif Level == 30:
        Level = 31
        text = TextFile(31)
        user_options = ['Physics Major', 'Chemistry Major']
    elif Level == 31:
        if 'Physics Major' in options.value:
            Level = 32
            text = TextFile(32)
            user_options = ['Restart', 'Quit']
        if 'Chemistry Major' in options.value:
            Level = 33
            text = TextFile(33)
            user_options = ['Stick to Chemistry', 'Add Biology']
    elif Level == 32:
        if 'Restart' in options.value:
            Level = 0
            text = 'You have restarted the game. \n Use the character creator or randomize your stats.'
            user_options = ['Creator', 'Random']
            Living = []
        if 'Quit' in options.value:
            exit()
    elif Level == 33:
        if 'Stick to Chemistry' in options.value:
            Level = 34
            text = TextFile(34)
            user_options = ['Restart', 'Quit']
        if 'Add Biology' in options.value:
            Level = 35
            text = TextFile(35)
            Living[0].education += 1
            user_options = ['Next']

    Display_Dialogue(text)
    Display_Options(user_options)
    Display_Characters(Living)


#-----------------#
app = App(title="The True Monster", width=1200, height=600, layout="grid")
dialogue = ListBox(app, grid=[0, 0, 8, 6], scrollbar=True, items=[
                   'dialogue'], width=900, height=250)
dialogue.font = "Courier"
title = Text(app, text="The True", grid=[9, 0, 1, 1], size=30)
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
Level = 0
Living = []

Display_Dialogue(
    "Before we begin, would you like to enter the character creator, or would you like random characters?")

Display_Options(["Creator", "Random"])
Display_Characters(Living)

app.display()
