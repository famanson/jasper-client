from awake import wol
import commands
import re
import serial
import time


WORDS = ["ACTIVATE", "RESET", "CLOSE", "COMPUTER", "UBUNTU", "WINDOWS", "FEDORA"]
EMPTY_DATA_SIZE = 2 # a magic number

def read(ser):
    count = 0
    while count < 50:
        data = ser.read(256).__repr__()
        if data and len(data) > 2:
            return str(data[:-5])
        else:
            print "Looping."
        count = count + 1
    return None

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
            if target != "reset":
                #target not recognised
                mic.say("I'm sorry. Target operating system %s is not recognised." % target)
                return # break
        if action == "activate":
            ser = serial.Serial('/dev/ttyUSB0', 38400, timeout=1)
            try:
                if target == "reset":
                    ser.write("reset")
                    mic.say("Activation reset!")
                else:
                    mic.say("Activating %s." % target)
                    mac = os_config[target]["mac"]
                    wol.send_magic_packet(mac)

                    # Now sleep for 20 seconds to wait for grub to show up
                    time.sleep(20)

                    # Send the activate command
                    ser.write("activate")
                    # Receive ACK1
                    ack1 = read(ser)
                    if not ack1 or ACK1 not in ack1:
                        print ack1
                        mic.say("Acknowledge signal 1 was not received")
                        raise ValueError
                    # Got ACK1 here, send target system
                    ser.write(target)
                    ack2 = read(ser)
                    if not ack2 or ACK2 not in ack2:
                        print ack2
                        mic.say("Acknowledge signal 2 was not received")
                        raise ValueError
                    # Got ack2
                    mic.say("Activation completed!")
            except:
                mic.say("Error found. Activation failed!")
            finally:
                ser.close()

        elif action == "close":
            mic.say("Closing %s." % target)
            if target == "windows":
                return
            else:
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
    return bool(re.search(r"\b((close|activate)\ (reset|ubuntu|fedora|windows))\b", text, re.IGNORECASE))
