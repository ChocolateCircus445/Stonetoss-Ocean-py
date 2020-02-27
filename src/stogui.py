from tkinter import messagebox
from tkinter import *
from PIL.Image import ANTIALIAS
import stocean, requests, random
from PIL import Image, ImageTk
from io import BytesIO
import pyperclip
from scrollimg import ScrollableImage
from scrollframe import ScrollFrame
from html import unescape


def imgFromURL(url):
    # Thanks to Andres Kull from StackOverflow
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img

def joinNS(list):
    s = ""
    for i in list:
        s += i
    return s

def splitNS(str):
    l = []
    for i in str:
        l.append(i)
    return l

def clear(frame):
    # Thank you, https://stackoverflow.com/users/1852928/tom-slick
    for widget in frame.winfo_children():
        widget.destroy()

# initialize
root = Tk()
root.title("Stonetoss Ocean")
root.geometry("800x710")
screen = 0
comicName = ""

def createLogo(frame):
    logoLoad = imgFromURL("https://raw.githubusercontent.com/ChocolateCircus445/Stonetoss-Ocean/master/logo.png")
    logoLoad = logoLoad.resize((175, 62), ANTIALIAS)  # logo too big, must resize
    logoRender = ImageTk.PhotoImage(logoLoad)
    logo = Label(root, image=logoRender)
    logo.image = logoRender
    logo.pack()

def createBtns(frame, comicobj):
    btnframe = Frame(frame)
    btnframe.pack()
    clb = Button(btnframe, text="Copy link", command=lambda: copyLink(comicobj.image))
    clb.pack(side=LEFT)
    ab = Button(btnframe, text="Go to Archives", command=gotoArchives)
    ab.pack(side=RIGHT)
    ib = Button(btnframe, text="Get info", command=lambda: displayInfo(comicobj))
    ib.pack(side=RIGHT)
    lb = Button(btnframe, text="See latest", command=displayLatest)
    lb.pack(side=RIGHT)


def copyLink(link):
    pyperclip.copy(link)
    messagebox.showinfo("Copied", "Link copied.")


def gotoArchives():
    global screen
    screen = 2
    clear(root)
    displayArchives()


def displayInfo(cm):
    messagebox.showinfo(cm.name, """
    Name: %s

    Description: %s

    Publish date: %s

    Alt text: %s
    """ % (cm.name, unescape(cm.description), cm.date, unescape(cm.alt)))


def displayLatest():
    # Clear the frame in case the user wants to go back to latest
    clear(root)

    # Load logo
    createLogo(root)

    cmc = stocean.grabLatest()

    # Display comic name
    cName = Label(root, text=cmc.name, font="Arial 30 bold")
    cName.pack()

    # Display buttons
    createBtns(root, cmc)

    # Display comic
    #comicImg = imgFromURL('https://i2.wp.com/stonetoss.com/wp-content/uploads/2019/02/boobs-butt-and-feet-comic.png')
    comicImg = imgFromURL(cmc.image)
    cwidth, cheight = comicImg.size
    cwidth //= 2
    cheight //= 2
    comicImg = comicImg.resize((cwidth, cheight), ANTIALIAS)  # logo too big, must resize
    comicRender = ImageTk.PhotoImage(comicImg)
    comicDisplay = ScrollableImage(root, image=comicRender, width=cwidth, height=cheight)
    comicDisplay.pack()


def displaySpecific(cname):
    try:
        # Clear the frame in case the user wants to go back to latest
        clear(root)

        # Load logo
        createLogo(root)

        cmc = stocean.grabSpecific(cname)

        # Display comic name
        cName = Label(root, text=cmc.name, font="Arial 30 bold")
        cName.pack()

        # Display buttons
        createBtns(root, cmc)

        # Display comic
        # comicImg = imgFromURL('https://i2.wp.com/stonetoss.com/wp-content/uploads/2019/02/boobs-butt-and-feet-comic.png')
        comicImg = imgFromURL(cmc.image)
        cwidth, cheight = comicImg.size
        cwidth //= 2
        cheight //= 2
        comicImg = comicImg.resize((cwidth, cheight), ANTIALIAS)  # logo too big, must resize
        comicRender = ImageTk.PhotoImage(comicImg)
        comicDisplay = ScrollableImage(root, image=comicRender, width=cwidth, height=cheight)
        comicDisplay.pack()
    except IndexError:
        clear(root)
        createLogo(root)
        etit = Label(root, text="This comic doesn't exist.", font="Arial 30 bold")
        etit.pack()
        hbtn = Button(root, text="Latest comic", command=displayLatest)
        hbtn.pack()

def randComic():
    displaySpecific(stocean.grabArchives()[random.randint(1, len(stocean.grabArchives())) - 1]['link'])

def displayArchives():
    clear(root)
    createLogo(root)
    l = Label(root, text="Archives", font="Arial 30 bold")
    l.pack()
    archs = stocean.grabArchives()[::-1]
    randButton = Button(root, text="Random", fg="blue", command=randComic)
    randButton.pack()
    archFrame = ScrollFrame(root)
    archFrame.pack(side="top", fill="both", expand=True)
    ttp = []
    for i in archs:
        n = i["name"]
        link = i["link"]
        chrs = splitNS(n)
        nchrs = []
        for j in chrs:
            if j == "\"":
                nchrs.append("\\" + j)
            else:
                nchrs.append(j)
        n = joinNS(nchrs)
        cbtn = eval("Button(archFrame.viewPort, text=\"" + n + "\", command=lambda: displaySpecific(\"" + link + "\"))")
        ttp.append(cbtn)
    for i in ttp:
        i.pack()



displayLatest()

root.mainloop()
