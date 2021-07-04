#---------------------------------------
# Libraries and references
#---------------------------------------
from collections import deque
import codecs
import json
import os
import ctypes
import winsound
import time
#---------------------------------------
# [Required] Script information
#---------------------------------------
ScriptName = "Emote Counter"
Website = "https://lion-blanc.com"
Description = "Test"
Creator = "DLLB"
Version = "1.0.0"
Description = "Count Message and trigger a sound if a strike is done in a certain defined time"

#---------------------------------------
# Versions
#---------------------------------------
"""
1.0 - Initial release
"""
#---------------------------------------
# Variables
#---------------------------------------
settingsFile = os.path.join(os.path.dirname(__file__), "settings.json")
AudioFilesPath = os.path.join(os.path.dirname(__file__), "sounds")
AudioPlaybackQueue2 = deque()
MessageBox = ctypes.windll.user32.MessageBoxW
MB_YES = 6
COUNT = 0
DESC = False
#---------------------------------------
# Classes
#---------------------------------------
class Settings:
    """" Loads settings from file if file is found if not uses default values"""
    # The 'default' variable names need to match UI_Config
    def __init__(self, settingsFile=None):
        if settingsFile and os.path.isfile(settingsFile):
            with codecs.open(settingsFile, encoding='utf-8-sig', mode='r') as f:
                self.__dict__ = json.load(f, encoding='utf-8-sig')

        else: #set variables if no settings file is found
            self.Volume = 50
            self.Cooldown = 3
            self.Sound = "Discord"
            self.Caster = True
            self.Blacklist = "Streamlabs,Nightbot,Moobot,StreamElements"
            self.EmoteMessage = "drake62Gg"
            self.EmoteTreshold = 10
            self.EventCooldown = 1

    # Reload settings on save through UI
    def Reload(self, data):
        """Reload settings on save through UI"""
        self.__dict__ = json.loads(data, encoding='utf-8-sig')

    def Save(self, settingsfile):
        """ Save settings contained within the .json and .js settings files. """
        try:
            with codecs.open(settingsfile, encoding="utf-8-sig", mode="w+") as f:
                json.dump(self.__dict__, f, encoding="utf-8", ensure_ascii=False)
            with codecs.open(settingsfile.replace("json", "js"), encoding="utf-8-sig", mode="w+") as f:
                f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8', ensure_ascii=False)))
        except ValueError:
            Parent.Log(ScriptName, "Failed to save settings to file.")

#---------------------------------------
# Settings functions
#---------------------------------------
def SetDefaults():
    """Set default settings function"""
    winsound.MessageBeep()
    returnValue = MessageBox(0, u"You are about to reset the settings, "
                                "are you sure you want to contine?"
                             , u"Reset settings file?", 4)

    if returnValue == MB_YES:

        returnValue = MessageBox(0, u"Settings successfully restored to default values"
                                 , u"Reset complete!", 0)

        MySet = Settings()
        MySet.Save(settingsFile)

def ReloadSettings(jsonData):
    """Reload settings on Save"""
    global MySet
    MySet.Reload(jsonData)

def OpenReadMe():
    """Open the readme.txt in the scripts folder"""
    location = os.path.join(os.path.dirname(__file__), "README.txt")
    os.startfile(location)

#---------------------------------------
# [Required] functions
#---------------------------------------
def Init():
    """Data on Load, required function"""
    global MySet
    global lastMessage

    MySet = Settings(settingsFile)
    lastMessage = time.time() - MySet.Cooldown*60

def Tick():
    """Required tick function"""
    if AudioPlaybackQueue2:
        if Parent.PlaySound(AudioPlaybackQueue2[0], MySet.Volume * 0.01):
            AudioPlaybackQueue2.popleft()

def Execute(data):
    """Required Execute Data function"""
    if data.IsChatMessage():
        if Parent.HasPermission(data.User, "Caster", "") and MySet.Caster:
            return

        wordslist = MySet.Blacklist.split(",")
        for word in wordslist:
            if data.UserName.lower() == word.lower():
                return

        process(data.Message)

        global COUNT

        if (COUNT>=MySet.EmoteTreshold):
            EnqueueAudioFile(MySet.Sound)
            reset()

        lastMessage = time.time()

def process(message):
    global COUNT, lastMessage
    split = message.strip().split(" ")
    if (MySet.EmoteMessage in split):
        COUNT += 1
    elif (lastMessage + MySet.EventCooldown*60) >= time.time():
        reset()

def reset():
    global COUNT
    COUNT = 0

def EnqueueAudioFile(audiofile):
    """ Adds an audio file from the audio folder to the play queue. """
    SoundsPath = os.path.join(AudioFilesPath, audiofile + ".mp3")
    AudioPlaybackQueue2.append(SoundsPath)

def TestSound():
    """Test sound & volume through UI button"""
    SoundsPath = os.path.join(AudioFilesPath, MySet.Sound + ".mp3")
    Parent.PlaySound(SoundsPath, MySet.Volume*0.01)
