# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.template import loader
import re
import os
import datetime

# import cv2
# import sys
# import json
# import time
# import numpy as np
# from keras.models import model_from_json

# # load json and create model arch
# json_file = open('model.json','r')
# loaded_model_json = json_file.read()
# json_file.close()
# model = model_from_json(loaded_model_json)

# # load weights into new model
# model.load_weights('model.h5')

# def predict_emotion(face_image_gray): # a single cropped face
#     resized_img = cv2.resize(face_image_gray, (48,48), interpolation = cv2.INTER_AREA)
#     # cv2.imwrite(str(index)+'.png', resized_img)
#     image = resized_img.reshape(1, 1, 48, 48)
#     list_of_list = model.predict(image, batch_size=1, verbose=1)
#     angry, fear, happy, sad, surprise, neutral = [prob for lst in list_of_list for prob in lst]
#     return [angry, fear, happy, sad, surprise, neutral]



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

def demo(request):
    import base64
    if request.method == 'POST':
        dirname = request.POST.get('email')
        directory = os.path.join(os.curdir+"/UserImage", dirname)
        if(not os.path.exists(directory)):
            os.mkdir(directory)
        data = request.POST.get('image','')
        if(data==''):
            return render(request, 'polls/demo.html', {'email': dirname})
        data = re.sub('data:image/png;base64,','',data)
        missing_padding = len(data) % 4
        imgdata = base64.b64decode(data)
        now = datetime.datetime.now()
        filename = directory+'/'+str(now).replace(":","")+".png"
        with open(filename, 'wb') as f:
            f.write(imgdata)
        return render(request, 'polls/demo.html', {'email': dirname})
    return render(request, 'polls/demo.html')
        
