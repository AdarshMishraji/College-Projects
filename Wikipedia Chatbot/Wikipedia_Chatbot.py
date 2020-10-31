# PLEASE INSTALL REQUIRED MODULES/LIBRARIES (MENTIONED BELOW) FIRST FOR UNINTERRUPTED WOKRING.

import Listen_And_Speak as listenAndSpeak # importing Local file for speech recognition.
import Response  # importing local file to get the response
import tkinter
from tkinter import BooleanVar, Button, Entry, Frame, IntVar, Listbox, Menu, Scrollbar, Text, Toplevel, messagebox, Label, Checkbutton
from PIL import ImageTk, Image
import mysql.connector as mycon
from datetime import datetime
import wikipedia
import nltk
from sys import platform
import sys
sys.path.append('Project/Wikipedia Chatbot')

# establish mysql connection. (BEFORE RUNNING THIS FILE. PLEASE RUN "msg_db.py" FILE)
msg_db = mycon.connect(user="ENTER YOUR USERNAME", password="ENTER YOUR PASSWORD",
                       database="ENTER YOUR DATABASE NAME", host="localhost")  # enter your database name and password to access it.
mycursor = msg_db.cursor()

# signUp window act as top most window in the project but it will shown only when a user have to sign up to start the conversation.
signUpWindow = tkinter.Tk()
signUpWindow.title('Login')
signUpWindow.geometry("500x500")
signUpWindow.config(bg="white")
signUpWindow.resizable(height=False, width=False)

# these are the global bariables.
userEmailAddress = None
stringToSpeak = None

# image for logo
logo_image = Image.open("Project/Wikipedia Chatbot/images/Wikipedia Chatbot Logo.png")
logo_image = logo_image.resize((400, 200), Image.ANTIALIAS)
logo_image = ImageTk.PhotoImage(logo_image)

# image for the clear button   
clear_button_image = Image.open("Project/Wikipedia Chatbot/images/clear.png")
clear_button_image = clear_button_image.resize((50, 47), Image.ANTIALIAS)
clear_button_image = ImageTk.PhotoImage(clear_button_image)

# image for the mic_button 
mic_button_image = Image.open("Project/Wikipedia Chatbot/images/mic.png")
mic_button_image = mic_button_image.resize((50, 47), Image.ANTIALIAS)
mic_button_image = ImageTk.PhotoImage(mic_button_image)

# image for send button 
send_button_image = Image.open("Project/Wikipedia Chatbot/images/send.png")
send_button_image = send_button_image.resize((50, 47), Image.ANTIALIAS)
send_button_image = ImageTk.PhotoImage(send_button_image)

# image for change password button
change_password_button_image = Image.open("Project/Wikipedia Chatbot/images/change password.png")
change_password_button_image = change_password_button_image.resize((150, 50), Image.ANTIALIAS)
change_password_button_image = ImageTk.PhotoImage(change_password_button_image)

# image for signup button
sign_up_button_image = Image.open("Project/Wikipedia Chatbot/images/signUp.png")
sign_up_button_image = sign_up_button_image.resize((150, 50), Image.ANTIALIAS)
sign_up_button_image = ImageTk.PhotoImage(sign_up_button_image)

# image for create account
create_account_button_image = Image.open(
    "Project/Wikipedia Chatbot/images/create-account.png")
create_account_button_image = create_account_button_image.resize(
    (150, 50), Image.ANTIALIAS)
create_account_button_image = ImageTk.PhotoImage(create_account_button_image)

