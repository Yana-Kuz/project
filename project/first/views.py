from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.context_processors import csrf
import datetime
from .forms import UserForm
from .forms import ltiForm
from .forms import ToolsForm
from .models import Tools
import oauth
import oauthlib
import math
import base64
import requests
from requests_oauthlib import OAuth2 as oauth2
from requests_oauthlib import OAuth1
import urllib
from hashlib import sha1

import binascii
import hashlib
import hmac
import webbrowser

from lti import ToolConsumer

def index(request):
    submitbutton= request.POST.get("submit")
    
    firstname=''
    lastname=''
    emailvalue=''
    
    form= UserForm(request.POST or None)
    if form.is_valid():
        firstname= form.cleaned_data.get("first_name")
        lastname= form.cleaned_data.get("last_name")
        emailvalue= form.cleaned_data.get("email")
    
    context= {'form': form, 'firstname': firstname,
              'lastname':lastname, 'submitbutton': submitbutton,
              'emailvalue':emailvalue}
    
    
    return render(request, 'index.html', context)


def lti(request):
    submitbutton= request.POST.get("submit")
    submitbutton = 'Submit'

    consumer_key = '185122693323-9c7rfjhot9fragcfs8c3lr02q2kgblra.apps.googleusercontent.com'
    consumer_secret = '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'
    

    Lti_message_type = ''
    Lti_version = ''
    Resource_link_id = ''
    Oauth_consumer_key = ''
    Oauth_signature_method = ''
    Oauth_version = ''
    Oauth_nonce = ''
    Oauth_timestamp = 0
    timest = math.floor(datetime.datetime.now().timestamp())

    form = ltiForm(request.POST or None)
    # if form.is_valid():
    '''Lti_message_type= form.cleaned_data.get("lti_message_type")
    Lti_version= form.cleaned_data.get("lti_version")
    Resource_link_id= form.cleaned_data.get("resource_link_id")
    Oauth_consumer_key= form.cleaned_data.get("oauth_consumer_key")
    Oauth_signature_method= form.cleaned_data.get("oauth_signature_method")
    Oauth_version= form.cleaned_data.get("oauth_version")'''
    Lti_message_type= "basic-lti-launch-request"
    Lti_version= "LTI-1p0"
    Resource_link_id= "resourceLinkId"
    Oauth_consumer_key= "jisc.ac.uk"
    Oauth_signature_method= "HMAC-SHA1"
    Oauth_version= "1.0"
    Oauth_nonce =  '' #base64.b64encode(str(timest).encode('utf-8'))
    Oauth_timestamp = '' # timest
        
    # client = requests.session()
    # # Retrieve the CSRF token first
    # client.get(url)  # sets cookie
    # csrftoken = client.cookies['csrftoken']
    # context = {}
    # context.update(csrf(request))
    for d in csrf(request):
        print(d,csrf(request)[d])
    c = csrf(request)['csrf_token']
    # c = csrftoken
    print('c',c)
    context= {'form': form, 'csrfmiddlewaretoken': c,
              'lti_message_type': Lti_message_type,
              'lti_version':Lti_version, 'oauth_consumer_key':Oauth_consumer_key, 
              'oauth_nonce': Oauth_nonce, 'oauth_signature_method':Oauth_signature_method,
              'oauth_timestamp':Oauth_timestamp, 'oauth_version':Oauth_version,
              'resource_link_id':Resource_link_id, 'submit': submitbutton}
        
    # print('context',context)

    Base_string = 'POST&'+urllib.parse.quote('https://lti.tools/saltire/tp',safe='')+'&'
    f = False
    for parametr in context:
        if parametr!='form':
            if f:
                Base_string+=urllib.parse.quote('&',safe='')
            f=True
            Base_string+=parametr+urllib.parse.quote('=',safe='')+urllib.parse.quote(str(context[parametr]),safe='')
    context['oauth_signature'] = oauthlib.oauth1.rfc5849.signature.sign_hmac_sha1(
        Base_string, 
        'secret', 
        '' # resource_owner_secret - not used
    )
    print('Base',Base_string)
    # key = b"secret&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"
    # raw = Base_string.encode('utf-8')
    # hashed = hmac.new(key, raw, sha1)
    # context['oauth_signature'] = hashed.digest().encode().rstrip('\n')
    return render(request,'lti.html',context)

tools = Tools.objects.all()
consumer = {}
for tool in tools:
    # print(tool.id, 'add')
    consumer[str(tool.id)] = ToolConsumer(
    consumer_key=tool.consumer_key,
    consumer_secret=tool.consumer_secret,
    launch_url=tool.launch_url,
    params={
        'lti_message_type': 'basic-lti-launch-request',
        'lti_version': "LTI-1p0",
        'resource_link_id': "resourceLinkId"
    }
    )


def lti_python(request):
    id_tool = request.GET.get("id", "11")
    print(consumer)
    return render(
        request,
        'lti_python.html',
        {
            'launch_data': consumer[id_tool].generate_launch_data(),
            'launch_url': consumer[id_tool].launch_url,
        }
    )

def add_tool(request):
    error = ''
    if request.method =='POST':
        form = ToolsForm(request.POST)
        if form.is_valid():
            consumer_key = form.cleaned_data.get("consumer_key")
            consumer_secret = form.cleaned_data.get("consumer_secret")
            launch_url = form.cleaned_data.get("launch_url")
            search = Tools.objects.in_bulk()
            for i in search:
                if search[i].launch_url == launch_url:
                    error = 'Такой инструмент уже есть'
                    break
            else:
                form.save()
                return redirect('all_tools')
        else:
            error = 'Форма была неверной'
    form = ToolsForm()
    context = {'form': form,
    'error': error}
    return render(request, 'add_tool.html', context)

def all_tool(request):
    Tools.objects.filter(launch_url='https://lti.tools/saltire/tpe').delete()
    tools = Tools.objects.all()
    # post_data = {'username': 'admin', 'password': '8975yAk2276#', 'service': 'gradebook'}
    # 770b45b6-b7bb-428d-8ee9-412836008071
    post_data = {'username': 'yaakuznetsova_1@edu.hse.ru', 'password': '8975yAk2276!', 'service': 'gradebook'}
    # response = requests.post('https://edu-test.hse.ru/login/token.php', data=post_data)
    # response = requests.post('http://localhost:8000/login/token.php', data=post_data)
    post_data = {'wstoken': '284e3ab4cef0a2f4daa86b3372560c3e', 'wsfunction': 'core_user_get_users_by_field', 'field': 'email', 'values': ['yaakuznetsova_1@edu.hse.ru'], 'moodlewsrestformat': 'json'}
    response = requests.post('https://edu-test.hse.ru/webservice/rest/server.php', data=post_data)
    # response = requests.post('https://edu-test.hse.ru/webservice/rest/server.php?wstoken=284e3ab4cef0a2f4daa86b3372560c3e&wsfunction=core_enrol_get_users_courses&userid=31635&moodlewsrestformat=json')
    content = response.content
    print(content)
    return render(request, "all_tool.html", {"tools": tools})

# "https://localhost/login/token.php?username=USERNAME&password=PASSWORD&service=SERVICESHORTNAME"
# post_data = {'username': 'admin', 'password': '8975yAk2276#', 'service': 'gradebook'}
# response = requests.post('https://localhost/login/token.php', data=post_data)
# content = response.content
# print(content)