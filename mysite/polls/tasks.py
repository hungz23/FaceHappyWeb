from __future__ import absolute_import, unicode_literals
from celery import task
from celery.task.schedules import crontab
from celery.decorators import periodic_task


@periodic_task(run_every=(crontab(minute='*/1')), name="AlignImage", ignore_result=True)
def AlignImage():
    # aligneddirectory = os.path.join(os.curdir+"/Temp_Align/Image")
    # os.system("python ./facenet/src/align/align_dataset_mtcnn.py\
    #  ./Temp\
    #  ./Temp_Align\
    #  --image_size 182 --margin 44")
    os.mkdir("HUNG")
