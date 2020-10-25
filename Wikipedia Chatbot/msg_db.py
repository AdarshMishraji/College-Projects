import mysql.connector as mycon
from datetime import datetime

database = mycon.connect(user = "root", password = "Nursinha.01", host = "localhost", database = "msg_db")
cursor = database.cursor()

cursor.execute("""
                    create table MsgStore(
	                        date datetime, 
	                        sender varchar(50) default "me",
	                        message varchar(1000), 
	                        primary key(date, sender)
                    )
                """)

cursor.execute("""
                    create table MsgStoreHistory(
	                        date datetime, 
	                        sender varchar(50) default "me",
	                        message varchar(1000), 
	                        primary key(date, sender)
                    )
                """)
