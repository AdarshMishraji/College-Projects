import mysql.connector as mycon
from datetime import datetime

database = mycon.connect(user = "root", password = "Nursinha.01", host = "localhost", database = "msg_db") # provide your password.
cursor = database.cursor()

cursor.execute("""
                    create table MsgStore(
	                        date varchar(25), 
	                        sender varchar(50) default "me",
	                        message varchar(1000)
                    )
                """) # this table is used for storing the messages for ChatBox widget.

cursor.execute("""
                    create table MsgStoreHistory(
	                        date varchar(25), 
	                        sender varchar(50) default "me",
	                        message varchar(1000)
                    )
                """) # this table is used for storing all chats (History).
