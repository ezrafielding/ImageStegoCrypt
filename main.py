# COS738 Assignment 3
# Ezra Fielding, 3869003

from tkinter import filedialog
from tkinter import*
import time
from stegcrypt import StegCrypt

#=========================Methods=================================
def browse_button_plainfile():
    '''
    Spawns filedialog to select Plaintext Image
    '''
    file_path=filedialog.askopenfilename()
    folder_path_plainfile.set(file_path)
    print (folder_path_plainfile)

def browse_button_stegofile():
    '''
    Spawns filedialog to select Stegotext Image
    '''
    file_path=filedialog.askopenfilename()
    folder_path_stegofile.set(file_path)
    print (folder_path_stegofile)

def browse_button_coverfile1():
    '''
    Spawns filedialog to select Covertext Image for encryption
    '''
    file_path=filedialog.askopenfilename()
    folder_path_coverfile1.set(file_path)
    print (folder_path_coverfile1)

def browse_button_coverfile2():
    '''
    Spawns filedialog to select Covertext Image for decryption
    '''
    file_path=filedialog.askopenfilename()
    folder_path_coverfile2.set(file_path)
    print (folder_path_coverfile2)

def btnEncrypt():
    '''
    Encrypts the Plaintext with the Covertext
    '''
    try:
        # Open and load image files
        plaintext = SC.open_img(folder_path_plainfile.get())
        covertext = SC.open_img(folder_path_coverfile1.get())
        # Encrypt Plaintext image
        stegotext = SC.encrypt(plaintext, covertext)
        # Save Stegotext Image
        SC.save_stegotext_tiff(stegotext, "Stegotext.tiff")
        # Set status
        status_text.set("Encryption Complete! Stegotext Image Saved")
    except ValueError as v:
        status_text.set(v)
    except Exception as e:
        status_text.set(e)

def btnDecrypt():
    '''
    Decrypts Stegotext with the Covertext
    '''
    try:
        # Open and load image files
        stegotext = SC.open_stegotext_tiff(folder_path_stegofile.get())
        covertext = SC.open_img(folder_path_coverfile2.get())
        # Decrypt Stegotext Image
        plaintext = SC.decrypt(stegotext, covertext)
        # Save Plaintext Image
        SC.save_image(plaintext, "Plaintext.jpg")
        # Set Status
        status_text.set("Decryption Complete! Plaintext Image Saved")
    except ValueError as v:
        status_text.set(v)
    except Exception as e:
        status_text.set(e)

def quit():
    '''
    Function to end program after Tkinter window is closed
    '''
    root.quit()
    root.destroy()

#=============Tkinter root Window Creation=========================
root = Tk()
Tk().withdraw()
root.geometry("600x650+0+0")
root.title("Image Steganocryptography Implementation")
root.protocol("WM_DELETE_WINDOW", quit)
# Window Framing
Tops = Frame(root, width = 1000, relief = SUNKEN)
Tops.pack(side=TOP)
window = Frame(root, width = 1000, relief = SUNKEN)
window.pack(side=TOP)

#================Variable Declaration==============================
# Image File Path Variables
folder_path_plainfile = StringVar()
folder_path_coverfile1 = StringVar()
folder_path_coverfile2 = StringVar()
folder_path_stegofile = StringVar()
# Status Variable
status_text = StringVar()
# StegCrypt Object
SC = StegCrypt()

#=========================Time======================================
localtime=time.asctime(time.localtime(time.time()))

