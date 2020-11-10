# PLEASE INSTALL REQUIRED MODULES/LIBRARIES (MENTIONED BELOW) FIRST FOR UNINTERRUPTED WOKRING.

import Listen_And_Speak as listenAndSpeak # importing Local file for speech recognition.
import Response  # importing local file to get the response
import tkinter
from tkinter import BooleanVar, Button, Entry, Frame, IntVar, Listbox, Menu, Scrollbar, Text, Toplevel, messagebox, Label, Checkbutton
from PIL import ImageTk, Image
import sqlite3 as sql
from datetime import datetime
import wikipedia
import nltk
from sys import platform
import sys
import re
import os.path
from tkinter.ttk import Combobox
sys.path.append('Project/Wikipedia Chatbot')

if not os.path.exists('msg_db.db'):
    con = sql.connect('msg_db.db')
    con.execute(""" CREATE TABLE "MsgStoreHistory" (
	"time"	TEXT,
	"sender"	TEXT NOT NULL,
	"message"	TEXT DEFAULT '',
	PRIMARY KEY("time")
    ) """) # this table is used for storing all chats (History).

    con.execute(""" CREATE TABLE "SignUpTable" (
	"emailAddress"	TEXT,
	"password"	TEXT NOT NULL,
	"keep_me_signed_in"	INTEGER DEFAULT 0,
	PRIMARY KEY("emailAddress")
    ) """) # this table stores the login details

# making sqlite3 connection to msg_db.db database.
con = sql.connect('msg_db.db')

# signUp window act as top most window in the project but it will shown only when a user have to sign up to start the conversation.
signUpWindow = tkinter.Tk()
signUpWindow.title('Sign Up')
signUpWindow.geometry("500x500")
signUpWindow.config(bg="#ccffcc")
signUpWindow.resizable(height=False, width=False)

# these are the global bariables.
userEmailAddress = None
stringToSpeak = None

# image for logo
logo_image = Image.open("images/Wikipedia Chatbot Logo.png")
logo_image = logo_image.resize((400, 200), Image.ANTIALIAS)
logo_image = ImageTk.PhotoImage(logo_image)

# image for the clear button   
clear_button_image = Image.open("images/clear.png")
clear_button_image = clear_button_image.resize((50, 47), Image.ANTIALIAS)
clear_button_image = ImageTk.PhotoImage(clear_button_image)

# image for the mic_button 
mic_button_image = Image.open("images/mic.png")
mic_button_image = mic_button_image.resize((50, 47), Image.ANTIALIAS)
mic_button_image = ImageTk.PhotoImage(mic_button_image)

# image for send button 
send_button_image = Image.open("images/send.png")
send_button_image = send_button_image.resize((50, 47), Image.ANTIALIAS)
send_button_image = ImageTk.PhotoImage(send_button_image)

# image for change password button
change_password_button_image = Image.open("images/change password.png")
change_password_button_image = change_password_button_image.resize((150, 50), Image.ANTIALIAS)
change_password_button_image = ImageTk.PhotoImage(change_password_button_image)

# image for signup button
sign_up_button_image = Image.open("images/signUp.png")
sign_up_button_image = sign_up_button_image.resize((150, 50), Image.ANTIALIAS)
sign_up_button_image = ImageTk.PhotoImage(sign_up_button_image)

# image for create account
create_account_button_image = Image.open("images/create-account.png")
create_account_button_image = create_account_button_image.resize((150, 50), Image.ANTIALIAS)
create_account_button_image = ImageTk.PhotoImage(create_account_button_image)

# image for show password
show_password = Image.open("images/show password.png")
show_password = show_password.resize((25, 25), Image.ANTIALIAS)
show_password = ImageTk.PhotoImage(show_password)

# image for not show password
not_show_password = Image.open("images/not show password.png")
not_show_password = not_show_password.resize((25, 25), Image.ANTIALIAS)
not_show_password = ImageTk.PhotoImage(not_show_password)

