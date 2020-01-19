import hashlib, shutil, os
import webbrowser, emoji, random
from datetime import datetime
from time import sleep
from tkinter import *
from tkinter import Frame, Tk, BOTH, Text, Menu, END, filedialog, messagebox
from functools import partial

import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image, ImageTk

root = Tk()
canvas = Canvas(root)
canvas.grid(row=1920, column=1080)

path = "D:\\Programs\\Official\\studentDB\\images"
image_list = os.listdir(path)
image_list.pop()
im = Image.open(os.path.join(path, image_list[random.randint(0, len(image_list))]))

def bg():
    im.thumbnail((1800, 900), Image.ANTIALIAS)
    render = ImageTk.PhotoImage(im)
    img = Label(image=render)
    img.image = render
    img.grid(row=0, column=0)
bg()

proof = []
pos = IntVar()

def backup():
    reset_canvas()
    def compress():
        import os
        import zipfile

        os.system("mkdir DB_backup")
        dirs = os.listdir("D:\\Programs\\Official\\studentDB\\DB")
        for dir in dirs:
            zf = zipfile.ZipFile(f"DB_backup\\{dir}.zip", "w")
            for dirname, subdirs, files in os.walk("D:\\Programs\\Official\\studentDB\\DB"):
                zf.write(dirname)
                for filename in files:
                    zf.write(os.path.join(dirname, filename))
            zf.close()

    def drive():
        from pydrive.auth import GoogleAuth
        from pydrive.drive import GoogleDrive
        import os

        compress()
        messagebox.showinfo("Backup instruction",
                            "Now you will be redirected to google authenticationpage, \nplease allow acces to the app so that your Ddatabase will be\nuploaded in your google drive")
        g_login = GoogleAuth()
        g_login.LocalWebserverAuth()
        drive = GoogleDrive(g_login)

        try:
            with open("studentDB.csv", 'r') as f:
                file_drive = drive.CreateFile({'title': 'studentDB.csv'})
                file_drive.SetContentString(f.read())
                file_drive.Upload()
                messagebox.showinfo("Success", "Upload compleated successfully!")
        except:
            messagebox.showerror("Error", "Something went wrong..")
    Label(root, text="For better protection backup in google drive.").grid(row=0, column=0)
    Button(root, text="Drive Backup", fg="green", command=drive).grid(row=1, column=0)
    Button(root, text="Local Backup", fg="blue", command=compress).grid(row=2, column=0)


def call_proof():
    global row, path, f, proof
    row += 1
    fileType = [('Image file', '*.jpg')]
    dBox = filedialog.Open(filetypes=fileType)
    path = dBox.show()
    proof.append(path)
    im = Image.open(path)
    im.thumbnail((128,128), Image.ANTIALIAS)
    render = ImageTk.PhotoImage(im)
    img = Label(image=render)
    img.image = render
    img.grid(row=4, column=row-2)

    Label(root, text=f"Proof{row - 6} loaded: {path.split('/')[-1]}") \
        .grid(row=row, column=6)

def reset_canvas(*op):
    global canvas, root
    # canvas.destroy()
    # canvas = Canvas(root, width=600, height=600)
    li = []
    for widget in root.winfo_children():
        a = str(widget)
        if a == '.!menu':
            pass
        else:
            widget.destroy()
    try:
        if op[0] == "back":
            print("hi")
            bg()
    except IndexError:
        pass

