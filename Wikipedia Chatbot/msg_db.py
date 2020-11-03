import mysql.connector as mycon
from datetime import datetime

 # enter your user name, password, database name and host to access it.
mysqluser = "ENTER-YOUR-USERNAME"
mysqlpassword = "ENTER-YOUR-PASSWORD"
mysqldatabase = "ENTER-YOUR-DATABASE NAME"
mysqlhost = "ENTER-YOUR-HOST"

msg_db = mycon.connect(user=mysqluser, password=mysqlpassword, database=mysqldatabase, host=mysqlhost)
cursor = msg_db.cursor()

cursor.execute("""
                    create table SignUpTable(
	                        emailAddress varchar(50), 
	                        password varchar(32) not null,
                            remembered boolean default 0,
                            primary key (emailAddress)
                    )
                """) # this table stores the login details

cursor.execute("""
                    create table MsgStoreHistory(
                            date varchar(25), 
	                        sender varchar(50) not null,
	                        message varchar(1000),
                            primary key(date)
                    )
                """) # this table is used for storing all chats (History).

cursor.execute("""
                    create table MsgStore(
	                        date varchar(25), 
	                        sender varchar(50) not null,
	                        message varchar(1000),
                            primary key(date)
                    )
                """) # this table is used for storing the messages for ChatBox widget.
