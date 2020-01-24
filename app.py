import requests
import random
import time
from apscheduler.schedulers.background import BackgroundScheduler
from tkinter import *
from tkinter import messagebox
import configparser
from PIL import ImageTk, Image

sched = BackgroundScheduler()
config = configparser.RawConfigParser()
config.read('config.ini')


def waka():

    f = open("hb.txt", "r")
    numheartbeat = int(f.readline())
    f.close()
    url = config.get('DEFAULT', 'Url')
    api = config.get('DEFAULT', 'Api')

    files = config.items('FILES')

    file_list = []
    for value in files:
        file_list.append(value)

    selectedfile = random.choice(file_list)
    pl = selectedfile[1]
    proegramminglang = str.upper(str(pl[-3:]))

    payload = {
        "entity": pl,
        "type": config.get('HEARTBEAT', 'Type'),
        "category": config.get('HEARTBEAT', 'Category'),
        "time": time.time(),
        "project": config.get('HEARTBEAT', 'Project'),
        "language": proegramminglang,
        "lines": random.randint(2, 20),
        "is_write": True,
        "hostname": config.get('HEARTBEAT', 'Hostname'),
        "user_agent": config.get('HEARTBEAT', 'Useragent')
    }

    req = requests.post(url, data='', json=payload, auth=(
        '', api))
    if(req.ok):
        response = req.json()
        local_time = time.ctime(time.time())
        print("Aye,Aye Captain, Successful")
        print('Response id ' + response['data']['id'] + ' at ' + local_time)
        numheartbeat += 1
        f = open("hb.txt", "w+")
        f.write(str(numheartbeat))
        f.close()
        hblabel['text'] = f"{numheartbeat} heartbeats sent. Last sent @ {local_time}"
    else:
        print("Abort Bitch")
        print(req.text)
        exit()


def start():
    local_time = time.ctime(time.time())
    sched.add_job(waka, 'interval', minutes=random.randint(1, 10))
    try:
        sched.start()
        status['text'] = f"Task Started @ {local_time}"
        return True
    except:
        status['text'] = f"Task Start Failed @ {local_time}"
        return False


def quit():
    try:
        sched.shutdown()
        sched.remove_all_jobs()
    finally:
        f = open("hb.txt", "w+")
        f.write(str(0))
        f.close()
        exit()


window = Tk()
window.geometry("300x300")
window.title("Waka Time Spoof")
window.configure(background='white')
mainlbl = Label(window, text="Waka Time Spoof", fg='white', bg='brown',
                relief=SOLID, font=("arial", 16, "bold"))
startbutton = Button(window, text="start", fg='white', bg='green',
                     relief=RAISED, font=("arial", 16, "bold"), command=start)
stopbutton = Button(window, text="stop", fg='white', bg='red',
                    relief=RAISED, font=("arial", 16, "bold"), command=quit)
hblabel = Label(window, text="0 heartbeats")
status = Label(window, text="")

load = Image.open("wakatime.jpg")
render = ImageTk.PhotoImage(load)
img = Label(window, image=render, width=50, height=50)
img.image = render

img.place(x=120, y=10)
mainlbl.place(x=52, y=90)
startbutton.place(x=112, y=150)
stopbutton.place(x=112, y=200)
status.place(x=5, y=240)
hblabel.place(x=5, y=270)
window.mainloop()
