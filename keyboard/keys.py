import time
import mouse
import keyboard

commands = [
    "torrentfile -V",
    "torrentfile create ExampleData",
    "ls",
    "rm ExampleData.torrent",
    "torrentfile create --private --announce https://tracker1 https://tracker2 --source Example --piece-length 20 --out ExampleData.torrent ExampleData",
    "ls",
    "torrentfile recheck ExampleData.torrent ExampleData",
]

def write_command(msg, delay, clear):
    keyboard.write(msg,.04)
    keyboard.send("enter")
    time.sleep(delay)
    if clear:
        keyboard.write("clear",.03)
        keyboard.send("enter")
        time.sleep(.5)


def main():
    mouse.click()
    time.sleep(2)
    delays = [2,4,2,2,4,2,4]
    clears = [0,1,0,0,1,0,0]
    for cmd, delay, clear in zip(commands, delays, clears):
        write_command(cmd, delay, clear)

keyboard.read_key("esc")
main()
