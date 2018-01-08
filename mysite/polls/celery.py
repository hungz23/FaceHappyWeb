from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
from emotiondetection import predict_emotion

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
app = Celery('polls')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)





@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

from celery.task.schedules import crontab
from celery.decorators import periodic_task


def AlignImage():
    os.system("python ./facenet/src/align/align_dataset_mtcnn.py\
     ./Temp\
     ./Temp_Align\
     --image_size 182 --margin 44")
    os.system("rm ./Temp_Align/bounding*")
    os.system("rm ./Temp_Align/revision*")


def makeEmotion(email, L):
    from .models import Emotion
    print(L[0])
    print(L[1])
    print(L[2])
    print(L[3])
    print(L[4])
    print(L[5])
    emotion = Emotion(email=email,angry=L[0],fear=L[1],happy=L[2],sad=L[3],
    surprise=L[4],neutral=L[5])
    emotion.save()

def StrToNumericalList(string):
    strlist = string.split('[')[1].split(']')[0].split(',')
    numericallist = []
    for str in strlist:
        numericallist.append(float(str))
    return numericallist


def parser(path):
    f = open(path,"r")
    results = f.read().splitlines()
    rows = []
    for result in results:
        infos = result.split('\t')
        email = infos[0]
        emotionStr = infos[1]
        emotionL = StrToNumericalList(emotionStr)
        rows.append([email, emotionL])
    return rows



@periodic_task(run_every=(crontab(minute='*/1')), name="FaceDetect", ignore_result=True)
def FaceDetect():
    AlignImage()
    os.system("python ./facenet/src/classifier.py\
     CLASSIFY Temp_Align/\
     ModelsForTrain/20170511-185253.pb\
     models/lfw_classifier.pkl --batch 5")
    rows = parser(os.path.join(os.curdir+"/result.txt"))
    for row in rows:
        makeEmotion(row[0], row[1])
    #Delete Processed Files
    os.system("rm -rf Temp")
    os.system("rm -rf Temp_Align")
