from awake import wol
import commands
import re


WORDS = ["ACTIVATE", "CLOSE", "COMPUTER", "UBUNTU", "WINDOWS", "FEDORA"]


def handle(text, mic, profile):
    """
        Broadcast a magic packet to wake up the computer and send a signal to the
        Arduino to tell it which OS to pick from

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone number)
    """

    text = text.lower()
    ## Try to work out which OS to wake up
    match = re.search(r"(?P<action>\w+) (?P<target>\w+)", text)
    if match:
        ## tempted to just use "os" here but it is a package name, meh
        target = match.group("target")
        action = match.group("action")
        os_config = profile["activator"]
        if target not in os_config:
            #target not recognised
            mic.say("I'm sorry. Target operating system %s is not recognised." % target)
            return # break
        if action == "activate":
            mic.say("Activating %s." % target)
            mac = os_config[target]["mac"]
            wol.send_magic_packet(mac)
        elif action == "close":
            mic.say("Closing %s." % target)
            if target == "windows":
                return
            else:
                passwd = os_config[target]["passwd"]
                host = os_config[target]["host"]
                commands.getoutput("ssh pi@%s sudo poweroff" % host)

    else:
        mic.say("I'm sorry I did not catch your last command. Please try again.")


def isValid(text):
    """
        Returns True if input is related to boot sequence.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r"\b((close|activate)\ (ubuntu|fedora|windows))\b", text, re.IGNORECASE))
