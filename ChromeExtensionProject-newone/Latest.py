from string import punctuation
from prettytable import PrettyTable
from asyncio.windows_events import NULL
from email.quoprimime import body_check
import json
import re
from urllib import response
#from flask import Flask,request
import requests
import pandas as pd
from integration import *
import sqlite3
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from integration import *
response=requests.get('http://127.0.0.1:5000/unread')


sender=[]
sub=[]
hbody=[]
links=[]
data=len(response.json())
sr=response.json()

def preprocess_text(text):
          text = text.lower()  # Lowercase text
          text = re.sub(f"[{re.escape(punctuation)}]", "", text)  # Remove punctuation
          text = " ".join(text.split())  # Remove extra spaces, tabs, and new lines
          return text
     
 
nltk.download("stopwords")
stopwords_ = set(stopwords.words("english"))

connection=sqlite3.connect("Project.db",check_same_thread=False)
listofTabs = connection.execute("select name from sqlite_master where type='table' AND name='user'").fetchall()

if listofTabs!=[]:
    print("Table exist already")
    # connection.execute("drop table user")
    # connection.commit()
    # print("Table Creessfully")
else:
    connection.execute('''create table user(
                             ID integer primary key autoincrement,
                             dbbfrom text,
                             dbsubject text,
                             dbbody text,
                             dbhtmlbody text,
                             dbparsehtml text,
                             dblinks text
                             )''')
    print("Table Created Successfully")
    
cur = connection.cursor()

global urls
#urls=''
if response.status_code == 200 and data is not None:
        for i in range(data):
            getsender=sr[i]['from']
            getsub=sr[i]['subject']
            gethbody=sr[i]['html_body']
            getdate=sr[i]['date']
            getbody=sr[i]['body']
            #------------------------------------------
            #urls=[]
            urls = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', gethbody) 
            
            sender.append(sr[i]['from'])
            sub.append(sr[i]['subject'])
            hbody.append(sr[i]['html_body'])
            links.append(urls)
            #------------------------------------------
            df=pd.DataFrame(list(gethbody))
            # df.map(preprocess_text)
            sample_text=(preprocess_text(gethbody))
            clean_text = sample_text
            print(tuple(urls))
            print (links)
            tokens = clean_text.split()
            clean_tokens = [t for t in tokens if not t in stopwords_]
            clean_text = " ".join(clean_tokens)
            word_tokenize(clean_text)
            print(clean_text)
            #---------------------------
            connection.execute("INSERT INTO user (dbbfrom,dbsubject,dbbody,dbhtmlbody,dbparsehtml) VALUES ('"+getsender+"','"+getsub+"','"+getbody+"','"+gethbody+"','"+clean_text+"')")
            connection.commit()
            #connection.execute("INSERT INTO user (dbparsehtml) VALUES ('"+clean_text+"')")
        #print(urls)   
query = cur.execute("SELECT * FROM user").fetchall()   
table=PrettyTable(query)         
print(table)

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
mybody=[]
# Creating an instance of our class.
parser = Parser()

# Poviding the input.
#abc[0].encode('ascii','ignore').decode()
abc=cur.execute("SELECT dbbody FROM user as qw").fetchall()
print(abc)
for row in range(len(abc)):
  parser.feed(str(abc[row]))
  print("data:", all_data)
sub=cur.execute("SELECT dbsubject FROM user as qw").fetchall()
lsub=len(sub)
#date=
ocs=len(abc)
def Find(stringed): 
    # findall() has been used  
    # with valid conditions for urls in string 
      pattern1='https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
      #pattern1='http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
      url = re.findall(pattern1, stringed) 
      return url 
def is_phish(text_pred,url_pred,text_prob,url_prob):
        if(text_pred==1) and (url_pred==1):
            phishing = 1
        elif(text_pred==1) and (url_pred==0):
            if(text_prob>0.97):
                phishing = 1
            else:
                phishing = 0
        elif(text_pred==0) and (url_pred==1):
            if(url_prob>0.97):
                phishing = 1
            else:
                phishing = 0
        else:
            phishing = 0
        return phishing
for row in range(ocs):
    cleantext=abc[row]
    
    # url=Find(cleantext)
    # urls = [] 
    # for i in url: 
    #     if i not in urls: 
    #         urls.append(i)
    # print(urls)
    print('*'*30, 'MESSAGE', '*'*30)
    #print(string)
    text_prob,text_pred = text_prediction(cleantext)
    print(text_prob)
    if len(urls) == 0:
      url_prob = 0
      url_pred=0
    else:
      url_prob,url_pred = url_prediction(urls)

    print(url_prob)

    phishing = is_phish(text_pred,url_pred,text_prob,url_prob)
    print("final classify" +str(phishing))
    conn = sqlite3.connect('email_db.db')
    conn.execute('''INSERT INTO EMAIL (SENDER,MESSAGE_BODY,PHISHING,TEXT_PHISHING,URL_PHISHING)
    VALUES (?,?,?,?,?,?,?)''',(sender,cleantext,int(phishing),int(text_pred),int(url_pred)));
    conn.commit()
    conn.close()
for row in range(lsub):
    cleantext=sub[row]
    # url=Find(cleantext)
    # urls = [] 
    # for i in url: 
    #     if i not in urls: 
    #         urls.append(i)
    # print(urls)
    print('*'*30, 'MESSAGE', '*'*30)
    #print(string)
    text_prob,text_pred = text_prediction(cleantext)
    print(text_prob)
    if len(urls) == 0:
      url_prob = 0
      url_pred=0
    else:
      url_prob,url_pred = url_prediction(urls)

    print(url_prob)
    
    url=Find(cleantext)
    urls = [] 
    for i in url: 
        if i not in urls: 
            urls.append(i)
    print(urls)
    print('*'*30, 'MESSAGE', '*'*30)
    #print(string)
    text_prob,text_pred = text_prediction(cleantext)
    print(text_prob)
    if len(urls) == 0:
      url_prob = 0
      url_pred=0
    else:
      url_prob,url_pred = url_prediction(urls)

    print(url_prob)
    

    phishing = is_phish(text_pred,url_pred,text_prob,url_prob)
    print("final classify" +str(phishing))
    conn = sqlite3.connect('email_db.db')
    conn.execute('''INSERT INTO EMAIL (SENDER,SUBJECT,MESSAGE_BODY,PHISHING,TEXT_PHISHING,URL_PHISHING)
    VALUES (?,?,?,?,?,?,?)''',(sender,sub,cleantext,int(phishing),int(text_pred),int(url_pred)));
    conn.commit()
    conn.close()