# importing Local file for speech recognition.
import Listen_And_Speak as listenAndSpeak
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

# establish mysql connection.
msg_db = mycon.connect(user="root", password="Nursinha.01",
                       database="msg_db", host="localhost")  # enter your database name and password to access it.
mycursor = msg_db.cursor()

loginWindow = tkinter.Tk()
loginWindow.title('Login')
loginWindow.geometry("500x500")
loginWindow.config(bg="white")
loginWindow.resizable(height=False, width=False)

userEmailAddress = None
stringToSpeak = None

clear_button_image = Image.open("Project/Wikipedia Chatbot/images/clear.png")
clear_button_image = clear_button_image.resize((50, 47), Image.ANTIALIAS)
clear_button_image = ImageTk.PhotoImage(clear_button_image)

mic_button_image = Image.open("Project/Wikipedia Chatbot/images/mic.png")
mic_button_image = mic_button_image.resize((50, 47), Image.ANTIALIAS)
mic_button_image = ImageTk.PhotoImage(mic_button_image)

send_button_image = Image.open("Project/Wikipedia Chatbot/images/send.png")
send_button_image = send_button_image.resize((50, 47), Image.ANTIALIAS)
send_button_image = ImageTk.PhotoImage(send_button_image)

# change_password_button_image = Image.open("Project/Wikipedia Chatbot/images/changePassword.png")
# change_password_button_image = change_password_button_image.resize((50, 47), Image.ANTIALIAS)
# change_password_button_image = ImageTk.PhotoImage(change_password_button_image)

