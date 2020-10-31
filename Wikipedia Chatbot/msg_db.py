import mysql.connector as mycon
from datetime import datetime

database = mycon.connect(user = "ENTER YOUR USERNAME", password = "ENTER YOUR PASSWORD", host = "localhost", database = "ENTER YOUR DATABASE NAME") # provide your user and password along with a database
cursor = database.cursor()

cursor.execute("""
                    create table LoginTable(
	                        emailAddress varchar(50), 
	                        password varchar(32),
                            remembered boolean default 0,
                            primary key (emailAddress)
                    )
                """) # this table stores the login details

cursor.execute("""
                    create table MsgStoreHistory(
	                        date varchar(25), 
	                        sender varchar(50),
	                        message varchar(1000)
                    )
                """) # this table is used for storing all chats (History).

cursor.execute("""
                    create table MsgStore(
	                        date varchar(25), 
	                        sender varchar(50),
	                        message varchar(1000)
                    )
                """) # this table is used for storing the messages for ChatBox widget.
