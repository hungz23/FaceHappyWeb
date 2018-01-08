from polls.models import Emotion
import os

def AlignImage():
    os.system("python ./facenet/src/align/align_dataset_mtcnn.py\
     ./Temp\
     ./Temp_Align\
     --image_size 182 --margin 44")
    os.system("rm ./Temp_Align/bounding*")
    os.system("rm ./Temp_Align/revision*")


def makeEmotion(email, L):
    print("L..............")
    print(email)
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



AlignImage()
os.system("python ./facenet/src/classifier.py\
 CLASSIFY Temp_Align/\
 ModelsForTrain/20170511-185253.pb\
 models/lfw_classifier.pkl --batch 5")
rows = parser(os.path.join(os.curdir+"/result.txt"))
for row in rows:
    makeEmotion(row[0], row[1])
#Delete Processed Files
# os.system("rm -rf Temp")
# os.system("rm -rf Temp_Align")