def mainWindow():
    loginWindow.withdraw()
    # inserts the given parameter to the database.

    def insertIntoDatabase(table, sender, message):
        mycursor.execute("""insert into {} (date, sender, message) value(now(3), "{}", "{}")""".format(
            table, sender, message))
        msg_db.commit()

    # disables the mic_button when user types anything in the EntryBox.
    def entryFocusInHandler(event=None):
        mic_button.config(state="disabled")

    # # establish mysql connection.
    # msg_db = mycon.connect(user="root", password="Nursinha.01",
    #                     database="msg_db", host="localhost") # enter your database name and password to access it.
    # mycursor = msg_db.cursor()

    root = Toplevel(loginWindow)
    root.title("Wikipedia Chatbot")
    root.geometry("1000x800")
    root.config(bg="white")
    root.resizable(height=False, width=False)

    ChatBox = Listbox(root, height=35, width=96,
                      foreground="#446665", font=("Verdana", 12), borderwidth=5)
    ChatBox.place(x=5, y=5)

    # for the initial purpose.
    initialMsg = "Hi there, I am Wikibot. You can ask me anything. Tell me, what you want to search?"
    mycursor.execute("""delete from MsgStore""")
    msg_db.commit()
    ChatBox.insert("end", "Bot: " + initialMsg)
    ChatBox.itemconfig('end', {'fg': 'green'})
    insertIntoDatabase("MsgStore", "bot", initialMsg)
    insertIntoDatabase("MsgStoreHistory", "bot", initialMsg)

    # scrollbars for ChatBox.
    scrollbary = Scrollbar(root, command=ChatBox.yview)
    ChatBox['yscrollcommand'] = scrollbary.set
    scrollbary.place(x=980, y=8, height=720)
    scrollbary.config(bg="white")
    scrollbarx = Scrollbar(root, command=ChatBox.xview, orient="horizontal")
    scrollbarx.config(bg="white")
    ChatBox['xscrollcommand'] = scrollbarx.set
    scrollbarx.place(x=8, y=725, width=975)

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

    # clear_button for clearing all the entries of the ChatBox.
    # clear_button_image = Image.open("Project/Wikipedia Chatbot/images/clear.png")
    # clear_button_image = clear_button_image.resize((50, 47), Image.ANTIALIAS)
    # clear_button_image = ImageTk.PhotoImage(clear_button_image)
    clear_button = Button(root, image=clear_button_image, bg="white",
                          borderwidth=0, command=clearButtonListener)
    clear_button.place(x=8, y=740)

    # listens the user input when user clicks on mic_button. (Invokes when mic_button invokes)
    def micButtonListener():
        global stringToSpeak
        text = listenAndSpeak.takeUserSpeech()
        EntryBox.delete(0, "end")
        EntryBox.insert(0, text)
        sendButtonListener()
        listenAndSpeak.speak(stringToSpeak)

    # mic_button for getting user speech.
    # mic_button_image = Image.open("Project/Wikipedia Chatbot/images/mic.png")
    # mic_button_image = mic_button_image.resize((50, 47), Image.ANTIALIAS)
    # mic_button_image = ImageTk.PhotoImage(mic_button_image)
    mic_button = Button(root, image=mic_button_image, bg="white",
                        borderwidth=0, padx=2, pady=2, command=micButtonListener)
    mic_button.place(x=935, y=740, height=50, width=60)
    mic_button.bind('')

    # send the user response for evaluation. (Invokes when send_button invokes)
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

    # send_button for giving user input for evaluation.
    # send_button_image = Image.open("Project/Wikipedia Chatbot/images/send.png")
    # send_button_image = send_button_image.resize((50, 47), Image.ANTIALIAS)
    # send_button_image = ImageTk.PhotoImage(send_button_image)
    send_button = Button(root, image=send_button_image, bg="white",
                         borderwidth=0, command=sendButtonListener)
    root.bind('<Return>', sendButtonListener)
    send_button.place(x=880, y=740)

    # history tab. (Invokes when history option in invoke in menu bar)

    def historyTab():
        historyWindow = Toplevel(root)
        root.withdraw()
        historyWindow.title("History")
        historyWindow.geometry("1000x800")
        historyWindow.config(bg="white")
        historyWindow.resizable(height=False, width=False)
        historyList = Listbox(historyWindow, height=35, width=96,
                              foreground="#446665", font=("Verdana", 12), borderwidth=5, )
        historyList.place(x=10, y=10)
        scrollbary = Scrollbar(historyWindow, command=historyList.yview)
        historyList['yscrollcommand'] = scrollbary.set
        scrollbary.place(x=985, y=10, height=720)
        scrollbary.config(bg="white")
        scrollbarx = Scrollbar(
            historyWindow, command=historyList.xview, orient="horizontal")
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
                print(chatsDate, chatsTime, date)
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
                    historyList.insert(
                        i, chatsTime + " : You: " + chats[2])
                    historyList.itemconfig(i-1, {'fg': 'blue'})
                    i += 1
                elif chats[1] == "bot" + userEmailAddress:
                    historyList.insert(
                        i, chatsTime + " : Bot: " + chats[2])
                    historyList.itemconfig(i-1, {'fg': 'green'})
                    i += 1
        except IndexError:
            pass

        def clearButtonListener():
            answer = messagebox.askyesno("Clear", "Sure?")
            if answer == True:
                command = """ delete from MsgStoreHistory """
                mycursor.execute(command)
                msg_db.commit()
                historyList.delete(0, "end")
                messagebox.showinfo(
                    "Clear", "All the chat history has been deleted.")
            else:
                pass

        global clear_button_image
        clearButton = Button(
            historyWindow, image=clear_button_image, bg="white", borderwidth=0, command=clearButtonListener)
        clearButton.place(x=8, y=740)

        # exports the chats to a file appended with current time. (Invokes when 'export chats history' invoke in menu bar of this particular window.)
        def exportChats():
            time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            textFile = open(
                "Project/Wikipedia Chatbot/Histories/chatHistories({}).txt".format(time), 'w')
            mycursor.execute(
                """ select * from MsgStoreHistory """)
            messages = mycursor.fetchall()
            for message in messages:
                if message[1] == "me":
                    textFile.write(str(message[0]) +
                                   " => You:" + message[2] + '\n')
                else:
                    textFile.write(str(message[0]) +
                                   " => Bot:" + message[2] + '\n')
            textFile.close()
            messagebox.showinfo(
                "Export", """ Chats has been exported to "chatsHistory({}).txt" file """.format(time))

        def exitWindow():
            root.deiconify()
            historyWindow.withdraw()

        menubar = Menu(historyWindow, bg="white")
        options = Menu(menubar, tearoff=0, bg="white")
        menubar.add_cascade(label="Options", menu=options)
        options.add_command(label="Export Chat History", command=exportChats)
        options.add_separator()
        options.add_command(label="Exit", command=exitWindow)
        historyWindow.config(menu=menubar)

        def on_closing():
            historyWindow.withdraw()
            root.deiconify()

        historyWindow.protocol("WM_DELETE_WINDOW", on_closing)

    # exports chats to a file appended with current time. (Invokes when 'exports chats' invokes in menubar of root.)

    def exportChats():
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        textFile = open(
            "Project/Wikipedia Chatbot/Chats/chats({}).txt".format(time), 'w')
        mycursor.execute(
            """ select * from MsgStore """)
        messages = mycursor.fetchall()
        for message in messages:
            if message[1] == "me":
                textFile.write(str(message[0]) +
                               " => You:" + message[2] + '\n')
            else:
                textFile.write(str(message[0]) +
                               " => Bot:" + message[2] + '\n')
        textFile.close()
        messagebox.showinfo(
            "Export", """ Chats has been exported to "chats({}).txt" file """.format(time))

    def signout():
        mycursor.execute(""" update LoginTable set remembered = 0  where emailAddress = "{}" """.format(userEmailAddress))
        msg_db.commit()
        loginWindow.destroy()


    def changePassword():
        changePasswordWindow = Toplevel(loginWindow)
        root.withdraw()
        changePasswordWindow.title("Create Account")
        changePasswordWindow.geometry("500x500")
        changePasswordWindow.config(bg="white")
        changePasswordWindow.resizable(height=False, width=False)

        oldPasswordLabel= Label(changePasswordWindow, text='Old Password', bg='white')
        oldPasswordLabel.place(x=100, y=200)
        oldPasswordEntryBox = Entry(changePasswordWindow, show='*')
        oldPasswordEntryBox.place(x=250, y=200)

        newPasswordLabel = Label(changePasswordWindow, text='Password', bg='white')
        newPasswordLabel.place(x=100, y=240)
        newPasswordEntryBox = Entry(changePasswordWindow, show='*')
        newPasswordEntryBox.place(x=250, y=240)

        confirmNewPasswordLabel = Label(changePasswordWindow, text='Confirm Password', bg='white')
        confirmNewPasswordLabel.place(x=100, y=280)
        confirmNewPasswordEntryBox = Entry(changePasswordWindow, show='*')
        confirmNewPasswordEntryBox.place(x=250, y=280)

        def changePasswordButtonListenener():
            mycursor.execute(""" select password from LoginTable where emailAddress = "{}" """.format(userEmailAddress))
            password = mycursor.fetchall()[0][0]
            if password == oldPasswordEntryBox.get():
                if newPasswordEntryBox.get() == confirmNewPasswordEntryBox.get():
                    mycursor.execute(""" update LoginTable set password = "{}" where emailAddress = "{}" """.format(newPasswordEntryBox.get(), userEmailAddress))
                    msg_db.commit()
                    messagebox.showinfo(title="Password", message='Password has been changed.')    
                else:
                    messagebox.showerror(title="Error", message='New password should be same as confirm password.')    
            else:
                messagebox.showerror(title="Error", message='Wrong old password.')

        # change_password_button = Button(
        #     changePasswordWindow, image=change_password_button_image, command=changePasswordButtonListenener)


        change_password_button = Button(
            changePasswordWindow, text="Change Password", command=changePasswordButtonListenener)
        change_password_button.place(x=180, y=375)

        def on_closing():
            changePasswordWindow.withdraw()
            root.deiconify()

        changePasswordWindow.protocol("WM_DELETE_WINDOW", on_closing)


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

    def on_closing():
        root.withdraw()
        loginWindow.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)


