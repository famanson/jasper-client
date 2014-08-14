from awake import wol
import commands
import re

WORDS = ["NETWORK", "ADDRESS"]

def handle(text, mic, profile):
    """
        Get Jasper to locate the Pi on the network

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone number)
    """
    ipadd = commands.getoutput("/sbin/ifconfig").split("\n")[1].split()[1][5:]
    mic.say("I am located at")
    for c in list(ipadd):
        mic.say(c)


def isValid(text):
    """
        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r"\b(network)?address\b", text, re.IGNORECASE))
