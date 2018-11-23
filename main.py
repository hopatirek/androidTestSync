
from subprocess import Popen,PIPE,STDOUT
from time import time
import bs4
from androidKeyMaps import KEY_MAP
STR_OPENING_SQUARE_BRACKET = "["
STR_CLOSING_SQUARE_BRACKET = "]"
listOfPrevValues = []

def main():
    STR_POS_Y = "ABS_MT_POSITION_X"
    STR_POS_X = "ABS_MT_POSITION_Y"
    listOfPosWithTime = []

    streamFromAdb = Popen(["adb", "shell", "getevent", "-lt"],stdout=PIPE,stderr=STDOUT,bufsize=0)


    for line in iter(streamFromAdb.stdout.readline, b''):
          line = line.strip().decode('utf-8')
          timeParsed = parseTime(line)
          #print(line)

          if line.find(STR_OPENING_SQUARE_BRACKET)> -1:
              if len(listOfPosWithTime)>0:
                  currentTime = time()
                  if (len(listOfPosWithTime) == 1):
                    lastTime = time() # lasttime is initialised here
                    initialisePreviousValue()
                  if (currentTime - lastTime > 0.5):
                    getEventType(listOfPosWithTime)
                    listOfPosWithTime = []




          if line != '':
              if line.find(STR_POS_X) > 0:
                  posOfX = parsePosition(line, STR_POS_X)
                  listOfPosWithTime.insert(0, [timeParsed, posOfX, posOfY])
              elif line.find(STR_POS_Y) > 0:
                  posOfY = parsePosition(line, STR_POS_Y)




def initialisePreviousValue():
    Popen(["adb", "shell", "uiautomator", "dump"])
    outputXML = Popen(["adb", "shell", "cat", "/sdcard/window_dump.xml"],stdout=PIPE).communicate()[0]
    soup = bs4.BeautifulSoup(outputXML,'xml')
    editTextList = soup.findAll("node", {"class": "android.widget.EditText"})
    i = 0
    for editText in editTextList:
        listOfPrevValues.append(editText['text'])
        i=i+1

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
    lastIndexOfList = len(listOfPosWithTime)-1

    endTimeOfEvent = listOfPosWithTime[0][0]
    startTimeOfEvent = listOfPosWithTime[lastIndexOfList][0]
    intervalOfEvent = endTimeOfEvent - startTimeOfEvent


    firstWidth = str(listOfPosWithTime[lastIndexOfList][1])
    lastWidth = str(listOfPosWithTime[0][1])
    diffBetweenWidth = abs(int(lastWidth) - int(firstWidth))

    firstHeight = str(listOfPosWithTime[lastIndexOfList][2])
    lastHeight = str(listOfPosWithTime[0][2])
    diffBetHeight = abs(int(lastHeight) - int(firstHeight))

    if(textNotEntered()):
        if intervalOfEvent > 0.1:

            if diffBetHeight < 8 or diffBetweenWidth < 8:
                Popen(["adb", "shell", "input", "touchscreen", "swipe",
                       firstWidth,firstHeight,
                       firstWidth,firstHeight,
                       '1000'])
                print("Long Press")
            else:
                Popen(["adb", "shell", "input", "touchscreen", "swipe",
                       firstWidth, firstHeight,
                       lastWidth, firstHeight,
                       '1000'])
                print("Swipe")

        else:
            Popen(["adb", "shell", "input", "tap",
                   firstWidth, firstHeight])
            print("Click")





def textNotEntered():
    Popen(["adb", "shell", "uiautomator", "dump"])
    outputXML = Popen(["adb", "shell", "cat", "/sdcard/window_dump.xml"],stdout=PIPE).communicate()[0]
    soup = bs4.BeautifulSoup(outputXML,'xml')
    editTextList = soup.findAll("node", {"class": "android.widget.EditText"})
    i = 0
    for editText in editTextList:
        i = i + 1
        print(editText['text'])
        if len(listOfPrevValues)!=len(editText):
            compareAndType(editText['text'],listOfPrevValues[i])
            return False


    return True







def compareAndType(editText,prevEditText):
    lenOfEditText = len(editText)
    lenOfPrevEditText = len(prevEditText)
    if lenOfEditText < lenOfPrevEditText:
        for i in range(lenOfEditText-1,lenOfPrevEditText):
            Popen(["adb","shell","input","keyevent",KEY_MAP['BACKSLASH']])
    else:
        for i in range(lenOfPrevEditText-1,lenOfEditText):
            inputText = prevEditText[i]
            print(inputText)
            Popen(["adb", "shell", "input", "text",inputText])







    #print(soup.prettify())



main()