# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.template import loader
import re
import os
import datetime

import cv2
import sys
import json
import time
import numpy as np
from keras.models import model_from_json
from django.conf.urls import url
from django.contrib.auth.decorators import user_passes_test

from django.contrib.admin.views.decorators import staff_member_required

import base64


def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)


from django.http import HttpResponse

from .models import Question


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))


def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})

# def demo(request):
# 	return render(request, 'polls/demo.html')

def getdata(request, inputname):
    dirname = request.POST.get('email')
    directory = os.path.join(os.curdir+"/UserImage", dirname)
    if(not os.path.exists(directory)):
        os.mkdir(directory)
    data = request.POST.get(inputname,'')
    if(data==''):
        return render(request, 'polls/imageup.html', {'email': dirname})
    data = re.sub('data:image/png;base64,','',data)
    missing_padding = len(data) % 4
    imgdata = base64.b64decode(data)
    now = datetime.datetime.now()
    filename = directory+'/'+str(now).replace(":","")+".png"
    with open(filename, 'wb') as f:
        f.write(imgdata)

def imageup(request):
    if request.method == 'POST':
        dirname = request.POST.get('email')
        directory = os.path.join(os.curdir+"/UserImage", dirname)
        if(not os.path.exists(directory)):
            os.mkdir(directory)
        getdata(request, "image0")
        getdata(request, "image1")
        getdata(request, "image2")
        getdata(request, "image3")
        getdata(request, "image4")
        getdata(request, "image5")
        getdata(request, "image6")
        getdata(request, "image7")
        getdata(request, "image8")
        getdata(request, "image9")
        getdata(request, "image10")
        return render(request, 'polls/imageup.html', {'email': dirname})
    return render(request, 'polls/imageup.html')

@staff_member_required
def align(request):
    os.system("export PYTHONPATH=/vagrant/django/FaceHappyWeb/mysite/facenet/src")
    os.system("python ./facenet/src/align/align_dataset_mtcnn.py\
     ./UserImage\
     ./UserImage_Align\
     --image_size 182 --margin 44")
    os.system("rm ./UserImage_Align/bounding_boxes*")
    os.system("rm ./UserImage_Align/revision_info")
    # response = "ALign complete"
    # HttpResponse(response)
    return redirect('/polls/')

@staff_member_required
def train(request):
    os.system("python ./facenet/src/classifier.py TRAIN\
     ./UserImage_Align\
     ./ModelsForTrain/20170511-185253.pb\
     ./models/lfw_classifier.pkl --batch_size 5")
    # response = "Training complete"
    # HttpResponse(response)
    return redirect('/polls/')

def makeEmotion(email, L):
    from .models import Emotion
    emotion = Emotion(email=email,angry=L[0],fear=L[1],happy=L[2],sad=L[3],
    surprise=L[4],neutral=L[5])
    emotion.save()

def getimage(request):
    import base64
    if request.method == 'POST':
        now = datetime.datetime.now()
        data = request.POST.get('image','')
        if(data==''):
            return render(request, 'polls/webcam.html')
        directory = os.path.join(os.curdir+"/Temp/Image")
        os.mkdir("Temp")
        os.mkdir("Temp/"+str(now).replace(":",""))
        aligneddirectory = os.path.join(os.curdir+"/Temp_Align/"+str(now).replace(":",""))
        data = re.sub('data:image/png;base64,','',data)
        missing_padding = len(data) % 4
        imgdata = base64.b64decode(data)
        filename = directory+'/'+str(now).replace(":","")+".png"
        alignedfilename = aligneddirectory + '/'+str(now).replace(":","")+".png"
        with open(filename, 'wb') as f:
            f.write(imgdata)
        os.system("export PYTHONPATH=./facenet/src")
        os.system("python ./facenet/src/align/align_dataset_mtcnn.py\
         ./Temp\
         ./Temp_Align\
         --image_size 182 --margin 44")
        imgdata = cv2.imread(alignedfilename, 0)
        L = predict_emotion(imgdata)
        os.system("python ./facenet/src/classifier.py\
         CLASSIFY Temp_Align/\
         ModelsForTrain/20170511-185253.pb\
         models/lfw_classifier.pkl --batch 5")
        f = open("result.txt","r")
        email = f.read().splitlines()[0]
        makeEmotion(email,L)
        os.system("rm -rf Temp")
        os.system("rm -rf Temp_Align")
        return render(request, 'polls/webcam.html')
    return render(request, 'polls/webcam.html')

def standardstring(string):
    return string.replace(":","").replace(" ","")

def uploademotion(request):
    import base64
    data = request.POST.get('image','')
    if request.method == 'POST':
        now = datetime.datetime.now()
        nowname = standardstring(str(now))
        data = request.POST.get('image','')
        if(data==''):
            return render(request, 'polls/webcam.html')
        tempdirectory = os.path.join(os.curdir+"/Temp")
        directory = os.path.join(os.curdir+"/Temp/"+nowname+"/"+nowname)
        if(not os.path.exists(tempdirectory)):
            os.mkdir("Temp")
        if(not os.path.exists(directory)):
            os.mkdir("Temp/"+nowname)
            os.mkdir("Temp/"+nowname+"/"+nowname)
        data = re.sub('data:image/png;base64,','',data)
        missing_padding = len(data) % 4
        imgdata = base64.b64decode(data)
        filename = directory+'/'+str(now).replace(":","")+".png"
        with open(filename, 'wb') as f:
            f.write(imgdata)
    return render(request, 'polls/webcam.html')
