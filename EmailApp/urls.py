from django.urls import path
from EmailApp import views


# TEMPLATE URLs
app_name = 'EmailApp'

urlpatterns = [
    path('', views.inbox, name='EmailApp-inbox'),
    path('sent/', views.sent, name='EmailApp-sentbox'),
    path('trashmail/', views.move_mesg_to_trash, name='EmailApp-move_to_trash'),
    path('starred/', views.mark_as_star, name='EmailApp-mark_as_star'),
    path('search_mails/', views.search_mails, name='EmailApp-search_mails'),
    path('trash/', views.trash, name='EmailApp-trash'),
    path('starred_mails/', views.starred, name='EmailApp-star'),
    path('compose/', views.compose, name='EmailApp-compose'),
    path('read_email/<str:messageid>/', views.read_email, name='EmailApp-read_email'),
    path('ajax/recognized/', views.handleSpeechRecognition,
         name='EmailApp-handleSpeechRecognition'),
    path('ajax/submit/',views.handleajaxsubmit,name="handleajaxsubmit"),

]


# handler404 = 'EmailApp.views.handle_not_found'