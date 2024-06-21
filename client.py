from tkinter import Button,StringVar,Label,Canvas,PhotoImage,Radiobutton,Entry,Tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from PIL import ImageTk,Image

def Fmenu():
    global currentf
    Fmenu = Canvas(main,width=960,height=540)
    Fmenu.pack(expand = True, fill = 'both')
    Fmenu.pack_propagate(False)
    currentf = Fmenu

    buttonEnc = Button(Fmenu,text='Encode', bg='red', fg='white', width=20, command=Fencode)
    buttonEnc.place(relx=0.2,rely = 0.8,anchor='center')
    buttonDec = Button(Fmenu,text='Decode', bg='blue',fg='white', width=20, command=Fdecode)
    buttonDec.place(relx=0.8,rely = 0.8,anchor='center')
    buttonExit = Button(text='Exit', bg='black',fg='white', width=15, command=exit)
    buttonExit.place(relx=0.5,rely=0.9,anchor='center') #a