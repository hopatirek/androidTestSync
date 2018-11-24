
from subprocess import Popen,PIPE,STDOUT
from time import sleep,time
import bs4
from androidKeyMaps import KEY_MAP
STR_OPENING_SQUARE_BRACKET = "["
STR_CLOSING_SQUARE_BRACKET = "]"
listOfPrevValues = []
master = "192.168.0.104:5000"
slave = "TA99300IWW"
def main():
    STR_POS_Y = "ABS_MT_POSITION_X"
    STR_POS_X = "ABS_MT_POSITION_Y"
    listOfPosWithTime = []
    initialisePreviousValue()
    streamFromAdb = Popen(["adb", "-s", master, "shell", "getevent", "-lt"],stdout=PIPE,stderr=STDOUT,bufsize=0)


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
                  if (currentTime - lastTime > 1):
                    getEventType(listOfPosWithTime)
                    listOfPosWithTime = []





          if line != '':
              if line.find(STR_POS_X) > 0:
                  posOfX = parsePosition(line, STR_POS_X)
                  listOfPosWithTime.insert(0, [timeParsed, posOfX, posOfY])
              elif line.find(STR_POS_Y) > 0:
                  posOfY = parsePosition(line, STR_POS_Y)




def initialisePreviousValue():
    Popen(["adb", "-s", master, "shell", "uiautomator", "dump"])
    outputXML = Popen(["adb", "-s", master, "shell", "cat", "/sdcard/window_dump.xml"],stdout=PIPE).communicate()[0]
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

            if diffBetHeight < 16 or diffBetweenWidth < 16:
                Popen(["adb", "-s", slave, "shell", "input", "touchscreen", "swipe",
                       firstHeight, firstWidth,
                       firstHeight, firstWidth,    
                       '1000'])
                print("Long Press")
            else:
                Popen(["adb", "-s", slave, "shell", "input", "touchscreen", "swipe",
                       firstHeight, firstWidth,
                       lastHeight, lastWidth,
                       '1000'])
                print("Swipe")

        else:
            Popen(["adb", "-s", slave, "shell", "input", "tap",
                   firstWidth, firstHeight])
            print("Click")



def getEditText(device):
    Popen(["adb", "-s", master, "shell", "uiautomator", "dump"])
    outputXML = Popen(["adb", "-s", device, "shell", "cat", "/sdcard/window_dump.xml"],stdout=PIPE).communicate()[0]
    soup = bs4.BeautifulSoup(outputXML,'xml')
    editTextList = soup.findAll("node", {"class": "android.widget.EditText"})
    return editTextList




def textNotEntered():
    editTextList =  getEditText(master)

    for i in range(len(editTextList)):

        while editTextList[i]['focused']=="true" :
            editTextList =  getEditText(master)
            sleep(0.1)
            if len(editTextList)>0:
                editTextList[i]['password']='false'
                print("hey",editTextList[i]['text'])
                textEntered = editTextList[i]['text']
            if len(editTextList)<=0 or editTextList[i]['focused']=="false":
                typeInSlave(textEntered,i)
                return False




    return True







def typeInSlave(textToBeEntered,currentEditText):
     editTextList =  getEditText(slave)
     positionOfEditText = editTextList[currentEditText]['bounds']
     bound_X = int(positionOfEditText[positionOfEditText.find("[")+1:positionOfEditText.find(",")]) +1
     bound_Y = int(positionOfEditText[positionOfEditText.find(",")+1:positionOfEditText.find("]")]) +1
     print(bound_X,bound_Y)
     Popen(["adb", "-s", slave, "shell", "input", "tap",str(bound_X),str(bound_Y)])
     sleep(2)
     Popen(["adb", "-s", slave, "shell", "input", "text",textToBeEntered])






    #print(soup.prettify())



main()