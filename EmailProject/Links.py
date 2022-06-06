# import http
# from urllib import response
# import httplib2
# from bs4 import BeautifulSoup,SoupStrainer

# url='http://127.0.0.1:5000/unread'
# http=httplib2.Http()
# response,content = http.request(url)
# links=[]
# for link in BeautifulSoup(content).find_all('a',href=True):
#     links.append(link['href'])

# for link in links:
#     print(links)


# from prettytable import PrettyTable
# from asyncio.windows_events import NULL
# from email.quoprimime import body_check
# import json
# import re
# from urllib import response
# import requests
# response=requests.get('http://127.0.0.1:5000/unread')
# #print(response.status_code)
# #print(response.json())
# sender=[]
# sub=[]
# hbody=[]
# data=len(response.json())
# sr=response.json()


#body1=response.json()[0]['subject']
# data=response.text
# json.loads(data)
# #sub=parse_json['subject']
# print(sub)

# if response.status_code == 200:
#         for i in range(data):
#             sender.append(sr[i]['from'])
#             sub.append(sr[i]['subject'])
#             hbody.append(sr[i]['html_body'])

        # for i in response.json()[c]['subject']:
            # res.append(response.json()[0]['subject'])
            # c+=1
# print(f"sdetails: {sender}")
# print(f"subdetails: {sub}")
# print(f"hbodydetails: {hbody}")



import sqlite3

connection=sqlite3.connect("Project.db",check_same_thread=False)
listofTabs = connection.execute("select name from sqlite_master where type='table' AND name='user'").fetchall()

if listofTabs!=[]:
    print("Table exist already")
else:
    connection.execute('''create table user(
                             ID integer primary key autoincrement,
                             dbbfrom text,
                             dbsubject text,
                             dbhtmlbody text,
                             dbparsehtml text,
                             dblinks text
                             )''')
    print("Table Created Successfully")
cur = connection.cursor()
# if response.status_code == 200:
#         for i in range(data):
#             getsender=sr[i]['from']
#             getsub=sr[i]['subject']
#             gethbody=sr[i]['html_body']
#             # sender.append(sr[i]['from'])
#             # sub.append(sr[i]['subject'])
#             # hbody.append(sr[i]['html_body'])
#             connection.execute("INSERT INTO user (dbbfrom,dbsubject,dbhtmlbody) VALUES ('"+getsender+"','"+getsub+"','"+gethbody+"')")
#             connection.commit()
# query = cur.execute("SELECT * FROM user").fetchall()   
# table=PrettyTable(query)         
# print(table)


#############

# parsed data //html parser

##############
# abc=cur.execute("SELECT dbhtmlbody FROM user as qw").fetchall()
# ocs={}
# for row in abc:
#     #ocs[row[0]]=int(row[0])
#     print(row)
from html.parser import HTMLParser
class Parser(HTMLParser):
  # method to append the start tag to the list start_tags.
  def handle_starttag(self, tag, attrs):
    global start_tags
    start_tags.append(tag)
    # method to append the end tag to the list end_tags.
  def handle_endtag(self, tag):
    global end_tags
    end_tags.append(tag)
  # method to append the data between the tags to the list all_data.
  def handle_data(self, data):
    global all_data
    all_data.append(data)
  # method to append the comment to the list comments.
  def handle_comment(self, data):
    global comments
    comments.append(data)
start_tags = []
end_tags = []
all_data = []
comments = []
# Creating an instance of our class.
parser = Parser()
# Poviding the input.
#abc[0].encode('ascii','ignore').decode()
abc=cur.execute("SELECT dbhtmlbody FROM user as qw").fetchall()
ocs=len(abc)
for row in range(ocs):
    #ocs[row[0]]=int(row[0])
    print(abc[row])
    parser.feed(str(abc[row]))
    print("start tags:", start_tags)
    print("end tags:", end_tags)
    print("data:", all_data)
    print("comments", comments)





# d = requests.request.get("http://127.0.0.1:5000/unread")
# d = d.json()
# componentrs = d["body"]["from"]["html_body"]["subject"]

# response=requests.get('http://127.0.0.1:5000/unread')
# body=response.json()[0]['body']
# sub=response.json()[0]['subject']
# hbody=response.json()[0]['html_body']
# d=response.json()
# componentrs = d["body"]["from"]["html_body"]["subject"]
# for dr in componentrs:
#     name = dr["familyName"]
#     number = dr["permanentNumber"]
#     prod={}
#     newinsert=cur.execute('''INSERT INTO user(dbbody,dbsubject,dbhtmlbody) VALUES(body,subject,html_body)''')    
#     val = (name,number)
#     cur.execute(sql,val)
