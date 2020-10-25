import mysql.connector as mycon
from datetime import datetime

database = mycon.connect(user = "root", password = "**********", host = "localhost", database = "msg_db") # provide your password.
cursor = database.cursor()

cursor.execute("""
                    create table MsgStore(
	                        date datetime, 
	                        sender varchar(50) default "me",
	                        message varchar(1000), 
	                        primary key(date, sender)
                    )
                """) # this table is used for storing the messages for ChatBox widget.

cursor.execute("""
                    create table MsgStoreHistory(
	                        date datetime, 
	                        sender varchar(50) default "me",
	                        message varchar(1000), 
	                        primary key(date, sender)
                    )
                """) # this table is used for storing all chats (History).
