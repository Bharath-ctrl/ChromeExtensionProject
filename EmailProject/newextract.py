from flask import Flask,jsonify, request
import email
import imaplib
# import requests, sqlite3

# connection=sqlite3.connect("Project.db",check_same_thread=False)
# listofTabs = connection.execute("select name from sqlite_master where type='table' AND name='user'").fetchall()

# if listofTabs!=[]:
#     print("Table exist already")
# else:
#     connection.execute('''create table user(
#                              ID integer primary key autoincrement,
#                              dbbody text,
#                              dbsubject text,
#                              dbhtmlbody text,
#                              dblinks text
#                              )''')
#     print("Table Created Successfully")
# cur = connection.cursor()

global UN,PW,host
UN='1ep18cs017.cse@eastpoint.ac.in'
PW='charlie_X95'
host='imap.gmail.com' 
appFlask = Flask(__name__)
@appFlask.route('/all')
def get_inbox():
    mail = imaplib.IMAP4_SSL(host)
    mail.login(UN, PW)
    mail.select("inbox")
    _, search_data = mail.search(None, 'ALL')
    my_message = []
    for num in search_data[0].split():
        email_data = {}
        _, data = mail.fetch(num, '(RFC822)')
        # print(data[0])
        _, b = data[0]
        email_message = email.message_from_bytes(b)
        for header in ['subject', 'to', 'from', 'date']:
            print("{}: {}".format(header, email_message[header]))
            email_data[header] = email_message[header]
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True)
                email_data['body'] = body.decode()
            elif part.get_content_type() == "text/html":
                html_body = part.get_payload(decode=True)
                email_data['html_body'] = html_body.decode()
        my_message.append(email_data)
        #print(my_message)
    return jsonify(my_message)
 
@appFlask.route('/unread')
def unread():
    mail = imaplib.IMAP4_SSL(host)
    mail.login(UN, PW)
    mail.select("inbox")
    _, search_data = mail.search(None, 'UNSEEN')
    my_message = []
    for num in search_data[0].split():
        email_data = {}
        _, data = mail.fetch(num, '(RFC822)')
        # print(data[0])
        _, b = data[0]
        email_message = email.message_from_bytes(b)
        for header in ['subject', 'to', 'from', 'date']:
            print("{}: {}".format(header, email_message[header]))
            email_data[header] = email_message[header]
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True)
                email_data['body'] = body.decode()
            elif part.get_content_type() == "text/html":
                html_body = part.get_payload(decode=True)
                email_data['html_body'] = html_body.decode()
        my_message.append(email_data)
        #print(my_message)
    return jsonify(my_message)
    # apiformat= jsonify(my_message)
    # d = request.get("http://127.0.0.1:5000/unread")
    # d = d.json()
    # componentrs = d["body"]["from"]["html_body"]["subject"]
    # for dr in componentrs:
    #     name = dr["familyName"]
    #     number = dr["permanentNumber"]
    #     prod={}
    #     newinsert=cur.execute('''INSERT INTO user(dbbody,dbsubject,dbhtmlbody) VALUES(body,subject,html_body)''')    
    #     val = (name,number)
    #     cur.execute(sql,val)


if __name__ == "__main__":
    appFlask.run(debug=True)


    #my_inbox = get_inbox()
    #print(my_inbox)
# print(search_data)
