from flask import Flask, jsonify
import email
import imaplib
import sqlite3
import mysql.connector
from itertools import count
from flask_mysqldb import MySQL,MySQLdb
# mydb = mysql.connector.connect(
#   host="localhost",
#   user="qwer",
#   password="123",
#   database = "myemail"
# )

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'testing.db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql=MySQL(app)
mycursor.execute("CREATE DATABASE myemail")
mycursor = testing.cursor()
#

#

mycursor.execute("CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY,sender VARCHAR(255), subject VARCHAR(255),bodycontent VARCHAR(255))")
mycursor.execute("SHOW tables")
for x in mycursor:
  print(x)

#
# connection = sqlite3.connect("MY.db", check_same_thread=False)
# table1 = connection.execute("select * from sqlite_master where type = 'table' and name = 'user'").fetchall()
# if table1 != []:
#     connection.execute('''create table user(
#                             ID INTEGER PRIMARY KEY AUTOINCREMENT,
#                             SENDER TEXT,
#                             SUBJECT TEXT,
#                             BODY_CONTENT TEXT
#
#                         )''')
#     print("table created")
# else:
#     print("table already exists")




@app.route('/')
def extract():
    EMAIL = '1ep18cs017.cse@eastpoint.ac.in'
    PASSWORD = 'charlie_X95'
    SERVER = 'imap.gmail.com'

    # connect to the server and go to its inbox
    mail = imaplib.IMAP4_SSL(SERVER)
    mail.login(EMAIL, PASSWORD)
    # we choose the inbox but you can select others
    mail.select('inbox')

    # we'll search using the ALL criteria to retrieve
    # every message inside the inbox
    # it will return with its status and a list of ids
    status, data = mail.search(None, 'ALL')
    # the list returned is a list of bytes separated
    # by white spaces on this format: [b'1 2 3', b'4 5 6']
    # so, to separate it first we create an empty list
    mail_ids = []
    # then we go through the list splitting its blocks
    # of bytes and appending to the mail_ids list
    for block in data:
        # the split function called without parameter
        # transforms the text or bytes into a list using
        # as separator the white spaces:
        # b'1 2 3'.split() => [b'1', b'2', b'3']
        mail_ids += block.split()

    # now for every id we'll fetch the email
    # to extract its content
    for i in mail_ids:
        # the fetch function fetch the email given its id
        # and format that you want the message to be
        status, data = mail.fetch(i, '(RFC822)')

        # the content data at the '(RFC822)' format comes on
        # a list with a tuple with header, content, and the closing
        # byte b')'
        for response_part in data:
            # so if its a tuple...
            if isinstance(response_part, tuple):
                # we go for the content at its second element
                # skipping the header at the first and the closing
                # at the third
                message = email.message_from_bytes(response_part[1])

                # with the content we can extract the info about
                # who sent the message and its subject
                mail_from = message['from']
                mail_subject = message['subject']

                # then for the text we have a little more work to do
                # because it can be in plain text or multipart
                # if its not plain text we need to separate the message
                # from its annexes to get the text
                if message.is_multipart():
                    mail_content = ''

                    # on multipart we have the text message and
                    # another things like annex, and html version
                    # of the message, in that case we loop through
                    # the email payload
                    for part in message.get_payload():
                        # if the content type is text/plain
                        # we extract it
                        if part.get_content_type() == 'text/plain':
                            mail_content += part.get_payload()
                else:
                    # if the message isn't multipart, just extract it
                    mail_content = message.get_payload()
                print(mail_from)

                # and then let's show its result
                # print(f'From: {mail_from}')
                # print(f'Subject: {mail_subject}')
                # print(f'Content: {mail_content}')
                getFrom = mail_from
                getSub = mail_subject
                getContent = mail_content

                # cur = connection.cursor()
                # # query = "SELECT * FROM USER"
                # cur.execute("select * from user;")
                # res = cur.fetchall()
                # user = []
                # inbox = {}
                #
                # if len(res) > 0:
                #     return 1
                # else:
                #     cur.execute("insert into user(SENDER,SUBJECT,BODYCONTENT)\
                #                                     values('" + getFrom + "','" + getSub + "','" + getContent + "')")
                #     connection.commit()

                sql = "INSERT INTO users (sender, subject,bodycontent) VALUES (%s, %s, %s)"
                val = (getFrom, getSub, getContent)
                mycursor.execute(sql, val)

                mydb.commit()

                print(mycursor.rowcount, "record inserted.")
                mycursor.execute("SELECT * FROM customers")

                res = mycursor.fetchall()
                users=[]
                inbox2={}
                print("select * from ")
                for result in res:
                    inbox2 = {'Sender': result['sender'], 'Subject': ['subject'], 'BodyContent': ['bodycontent']}
                    users.append(inbox2)
                    inbox = {}
                return jsonify(users)
                # result={
                #     "Sender": mail_from,
                #     "Subject": mail_subject,
                #     "Body": mail_content
                # }

                # return jsonify(result)


if __name__ == ("__main__"):
    app.run(debug=True)
