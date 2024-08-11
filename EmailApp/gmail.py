from __future__ import print_function
import base64
import re
from bs4 import BeautifulSoup
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://mail.google.com/',
         'https://www.googleapis.com/auth/gmail.labels',
         'https://www.googleapis.com/auth/userinfo.profile',
         'https://www.googleapis.com/auth/gmail.addons.current.action.compose']

basedir = os.path.abspath(os.path.dirname(__file__))
data_json = basedir +'/credentials.json'

class MailManager:
    def __init__(self):
        self.creds = None
        self.service = None
        self.managecredentials()
        self.username = ""
        

    def managecredentials(self):
         # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(data_json, SCOPES)
                self.creds = flow.run_local_server(host='127.0.0.1',port=8080)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)
        self.service = build('gmail', 'v1', credentials=self.creds)

    def getmails(self,label):
        
        allMessages = self.service.users().messages().list(userId='me',includeSpamTrash= False,labelIds= label, maxResults=12).execute()
        messageList = []

        if 'messages' in allMessages:
            for message in allMessages['messages']:
                messageList.append(self.service.users().messages().get(userId='me', id=message['id']).execute())
        finalmessage = self.cleanmessage(messageList)
        
        if label == "INBOX":
            self.username = finalmessage[0]["receiver_name"]
        # print(self.username, "username")
        return finalmessage

    def cleanmessage(self,messageList):
        finalmessage = []
        for mes in messageList:
            tempdic = {}
            tempdic["snippet"] =  mes["snippet"]
            tempdic["messageid"] = mes["threadId"]

            if 'parts' in mes['payload']:
                if mes['payload']['parts'][0]['mimeType'] == 'multipart/alternative':
                    part_data = mes['payload']['parts'][0]['parts'][0]['body']['data']    
                else:
                     part_data = mes['payload']['parts'][0]['body']['data']   
            else:
                part_data = mes['payload']['body']['data']
             
# payload.body.data
            clean_one = part_data.replace("-","+") 
            clean_one =clean_one.replace("_","/")
            clean_two = base64.b64decode (bytes(clean_one, 'UTF-8')) # decoding from Base64 to UTF-8
            soup = BeautifulSoup(clean_two , "lxml" )
            mssg_body = soup.body()
            

            x = re.sub("[\(\[].*?[\)\]]", "", str(mssg_body[0]))
            y = re.sub("[\<\[].*?[\>\]]", "", x)
            z = re.sub('(?:\s)https[^, ]*', '', y)
            u = re.sub('(?:\s)http[^, ]*', '', z)
            w = re.sub('(?<!Dr)(?<!Esq)\. +(?=[A-Z])','.\n',u)
            mystring = w.replace('\t', '\n \1').replace('\r', '')
            final_string = "\n".join(mystring.splitlines())
           

            tempdic["fullmessage"]= final_string
            if "UNREAD" in mes["labelIds"]:
                tempdic["readstatus"] = "unread"
            else:
                tempdic["readstatus"] = "read"
            
            if "STARRED" in mes["labelIds"]:
                tempdic["starstatus"] = "fa-star-o"
                
            else:
                tempdic["starstatus"] = "fa-star"
               
            tempdic["labelIds"] = mes["labelIds"]
            for m in mes["payload"]["headers"]:
                if m["name"].upper() == "FROM":
                    sender_name = ""
                    sender_email = ""
                    for i in m["value"]:
                        if i == "<":
                            sender_email = m["value"][m["value"].index('<')+1: m["value"].index('>')]
                            break

                        else:
                            sender_name += i
                    tempdic["sender_name"] = sender_name
                    tempdic["sender_email"] = sender_email
                elif m["name"].upper() == "TO":
                    receiver_name = ""
                    receiver_email = ""
                    for i in m["value"]:
                        if i == "<":
                            receiver_email = m["value"][m["value"].index('<')+1: m["value"].index('>')]
                            break

                        else:
                            receiver_name += i
                    if receiver_email == "":
                        receiver_email = receiver_name
                    tempdic["receiver_name"] = receiver_name
                    tempdic["receiver_email"] = receiver_email
                elif m["name"].upper() == "SUBJECT":
                    tempdic["subject"]= m["value"]

                elif m["name"].upper() == "DATE":
                    tempdic["date"]= m["value"]
                
            
            finalmessage.append(tempdic)
        
        
        return finalmessage
        

    def composemessage(self,sender, to, subject, message_text):
        """Create a message for an email.

        Args:
            sender: Email address of the sender.
            to: Email address of the receiver.
            subject: The subject of the email message.
            message_text: The text of the email message.

        Returns:
            An object containing a base64url encoded email object.
        """
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        b64_bytes = base64.urlsafe_b64encode(message.as_bytes())
        b64_string = b64_bytes.decode('utf-8')
        return  {'raw': b64_string}
        

    def readmail(self, megid):
        messageList = []
        messageList.append(self.service.users().messages().get(userId='me', id=megid).execute())
        # print(self.cleanmessage(messageList))
        self.service.users().messages().modify(userId='me', id=megid, body={'removeLabelIds': ['UNREAD']}).execute()

        return (self.cleanmessage(messageList)) 

    def search_mail(self,label,q):
        allMessages = self.service.users().messages().list(userId='me',includeSpamTrash= False,labelIds= label, maxResults=12,q=q).execute()
        messageList = []
        if 'messages' in allMessages:
            for message in allMessages['messages']:
                messageList.append(self.service.users().messages().get(userId='me', id=message['id']).execute())
        finalmessage = self.cleanmessage(messageList)
        return finalmessage



    def move_to_trash(self, megid):
        self.service.users().messages().trash(userId='me', id=megid).execute()
        print('Message with id: %s trashed successfully.' % megid)
        return

    def update_as_star(self, megid):
        print("inside update label function", megid)
        self.service.users().messages().modify(userId='me', id=megid, body={'addLabelIds': ['STARRED']}).execute()
        print('Message with id: %s starred successfully.' % megid)
        return
    
    def remove_as_star(self, megid):
        print("inside update label function", megid)
        self.service.users().messages().modify(userId='me', id=megid, body={'removeLabelIds': ['STARRED']}).execute()
        print('Message with id: %s unstarred successfully.' % megid)
        return

if __name__ == '__main__':
     obj = MailManager()
    