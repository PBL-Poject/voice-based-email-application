from cProfile import label
import sys
import os
import json
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .gmail import MailManager
from django.http import HttpResponse
path = os.getcwd()
sys.path.insert(0, path + '/ml')
from ml_model import predict_intent, predict_entity
from .sentences import recognizedsentences
from fuzzywuzzy import fuzz, process 

# Create your views here.
services = MailManager()
profileInfo = services.service.users().getProfile(userId='me').execute()

def inbox(request):  
    finalmessage = services.getmails("INBOX")
    my_dictionary = json.dumps(finalmessage)
    # print(finalmessage)
    return render(request,'EmailApp/inbox.html',{'profileInfo':profileInfo,'allMessages':finalmessage,'username': services.username, 'my_dic':my_dictionary})


def sent(request):
    finalmessage = services.getmails("SENT")
    my_dictionary = json.dumps(finalmessage)
    return render(request,'EmailApp/sent.html',{'profileInfo':profileInfo,'allMessages':finalmessage,'username': services.username, 'my_dic':my_dictionary})


def trash(request):
    finalmessage = services.getmails("TRASH")
    my_dictionary = json.dumps(finalmessage)
    return render(request,'EmailApp/trash.html',{'profileInfo':profileInfo,'allMessages':finalmessage,'username': services.username, 'my_dic':my_dictionary})
    


def starred(request):
    finalmessage = services.getmails("STARRED")
    my_dictionary = json.dumps(finalmessage)
    # print(finalmessage)
    return render(request,'EmailApp/starred.html',{'profileInfo':profileInfo,'allMessages':finalmessage,'username': services.username, 'my_dic':my_dictionary})

    


def compose(request):
    if request.method == 'POST':
        receiver = request.POST.get('receipent')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # print(receiver,subject, message)
        returned = services.composemessage(str(profileInfo['emailAddress']), str(receiver),
                                          str(subject), str(message))
        services.service.users().messages().send(userId='me', body=returned).execute()
        return HttpResponseRedirect('/')
    else:
        return render(request, 'EmailApp/compose.html',{'profileInfo':profileInfo,'username': services.username})


    
def move_mesg_to_trash(request, messageid=None):
    if messageid == None:
        mesgId = request.POST.get('megid')
        # print(mesgId)
        services.move_to_trash(mesgId)
        return HttpResponseRedirect('/')
    else:
        print(messageid)
        services.move_to_trash(messageid)
        # inbox(request)
        # return redirect('/')
        finalmessage = services.getmails("INBOX")
        my_dictionary = json.dumps(finalmessage)
    # print(finalmessage)
        return render(request,'EmailApp/inbox.html',{'profileInfo':profileInfo,'allMessages':finalmessage,'username': services.username, 'my_dic':my_dictionary})

def mark_as_star(request, messageid=None):
    if messageid == None:
        messageid = request.GET.get('megid')
    message = services.readmail(messageid)
    if "STARRED" in message[0]["labelIds"]:
        services.remove_as_star(messageid)
    else:
        services.update_as_star(messageid)
    return HttpResponseRedirect('/read_email/'+ messageid +'/')
    
   


       



def read_email(request, *args, **kwargs):
    message = services.readmail(kwargs['messageid'])
    # print(message)
    return render(request,'EmailApp/read_email.html', {'profileInfo': profileInfo, 'message': message,'username': services.username})


def search_mails(request):
     if request.method == 'GET':
        searchtext = request.GET.get('searchfield')
        label = request.GET.get('labelname')
        # print(searchtext, label)
        finalmessage = services.search_mail(label, searchtext)
        return render(request,'EmailApp/search_mails.html',{'profileInfo':profileInfo,'allMessages':finalmessage,'username': services.username})


def handleSpeechRecognition(request):
    # String = request.GET.get('post_id')
    String = request.GET.get('post_id').replace("email", "mail")
    messageid = request.GET.get('post_mess_id')
    label = request.GET.get('post_label')
    process_text =  String.replace("mails", "mail")
    print(process_text, label)
    
    intent = predict_intent(process_text)
    entity = predict_entity(process_text)
    
    

    print(intent, entity)

    if "star" in process_text:
        goto = fuzz.WRatio("go to starred message", process_text)
        mark = fuzz.WRatio("mark this email as star", process_text)
        unmark = fuzz.WRatio("unmark this email", process_text)
        if goto > mark:
            if goto > unmark:
                print(goto, mark)
                data = recognizedsentences.get("go_to_star")
                print(data)
                return JsonResponse(data,safe=False)
            else: 
                mark_as_star(request, messageid) 
        else:
            mark_as_star(request, messageid)



    if intent[0] == "open_mail" and messageid != "":
        recognizedsentences["open_mail"]["url"] = "/read_email/"+messageid+"/"

        # print(recognizedsentences["open_mail"]["url"])

    if intent[0] == "delete_mail" and messageid != "":
        move_mesg_to_trash(request, messageid)
       
       

    if "search " in process_text:

        print("line 101 "+ process_text) 

        if intent[0] == "search_mail":
            index = entity.index('SRM')
            splited_text = process_text.split()[index]
            if splited_text != "":
                # http://127.0.0.1:8000/search_mails/?searchfield=medium&labelname=INBOX
                recognizedsentences["search_mail"]["url"] = "/search_mails/?searchfield="+splited_text+"&labelname="+ label
            
            if intent[0] in recognizedsentences.keys():
                data = recognizedsentences.get(intent[0])
                print(data)
            else:
                data = {"message":"error"}
            return JsonResponse(data,safe=False)
        
    if intent[0] in recognizedsentences.keys() and intent[0] != "search_mail":
        data = recognizedsentences.get(intent[0])
        print(data)
    else:
        data = {"message":"error"}
    return JsonResponse(data,safe=False)   

    

def handleajaxsubmit(request):
        receiver = request.GET.get('receiver')
        subject = request.GET.get('subject')
        message = request.GET.get('message')
        returned = services.composemessage(str(profileInfo['emailAddress']), str(receiver),
                                          str(subject), str(message))
        services.service.users().messages().send(userId='me', body=returned).execute()
        return JsonResponse({'status':'success'})


