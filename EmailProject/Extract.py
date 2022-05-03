import email
import imaplib
from itertools import count
import pandas as pd
import numpy as np


# file=pd.DataFrame([[],[],[]],columns=['Sender','Subject','BodyContent'])
# file.to_csv("extractreport.csv",mode='a',index=False, header=False)
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
k=0
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

                # and then let's show its result
                # print(f'From: {mail_from}')
                # print(f'Subject: {mail_subject}')
                # print(f'Content: {mail_content}')
                # file = pd.DataFrame([[mail_from], [mail_subject], [mail_content]],columns=['Sender', 'Subject', 'BodyContent'])
                # file.to_csv("extractreport.csv")
                # DF=pd.DataFrame([[mail_from], [mail_subject], [mail_content]])
                # print(DF)
                # if k==0:
                #     file=pd.DataFrame([[mail_from],[mail_subject],[mail_content]])
                #     file.to_csv("extractreport.csv")
                #     k+=1
                #     break
                # with open('exctractfile.csv', 'w') as f1:
                #     writer = csv.writer(f1, delimiter='\t', lineterminator='\n', )
                #     for i in range(1000000):
                #         for j in range(i + 1):
                #             file.append(newdata)
                #         file=[]
                #file=pd.DataFrame([[mail_from,1],[mail_subject],[mail_content]],columns=['Sender','Subject','BodyContent'])
                newdata = {
                    'Sender': [mail_from],
                    'Subject': [mail_subject],
                    'BodyContent': [mail_content]
                }

                file=pd.DataFrame(newdata)
                file.to_csv("extractreport.csv",mode='a',index=False, header=False)
print("Data added")
    #////////////