# main window. Opened only when user enter correct sign up details
def mainWindow():
    signUpWindow.withdraw()
    # inserts the given parameter to the database.

    # this temporary table is used to store the messages of the chat window.
    con.execute(""" CREATE TEMP TABLE "MsgStore" (
	                    "time"	TEXT,
                    	"sender"	TEXT NOT NULL,
	                    "message"	TEXT DEFAULT '',
	                    PRIMARY KEY("time") ) """)

    def insertIntoDatabase(table, sender, message):
        con.execute("""insert into {} values ("{}", "{}", "{}")""".format(table, datetime.now(), sender, message))
        con.commit()

    # disables the mic_button when user types anything in the EntryBox.
    def entryFocusInHandler(event=None):
        mic_button.config(state="disabled")

    # top level window for chatbot, but comes under signUpWindow
    root = Toplevel(signUpWindow)
    root.title("{} - Wikipedia Chatbot".format(userEmailAddress))
    root.geometry("1000x800")
    root.config(bg="#ccffcc")
    root.resizable(height=False, width=False)

    no_of_linesLabel = Label(root, text="No. of lines:", bg='#ccffcc')
    no_of_linesLabel.place(x=5, y=5)
    no_of_lines = IntVar()
    ComboBox = Combobox(root, textvariable=no_of_lines, width=5, justify='left')
    ComboBox['values']=(1,2,3,4,5)
    ComboBox.set(2)
    ComboBox.place(x=100, y=5)

    # listbox which displays the chats between the user and the bot.
    ChatBox = Listbox(root, height=36, width=96, background="#ccffcc", foreground="#446665", font=("Verdana", 12), borderwidth=5)
    ChatBox.place(x=5, y=30)

    # scrollbars for ChatBox.
    scrollbary = Scrollbar(root, command=ChatBox.yview)
    ChatBox['yscrollcommand'] = scrollbary.set
    scrollbary.place(x=980, y=30, height=690)
    scrollbary.config(bg="#ccffcc")
    #scrollbarx = Scrollbar(root, command=ChatBox.xview, orient="horizontal")
    #scrollbarx.config(bg="#ccffcc")
    #ChatBox['xscrollcommand'] = scrollbarx.set
    #scrollbarx.place(x=8, y=725, width=975)

    # used to switching focus. (This widget will no display on the screen)
    tempFrame = Frame(root, height=0, width=0)
    tempFrame.place(x=0, y=0)

    # EntryBox for user input.
    EntryBox = Entry(root, bd=0, bg="#ccffcc",
                     font="Arial", relief="ridge", borderwidth=5)
    EntryBox.place(x=68, y=740, height=55, width=810)
    EntryBox.bind("<Key>", entryFocusInHandler)

    # deletes all the entries of ChatBox. (Invokes when clearButton invokes).
    def clearButtonListener():
        answer = messagebox.askyesno("Clear", "Sure?")
        if answer == True:
            command = """ delete from MsgStore """
            con.execute(command)
            con.commit()
            ChatBox.delete(0, "end")
            messagebox.showinfo("Clear", "All chats has been cleared.")
        else:
            pass

    # clear button (Clear the chats from the chatbox and delete the chats from the MsgStore)
    clear_button = Button(root, image=clear_button_image, bg="#ccffcc", borderwidth=0, command=clearButtonListener)
    clear_button.place(x=8, y=740)

    # listens the user input when user clicks on mic_button. (Invokes when mic_button invokes)
    def micButtonListener():
        global stringToSpeak
        text = listenAndSpeak.takeUserSpeech()
        EntryBox.delete(0, "end")
        EntryBox.insert(0, text)
        sendButtonListener()
        listenAndSpeak.speak(stringToSpeak)
	    
    # mic button (When invkokes listens to user's speech)
    mic_button = Button(root, image=mic_button_image, bg="#ccffcc", borderwidth=0, padx=2, pady=2, command=micButtonListener)
    mic_button.place(x=935, y=740, height=50, width=60)
    mic_button.bind('')

    # send the user response for evaluation. (Invokes when send_button invokes and by micButtonListener)
    def sendButtonListener(event=None):
        EntryBox.bind("<Return>", lambda event: tempFrame.focus_set())
        userInput = EntryBox.get()
        if len(userInput) != 0:
            ChatBox.insert("end", "You: " + userInput)
            ChatBox.itemconfig('end', {'fg': 'blue'})
            root.update_idletasks()
            responseList = Response.getResponse(userInput, no_of_lines.get())
            ChatBox.insert("end", "Bot: " + responseList[0])
            ChatBox.itemconfig('end', {'fg': 'green'})
            ChatBox.config(foreground="#446665", font=("Verdana", 12))
            root.update_idletasks()
            signUpWindow.update_idletasks()
            for response in responseList[1:]:
                ChatBox.insert("end", "       " + response)
                ChatBox.itemconfig('end', {'fg': 'green'})
                ChatBox.config(foreground="#446665", font=("Verdana", 12))
                root.update_idletasks()
                signUpWindow.update_idletasks()
            root.update_idletasks()
            signUpWindow.update_idletasks()
            mic_button.config(state='active')
            response = "".join(responseList)
            insertIntoDatabase("MsgStore", userEmailAddress, userInput)
            insertIntoDatabase("MsgStoreHistory", userEmailAddress, userInput)
            insertIntoDatabase("MsgStore", "bot" + userEmailAddress, response)
            insertIntoDatabase("MsgStoreHistory", "bot" + userEmailAddress, response)
            EntryBox.delete(0, 'end')
            global stringToSpeak
            stringToSpeak = response
        else:
            return

    # send button (sends the message to the chatbox)        
    send_button = Button(root, image=send_button_image, bg="#ccffcc", borderwidth=0, command=sendButtonListener)
    root.bind('<Return>', sendButtonListener)
    send_button.place(x=880, y=740)

    # history tab. (Invokes when history option in invoke in menu bar)
    def historyTab():
        # window that shows history of all chats.
        historyWindow = Toplevel(root)
        root.withdraw()
        historyWindow.title("{} - History".format(userEmailAddress))
        historyWindow.geometry("1000x800")
        historyWindow.config(bg="#ccffcc")
        historyWindow.resizable(height=False, width=False)

        historyList = Listbox(historyWindow, height=37, width=96, bg="#ccffcc", foreground="#446665", font=("Verdana", 12), borderwidth=5, )
        historyList.place(x=10, y=10)

        def returnList(text):
            responseList = []
            i = 0
            while i < len(text):
                if len(text) - i > 87:
                    responseList.append(text[i:i + 87] + '-')
                    i = i + 87
                else:
                    responseList.append(text[i:])
                    break
            return responseList

        scrollbary = Scrollbar(historyWindow, command=historyList.yview)
        historyList['yscrollcommand'] = scrollbary.set
        scrollbary.place(x=985, y=10, height=720)
        scrollbary.config(bg="#ccffcc")

        #scrollbarx = Scrollbar(historyWindow, command=historyList.xview, orient="horizontal")
        #historyList['xscrollcommand'] = scrollbarx.set
        #scrollbarx.place(x=10, y=725, width=980)
        #scrollbarx.config(bg="#ccffcc")

        mycursor = con.execute(""" select * from MsgStoreHistory """)
        histories = mycursor.fetchall()
        i = 1
        try:
            dateTime = str(histories[0][0])
            date = dateTime[:10]
            historyList.insert(i, date)
            historyList.itemconfig(i-1, {'fg': 'red'})
            i += 1
            for chats in histories:
                chatsDateTime = str(chats[0])
                chatsDate = chatsDateTime[:10]
                chatsTime = chatsDateTime[11:]
                if chatsDate != date:
                    historyList.insert(i, " ")
                    i += 1
                    date = chatsDate
                    historyList.insert(i, date)
                    historyList.itemconfig(i-1, {'fg': 'red'})
                    i += 1
                else:
                    pass
                if chats[1] == userEmailAddress:
                    textList = returnList(chats[2])
                    historyList.insert("end", chatsTime + " : You: " + textList[0])
                    historyList.itemconfig("end", {'fg': 'blue'})
                    for response in textList[1:]:
                        historyList.insert("end", "                            " + response)
                        historyList.itemconfig("end", {'fg': 'blue'})
                    i += 1
                elif chats[1] == "bot" + userEmailAddress:
                    textList = returnList(chats[2])
                    historyList.insert("end", chatsTime + " : Bot: " + textList[0])
                    historyList.itemconfig("end", {'fg': 'green'})
                    for response in textList[1:]:
                        historyList.insert("end", "                                 " + response)
                        historyList.itemconfig("end", {'fg': 'green'})
                    i += 1
        except IndexError:
            pass

        # calls when user invokes clear button
        def clearButtonListener():
            answer = messagebox.askyesno("Clear", "Sure?")
            if answer == True:
                con.execute(""" delete from MsgStoreHistory where sender in ("{}", "{}") """.format(userEmailAddress,'bot' + userEmailAddress))
                con.commit()
                historyList.delete(0, "end")
                messagebox.showinfo("Clear", "All the chat history has been deleted.")
            else:
                pass

        # loading and using clear button image
        clearButton = Button(
            historyWindow, image=clear_button_image, bg="#ccffcc", borderwidth=0, command=clearButtonListener)
        clearButton.place(x=8, y=740)

        # exports the chats to a file appended with current time. (Invokes when 'export chats history' invoke in menu bar of this particular window.)
        def exportChats():
            timestr = str(datetime.now())
            textFile = open("Histories/{}_chatHistories_{}.txt".format(userEmailAddress, '_'.join([timestr[:4], timestr[5:7], timestr[8:10], timestr[11:13], timestr[14:16], timestr[17:19]])), 'w')
            mycursor = con.execute(""" select * from MsgStoreHistory """)
            messages = mycursor.fetchall()
            for message in messages:
                if message[1] == userEmailAddress:
                    textFile.write(str(message[0]) + " => You:" + message[2] + '\n')
                elif message[1] == 'bot' + userEmailAddress:
                    textFile.write(str(message[0]) + " => Bot:" + message[2] + '\n')
            textFile.close()
            messagebox.showinfo("Export", """ Chats has been exported to "{}_chatsHistory_{}.txt" file """.format(userEmailAddress, '_'.join([timestr[:4], timestr[5:7], timestr[8:10], timestr[11:13], timestr[14:16], timestr[17:19]])))

        # calks when user exits from the history window.
        def exitWindow():
            root.deiconify()
            historyWindow.withdraw()

        # menu bar for history window
        menubar = Menu(historyWindow, bg="#ccffcc")
        options = Menu(menubar, tearoff=0, bg="#ccffcc")
        menubar.add_cascade(label="Options", menu=options)
        options.add_command(label="Export Chat History", command=exportChats)
        options.add_separator()
        options.add_command(label="Exit", command=exitWindow)
        historyWindow.config(menu=menubar)

        historyWindow.protocol("WM_DELETE_WINDOW", exitWindow)

    # exports chats to a file appended with current time. (Invokes when 'exports chats' invokes in menubar of root.)
    def exportChats():
        time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        textFile = open("Chats/{}_chats_{}.txt".format(userEmailAddress, time), 'w')
        mycursor = con.execute(""" select * from MsgStoreHistory """)
        messages = mycursor.fetchall()
        for message in messages:
            if message[1] == userEmailAddress:
                textFile.write(str(message[0]) + " => You:" + message[2] + '\n')
            elif message[1] == 'bot' + userEmailAddress:
                textFile.write(str(message[0]) + " => Bot:" + message[2] + '\n')
        textFile.close()
        messagebox.showinfo("Export", """ Chats has been exported to "{}_chats_{}.txt" file """.format(userEmailAddress, time))

    # calls when sign out invokes
    def signout():
        answer = messagebox.askyesno("Sign Out", "Sure?")
        if answer == True:
            con.execute(""" update SignUpTable set keep_me_signed_in = 0  where emailAddress = "{}" """.format(userEmailAddress))
            con.commit()
            root.withdraw()
            signUpWindow.deiconify()
            con.execute(""" drop table MsgStore """)
            con.commit()
        else:
            pass

    # invokes when click on change password from menu bar
    def changePassword():
        
        # window for changing password.
        changePasswordWindow = Toplevel(signUpWindow)
        root.withdraw()
        changePasswordWindow.title("Change Password")
        changePasswordWindow.geometry("500x500")
        changePasswordWindow.config(bg="#ccffcc")
        changePasswordWindow.resizable(height=False, width=False)

        # loading and using logo image
        logo = Label(changePasswordWindow, image=logo_image, bg='#ccffcc')
        logo.place(x=50, y=10)

        # old password label and entry box.
        oldPasswordLabel= Label(changePasswordWindow, text='Old Password', bg='#ccffcc')
        oldPasswordLabel.place(x=80, y=250)
        oldPasswordEntryBox = Entry(changePasswordWindow, show='*')
        oldPasswordEntryBox.place(x=250, y=250)

        # new password label and entry box.
        newPasswordLabel = Label(changePasswordWindow, text='Password', bg='#ccffcc')
        newPasswordLabel.place(x=80, y=290)
        newPasswordEntryBox = Entry(changePasswordWindow, show='*')
        newPasswordEntryBox.place(x=250, y=290)

        # confirn new password label and entry box.
        confirmNewPasswordLabel = Label(changePasswordWindow, text='Confirm Password', bg='#ccffcc')
        confirmNewPasswordLabel.place(x=80, y=330)
        confirmNewPasswordEntryBox = Entry(changePasswordWindow, show='*')
        confirmNewPasswordEntryBox.place(x=250, y=330)

        # calls when user invokes chnage password button
        def changePasswordButtonListenener(event=None):
            mycursor = con.execute(""" select password from SignUpTable where emailAddress = "{}" """.format(userEmailAddress))
            password = mycursor.fetchall()[0][0]
            if password == oldPasswordEntryBox.get():
                if newPasswordEntryBox.get() == confirmNewPasswordEntryBox.get():
                    con.execute(""" update SignUpTable set password = "{}" where emailAddress = "{}" """.format(newPasswordEntryBox.get(), userEmailAddress))
                    con.commit()
                    messagebox.showinfo(title="Password", message='Password has been changed.')   
                    oldPasswordEntryBox.delete(0, 'end') 
                    newPasswordEntryBox.delete(0, 'end') 
                    confirmNewPasswordEntryBox.delete(0, 'end') 
                    changePasswordWindow.withdraw()
                    root.deiconify()
                else:
                    messagebox.showerror(title="Error", message='New password should be same as confirm password.')    
            else:
                messagebox.showerror(title="Error", message='Wrong old password.')

        # loading and using chnage password image
        change_password_button = Button(changePasswordWindow, image=change_password_button_image, command=changePasswordButtonListenener, borderwidth=0)
        change_password_button.place(x=180, y=400)
        changePasswordWindow.bind('<Return>', changePasswordButtonListenener)

        # calls when user exits from the chnage password window.
        def on_closing():
            changePasswordWindow.withdraw()
            root.deiconify()

        changePasswordWindow.protocol("WM_DELETE_WINDOW", on_closing)

    # deletes the current user and all the chats.
    def deleteAccount():
        answer = messagebox.askyesno("Delete", "Sure?")
        if answer == True:
            con.execute(""" delete from SignUpTable where emailAddress = "{}" """.format(userEmailAddress))
            con.execute(""" delete from MsgStoreHistory where sender in ("{}", "{}") """.format(userEmailAddress, 'bot' + userEmailAddress))
            con.commit()
            messagebox.showinfo(title="Delete",message="Account has been deleted.")
            root.withdraw()
            signUpWindow.deiconify()
            con.execute(""" drop table MsgStore """)
            con.commit()
        else:
            pass

    # menu bar for chat window
    menubar = Menu(root, bg="#000000")
    options = Menu(menubar, tearoff=0, bg="#ccffcc")
    menubar.add_cascade(label="Options", menu=options)
    options.add_command(label="History", command=historyTab)
    options.add_separator()
    options.add_command(label="Export Chats.", command=exportChats)
    options.add_separator()
    options.add_command(label="Change Password", command=changePassword)
    options.add_command(label="Delete Account", command=deleteAccount)
    options.add_separator()
    options.add_command(label="Sign Out", command=signout)
    root.config(menu=menubar)

    # calls when user exits from the chat window.
    def on_closing():
        root.withdraw()
        signUpWindow.destroy()
        con.execute(""" drop table MsgStore """)
        con.commit()

    root.protocol("WM_DELETE_WINDOW", on_closing)

