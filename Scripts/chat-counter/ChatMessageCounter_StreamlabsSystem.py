#---------------------------------------
# Libraries and references
#---------------------------------------
import os

#---------------------------------------
# [Required] Script information
#---------------------------------------
ScriptName = "Chat Message Counter"
Website = "https://lion-blanc.com"
Description = "Test"
Creator = "DLLB"
Version = "1.0.0"
Description = "Count Message and trigger a funny line for some numbers"

#---------------------------------------
# Versions
#---------------------------------------
"""
1.0 - Initial release
"""
#---------------------------------------
# Variables
#---------------------------------------


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
    eventIds = [1, 2, 5]

def Execute(data):
    """Required Execute Data function"""
    global count, eventIds

    if data.IsChatMessage():
        count += 1
        print(count)

        if count in eventIds:
            talk(data.UserName)

def Tick():
    return


#---------------------------------------
# functions
#---------------------------------------
def talk(username):
    global count
    reward = "C'est le $count message tu remportes : ".replace("$count", str(count))


    if count == 2:
        Parent.SendStreamMessage(reward + "NICE uwu $user".replace("$user", username))
        return

    # Pick a random reward
    Parent.SendStreamMessage(reward + "Un message bien encourageant $user".replace("$user", username))