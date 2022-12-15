import os
try:
    from guizero import App, ListBox, Text, PushButton

except ImportError:
    print("installing guizero...")
    os.system("python3 -m pip install guizero")
    from guizero import App, ListBox, Text, PushButton

import random
from tkinter import font
from textwrap import wrap


class Character:  # class to represent a character within the story
    def __init__(self, health=10, enthusiasm=5, education=0, ability=5, name="Character"):
        # luck is a random number between 1 and 5 no matter what
        self.luck = random.randint(1, 5)
        self.health = health  # unused in this game
        self.enthusiasm = enthusiasm  # represents how much the character wants to do the task
        self.education = education  # represents how much the character knows about the task
        self.ability = ability  # represents how good the character is at the task
        self.name = name  # name of the character
        self.sick = False  # whether or not the character is sick

        # if the character has good luck, they get a bonus
        if (self.luck == 5 and random.randint(1, 2) == 1):
            self.ability += random.randint(1, 3)
            self.enthusiasm += random.randint(1, 3)
            self.education += random.randint(1, 3)

    def Make_Random(self):  # randomizes character after initialization or whenever called
        self.luck = random.randint(1, 5)
        self.health = random.randint(1, 10)
        self.enthusiasm = random.randint(1, 5)
        self.education = random.randint(1, 5)
        self.ability = random.randint(1, 5)

        if (self.luck == 5 and random.randint(1, 2) == 1):
            self.ability += random.randint(1, 3)
            self.enthusiasm += random.randint(1, 3)
            self.education += random.randint(1, 3)

    def Luck_Check(self):  # checks if the character has good luck and gives a bonus if they do
        if (self.luck == 5 and random.randint(1, 2) == 1):
            self.ability += random.randint(1, 3)
            self.enthusiasm += random.randint(1, 3)
            self.education += random.randint(1, 3)


def Display_Dialogue(text):  # converts strings into a display in the GUI
    # splits the text into a list of strings as listbox can't handle new lines
    text = text.split("\n")
    display_text = []
    for section in text:  # for each line of text
        if len(section) > 120:  # if the line is too long
            section = wrap(section, 120)  # wrap the line to fit the screen
            for i in range(len(section)):
                if i < len(section)-1:
                    # add a line break to the end of each line except the last if wanted
                    section[i] = section[i] + ""
                # add the line to the display text
                display_text.append(section[i])
        else:
            # if the line is short enough, add it to the display text
            display_text.append(section)

    dialogue.clear()  # clear the dialogue box
    for i in range(len(display_text)):  # add the text to the dialogue box
        dialogue.append(display_text[i])


def Display_Options(options_inputs):  # converts strings into a display in the GUI
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

    options.clear()
    for i in range(len(displaytext)):
        options.append(displaytext[i])


def Display_Characters(objects):  # converts strings into a display in the GUI
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


def TextFile(num):  # reads the text file and returns the text for the given scene number
    try:
        with open('Dialouge.txt', "r") as file:  # opens the text file
            text = file.read()  # reads the text file
            text = text.split('*')  # splits the text file into scenes
            # removes empty strings from the list
            text = [x for x in text if x]
            # ^ this kind of pythonic code is called a list comprehension and is amazing
            for i in range(len(text)):  # for each scene
                # split the scene into lines into a new variable
                temp = text[i].split('\n')
                numdial = temp[0]  # find the scene number
                if str(num) == numdial:  # if the scene number matches the one we want
                    # get the text for the scene minus the scene number and first line break
                    val = text[i][(len(numdial)+1):]
                    return val

    except FileNotFoundError:
        print("Dialouge.txt not found. Please make sure it is in the same folder as this program.")
        exit()


# list of characters attribute checkers
def IsAlive(Living, name):  # checks if a character is alive
    for person in Living:
        if person.name == name:
            return True
    return False


def GetBadLuck(Living):  # gets a list of characters with bad luck
    peeps = []
    for person in Living:
        # if the character has a lower .luck they have a higher chance of getting bad luck
        if random.randint(0, 5) - person.luck > 0:
            peeps.append(person.name)
    return peeps  # returns a list of characters with bad luck
    # list is helpful for when multiple characters can get bad luck