emailLabel = Label(loginWindow, text='Email', bg='white')
emailLabel.place(x=100, y=250)
emailEntryBox = Entry(loginWindow)
emailEntryBox .place(x=200, y=250)

userEmailAddress = emailEntryBox.get()

passwordLabel = Label(loginWindow, text='Password', bg='white')
passwordLabel.place(x=100, y=280)
passwordEntryBox = Entry(loginWindow, show='*')
passwordEntryBox.place(x=200, y=280)



sign_up_button_image = Image.open(
    "Project/Wikipedia Chatbot/images/signUp.png")
sign_up_button_image = sign_up_button_image.resize((150, 50), Image.ANTIALIAS)
sign_up_button_image = ImageTk.PhotoImage(sign_up_button_image)

create_account_button_image = Image.open(
    "Project/Wikipedia Chatbot/images/create-account.png")
create_account_button_image = create_account_button_image.resize(
    (150, 50), Image.ANTIALIAS)
create_account_button_image = ImageTk.PhotoImage(create_account_button_image)

remember_me = BooleanVar()
remember_me_checkBox = Checkbutton(
    loginWindow, text='Remember me', variable=remember_me, onvalue=True, offvalue=False, bg='white')
remember_me_checkBox.place(x=100, y=325)

def signUpButtonListener():
    global userEmailAddress
    userEmailAddress = emailEntryBox.get()
    # print(emailEntryBox.get(), passwordEntryBox.get())
    mycursor.execute(""" select password from LoginTable where emailAddress = "{}" """.format(userEmailAddress))
    password = mycursor.fetchall()[0][0]
    # print(password)
    if remember_me.get() == True:
        mycursor.execute(""" update LoginTable set remembered = 1 where emailAddress = "{}" """.format(userEmailAddress))
        msg_db.commit()
    if password == passwordEntryBox.get():
        mainWindow()
    else:
        messagebox.showerror(title="Error", message='Wrong Password. Please try again.')

