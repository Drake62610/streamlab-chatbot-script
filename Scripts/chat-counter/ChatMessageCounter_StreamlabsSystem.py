#---------------------------------------
# Libraries and references
#---------------------------------------
import os
import random

#---------------------------------------
# [Required] Script information
#---------------------------------------
ScriptName = "Chat Message Counter"
Website = "https://lion-blanc.com"
Creator = "DLLB"
Version = "1.1.0"
Description = "Count Message and trigger a funny line for some numbers"

#---------------------------------------
# Versions
#---------------------------------------
"""
1.0 - Initial release
1.1 - Add reward.txt support
"""
#---------------------------------------
# Variables
#---------------------------------------
rewards = open(os.path.abspath(__file__) + '/../reward.txt').read().splitlines()

#---------------------------------------
# Settings functions
#---------------------------------------
def OpenReadMe():
    """Open the readme.txt in the scripts folder"""
    location = os.path.join(os.path.dirname(__file__), "README.txt")
    os.startfile(location)

#---------------------------------------
# [Required] functions
#---------------------------------------
def Init():
    """Data on Load, required function"""
    global count, eventIds
    count = 0
    eventIds = [1, 25, 50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400, 425, 450, 475, 500, 69, 666]
    random.shuffle(rewards)

def Execute(data):
    """Required Execute Data function"""
    global count, eventIds

    if data.IsChatMessage():
        count += 1

        talk(data.UserName)
        # print(randnum())
        # if count in eventIds:
        #     talk(data.UserName)

def Tick():
    return


#---------------------------------------
# functions
#---------------------------------------
def talk(username):
    global count
    reward = "C'est le $count message $user tu remportes : ".replace("$count", str(count)).replace("$user", username)

    if count == 69:
        Parent.SendStreamMessage(reward + "NICE uwu")
        return
    if count == 666:
        Parent.SendStreamMessage(reward + "Un ban")
        return
    
    Parent.SendStreamMessage(reward + rewards.pop())
    Parent.SendStreamMessage(str(len(rewards)))