def GetGoodLuck(Living):  # gets a list of characters with good luck
    peeps = []
    for person in Living:
        if random.randint(0, 5) + person.luck > 5:
            peeps.append(person.name)
    return peeps


def Kill(Living, name):  # kills a character by finding them in the list and removing them
    for person in Living:
        if person.name == name:
            Living.remove(person)
    return Living


def MarkSick(Living, name):  # marks a character as sick
    for person in Living:
        if person.name == name:
            person.sick = True
    return Living


def IsSick(Living, name):  # checks if a character is sick
    for person in Living:
        if person.name == name:
            return person.sick
    return False


def SicknessCheck(Living):  # checks if a character is sick and kills them if they have bad luck
    for person in Living:
        if person.sick == True:
            person.sick = False
            if random.randint(0, 5) - person.luck > 0:
                name = person.name
                Living.remove(person)
                return Living, name
    return Living, None


def continuegame():  # advance game based on parameters
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
            Living.append(Character(name='Henry'))
            Living[len(Living)-1].Make_Random()
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
    elif Level == 34:
        if 'Restart' in options.value:
            Level = 0
            text = 'You have restarted the game. \n Use the character creator or randomize your stats.'
            user_options = ['Creator', 'Random']
            Living = []
        if 'Quit' in options.value:
            exit()
    elif Level == 35:
        Level = 36
        text = TextFile(36)
        user_options = ['Single Cell Organisms', 'Human Form']
    elif Level == 36:
        if 'Single Cell Organisms' in options.value:
            Level = 37
            text = TextFile(37)
            user_options = ['Next']
        if 'Human Form' in options.value:
            Level = 43
            text = TextFile(43)
            user_options = ['Grave Robbing', 'Hunting']
    elif Level == 37:
        Level = 38
        text = TextFile(38)
        user_options = ['Natural Substance', 'Synthetic Substance']
    elif Level == 38:
        if 'Natural Substance' in options.value:
            if 'Victor' in GetGoodLuck(Living) or Living[0].ability > 4:
                Level = 39
                text = TextFile(39)
                user_options = ['Restart', 'Quit']
            else:
                Level = 40
                text = TextFile(40)
                user_options = ['Restart', 'Quit']
        if 'Synthetic Substance' in options.value:
            if 'Victor' in GetGoodLuck(Living) or Living[0].ability > 4:
                Level = 41
                text = TextFile(41)
                user_options = ['Restart', 'Quit']
            else:
                Level = 42
                text = TextFile(42)
                user_options = ['Restart', 'Quit']
    elif Level == 39 or Level == 40 or Level == 41 or Level == 42:
        if 'Restart' in options.value:
            Level = 0
            text = 'You have restarted the game. \n Use the character creator or randomize your stats.'
            user_options = ['Creator', 'Random']
            Living = []
        if 'Quit' in options.value:
            exit()
    elif Level == 43:
        if 'Hunting' in options.value:
            Level = 44
            text = TextFile(44)
            user_options = ['Next']
        if 'Grave Robbing' in options.value:
            Level = 51
            text = TextFile(51)
            user_options = ['Next']
    elif Level == 44:
        Level = 45
        text = TextFile(45)
        user_options = ['Gun', 'Spear']
    elif Level == 45:
        if 'Gun' in options.value:
            Level = 46
            text = TextFile(46)
            user_options = ['Next']
        if 'Spear' in options.value:
            Level = 47
            text = TextFile(47)
            user_options = ['Next']
    elif Level == 46:
        Level = 47
        text = TextFile(47)
        user_options = ['Next']
    elif Level == 47:
        Level = 48
        text = TextFile(48)
        user_options = ['Next']
    elif Level == 48:
        if 'Victor' in GetGoodLuck(Living) or Living[0].ability > 4:
            Level = 50
            text = TextFile(50)
            user_options = ['Next']
        else:
            Level = 49
            text = TextFile(49)
            user_options = ['Quit', 'Restart']
    elif Level == 49:
        if 'Restart' in options.value:
            Level = 0
            text = 'You have restarted the game. \n Use the character creator or randomize your stats.'
            user_options = ['Creator', 'Random']
            Living = []
        if 'Quit' in options.value:
            exit()
    elif Level == 50:
        Level = 55
        text = TextFile(55)
        user_options = ['Sneak into the engine room', 'Make spark generator']
    elif Level == 51:
        Level = 52
        text = TextFile(52)
        user_options = ['Hide in the grave', 'Hide behind the mausoleum']
    elif Level == 52:
        if 'Hide in the grave' in options.value:
            Level = 54
            text = TextFile(54)
            user_options = ['Next']
        if 'Hide behind the mausoleum' in options.value:
            Level = 53
            text = TextFile(53)
            user_options = ['Quit', 'Restart']
    elif Level == 53:
        if 'Restart' in options.value:
            Level = 0
            text = 'You have restarted the game. \n Use the character creator or randomize your stats.'
            user_options = ['Creator', 'Random']
            Living = []
        if 'Quit' in options.value:
            exit()
    elif Level == 54:
        Level = 55
        text = TextFile(55)
        user_options = ['Sneak into the engine room', 'Make a spark generator']
    elif Level == 55:
        if 'Sneak into the engine room' in options.value:
            Level = 57
            text = TextFile(57)
            user_options = ['Next']
        if 'Make a spark generator' in options.value:
            Level = 56
            text = TextFile(56)
            user_options = ['Quit', 'Restart']
    elif Level == 56:
        if 'Restart' in options.value:
            Level = 0
            text = 'You have restarted the game. \n Use the character creator or randomize your stats.'
            user_options = ['Creator', 'Random']
            Living = []
        if 'Quit' in options.value:
            exit()
    elif Level == 57:
        if Living[0].luck < 2:
            Level = 58
            text = TextFile(58)
            user_options = ['Restart', 'Quit']
        else:
            Level = 59
            text = TextFile(59)
            user_options = ['Next']
    elif Level == 58:
        if 'Restart' in options.value:
            Level = 0
            text = 'You have restarted the game. \n Use the character creator or randomize your stats.'
            user_options = ['Creator', 'Random']
            Living = []
        if 'Quit' in options.value:
            exit()
    elif Level == 59:
        Level = 60
        text = TextFile(60)
        user_options = ['Next']
    elif Level == 60:
        if Living[0].enthusiasm < 3:
            Level = 61
            text = TextFile(61)
            user_options = ['Restart', 'Quit']
        else:
            Level = 62
            text = TextFile(62)
            user_options = ['Next']
    elif Level == 61:
        if 'Restart' in options.value:
            Level = 0
            text = 'You have restarted the game. \n Use the character creator or randomize your stats.'
            user_options = ['Creator', 'Random']
            Living = []
        if 'Quit' in options.value:
            exit()
    elif Level == 62:
        if 'Victor' in GetGoodLuck(Living):
            Level = 63
            text = TextFile(63)
            user_options = ['Restart', 'Quit']
        else:
            Level = 64
            text = TextFile(64)
            user_options = ['Next']
    elif Level == 63:
        if 'Restart' in options.value:
            Level = 0
            text = 'You have restarted the game. \n Use the character creator or randomize your stats.'
            user_options = ['Creator', 'Random']
            Living = []
        if 'Quit' in options.value:
            exit()
    elif Level == 64:
        Level = 65
        text = TextFile(65)
        user_options = ['Next']
    elif Level == 65:
        if IsAlive(Living, 'Henry'):
            Level = 67
            text = TextFile(67)
            user_options = ['Next']
        else:
            Level = 66
            text = TextFile(66)
            user_options = ['Restart', 'Quit']
    elif Level == 66:
        if 'Restart' in options.value:
            Level = 0
            text = 'You have restarted the game. \n Use the character creator or randomize your stats.'
            user_options = ['Creator', 'Random']
            Living = []
        if 'Quit' in options.value:
            exit()
    elif Level == 67:
        Level = 68
        text = TextFile(68)
        user_options = ['Next']
    elif Level == 68:
        Level = 69
        text = TextFile(69)
        user_options = ['Next']
    elif Level == 69:
        if 'Elizabeth' in IsAlive(Living):
            Level = 71
            text = TextFile(71)
            user_options = ['Go after the monster', 'Let it go.']
        else:
            Level = 70
            text = TextFile(70)
            user_options = ['Go after the monster', 'Let it go.']
    elif Level == 70:
        if 'Let it go.' in options.value:
            Level = 72
            text = TextFile(72)
            user_options = ['Restart', 'Quit']
        if 'Go after the monster' in options.value:
            Level = 73
            text = TextFile(73)
            user_options = ['Next']
    elif Level == 71:
        if 'Let it go.' in options.value:
            Level = 72
            text = TextFile(72)
            user_options = ['Restart', 'Quit']
        if 'Go after the monster' in options.value:
            Level = 73
            text = TextFile(73)
            user_options = ['Next']
    elif Level == 72:
        if 'Restart' in options.value:
            Level = 0
            text = 'You have restarted the game. \n Use the character creator or randomize your stats.'
            user_options = ['Creator', 'Random']
            Living = []
        if 'Quit' in options.value:
            exit()
    elif Level == 73:
        Level = 74
        text = TextFile(74)
        user_options = ['Next']
    elif Level == 74:
        if 'Victor' in GetGoodLuck(Living):
            Level = 76
            text = TextFile(76)
            user_options = ['Next']
        else:
            Level = 75
            text = TextFile(75)
            user_options = ['Quit', 'Restart']
    elif Level == 75:
        if 'Restart' in options.value:
            Level = 0
            text = 'You have restarted the game. \n Use the character creator or randomize your stats.'
            user_options = ['Creator', 'Random']
            Living = []
        if 'Quit' in options.value:
            exit()
    elif Level == 76:
        Level = 77
        text = TextFile(77)
        user_options = ['Next']
    elif Level == 77:
        if Living[0].enthusiasm < 4:
            Level = 78
            text = TextFile(78)
            user_options = ['Restart', 'Quit']
        else:
            Level = 79
            text = TextFile(79)
            user_options = ['Kill the monster', 'Help him']
    elif Level == 78:
        if 'Restart' in options.value:
            Level = 0
            text = 'You have restarted the game. \n Use the character creator or randomize your stats.'
            user_options = ['Creator', 'Random']
            Living = []
        if 'Quit' in options.value:
            exit()
    elif Level == 79:
        if 'Kill the monster' in options.value:
            if 'Victor' in GetGoodLuck(Living):
                Level = 81
                text = TextFile(81)
                user_options = ['Restart', 'Quit']
            else:
                Level = 80
                text = TextFile(80)
                user_options = ['Restart', 'Quit']
        if 'Help him' in options.value:
            Level = 82
            text = TextFile(82)
            user_options = ['Next']
    elif Level == 80:
        if 'Restart' in options.value:
            Level = 0
            text = 'You have restarted the game. \n Use the character creator or randomize your stats.'
            user_options = ['Creator', 'Random']
            Living = []
        if 'Quit' in options.value:
            exit()
    elif Level == 81:
        if 'Restart' in options.value:
            Level = 0
            text = 'You have restarted the game. \n Use the character creator or randomize your stats.'
            user_options = ['Creator', 'Random']
            Living = []
        if 'Quit' in options.value:
            exit()
    elif Level == 82:
        Level = 83
        text = TextFile(83)
        user_options = ['Avoid the monsters request', 'Keep your promise']
    elif Level == 83:
        if 'Keep your promise' in options.value:
            Level = 85
            text = TextFile(85)
            user_options = ['Next']
        if 'Avoid the monsters request' in options.value:
            Level = 84
            text = TextFile(84)
            user_options = ['Restart', 'Quit']
    elif Level == 84:
        if 'Restart' in options.value:
            Level = 0
            text = 'You have restarted the game. \n Use the character creator or randomize your stats.'
            user_options = ['Creator', 'Random']
            Living = []
        if 'Quit' in options.value:
            exit()
    elif Level == 85:
        Level = 86
        text = TextFile(86)
        user_options = ['Next']
    elif Level == 86:
        Level = 87
        text = TextFile(87)
        user_options = ['Finish the second creature', 'Stop your work']
    elif Level == 87:
        if 'Finish the second creature' in options.value:
            Level = 88
            text = TextFile(88)
            user_options = ['Next']
        if 'Stop your work' in options.value:
            Level = 91
            text = TextFile(91)
            user_options = ['Next']
    elif Level == 88:
        if 'Victor' in GetGoodLuck(Living):
            Level = 90
            text = TextFile(90)
            user_options = ['Restart', 'Quit']
        else:
            Level = 89
            text = TextFile(89)
            user_options = ['Restart', 'Quit']
    elif Level == 89 or Level == 90:
        if 'Restart' in options.value:
            Level = 0
            text = 'You have restarted the game. \n Use the character creator or randomize your stats.'
            user_options = ['Creator', 'Random']
            Living = []
        if 'Quit' in options.value:
            exit()
    elif Level == 91:
        if not IsAlive(Living, 'Elizabeth'):
            Level = 92
            text = TextFile(92)
            user_options = ['Restart', 'Quit']
        else:
            Level = 93
            text = TextFile(93)
            user_options = ['Next']
    elif Level == 92:
        if 'Restart' in options.value:
            Level = 0
            text = 'You have restarted the game. \n Use the character creator or randomize your stats.'
            user_options = ['Creator', 'Random']
            Living = []
        if 'Quit' in options.value:
            exit()
    elif Level == 93:
        Level = 94
        text = TextFile(94)
        user_options = ['Next']
    elif Level == 94:
        Level = 95
        text = TextFile(95)
        user_options = ['Next']
    elif Level == 95:
        Level = 96
        text = TextFile(96)
        user_options = ['Next']
    elif Level == 96:
        Level = 97
        text = TextFile(97)
        user_options = ['Restart', 'Quit']
    elif Level == 97:
        if 'Restart' in options.value:
            Level = 0
            text = 'You have restarted the game. \n Use the character creator or randomize your stats.'
            user_options = ['Creator', 'Random']
            Living = []
        if 'Quit' in options.value:
            exit()

    Display_Dialogue(text)  # display the text for the next game level
    # display the options for the next game level
    Display_Options(user_options)
    # display the characters for the next game level
    Display_Characters(Living)


