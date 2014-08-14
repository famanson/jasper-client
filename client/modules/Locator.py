from awake import wol
import commands
import re

WORDS = ["WHERE", "ARE", "YOU"]

def handle(text, mic, profile):
    """
        Get Jasper to locate the Pi on the network

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone number)
    """
    ipadd = commands.getoutput("/sbin/ifconfig").split("\n")[1].split()[1][5:]
    mic.say("I am located at %s" % ipadd)

def isValid(text):
    """
        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r"\bwhere\ are\ you\b", text, re.IGNORECASE))
