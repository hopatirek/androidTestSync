from  subprocess import Popen, PIPE,check_output,CalledProcessError
from time import time

STR_OPENING_SQUARE_BRACKET = "["
STR_CLOSING_SQUARE_BRACKET = "]"


def main():
    STR_POS_Y = "ABS_MT_POSITION_X"
    STR_POS_X = "ABS_MT_POSITION_Y"
    statusOfTouch = 0
    listOfPosWithTime = []
    streamFromAdb = Popen(["adb", "shell", "getevent", "-lt"], stderr=PIPE, stdout=PIPE)
    REF_TIME_DIFF = 1542840622
    timeOfRecordingOfEvent=0
    i=0
    while True:

          line = streamFromAdb.stdout.readline().decode('utf-8')
          line = line.strip()
          timeParsed = parseTime(line)

          if line.find(STR_OPENING_SQUARE_BRACKET)> -1:
              timeDiff = int(time() - timeParsed)
              #print("test", time() - timeParsed)

              if timeDiff!=REF_TIME_DIFF and statusOfTouch == 0:
                if len(listOfPosWithTime)>0:
                    getEventType(listOfPosWithTime)
                    timeOfRecordingOfEvent = time()

                #print("Not Equal ",listOfPosWithTime)
                listOfPosWithTime = []
                statusOfTouch=1
          if time()-timeOfRecordingOfEvent > 0.2:
              statusOfTouch = 0





          if line != '':
              #print('checking ',i)
              i=i+1
              if line.find(STR_POS_X) > 0:
                  posOfX = parsePosition(line, STR_POS_X)
                  listOfPosWithTime.insert(0, [timeParsed, posOfX, posOfY])




              if line.find(STR_POS_Y) > 0:
                  posOfY = parsePosition(line, STR_POS_Y)








          else:
            break




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
    if(intervalOfEvent>0.12):
        print("Long touch")
    else:
        print("Short touch")









main()