# loading and using logo image
logo = Label(signUpWindow, image=logo_image, bg='#ccffcc')
logo.place(x=50, y=10)

# label and entry box for email
emailLabel = Label(signUpWindow, text='Email', bg='#ccffcc')
emailLabel.place(x=100, y=250)
emailEntryBox = Entry(signUpWindow, width=30)
emailEntryBox.place(x=200, y=250)
    
# label and entry box for password.
passwordLabel = Label(signUpWindow, text='Password', bg='#ccffcc')
passwordLabel.place(x=100, y=280)
passwordEntryBox = Entry(signUpWindow, show='*', width=30)
passwordEntryBox.place(x=200, y=280)

# checkbox for keep me signed .
keep_me_signed = BooleanVar()
keep_me_signed_checkBox = Checkbutton(signUpWindow, text='Keep me signed up.', variable=keep_me_signed, onvalue=True, offvalue=False, bg='#ccffcc')
keep_me_signed_checkBox.place(x=100, y=325)

showPassword = False

password = Button(signUpWindow)
def passwordHandler():
    global showPassword
    if showPassword == False:
       password.config(image=show_password)
       showPassword = True
       passwordEntryBox.config(show='')
    else:
        password.config(image=not_show_password)
        showPassword = False
        passwordEntryBox.config(show='*')

