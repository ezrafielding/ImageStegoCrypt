from tkinter import filedialog
from tkinter import*
import time
from stegcrypt import StegCrypt
from PIL import Image
import numpy as np

root = Tk()
Tk().withdraw()
root.geometry("600x620+0+0")
root.title("Image Steganocryptography Implementation")

#================Variable Declaration==============================
folder_path_plainfile = StringVar()
folder_path_coverfile1 = StringVar()
folder_path_coverfile2 = StringVar()
folder_path_stegofile = StringVar()
status_text = StringVar()
SC = StegCrypt()

#================Window Framing=================================
Tops = Frame(root, width = 1000, relief = SUNKEN)
Tops.pack(side=TOP)
window = Frame(root, width = 1000, relief = SUNKEN)
window.pack(side=TOP)

#=========================Time======================================
localtime=time.asctime(time.localtime(time.time()))

#=========================Info======================================
lblInfo = Label(Tops, font=('arial', 15, 'bold'), text="Image Steganocryptography\nImplementation",fg="Black")
lblInfo.grid(row=0,column=0)
lblInfo = Label(Tops, font=('arial', 8, 'bold', 'italic'),text=localtime, fg="Black")
lblInfo.grid(row=1,column=0)
lblInfo = Label(window, font=('arial', 15, 'bold'),text="\nEncryption and Image Hiding", fg="Black")
lblInfo.grid(row=2,column=0)
lblInfo = Label(window, font=('arial', 8, 'italic', 'bold'),text="\nAttach Plaintext Image file (.jpg)", fg="Steel Blue")
lblInfo.grid(row=3,column=0)
lblInfo = Label(window, font=('arial', 8, 'italic','bold'), text="\nAttach Covertext Image file (.jpg)", fg="Steel Blue")
lblInfo.grid(row=5,column=0)
lblInfo = Label(window, font=('arial', 15, 'bold'),text="\nDecryption", fg="Black")
lblInfo.grid(row=10,column=0)
lblInfo = Label(window, font=('arial', 8, 'italic', 'bold'),text="\nAttach Stegotext Image file (.jpg)", fg="Steel Blue")
lblInfo.grid(row=11,column=0)
lblInfo = Label(window, font=('arial', 8, 'italic','bold'), text="\nAttach Covertext Image file (.jpg)", fg="Steel Blue")
lblInfo.grid(row=13,column=0)
lblInfo = Label(window, font=('arial', 8, 'bold'), text=" \n \nSTATUS", fg="Steel Blue")
lblInfo.grid(row=17,column=0)

#=========================Operation=================================
def browse_button_plainfile():
    file_path=filedialog.askopenfilename()
    folder_path_plainfile.set(file_path)
    print (folder_path_plainfile)

def browse_button_stegofile():
    file_path=filedialog.askopenfilename()
    folder_path_stegofile.set(file_path)
    print (folder_path_stegofile)

def browse_button_coverfile1():
    file_path=filedialog.askopenfilename()
    folder_path_coverfile1.set(file_path)
    print (folder_path_coverfile1)

def browse_button_coverfile2():
    file_path=filedialog.askopenfilename()
    folder_path_coverfile2.set(file_path)
    print (folder_path_coverfile2)

def btnEncrypt():
    plaintext = SC.open_img(folder_path_plainfile.get())
    covertext = SC.open_img(folder_path_coverfile1.get())
    stegotext = SC.encrypt(plaintext, covertext)
    SC.save_stegotext_tiff(stegotext, "Stegotext.tiff")

def btnDecrypt():
    stegotext = SC.open_stegotext_tiff(folder_path_stegofile.get())
    covertext = SC.open_img(folder_path_coverfile2.get())
    plaintext = SC.decrypt(stegotext, covertext)
    SC.save_image(plaintext, "Plaintext.jpg")

#=========================Display===================================
txtDisplay = Entry(window, font=('arial',8),textvariable=folder_path_plainfile, bd=5,width =50, bg="white")
txtDisplay.grid(row=4,column=0)
textvariable=folder_path_plainfile.get()
txtDisplay = Entry(window, font=('arial',8),textvariable=folder_path_coverfile1, bd=5,width=50, bg="white")
txtDisplay.grid(row=6,column=0)
txtDisplay = Entry(window, font=('arial',8),textvariable=folder_path_stegofile, bd=5,width =50, bg="white")
txtDisplay.grid(row=12,column=0)
textvariable=folder_path_plainfile.get()
txtDisplay = Entry(window, font=('arial',8),textvariable=folder_path_coverfile2, bd=5,width=50, bg="white")
txtDisplay.grid(row=14,column=0)
txtDisplay = Entry(window, font=('arial',8),
textvariable=status_text, bd=5, width =50, bg="white")
txtDisplay.grid(row=18,column=0)

#=========================Buttons===================================
btnbrowseplaintxt=Button(window, padx=5,pady=5,bd=5,fg="black", font=('arial', 8,'bold'), text="BROWSE Image File",bg ="brown", command=browse_button_plainfile).grid(row=4,column=1)
btnbrowsecovertxt1=Button(window, padx=5,pady=5,bd=5,fg="black", font=('arial', 8,'bold'), text="BROWSE Image File",bg ="brown", command=browse_button_coverfile1).grid(row=6,column=1)
btnEncr=Button(window, padx=5,pady=5,bd=5,fg="black", font=('arial', 12,'bold'), text="Encrypt",bg ="powder blue", command=btnEncrypt).grid(row=9,column=0)
btnbrowsestegotxt=Button(window, padx=5,pady=5,bd=5,fg="black", font=('arial', 8,'bold'), text="BROWSE Image File",bg ="brown", command=browse_button_stegofile).grid(row=12,column=1)
btnbrowsecovertxt2=Button(window, padx=5,pady=5,bd=5,fg="black", font=('arial', 8,'bold'), text="BROWSE Image File",bg ="brown", command=browse_button_coverfile2).grid(row=14,column=1)
btnDecr=Button(window, padx=5,pady=5,bd=5,fg="black", font=('arial', 12,'bold'), text="Decrypt",bg ="powder blue", command=btnDecrypt).grid(row=15,column=0)
root.mainloop()