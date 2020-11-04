import sqlite3 as sql

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