# main window. Opened only when user enter correct sign up details
def mainWindow():
    signUpWindow.withdraw()
    # inserts the given parameter to the database.

    def insertIntoDatabase(table, sender, message):
        mycursor.execute("""insert into {} (date, sender, message) value(now(3), "{}", "{}")""".format(
            table, sender, message))
        msg_db.commit()

    # disables the mic_button when user types anything in the EntryBox.
    def entryFocusInHandler(event=None):
        mic_button.config(state="disabled")

    # top level window for chatbot, but comes under signUpWindow
    root = Toplevel(signUpWindow)
    root.title("{} - Wikipedia Chatbot".format(userEmailAddress))
    root.geometry("1000x800")
    root.config(bg="white")
    root.resizable(height=False, width=False)

    # listbox which displays the chats between the user and the bot.
    ChatBox = Listbox(root, height=35, width=96,
                      foreground="#446665", font=("Verdana", 12), borderwidth=5)
    ChatBox.place(x=5, y=5)

    # for the initial purpose.
    initialMsg = "Hi there, I am Wikibot. You can ask me anything. Tell me, what you want to search?"
    mycursor.execute("""delete from MsgStore""")
    msg_db.commit()
    ChatBox.insert("end", "Bot: " + initialMsg)
    ChatBox.itemconfig('end', {'fg': 'green'})
    insertIntoDatabase("MsgStore", "bot" + userEmailAddress, initialMsg)
    insertIntoDatabase("MsgStoreHistory", "bot" + userEmailAddress, initialMsg)

    # scrollbars for ChatBox.
    scrollbary = Scrollbar(root, command=ChatBox.yview)
    ChatBox['yscrollcommand'] = scrollbary.set
    scrollbary.place(x=980, y=8, height=720)
    scrollbary.config(bg="white")
    scrollbarx = Scrollbar(root, command=ChatBox.xview, orient="horizontal")
    scrollbarx.config(bg="white")
    ChatBox['xscrollcommand'] = scrollbarx.set
    scrollbarx.place(x=8, y=725, width=975)

    # used to switching focus. (This widget will no display on the screen)
    tempFrame = Frame(root, height=0, width=0)
    tempFrame.place(x=0, y=0)

    # EntryBox for user input.
    EntryBox = Entry(root, bd=0, bg="white",
                     font="Arial", relief="ridge", borderwidth=5)
    EntryBox.place(x=68, y=740, height=55, width=810)
    EntryBox.bind("<Key>", entryFocusInHandler)

    # deletes all the entries of ChatBox. (Invokes when clearButton invokes).
    def clearButtonListener():
        answer = messagebox.askyesno("Clear", "Sure?")
        if answer == True:
            command = """ delete from MsgStore """
            mycursor.execute(command)
            msg_db.commit()
            ChatBox.delete(0, "end")
            messagebox.showinfo("Clear", "All chats has been cleared.")
        else:
            pass

    # clear button (Clear the chats from the chatbox and delete the chats from the MsgStore)
    clear_button = Button(root, image=clear_button_image, bg="white", borderwidth=0, command=clearButtonListener)
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
    mic_button = Button(root, image=mic_button_image, bg="white", borderwidth=0, padx=2, pady=2, command=micButtonListener)
    mic_button.place(x=935, y=740, height=50, width=60)
    mic_button.bind('')

    # send the user response for evaluation. (Invokes when send_button invokes and by micButtonListener)
    def sendButtonListener(event=None):
        EntryBox.bind("<Return>", lambda event: tempFrame.focus_set())
        userInput = EntryBox.get()
        print(userInput)
        ChatBox.insert("end", "You: " + userInput)
        ChatBox.itemconfig('end', {'fg': 'blue'})
        root.update_idletasks()
        response = Response.getResponse(userInput)
        print(response)
        ChatBox.insert("end", "Bot: " + response)
        ChatBox.itemconfig('end', {'fg': 'green'})
        ChatBox.config(foreground="#446665", font=("Verdana", 12))
        root.update_idletasks()
        mic_button.config(state='active')
        insertIntoDatabase("MsgStore", userEmailAddress, userInput)
        insertIntoDatabase("MsgStoreHistory", userEmailAddress, userInput)
        insertIntoDatabase("MsgStore", "bot" + userEmailAddress, f"""{response}""")
        insertIntoDatabase("MsgStoreHistory", "bot" + userEmailAddress, f"""{response}""")
        EntryBox.delete(0, 'end')
        global stringToSpeak
        stringToSpeak = response

    # send button (sends the message to the chatbox)        
    send_button = Button(root, image=send_button_image, bg="white", borderwidth=0, command=sendButtonListener)
    root.bind('<Return>', sendButtonListener)
    send_button.place(x=880, y=740)

    # history tab. (Invokes when history option in invoke in menu bar)
    def historyTab():
        # window that shows history of all chats.
        historyWindow = Toplevel(root)
        root.withdraw()
        historyWindow.title("History")
        historyWindow.geometry("1000x800")
        historyWindow.config(bg="white")
        historyWindow.resizable(height=False, width=False)

        historyList = Listbox(historyWindow, height=35, width=96,foreground="#446665", font=("Verdana", 12), borderwidth=5, )
        historyList.place(x=10, y=10)

        scrollbary = Scrollbar(historyWindow, command=historyList.yview)
        historyList['yscrollcommand'] = scrollbary.set
        scrollbary.place(x=985, y=10, height=720)
        scrollbary.config(bg="white")

        scrollbarx = Scrollbar(historyWindow, command=historyList.xview, orient="horizontal")
        historyList['xscrollcommand'] = scrollbarx.set
        scrollbarx.place(x=10, y=725, width=980)
        scrollbarx.config(bg="white")

        mycursor.execute(""" select * from MsgStoreHistory """)
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
                    historyList.insert(i, chatsTime + " : You: " + chats[2])
                    historyList.itemconfig(i-1, {'fg': 'blue'})
                    i += 1
                elif chats[1] == "bot" + userEmailAddress:
                    historyList.insert(i, chatsTime + " : Bot: " + chats[2])
                    historyList.itemconfig(i-1, {'fg': 'green'})
                    i += 1
        except IndexError:
            pass

        # calls when user invokes clear button
        def clearButtonListener():
            answer = messagebox.askyesno("Clear", "Sure?")
            if answer == True:
                mycursor.execute(""" delete from MsgStoreHistory where sender = "{}" """.format(userEmailAddress))
                mycursor.execute(""" delete from MsgStoreHistory where sender = "{}" """.format('bot' + userEmailAddress))
                msg_db.commit()
                historyList.delete(0, "end")
                messagebox.showinfo("Clear", "All the chat history has been deleted.")
            else:
                pass

        # loading and using clear button image
        clearButton = Button(
            historyWindow, image=clear_button_image, bg="white", borderwidth=0, command=clearButtonListener)
        clearButton.place(x=8, y=740)

        # exports the chats to a file appended with current time. (Invokes when 'export chats history' invoke in menu bar of this particular window.)
        def exportChats():
            time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            textFile = open("Project/Wikipedia Chatbot/Histories/{}-chatHistories({}).txt".format(userEmailAddress, time), 'w')
            mycursor.execute(""" select * from MsgStoreHistory """)
            messages = mycursor.fetchall()
            for message in messages:
                if message[1] == userEmailAddress:
                    textFile.write(str(message[0]) + " => You:" + message[2] + '\n')
                elif message[1] == 'bot' + userEmailAddress:
                    textFile.write(str(message[0]) + " => Bot:" + message[2] + '\n')
            textFile.close()
            messagebox.showinfo("Export", """ Chats has been exported to "chatsHistory({}).txt" file """.format(time))

        # calks when user exits from the history window.
        def exitWindow():
            root.deiconify()
            historyWindow.withdraw()

        # menu bar for history window
        menubar = Menu(historyWindow, bg="white")
        options = Menu(menubar, tearoff=0, bg="white")
        menubar.add_cascade(label="Options", menu=options)
        options.add_command(label="Export Chat History", command=exportChats)
        options.add_separator()
        options.add_command(label="Exit", command=exitWindow)
        historyWindow.config(menu=menubar)

        historyWindow.protocol("WM_DELETE_WINDOW", exitWindow)

    # exports chats to a file appended with current time. (Invokes when 'exports chats' invokes in menubar of root.)
    def exportChats():
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        textFile = open("Project/Wikipedia Chatbot/Chats/{}-chats-({}).txt".format(userEmailAddress, time), 'w')
        mycursor.execute(""" select * from MsgStore """)
        messages = mycursor.fetchall()
        for message in messages:
            if message[1] == userEmailAddress:
                textFile.write(str(message[0]) + " => You:" + message[2] + '\n')
            elif message[1] == 'bot' + userEmailAddress:
                textFile.write(str(message[0]) + " => Bot:" + message[2] + '\n')
        textFile.close()
        messagebox.showinfo("Export", """ Chats has been exported to "{}-chats-({}).txt" file """.format(userEmailAddress, time))

    # calls when sign out invokes
    def signout():
        mycursor.execute(""" update LoginTable set remembered = 0  where emailAddress = "{}" """.format(userEmailAddress))
        msg_db.commit()
        root.withdraw()
        signUpWindow.deiconify()

    # invokes when click on change password from menu bar
    def changePassword():
        
        # window for changing password.
        changePasswordWindow = Toplevel(signUpWindow)
        root.withdraw()
        changePasswordWindow.title("Change Password")
        changePasswordWindow.geometry("500x500")
        changePasswordWindow.config(bg="white")
        changePasswordWindow.resizable(height=False, width=False)

        # loading and using logo image
        logo = Label(changePasswordWindow, image=logo_image, bg='white')
        logo.place(x=50, y=10)

        # old password label and entry box.
        oldPasswordLabel= Label(changePasswordWindow, text='Old Password', bg='white')
        oldPasswordLabel.place(x=80, y=250)
        oldPasswordEntryBox = Entry(changePasswordWindow, show='*')
        oldPasswordEntryBox.place(x=250, y=250)

        # new password label and entry box.
        newPasswordLabel = Label(changePasswordWindow, text='Password', bg='white')
        newPasswordLabel.place(x=80, y=290)
        newPasswordEntryBox = Entry(changePasswordWindow, show='*')
        newPasswordEntryBox.place(x=250, y=290)

        # confirn new password label and entry box.
        confirmNewPasswordLabel = Label(changePasswordWindow, text='Confirm Password', bg='white')
        confirmNewPasswordLabel.place(x=80, y=330)
        confirmNewPasswordEntryBox = Entry(changePasswordWindow, show='*')
        confirmNewPasswordEntryBox.place(x=250, y=330)

        # calls when user invokes chnage password button
        def changePasswordButtonListenener(event=None):
            mycursor.execute(""" select password from LoginTable where emailAddress = "{}" """.format(userEmailAddress))
            password = mycursor.fetchall()[0][0]
            if password == oldPasswordEntryBox.get():
                if newPasswordEntryBox.get() == confirmNewPasswordEntryBox.get():
                    mycursor.execute(""" update LoginTable set password = "{}" where emailAddress = "{}" """.format(newPasswordEntryBox.get(), userEmailAddress))
                    msg_db.commit()
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
        change_password_button = Button(changePasswordWindow, image=change_password_button_image, command=changePasswordButtonListenener)
        change_password_button.place(x=180, y=400)
        changePasswordWindow.bind('<Return>', changePasswordButtonListenener)

        # calls when user exits from the chnage password window.
        def on_closing():
            changePasswordWindow.withdraw()
            root.deiconify()

        changePasswordWindow.protocol("WM_DELETE_WINDOW", on_closing)

    # menu bar for chat window
    menubar = Menu(root, bg="white")
    options = Menu(menubar, tearoff=0, bg="white")
    menubar.add_cascade(label="Options", menu=options)
    options.add_command(label="History", command=historyTab)
    options.add_separator()
    options.add_command(label="Export Chats.", command=exportChats)
    options.add_separator()
    options.add_command(label="Sign Out", command=signout)
    options.add_separator()
    options.add_command(label="Change Password", command=changePassword)
    root.config(menu=menubar)

    # calls when user exits from the chat window.
    def on_closing():
        root.withdraw()
        signUpWindow.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

