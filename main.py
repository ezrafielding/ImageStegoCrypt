from tkinter import filedialog
from tkinter import*
import random
import time
import numpy as np
from numpy.fft import fft
import sys
import numpy
import PIL
from PIL import Image
import io
import base64
from io import BytesIO
import codecs

root = Tk()
Tk().withdraw()
root.geometry("600x600+0+0")
root.title("Phase-Only Digital Encryption using a Three-Pass Protocol")

#================Variable Declaration==============================
keyAB = IntVar()
keyC = DoubleVar()
folder_path_textfile = StringVar()
status_text = StringVar()
keyC = np.random.rand(1,1)*10**(np.round(np.random.rand(1,1)*6))

#================Window Framing=================================
Tops = Frame(root, width = 1000, relief = SUNKEN)
Tops.pack(side=TOP)
window = Frame(root, width = 1000, relief = SUNKEN)
window.pack(side=TOP)

#=========================Time======================================
localtime=time.asctime(time.localtime(time.time()))

#=========================Info======================================
lblInfo = Label(Tops, font=('arial', 15, 'bold'), text="Phase-Only Digital Encryption \n using a Three-Pass Protocol",fg="Black")
lblInfo.grid(row=0,column=0)
lblInfo = Label(Tops, font=('arial', 8, 'bold', 'italic'),
text=localtime, fg="Black")
lblInfo.grid(row=1,column=0)
lblInfo = Label(window, font=('arial', 8, 'italic', 'bold'),
text="\n \n \n Attach image file (.jpg)", fg="Steel Blue")
lblInfo.grid(row=3,column=0)
lblInfo = Label(window, font=('arial', 8, 'italic','bold'), text="\n\n KEY (string integers no more than 10 digits long) \n", fg="Steel Blue")
lblInfo.grid(row=5,column=0)
#lblInfo = Label(window, font=('arial', 8, 'italic', 'bold'), text="\n c (Spectral Embedding Constant) >> 1 ; \n use only for STEP 1 \n\n", fg="Steel Blue")
#lblInfo.grid(row=7,column=0)
lblInfo = Label(window, font=('arial', 8, 'bold'), text=" \n \nSTATUS", fg="Steel Blue")
lblInfo.grid(row=14,column=0)

#=========================Operation=================================
def browse_button_textfile():
    file_path=filedialog.askopenfilename()
    folder_path_textfile.set(file_path)
    print (folder_path_textfile)

def btnClick_STEP1():
    with open(folder_path_textfile.get(), "rb") as image:
        s = base64.b64encode(image.read()).decode('ASCII')

    l1=[c for c in s]
    P=[ord(c) for c in s]
    zero =np.zeros((1))
    P =np.concatenate((zero, P))
    N=np.size(P.transpose(),axis=0)
    np.random.seed(keyAB.get())
    Theta= np.random.rand((N))
    POS=(np.exp(1j*(np.angle(fft(Theta)))))
    E=fft(P)*POS+keyC*(POS)
    E=(np.fft.ifft(E)).real
    np.savetxt("CipherImage1.jpg", E)
    status_text.set("cipherImage 1 text file generated")

def btnClick_STEP2():
    E= np.loadtxt(folder_path_textfile.get())
    N=np.size(E.conj().transpose(),axis=0)
    E=fft(E)
    np.random.seed(keyAB.get())
    Theta= np.random.random((N))
    E=E*(np.exp(1j*(np.angle(fft(Theta)))))
    E=(np.fft.ifft(E)).real
    np.savetxt("CipherImage2.jpg", E)
    status_text.set("cipherImage 2 text file generated")

def btnClick_STEP3():
    E= np.loadtxt(folder_path_textfile.get())
    N=np.size(E.conj().transpose(),axis=0)
    E=fft(E)
    np.random.seed(keyAB.get())
    Theta= np.random.rand((N))
    E=E*(np.exp(-1j*(np.angle(fft(Theta)))))
    E=(np.fft.ifft(E)).real
    np.savetxt("CipherImage3.jpg", E, fmt="%10.5f")
    status_text.set("cipherImage 3 text file generated")

def btnClick_STEP4():
    pic = ""
    flag = True

    E= np.loadtxt(folder_path_textfile.get())
    try:
        N=np.size(E.conj().transpose(),axis=0)
        E=fft(E)
        np.random.seed(keyAB.get())
        Theta= np.random.random((N))
        E=E*(np.exp(-1j*(np.angle(fft(Theta)))))
        P=(np.fft.ifft(E)).real
        P[0] = 0
        P=np.round(P)
        P= (P.astype(int))
        l1=[c for c in P]
        P=[chr(c) for c in P]

        for character in P:
            if flag:
                flag = False
                continue
            else:
                pic = pic + character
        f = io.BytesIO(base64.b64decode(bytes(pic,'utf-8')))
        pilimage = Image.open(f)
        pilimage = pilimage.save("Decrypted_Image.jpg")
        status_text.set("decrypted Image file generated")
    except ValueError:
        status_text.set("ERROR: decrypted Image file NOT generated")

#=========================Display===================================
txtDisplay = Entry(window, font=('arial',8),
textvariable=folder_path_textfile, bd=5,width =50, bg="white")
txtDisplay.grid(row=4,column=0)
textvariable=folder_path_textfile.get()
txtDisplay = Entry(window, font=('arial',8), textvariable=keyAB,bd=5, width =20, bg="white")
txtDisplay.grid(row=5,column=1)
#txtDisplay = Entry(window, font=('arial',8), textvariable=keyC,bd=5, width =20, bg="white")
#txtDisplay.grid(row=7,column=1)
#textvariable=keyC
txtDisplay = Entry(window, font=('arial',8),
textvariable=status_text, bd=5, width =50, bg="white")
txtDisplay.grid(row=15,column=0)

#=========================Buttons===================================
btnbrowsetxt=Button(window, padx=5,pady=5,bd=5,fg="black",
font=('arial', 8,'bold'), text="BROWSE Image File",bg ="brown", command=browse_button_textfile).grid(row=4,column=1)
btnstep1=Button(window, padx=5,pady=5,bd=5,fg="black",
font=('arial', 12,'bold'), text="STEP 1",bg ="powder blue", command=btnClick_STEP1).grid(row=9,column=0)
btnstep2=Button(window, padx=5,pady=5,bd=5,fg="black",
font=('arial', 12,'bold'), text="STEP 2",bg ="powder blue", command=btnClick_STEP2).grid(row=10,column=0)
btnstep3=Button(window, padx=5,pady=5,bd=5,fg="black",font=('arial', 12,'bold'), text="STEP 3",bg ="powder blue", command=btnClick_STEP3).grid(row=11,column=0)
btnstep4=Button(window, padx=5,pady=5,bd=5,fg="black",font=('arial', 12,'bold'), text="STEP 4",bg ="powder blue", command=btnClick_STEP4).grid(row=12,column=0)

root.mainloop()