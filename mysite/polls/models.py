# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

#import webcam.admin # needed to show the right widget in the admin
from django.db import models
from django import forms
import datetime
import os

class Question(models.Model):
    question_text = models.CharField(max_length=256)
    pub_date = models.DateTimeField(default = datetime.date.today())


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

class Emotion(models.Model):
    email = models.EmailField()
    angry = models.FloatField()
    fear = models.FloatField()
    happy = models.FloatField()
    sad = models.FloatField()
    surprise = models.FloatField()
    neutral = models.FloatField()
    date = models.DateTimeField(default = datetime.date.today())

class Training(models.Model):
    name = models.CharField(max_length=256)
    def train():
        os.system("python src/align/align_dataset_mtcnn.py\
         ./UserImage\
         ./UserImage_Align\
         --image_size 182 --margin 44")