def store(Fname, Lname, phone, D, M, Y, a, g):
    global proof
    index = 0
    fn = Fname.get()
    ln = Lname.get()
    p = phone.get()
    d = D.get()
    m = M.get()
    y = Y.get()
    add = a.get("1.0", END)
    gen = g.get()
    if fn=="" or ln=="" or p=="" or d=="" or m=="" or y=="" or add=="" or gen == "" or len(proof) > 3:
        messagebox.showerror("Error", "Fill every boxes to continue.")
        return
    if gen == 1:
        gen = "Male"
    elif gen == 2:
        gen = "Female"
    else:
        gen = "Unselected"
    all = fn + ln + str(d) + str(m) + str(y) + add + gen
    destiny = hashlib.sha3_512(all.encode()).hexdigest()

    data = []
    data.append(fn)
    data.append(ln)
    data.append(p)
    data.append(f"{d}/{m}/{y}")
    data.append(str(datetime.now().strftime("%D")))
    data.append(f"\"{add}\"")
    data[-1] = data[-1].split('\n')[0] + "\""
    data.append(gen)
    for i in proof:
        data.append(f"DB/{destiny}/proof{proof.index(i)+1}.{i.split('.')[-1]}")
    data.append(destiny)

    try:
        f = open("studentDB.csv", 'r')
        li = f.readlines()
        if li[0] != "First Name,Last Name,Phone,DOB, Join date, Address,Gender,Proof1,Proof2,Proof3,Hash\n":
            print("heuy")
            f = open("studentDB.csv", 'w')
            f.write("First Name,Last Name,Phone,DOB, Join date, Address,Gender,Proof1,Proof2,Proof3,Hash\n")
            f.close()
    except FileNotFoundError:
        f = open("studentDB.csv", 'w+')
        f.write("First Name,Last Name,Phone,DOB, Join date, Address,Gender,Proof1,Proof2,Proof3,Hash\n")

    f = open("studentDB.csv", 'a')
    for i in data:
        comma = ','
        if data[-1] == i:
            comma = ''
        f.write(i + comma)
    f.write('\n')
    f.close()

    os.system("mkdir DB")
    os.system(f"mkdir {os.path.join('DB', destiny)}")
    for i in proof:
        shutil.copy(i, os.path.join('DB', destiny))
    for i in proof:
        os.rename(f"{os.path.join('DB', destiny, i.split('/')[-1])}", f"DB/{destiny}/proof{proof.index(i)+1}.{i.split('.')[-1]}")

    data.clear()
    proof.clear()
    messagebox.showinfo("Success", "Member added")
    reset_canvas()


def add_member_gui():
    reset_canvas()
    global row, hash_destiny, f, entry_Fname, pos
    row = 6
    hash_destiny = ""
    path = ""
    entry_post_status = DISABLED
    gender_state = 3
    entry_Fname = StringVar()
    entry_Lname = StringVar()
    entry_address = StringVar()
    spin_D = IntVar()
    spin_M = IntVar()
    spin_Y = IntVar()
    gender_state = IntVar()

    if pos.get() == 1:
        entry_post_status = DISABLED
        root.title("Add student")
    elif pos.get() == 2:
        entry_post_status = NORMAL
        root.title("Add staff")
    else:
        messagebox.showerror("Error", "Select an option to continue.")
        return

    Fname = Label(root, text="First Name: ").grid(row=0, column=0)
    entry_Fname = Entry(root)
    entry_Fname.grid(row=0, column=1)
    Lname = Label(root, text="Last Name: ").grid(row=1, column=0)
    entry_Lname = Entry(root)
    entry_Lname.grid(row=1, column=1)
    phone = Label(root, text="Phone").grid(row=2, column=0, sticky=W)
    entry_phone = Entry(root)
    entry_phone.grid(row=2, column=1)
    DOB = Label(root, text="DOB: ").grid(row=3, column=0, sticky=W)
    spin_D = Spinbox(root, from_=1, to=31)
    spin_D.grid(row=3, column=1)
    spin_M = Spinbox(root, from_=1, to=12)
    spin_M.grid(row=3, column=2)
    spin_Y = Spinbox(root, from_=1980, to=datetime.today().year)
    spin_Y.grid(row=3, column=3)
    address = Label(root, text="Address:").grid(row=4, column=0, sticky=W)
    entry_address = Text(root, height=5, width=16)
    entry_address.grid(row=4, column=1)
    post = Label(root, text="Post: ").grid(row=5, column=0)
    entry_post = Entry(root, state=entry_post_status)
    entry_post.grid(row=5, column=1)
    gender = Label(root, text="Gender: ").grid(row=6, column=0)
    m = Radiobutton(root, text="Male", variable=gender_state, value=1)
    m.grid(row=7, column=1)
    Radiobutton(root, text="Female", variable=gender_state, value=2) \
        .grid(row=8, column=1)
    Radiobutton(root, text="Unselected", variable=gender_state, value=3) \
        .grid(row=9, column=1)
    Button(root, text="Proof1", command=call_proof).grid(row=6, column=5)
    Button(root, text="Proof2", command=call_proof).grid(row=6, column=6)
    Button(root, text="Proof3", command=call_proof).grid(row=6, column=7)
    call = partial(store, entry_Fname, entry_Lname, entry_phone, spin_D, spin_M, spin_Y,\
                   entry_address, gender_state)
    Button(root, text="Add Member", command=call).grid(row=10, column=3)

def add_member():
    reset_canvas()
    Label(root, text="Select a option: ").grid(row=0, column=0)
    Radiobutton(root, text="Student", variable=pos, value=1).grid(row=1, column=1)
    Radiobutton(root, text="Staff", variable=pos, value=2).grid(row=2, column=1)
    Button(root, text="Add member", bg='green', command=add_member_gui).grid(row=3, column=4)

def search():
    reset_canvas()

