import tkinter as tk
from tkinter import Message ,Text, Toplevel, Grid, messagebox
import time 
import tkinter.ttk as ttk
import tkinter.font as font
import serial

unit = " g"
P = "P "

pBottCount = 0
canCount = 0
totalPBW = 0
totalCW = 0
totalRewardPb = 0
totalRewardC = 0
basePr = 10
baseW = 100 #Php 10 per 100grams 

ser = serial.Serial("COM3", baudrate=9600, timeout=1)

window = tk.Tk()
window.title("Plastic and Beverage Can Collector")
#window.attributes('-fullscreen', True)
window.geometry('800x480+0+0')
window.configure(background='gray')
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
window.resizable(0, 0)


background1 = tk.Label(window, bg="#008080", width=400, height=440)
background1.place(x=0,y=0)
background2 = tk.Label(window, bg="#cd5b45", width=400, height=440)
background2.place(x=400,y=0)
title = tk.Label(window, text="Plastic and Beverage Can Collector", bg="#133337", fg="white", width=73, font=('times', 15, 'italic bold'))
title.place(x =0, y = 0)#x170
plasticlbl = tk.Label(window, text="Plastic Bottles", bg="#008080", font=('times', 22,'italic bold'))
plasticlbl.place(x=100,y=60)
canlbl = tk.Label(window, text="Beverage Cans", bg="#cd5b45", font=('times', 22, 'italic bold'))
canlbl.place(x=510,y=60)

numBottles = tk.Label(window, text="Number of Bottles:", bg="#008080", font=('times', 17, 'bold'))
numBottles.place(x=40,y=160)
numBottRes = tk.Label(window, text="none", bg="white", width=11, height=1,font=('times', 15, 'bold'))
numBottRes.place(x=250,y=160)

numCans = tk.Label(window, text="Number of Cans:", bg="#cd5b45", font=('times', 17, 'bold'))
numCans.place(x=440,y=160)
numCanRes = tk.Label(window, text="none", bg="white", width=11, height=1, font=('times', 15, 'bold'))
numCanRes.place(x=635,y=160)

bottW = tk.Label(window, text="Total Weight:", bg="#008080", font=('times', 17, 'bold'))
bottW.place(x=40,y=250)
bottWRes = tk.Label(window, text="0" + unit, bg="white", width=13, height=1, font=('times', 15, 'bold'))
bottWRes.place(x=190,y=250)

cansW = tk.Label(window, text="Total Weight:", bg="#cd5b45", font=('times', 17, 'bold'))
cansW.place(x=440,y=250)
canWRes = tk.Label(window, text="0" + unit, bg="white", width=13, height=1, font=('times', 15, 'bold'))
canWRes.place(x=600,y=250)

bottRew = tk.Label(window, text="Cash Reward:", bg="#008080", font=('times', 17, 'bold'))
bottRew.place(x=40,y=340)
bottRewRes = tk.Label(window, text = P + "0.0", bg="white", width=16, height=1, font=('times', 15, 'bold'))
bottRewRes.place(x=190,y=340)

cansRew = tk.Label(window, text="Cash Reward:", bg="#cd5b45", font=('times', 17, 'bold'))
cansRew.place(x=440,y=340)
cansRewRes = tk.Label(window, text = P + "0.00", bg="white", width=16, height=1, font=('times', 15, 'bold'))
cansRewRes.place(x=590,y=340)


#funtions
while ser.in_waiting():
    inbytes = ser.readline().decode('ascii')
    splitMat = inbytes.split(x)
    if (inbytes == "liq"):
        msgBoxwarn1 = tk.showwarning('Liquid Detected', 'Liquid is detected in the bottle/can. Please empty the bottle/can first and insert again.')
    if(splitMat[0] == "p"):
        pBottCount += 1
        totalPBW = totalPBW + splitMat[1]
        percW = totalPBW / baseW
        a = basePr * percW
        totalRewardPb = totalRewardPb + a
        numBottRes.configure(text=str(pBottCount))
        bottWRes.configure(text=str(totalPBW))
        bottRewRes.configure(text=str(round(totalRewardPb)))
    if(splitMat[0] == "c"):
        canCount =+ 1
        totalCW = totalCW + splitMat[1]
        percW = totalCW / baseW
        a = basePr * baseW
        totalRewardC = totalRewardC + a
        numCans.configure(text=str(canCount))
        canWRes.configure(text=str(totalCW))
        cansRewRes.configure(text=str(round(totalRewardC)))
        
def getReward():
    msgBox = tk.messagebox.askquestion("Get Reward","Proceed getting cash reward?")
    totalRewards = totalRewardPb + totalRewardC
    sendRew = "rew:" + str(totalRewards)
    if msgBox == "yes":
        ser.write(sendRew.encode())
        plasticCount = 0
        totalReward = 0
    else:
        tk.messagebox.showinfo('Return','You will now return to the application screen')

mes1 = tk.Label(window, text="Is that all your bottles/cans?", bg="#008080", font=('times', 13))
mes1.place(x=125,y=428)

rewBtn = tk.Button(window, text="Get Rewards", command = getReward, bg="#133337", fg="white", height=1, font=('times', 14, 'bold'))
rewBtn.place(x=335,y=420)

window.mainloop()