from flask import Flask,jsonify
import email
import imaplib

global UN,PW,host
UN='1ep18cs017.cse@eastpoint.ac.in'
PW='charlie_X95'
host='imap.gmail.com' 
appFlask = Flask(__name__)
@appFlask.route('/')
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


if __name__ == "__main__":
    appFlask.run(debug=True)


    #my_inbox = get_inbox()
    #print(my_inbox)
# print(search_data)