sign_up_button = Button(image=sign_up_button_image,
                        command=signUpButtonListener, bg='white')
sign_up_button.place(x=80, y=375)


def createAccountButtonListener():
    createAccountWindow = Toplevel(loginWindow)
    loginWindow.withdraw()
    createAccountWindow.title("Create Account")
    createAccountWindow.geometry("500x500")
    createAccountWindow.config(bg="white")
    createAccountWindow.resizable(height=False, width=False)

    emailLabel = Label(createAccountWindow, text='Email', bg='white')
    emailLabel.place(x=100, y=250)
    emailEntryBox = Entry(createAccountWindow)
    emailEntryBox.place(x=200, y=250)

    passwordLabel = Label(createAccountWindow, text='Password', bg='white')
    passwordLabel.place(x=100, y=280)
    passwordEntryBox = Entry(createAccountWindow, show='*')
    passwordEntryBox.place(x=200, y=280)

    def createAccount():
        print(emailEntryBox.get())
        try:
            mycursor.execute(""" insert into LoginTable  values("{}", "{}", 0) """.format(emailEntryBox.get(), passwordEntryBox.get()))
            msg_db.commit()
            messagebox.showinfo(title='Account', message='Account Created.')
        except mycon.errors.IntegrityError :
            messagebox.showerror(title='Error', message='User Already Existed.')

    create_account_button = Button(
        createAccountWindow, image=create_account_button_image, command=createAccount)
    create_account_button.place(x=180, y=375)

    def on_closing():
        createAccountWindow.withdraw()
        loginWindow.deiconify()

    createAccountWindow.protocol("WM_DELETE_WINDOW", on_closing)


create_account_button = Button(
    image=create_account_button_image, command=createAccountButtonListener)
create_account_button.place(x=250, y=375)

mycursor.execute(""" select emailAddress from LoginTable where remembered = 1 """)
emails = mycursor.fetchall()
if emails != []:
    userEmailAddress = emails[0][0]
    mainWindow()

loginWindow.mainloop()