# loading and using logo image
logo = Label(signUpWindow, image=logo_image, bg='white')
logo.place(x=50, y=10)

# label and entry box for email
emailLabel = Label(signUpWindow, text='Email', bg='white')
emailLabel.place(x=100, y=250)
emailEntryBox = Entry(signUpWindow)
emailEntryBox.place(x=200, y=250)

# label and entry box for password.
passwordLabel = Label(signUpWindow, text='Password', bg='white')
passwordLabel.place(x=100, y=280)
passwordEntryBox = Entry(signUpWindow, show='*')
passwordEntryBox.place(x=200, y=280)

# checkbox for Remember me.
keep_me_signed = BooleanVar()
keep_me_signed_checkBox = Checkbutton(
    signUpWindow, text='Keep me signed up.', variable=keep_me_signed, onvalue=True, offvalue=False, bg='white')
keep_me_signed_checkBox.place(x=100, y=325)

# calls when user invkoes the signup button.
def signUpButtonListener(event=None):
    if emailEntryBox.get() != '' and passwordEntryBox.get() != '':
        global userEmailAddress
        userEmailAddress = emailEntryBox.get()
        mycursor.execute(""" select password from LoginTable where emailAddress = "{}" """.format(userEmailAddress))
        try:
            password = mycursor.fetchall()[0][0]
        except IndexError:
            pass
        if keep_me_signed.get() == True:
            mycursor.execute(""" update LoginTable set remembered = 1 where emailAddress = "{}" """.format(userEmailAddress))
            msg_db.commit()
        if password == passwordEntryBox.get():
            mainWindow()
        else:
            messagebox.showerror(title="Error", message='Wrong Password. Please try again.')
        emailEntryBox.delete(0, 'end')
        passwordEntryBox.delete(0, 'end')
    else:
        messagebox.showerror(title='Error', message='Empty Input Fields.')