password.config(image=not_show_password, command=passwordHandler, bg='#ccffcc', borderwidth=0)
    

# button for show password.

password.place(x=400, y=277)

# for validating an Email 
def isValidEmail(email):  
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if(re.search(regex,email)):  
        return True  
    else:  
        return False


# calls when user invkoes the signup button.
def signUpButtonListener(event=None):
    if emailEntryBox.get() != '' and passwordEntryBox.get() != '':
        if isValidEmail(emailEntryBox.get()):
            global userEmailAddress
            userEmailAddress = emailEntryBox.get()
            mycursor = con.execute(""" select password from SignUpTable where emailAddress = "{}" """.format(userEmailAddress))
            password = None
            try:
                password = mycursor.fetchall()[0][0]
            except IndexError:
                messagebox.showerror(title="Error", message='User not exists.')
                return
            if keep_me_signed.get() == True:
                con.execute(""" update SignUpTable set keep_me_signed_in = 1 where emailAddress = "{}" """.format(userEmailAddress))
                con.commit()
            if password == passwordEntryBox.get():
                mainWindow()
            else:
                messagebox.showerror(title="Error", message='Wrong Password. Please try again.')
            emailEntryBox.delete(0, 'end')
            passwordEntryBox.delete(0, 'end')
        else:
            messagebox.showerror(title='Error', message='Invalid Email Address.')
    else:
        messagebox.showerror(title='Error', message='Empty Input Fields.')

