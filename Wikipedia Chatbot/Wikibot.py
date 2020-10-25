import Listen_And_Speak as listenAndSpeak # importing Local file for speech recognition.
import Response  # importing local file to get the response
import tkinter
from tkinter import BooleanVar, Button, Entry, Frame, IntVar, Listbox, Menu, Scrollbar, Text, Toplevel, messagebox
from PIL import ImageTk, Image
import mysql.connector as mycon
from datetime import datetime
import wikipedia
import nltk
# import pyttsx3
from sys import platform
import sys
sys.path.append('Chatbot')

stringToSpeak = None


# inserts the given parameter to the database.
def insertIntoDatabase(table, sender, message):
    mycursor.execute("""insert into {} (date, sender, message) value(now(), "{}", "{}")""".format(
        table, sender, message))
    msg_db.commit()


# display all the messages for the first time.
def showMessages(): 
    mycursor.execute(
        """ select sender, message from MsgStore """)
    messages = mycursor.fetchall()
    for message in messages:
        if message[0] == "me":
            ChatBox.insert("end", "You: " + message[1])
            ChatBox.itemconfig('end', {'fg': 'blue'})
        elif message[0] == 'bot':
            ChatBox.insert("end", "Bot: " + message[1])
            ChatBox.itemconfig('end', {'fg': 'green'})
    ChatBox.config(foreground="#446665", font=("Verdana", 12))


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


# disables the mic_button when user types anything in the EntryBox.
def entryFocusInHandler(event=None):
    mic_button.config(state="disabled")


# listens the user input when user clicks on mic_button. (Invokes when mic_button invokes)
def micButtonListener(): 
    global stringToSpeak
    text = listenAndSpeak.takeUserSpeech()
    EntryBox.delete(0, "end")
    EntryBox.insert(0, text)
    sendButtonListener()
    listenAndSpeak.speak(stringToSpeak)


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
    insertIntoDatabase("MsgStore", "me", userInput)
    insertIntoDatabase("MsgStoreHistory", "me", userInput)
    insertIntoDatabase("MsgStore", "bot", f"""{response}""")
    insertIntoDatabase("MsgStoreHistory", "bot", f"""{response}""")
    global stringToSpeak
    stringToSpeak = response


# establish mysql connection.
msg_db = mycon.connect(user="root", password="Nursinha.01",
                       database="msg_db", host="localhost")
mycursor = msg_db.cursor()

root = tkinter.Tk()
root.title("Wiki-bot")
root.geometry("1000x800")
root.config(bg="white")
root.resizable(height=False, width=False)

ChatBox = Listbox(root, height=35, width=96,
                  foreground="#446665", font=("Verdana", 12), borderwidth=5)
ChatBox.place(x=5, y=5)

initialMsg = "Hi there, I am Wikibot. You can ask me anything. Tell me, what you want to search?"
insertIntoDatabase("MsgStore", "bot", initialMsg)
insertIntoDatabase("MsgStoreHistory", "bot", initialMsg)
showMessages()  # for the initial purpose.

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

# clear_button for clearing all the entries of the ChatBox.
clear_button_image = Image.open("Chatbot/images/clear.png")
clear_button_image = clear_button_image.resize((50, 47), Image.ANTIALIAS)
clear_button_image = ImageTk.PhotoImage(clear_button_image)
clear_button = Button(root, image=clear_button_image, bg="white",
                      borderwidth=0, command=clearButtonListener)
clear_button.place(x=8, y=740)

# mic_button for getting user speech.
mic_button_image = Image.open("Chatbot/images/mic.png")
mic_button_image = mic_button_image.resize((50, 47), Image.ANTIALIAS)
mic_button_image = ImageTk.PhotoImage(mic_button_image)
mic_button = Button(root, image=mic_button_image, bg="white",
                    borderwidth=0, padx=2, pady=2, command=micButtonListener)
mic_button.place(x=935, y=740, height=50, width=60)
mic_button.bind('')


# send_button for giving user input for evaluation.
send_button_image = Image.open("Chatbot/images/send.png")
send_button_image = send_button_image.resize((50, 47), Image.ANTIALIAS)
send_button_image = ImageTk.PhotoImage(send_button_image)
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
            if chats[1] == "me":
                historyList.insert(
                    i, chatsTime + " : You: " + chats[2])
                historyList.itemconfig(i-1, {'fg': 'blue'})
                i += 1
            else:
                historyList.insert(
                    i, chatsTime + " : Bot: " + chats[2])
                historyList.itemconfig(i-1, {'fg': 'green'})
                i += 1
    except IndexError:
        pass

    global clear_button_image

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

    clearButton = Button(
        historyWindow, image=clear_button_image, bg="white", borderwidth=0, command=clearButtonListener)
    clearButton.place(x=8, y=740)

    # exports the chats to a file appended with current time. (Invokes when 'export chats history' invoke in menu bar of this particular window.)
    def exportChats():
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        textFile = open(
            "Chatbot/Histories/chatHistories({}).txt".format(time), 'w')
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
    textFile = open("Chatbot/Chats/chats({}).txt".format(time), 'w')
    mycursor.execute(
        """ select * from MsgStore """)
    messages = mycursor.fetchall()
    for message in messages:
        if message[1] == "me":
            textFile.write(str(message[0]) + " => You:" + message[2] + '\n')
        else:
            textFile.write(str(message[0]) + " => Bot:" + message[2] + '\n')
    textFile.close()
    messagebox.showinfo(
        "Export", """ Chats has been exported to "chats({}).txt" file """.format(time))


menubar = Menu(root, bg="white")
options = Menu(menubar, tearoff=0, bg="white")
menubar.add_cascade(label="Options", menu=options)
options.add_command(label="History", command=historyTab)
options.add_separator()
options.add_command(label="Export Chats.", command=exportChats)
root.config(menu=menubar)

root.mainloop()