#=========================Labels======================================
# Heading
lblInfo = Label(Tops, font=('arial', 18, 'bold'), text="Image Steganocryptography\nImplementation",fg="Black")
lblInfo.grid(row=0,column=0)
lblInfo = Label(Tops, font=('arial', 8, 'bold', 'italic'),text=localtime, fg="Black")
lblInfo.grid(row=1,column=0)
# Encryption Subheading
lblInfo = Label(window, font=('arial', 15, 'bold'),text="\nEncryption and Image Hiding", fg="Black")
lblInfo.grid(row=2,column=0)
# Image Selection Labels
lblInfo = Label(window, font=('arial', 8, 'italic', 'bold'),text="\nAttach Plaintext Image file (.jpg)", fg="Steel Blue")
lblInfo.grid(row=3,column=0)
lblInfo = Label(window, font=('arial', 8, 'italic','bold'), text="\nAttach Covertext Image file (.jpg)", fg="Steel Blue")
lblInfo.grid(row=5,column=0)
# Decryption Subheading
lblInfo = Label(window, font=('arial', 15, 'bold'),text="\nDecryption", fg="Black")
lblInfo.grid(row=10,column=0)
# Image Selection Labels
lblInfo = Label(window, font=('arial', 8, 'italic', 'bold'),text="\nAttach Stegotext Image file (.jpg)", fg="Steel Blue")
lblInfo.grid(row=11,column=0)
lblInfo = Label(window, font=('arial', 8, 'italic','bold'), text="\nAttach Covertext Image file (.jpg)", fg="Steel Blue")
lblInfo.grid(row=13,column=0)
# Status Section label
lblInfo = Label(window, font=('arial', 8, 'bold'), text=" \n \nSTATUS", fg="Steel Blue")
lblInfo.grid(row=17,column=0)

#=========================Text Variable Display===================================
# Encryption Image Paths
txtDisplay = Entry(window, font=('arial',8),textvariable=folder_path_plainfile, bd=5,width =50, bg="white")
txtDisplay.grid(row=4,column=0)
textvariable=folder_path_plainfile.get()
txtDisplay = Entry(window, font=('arial',8),textvariable=folder_path_coverfile1, bd=5,width=50, bg="white")
txtDisplay.grid(row=6,column=0)
# Decryption Image Paths
txtDisplay = Entry(window, font=('arial',8),textvariable=folder_path_stegofile, bd=5,width =50, bg="white")
txtDisplay.grid(row=12,column=0)
textvariable=folder_path_plainfile.get()
txtDisplay = Entry(window, font=('arial',8),textvariable=folder_path_coverfile2, bd=5,width=50, bg="white")
txtDisplay.grid(row=14,column=0)
# Status Message
txtDisplay = Entry(window, font=('arial',8),textvariable=status_text, bd=5, width =50, bg="white")
txtDisplay.grid(row=18,column=0)

#=========================Buttons===================================
# Encryption Buttons
btnbrowseplaintxt=Button(window, padx=5,pady=5,bd=5,fg="black", font=('arial', 8,'bold'), text="Select Plaintext Image",bg ="brown", command=browse_button_plainfile).grid(row=4,column=1)
btnbrowsecovertxt1=Button(window, padx=5,pady=5,bd=5,fg="black", font=('arial', 8,'bold'), text="Select Covertext Image",bg ="brown", command=browse_button_coverfile1).grid(row=6,column=1)
btnEncr=Button(window, padx=5,pady=5,bd=5,fg="black", font=('arial', 12,'bold'), text="Encrypt",bg ="powder blue", command=btnEncrypt).grid(row=9,column=0)
# Decryption Buttons
btnbrowsestegotxt=Button(window, padx=5,pady=5,bd=5,fg="black", font=('arial', 8,'bold'), text="Select Stegotext Image",bg ="brown", command=browse_button_stegofile).grid(row=12,column=1)
btnbrowsecovertxt2=Button(window, padx=5,pady=5,bd=5,fg="black", font=('arial', 8,'bold'), text="Select Covertext Image",bg ="brown", command=browse_button_coverfile2).grid(row=14,column=1)
btnDecr=Button(window, padx=5,pady=5,bd=5,fg="black", font=('arial', 12,'bold'), text="Decrypt",bg ="powder blue", command=btnDecrypt).grid(row=15,column=0)

#=====================Start Main Loop==============================
root.mainloop()