# loading and using sign up image for sign up button.
sign_up_button = Button(image=sign_up_button_image,command=signUpButtonListener, bg='#ccffcc', borderwidth=0)
sign_up_button.place(x=80, y=375)
signUpWindow.bind('<Return>', signUpButtonListener)

# calls when user invokes create account button.
def createAccountButtonListener():
    # window for creating account.
    createAccountWindow = Toplevel(signUpWindow)
    createAccountWindow.title("Create Account")
    createAccountWindow.geometry("500x500")
    createAccountWindow.config(bg="#ccffcc")
    createAccountWindow.resizable(height=False, width=False)
    signUpWindow.withdraw()

    # loading and using logo image.
    logo = Label(createAccountWindow, image=logo_image, bg='#ccffcc')
    logo.place(x=50, y=10)

    # label and entry box for email
    emailLabel = Label(createAccountWindow, text='Email', bg='#ccffcc')
    emailLabel.place(x=80, y=250)
    emailEntryBox = Entry(createAccountWindow, width=30)
    emailEntryBox.place(x=250, y=250)

    # label and entry box for password.
    passwordLabel = Label(createAccountWindow, text='Password', bg='#ccffcc')
    passwordLabel.place(x=80, y=280)
    passwordEntryBox = Entry(createAccountWindow, show='*', width=30)
    passwordEntryBox.place(x=250, y=280)

    # confirn new password label and entry box.
    confirmPasswordLabel = Label(createAccountWindow, text='Confirm Password', bg='#ccffcc')
    confirmPasswordLabel.place(x=80, y=310)
    confirmPasswordEntryBox = Entry(createAccountWindow, show='*', width=30)
    confirmPasswordEntryBox.place(x=250, y=310)

    # calls when user invokes create account button of this window.
    def createAccount(event=None):
        try:
            if emailEntryBox.get() != '' and passwordEntryBox.get() != '':
                if isValidEmail(emailEntryBox.get()):
                    if passwordEntryBox.get() == confirmPasswordEntryBox.get():
                        con.execute(""" insert into SignUpTable  values("{}", "{}", 0) """.format(emailEntryBox.get(), passwordEntryBox.get()))
                        con.commit()
                        messagebox.showinfo(title='Account', message='Account has been created.')
                        emailEntryBox.delete(0, 'end')
                        passwordEntryBox.delete(0, 'end')
                        createAccountWindow.withdraw()
                        signUpWindow.deiconify()
                    else:
                        messagebox.showerror(title="Error", message='Password should be same as confirm password.')    
                else:
                    messagebox.showerror(title='Error', message='Invalid Email Address.')        
            else:
                messagebox.showerror(title='Error', message='Empty Input Fields.')    
        except Exception:
            messagebox.showerror(title='Error', message='User Already Existed.')

    # loading and using create account image for create account button.
    create_account_button = Button(createAccountWindow, image=create_account_button_image, command=createAccount, borderwidth=0)
    create_account_button.place(x=180, y=370)
    createAccountWindow.bind('<Return>', createAccount)

    # calls when user exits from the create account window.
    def on_closing():
        createAccountWindow.withdraw()
        signUpWindow.deiconify()

    createAccountWindow.protocol("WM_DELETE_WINDOW", on_closing)


# loading and using create accout image for create account button.
create_account_button = Button(image=create_account_button_image, command=createAccountButtonListener, borderwidth=0)
create_account_button.place(x=250, y=375)

# functionality for keep me signed in.
mycursor = con.execute(""" select emailAddress from SignUpTable where keep_me_signed_in = 1 """)
emails = mycursor.fetchall()
if emails != []:
    userEmailAddress = emails[0][0]
    mainWindow()

signUpWindow.mainloop()