# GUI object creation
app = App(title="The True Monster", width=1200,
          height=600, layout="grid")  # main window
dialogue = ListBox(app, grid=[0, 0, 8, 6], scrollbar=True, items=[
                   'dialogue'], width=900, height=250)  # main multi-select box that I am using to display the text
# make it a better font by modifying the tkinter sub object
dialogue.font = "Courier"
title = Text(app, text="The True", grid=[
             9, 0, 1, 1], size=30)  # show the title
title.font = 'Lucida Handwriting'
title2 = Text(app, text='Monster', grid=[9, 1, 1, 2], size=30)
title2.font = 'Lucida Handwriting'
options_text = Text(app, grid=[3, 7, 8, 1], text="Options")
options = ListBox(app, grid=[3, 8, 2, 3], scrollbar=True, items=[
                  'options'], width=450, height=300, multiselect=True)
options.font = "Times New Roman"
characters_text = Text(app, grid=[0, 7, 2, 1], text="Characters")
characters = ListBox(app, grid=[0, 8, 2, 3],
                     scrollbar=True, items=['characters'], width=450, height=300)
# use a monospaced font to make it easier to read as the lines are all the same length
characters.font = "Courier"

submit = PushButton(app, grid=[9, 8, 2, 1],
                    text="Submit", command=continuegame)  # submit button that advances the game

# Enter Character Creator or Randomize by default
Level = 0  # global variable to keep track of the level as the game advances
Living = []  # global variable to keep track of the characters as they are created
# Use character class

Display_Dialogue(
    "Before we begin, would you like to enter the character creator, or would you like random characters? \n Select one of the options below. Then click submit.  Selecting 'Next' is unnecessary when there are no other options.")

Display_Options(["Creator", "Random"])
Display_Characters(Living)

app.display()  # display the GUI with loop so the UI is responsive