# loading and using sign up image for sign up button.
sign_up_button = Button(image=sign_up_button_image,command=signUpButtonListener, bg='white')
sign_up_button.place(x=80, y=375)
signUpWindow.bind('<Return>', signUpButtonListener)

# calls when user invokes create account button.
def createAccountButtonListener():
    # window for creating account.
    createAccountWindow = Toplevel(signUpWindow)
    createAccountWindow.title("Create Account")
    createAccountWindow.geometry("500x500")
    createAccountWindow.config(bg="white")
    createAccountWindow.resizable(height=False, width=False)
    signUpWindow.withdraw()

    # loading and using logo image.
    logo = Label(createAccountWindow, image=logo_image, bg='white')
    logo.place(x=50, y=10)

    # label and entry box for email
    emailLabel = Label(createAccountWindow, text='Email', bg='white')
    emailLabel.place(x=100, y=250)
    emailEntryBox = Entry(createAccountWindow)
    emailEntryBox.place(x=200, y=250)

    # label and entry box for password.
    passwordLabel = Label(createAccountWindow, text='Password', bg='white')
    passwordLabel.place(x=100, y=280)
    passwordEntryBox = Entry(createAccountWindow, show='*')
    passwordEntryBox.place(x=200, y=280)

    # calls when user invokes create account button of this window.
    def createAccount(event=None):
        print(emailEntryBox.get())
        try:
            if emailEntryBox.get() != '' and passwordEntryBox.get() != '':
                mycursor.execute(""" insert into LoginTable  values("{}", "{}", 0) """.format(emailEntryBox.get(), passwordEntryBox.get()))
                msg_db.commit()
                messagebox.showinfo(title='Account', message='Account Created.')
                emailEntryBox.delete(0, 'end')
                passwordEntryBox.delete(0, 'end')
                createAccountWindow.withdraw()
                signUpWindow.deiconify()
            else:
                messagebox.showerror(title='Error', message='Empty input fiedls.')    
        except mycon.errors.IntegrityError :
            messagebox.showerror(title='Error', message='User Already Existed.')

    # loading and using create account image for create account button.
    create_account_button = Button(createAccountWindow, image=create_account_button_image, command=createAccount)
    create_account_button.place(x=180, y=375)
    createAccountWindow.bind('<Return>', createAccount)

    # calls when user exits from the create account window.
    def on_closing():
        createAccountWindow.withdraw()
        signUpWindow.deiconify()

    createAccountWindow.protocol("WM_DELETE_WINDOW", on_closing)


# loading and using create accout image for create account button.
create_account_button = Button(image=create_account_button_image, command=createAccountButtonListener)
create_account_button.place(x=250, y=375)

mycursor.execute(""" select emailAddress from LoginTable where remembered = 1 """)
emails = mycursor.fetchall()
if emails != []:
    userEmailAddress = emails[0][0]
    mainWindow()

signUpWindow.mainloop()
