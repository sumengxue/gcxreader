#!/bin/python
lastReadingCharacters = 10000
width = 1100
height = 800
columnMargin = 100
rowMargin = 10
centerMargin = 80
fontSize = 14
lastRow = 10
foreGroundColor = 'grey'
backGroundColor = 'white'
#### Imports
import _thread
from tkinter import *
import tkinter.font as tkFont
import codecs
import time

#### GUI init
rootWindow = Tk()
rootWindow.title('gcxReader')
windowPositionX = (rootWindow.winfo_screenwidth() - width) / 2
windowPositionY = (rootWindow.winfo_screenheight() - height) / 2
rootWindow.geometry('%dx%d+%d+%d' % (width, height, windowPositionX, windowPositionY))
rootWindow.configure(bg = backGroundColor)

#### Read bookValue
normalFont = tkFont.Font(family = 'Source Code Pro', size = fontSize)
text = codecs.open(sys.argv[1], 'r', 'gbk').read()
text2 = text.replace('\r', ' ').replace('\n', ' ')

#### Global varibles
characterPointer = lastReadingCharacters
rowLimit = (height) // (fontSize * 2.55)
nowRow = 0
rowStack = []
textLength = len(text)
calculatePointer = lastReadingCharacters
maxColumn = []
maxLine = 0
pythonFile = 0
otherCodes = 0
#### New thread to prepare to write sitting (codes)
def readMyself():
    global pythonFile
    global otherCodes
    pythonFile = open(__file__, 'r')
    pythonFile.readline()
    pythonFile.readline()
    otherCodes = pythonFile.read()
_thread.start_new_thread(readMyself, ())

#### thread calculating
def calculateMaxColumn():
    global textLength
    global calculatePointer
    global maxLine
    global text
    tempLimit = (width - columnMargin * 2 - centerMargin) // 2
    while calculatePointer < textLength:
        tempLine = ''
        pixelFontLength = fontSize * 1.5
        while pixelFontLength < tempLimit and calculatePointer < textLength:
            if text[calculatePointer] == '\n' or text[calculatePointer] == '\r':
                calculatePointer += 1
                break
            else:
                tempLine += text[calculatePointer]
                calculatePointer += 1
            pixelFontLength += normalFont.measure(text[calculatePointer - 1])
        maxColumn.append(calculatePointer)
        maxLine += 1
_thread.start_new_thread(calculateMaxColumn, ())

#### display
def turnPage(event):
    global rowLimit
    global pointerList
    global pointerListPointer
    global nowRow
    global text2

    rowStack.append(nowRow)
    for widget in rootWindow.winfo_children():
        widget.destroy()
    expectedRow = min(nowRow + rowLimit, maxLine)
    rowHeight = (height - 2 * rowMargin) / rowLimit / height
    originRow = nowRow
    relx = columnMargin / height
    yStart = columnMargin / width
    relheight = (height - 2 * rowMargin) / rowLimit / height
    relwidth = (width - columnMargin - centerMargin - columnMargin) / 2 / width
    while nowRow < expectedRow:
        rely = (nowRow - originRow) *  rowHeight + rowMargin / width
        Label(rootWindow, text = text2[maxColumn[nowRow]:maxColumn[nowRow + 1]], font = normalFont, fg = foreGroundColor, bg = backGroundColor, justify = LEFT, anchor = N + W).place(relheight = relheight, relwidth = relwidth, relx = relx, rely = rely)
        nowRow += 1


    expectedRow = min(nowRow + rowLimit, maxLine)
    originRow = nowRow
    relx = (width / 2 + centerMargin / 2) / width
    while nowRow < expectedRow:
        rely = (nowRow - originRow) *  rowHeight + rowMargin / width
        Label(rootWindow, text = text2[maxColumn[nowRow]:maxColumn[nowRow + 1]], font = normalFont, fg = foreGroundColor, bg = backGroundColor, justify = LEFT, anchor = N + W).place(relheight = relheight, relwidth = relwidth, relx = relx, rely = rely)
        nowRow += 1

        rootWindow.title('%.1f' % (maxColumn[nowRow - 1] / textLength * 100) + '%')

#### Events listener
def turnLeft(event):
    global characterPointer
    global pointerListPointer
    global pointerList
    global nowRow
    rowStack.pop()
    nowRow = rowStack.pop()
    turnPage(event)

#### Close with Saving
def closeWithSaving():
    global otherCodes
    newScriptFileValue = '#!/bin/python\nlastReadingCharacters = ' + str(maxColumn[nowRow]) + '\n' + otherCodes
    print(newScriptFileValue)
    exit(0)

#### Environment init
welcomeMessage = "I am preparing for reading, please wait a minute..."
welcomeMessagePixelWidth = normalFont.measure(welcomeMessage)
Label(rootWindow, text = welcomeMessage, font = normalFont, justify = LEFT, fg = foreGroundColor, bg = backGroundColor, anchor = N + W).place(relheight = 1, relwidth = 1, relx = (width - welcomeMessagePixelWidth) / 2 / width, rely = (height - fontSize) / 2 / height)
def closeWelcomeMessage():
    time.sleep(1)
    rootWindow.winfo_children()[0].destroy()
    turnPage(1)
_thread.start_new_thread(closeWelcomeMessage, ())

#### Events binds
rootWindow.bind('<Right>', turnPage)
rootWindow.bind('<Left>', turnLeft)
rootWindow.protocol('WM_DELETE_WINDOW', closeWithSaving)
mainloop()
