
from subprocess import Popen,PIPE,STDOUT
from time import time
import bs4
import  sys
STR_OPENING_SQUARE_BRACKET = "["
STR_CLOSING_SQUARE_BRACKET = "]"
def main():
    STR_POS_Y = "ABS_MT_POSITION_X"
    STR_POS_X = "ABS_MT_POSITION_Y"
    statusOfTouch = 0
    flag = 0
    listOfPosWithTime = []
    REF_TIME_DIFF = 1542649043

    streamFromAdb = Popen(["adb", "shell", "getevent", "-lt"],stdout=PIPE,stderr=STDOUT,bufsize=0)

    timeOfRecordingOfEvent=0

    for line in iter(streamFromAdb.stdout.readline, b''):
          line = line.strip().decode('utf-8')
          timeParsed = parseTime(line)
          #print(line)

          if line.find(STR_OPENING_SQUARE_BRACKET)> -1:
              timeDiff = int(time() - timeParsed)
              if flag == 0:
                  REF_TIME_DIFF = time() - timeParsed # defined ref time difference
                  flag = 1

              if timeDiff!=REF_TIME_DIFF and statusOfTouch == 0 and len(listOfPosWithTime)>0:
                    getEventType(listOfPosWithTime)
                    timeOfRecordingOfEvent = time()
                    listOfPosWithTime = []
                    statusOfTouch=1
          if time()-timeOfRecordingOfEvent > 0.5:
              statusOfTouch = 0


          if line != '':
              if line.find(STR_POS_X) > 0:
                  posOfX = parsePosition(line, STR_POS_X)
                  listOfPosWithTime.insert(0, [timeParsed, posOfX, posOfY])
              elif line.find(STR_POS_Y) > 0:
                  posOfY = parsePosition(line, STR_POS_Y)





def parseTime(line):

    if STR_OPENING_SQUARE_BRACKET in line:
        startOfSquareBracket = line.find(STR_OPENING_SQUARE_BRACKET)+len(STR_OPENING_SQUARE_BRACKET)
        stopOfSquareBracket = line.find(STR_CLOSING_SQUARE_BRACKET)
        timeInBracket = line[startOfSquareBracket:stopOfSquareBracket].strip()
        return float(timeInBracket)



def parsePosition(line, STR_POS):
    startOfpos = line.find(STR_POS) + len(STR_POS)
    stopOfpos = len(line)
    posString = line[startOfpos:stopOfpos].strip()
    pos = int(posString, 16)
    return pos

def getEventType(listOfPosWithTime):
    lenOfList = len(listOfPosWithTime)
    endTimeOfEvent = listOfPosWithTime[0][0]
    startTimeOfEvent = listOfPosWithTime[lenOfList-1][0]

    intervalOfEvent = endTimeOfEvent - startTimeOfEvent
    print(intervalOfEvent,listOfPosWithTime)

    getTextEntered()
    if(intervalOfEvent>0.07):
        print("Long touch")
    else:
        print("Short touch")



def getTextEntered():

    Popen(["adb", "shell", "uiautomator", "dump"])
    outputXML = Popen(["adb", "shell", "cat", "/sdcard/window_dump.xml"],stdout=PIPE).communicate()[0]
    soup = bs4.BeautifulSoup(outputXML,'xml')
    editTextList = soup.findAll("node", {"class": "android.widget.EditText"})
    for editText in editTextList:
        print(editText['text'])

    #print(soup.prettify())



main()