def openDB():
    reset_canvas()
    df = pd.read_csv("studentDB.csv")
    Label(root, text=df).grid(row=0, column=0)

def edit():
    reset_canvas()
    def delete_entry(entry):
        entry = entry.get()
        entry += 1
        df = pd.read_csv("studentDB.csv")
        entry_hash = df.iloc[entry,-1]
        print(entry_hash)
        file = open("studentDB.csv", 'r')
        lines = file.readlines()
        file.close()
        temp = lines.pop(entry)
        deleted_member = temp.split(',')[0] + " "
        deleted_member += temp.split(',')[1]
        file = open("studentDB.csv", 'w')
        for line in lines:
            file.write(line)
        file.close()
        os.system(f"RD /S /Q D:\\Programs\\Official\\studentDB\\DB\\{entry_hash}")
        messagebox.showinfo("Entry removed", f"The member you requested to delete '{deleted_member}' has removed successfully")


    def edit_entry(entry):
        pass

    df = pd.read_csv("studentDB.csv")
    pd.set_option('display.max_columns',15)
    pd.set_option('display.width', 300)
    df = df.drop(["Proof1", "Proof2", "Proof3"], axis=1)
    entry = IntVar()
    for i in range(df.shape[0]):
        if i == 0:
            state = True
            # Label(root, text="-" * 300).grid(row=i, column=0)
        else:
            state = False
            # Label(root, text="-"*300).grid(row=i+1, column=0)
            Radiobutton(root, text=df.iloc[[i]].to_string(header=state), variable=entry, value=i).grid(row=i, column=0)
            # to be developed
            # if i%10 != :
                # reset_canvas()

        """for j in range(df.shape[1]):
            Label(root, text=df.iloc[:,:]).grid(row=0, column=0)
            # Checkbutton(root, text=df.iloc[i, j]).grid(row=i, column=j+1)"""
    call_dell = partial(delete_entry, entry)
    call_edit = partial(edit_entry, entry)
    Button(root, text="Delete Entry", command=call_dell).grid(row=df.shape[0] + 1, column=0)
    Button(root, text="Edit Entry", command=call_edit).grid(row=df.shape[0] + 2, column=0)


def graph():
    reset_canvas()
    df = pd.read_csv("studentDB.csv")
    # working on this feature
    """plt.broken_barh(avg, persons)
    plt.savefig("fig.png")
    im = Image.open("fig.png")
    im.thumbnail((640, 640), Image.ANTIALIAS)
    render = ImageTk.PhotoImage(im)
    img = Label(image=render)
    img.image = render
    img.grid(row=0, column=0)"""

def back():
    reset_canvas("back")
    Label(root, text="-"*20 + "\n Select something from the File menu \n" + "-"*20).grid(row=0, column=0)


def about():
    reset_canvas()
    def git():
        webbrowser.open("https://github.com/hiruthic2002/Tkinter-DB-Manager")
    def insta():
        webbrowser.open("https://www.instagram.com/hiruthicsha/")
    def tweet():
        webbrowser.open("https://twitter.com/Hiruthic1")

    Label(root, text=f"""This software is open source and is under development mode..If you
    are facing any issues with the software contact immidiately to the 
    author and file your problem. 
    
    Feel free to give feed back in our github repo...and also think about donating us {emoji.emojize(":grinning_face_with_big_eyes:")}
    
    Contact:""").grid(row=0, column=0)
    Button(root, text="Github", command=git, width=10, fg="blue", bg="black").grid(row=5, column=0)
    Button(root, text="Instagram", command=insta, width=10, fg="blue", bg="black").grid(row=6, column=0)
    Button(root, text="Twitter", command=tweet, width=10, fg="blue", bg="black").grid(row=7, column=0)
    Label(root, text="Mail: hiruthic@karunya.edu.in").grid(row=8, column=0)
    Label(root, text="Phone: 9360843817").grid(row=9, column=0)


# menu
menu = Menu(root)
root.config(menu=menu)
fileMenu = Menu(menu)
aboutMenu = Menu(menu)
menu.add_cascade(label="File", menu=fileMenu)
fileMenu.add_command(label="Add member", command=add_member)
# fileMenu.add_command(label="Search", command=search)
fileMenu.add_command(label="Graph it", command=graph)
fileMenu.add_command(label="Edit", command=edit)
fileMenu.add_command(label="Go back", command=back)
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=root.quit)
menu.add_cascade(label="Help", menu=aboutMenu)
aboutMenu.add_command(label="About", command=about)
aboutMenu.add_command(label="Backup", command=backup)
# aboutMenu.add_separator()
# aboutMenu.add_command(label="Developer mode", command=developer)
root.mainloop()

