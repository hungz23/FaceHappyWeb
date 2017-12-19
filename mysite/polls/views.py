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

# load json and create model arch
json_file = open('model.json','r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)

# load weights into new model
model.load_weights('model.h5')

def predict_emotion(face_image_gray): # a single cropped face
    resized_img = cv2.resize(face_image_gray, (48,48), interpolation = cv2.INTER_AREA)
    # cv2.imwrite(str(index)+'.png', resized_img)
    image = resized_img.reshape(1, 1, 48, 48)
    list_of_list = model.predict(image, batch_size=1, verbose=1)
    angry, fear, happy, sad, surprise, neutral = [prob for lst in list_of_list for prob in lst]
    return [angry, fear, happy, sad, surprise, neutral]



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

def imageup(request):
    import base64
    if request.method == 'POST':
        dirname = request.POST.get('email')
        directory = os.path.join(os.curdir+"/UserImage", dirname)
        if(not os.path.exists(directory)):
            os.mkdir(directory)
        data = request.POST.get('image','')
        if(data==''):
            return render(request, 'polls/imageup.html', {'email': dirname})
        data = re.sub('data:image/png;base64,','',data)
        missing_padding = len(data) % 4
        imgdata = base64.b64decode(data)
        now = datetime.datetime.now()
        filename = directory+'/'+str(now).replace(":","")+".png"
        with open(filename, 'wb') as f:
            f.write(imgdata)
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
        data = request.POST.get('image','')
        if(data==''):
            return render(request, 'polls/webcam.html')
        directory = os.path.join(os.curdir+"/Temp/Image")
        os.mkdir("Temp")
        os.mkdir("Temp/Image")
        aligneddirectory = os.path.join(os.curdir+"/Temp_Align/Image")
        data = re.sub('data:image/png;base64,','',data)
        missing_padding = len(data) % 4
        imgdata = base64.b64decode(data)
        now = datetime.datetime.now()
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
