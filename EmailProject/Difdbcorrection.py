from flask import Flask, jsonify,session
from flask_sqlalchemy import SQLAlchemy
import email
import imaplib
# import sqlite3
from itertools import count
import psycopg2
from psycopg2 import Error

# try:
#     # Connect to an existing database
#     connection = psycopg2.connect(user="postgres",
#                                   password="pynative@#29",
#                                   host="127.0.0.1",
#                                   port="5432",
#                                   database="postgres_db")
#
#     # Create a cursor to perform database operations
#     cursor = connection.cursor()
from sqlalchemy.sql.functions import user

app = Flask(__name__)
app.config['SQLAlchemy_DATABASE_URI']= 'postgresql://charlie:123@localhost/ephish'
db=SQLAlchemy(app)

class User(db.Model):
  __tablename__='user'
  id=db.Column(db.Integer,primary_key=True)
  sender=db.Column(db.String())
  subject=db.Column(db.String())
  content=db.Column(db.String())

  def __init__(self,sender,subject,content):
    self.sender=sender
    self.subject=subject
    self.content=content

#
# connection = sqlite3.connect("Newdb.db", check_same_thread=False)
# table1 = connection.execute("select * from sqlite_master where type = 'table' and name = 'user'").fetchall()
# if table1 != []:
#     print("table already exists")
#     r = connection.execute('select * from user')
#     print(r)
# else:
#     connection.execute('''create table user(
#                                 ID INTEGER PRIMARY KEY AUTOINCREMENT,
#                                 SENDER TEXT,
#                                 BODYCONTENT TEXT,
#                                 SUBJECT TEXT
#
#
#                             );''')
#     print("table created")
#


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
                # res = cur.execute("select * from user").fetchall()
                # user = []
                # inbox = {}
                # cur.execute("insert into user(SENDER,SUBJECT) values('" + getFrom + "','" + getSub + "')")
                # connection.commit()
                # user = []
                # inbox = {}
                # print('select * from user')
                # for result in res:
                #     inbox = {'Sender': result['SENDER'], 'Subject': ['SUBJECT']}
                #     user.append(inbox)
                #     inbox = {}
                # return jsonify(user)
                # result={
                #     "Sender": mail_from,
                #     "Subject": mail_subject,
                #     "Body": mail_content
                # }

                # return jsonify(result)
                store=User(getFrom,getSub,getContent)
                db.session.add(store)
                db.session.commit()
                box = []
                inbox = {}
                # for result in store:
                #     inbox = {'Sender': result['sender'], 'Subject': ['subject'],'BodyContent':['content']}
                #     user.append(inbox)
                #     inbox = {}
                return jsonify(user)


if __name__ == ("__main__"):
    app.run(debug=True)
