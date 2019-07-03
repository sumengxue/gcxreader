#!/bin/python
width = 1100
height = 800
columnMargin = 5
rowMargin = 5
centerMargin = 80
fontSize = 14
lastRow = 10
lastReadingCharacters = 10000
#### Imports
import _thread
from tkinter import *
import tkinter.font as tkFont
import codecs
import time

#### New thread to prepare to write sitting (codes)
def readMyself():
    pythonFile = open(__file__, 'r')
    codes = pythonFile.read()
_thread.start_new_thread(readMyself, ())
#### GUI init
rootWindow = Tk()
rootWindow.title('gcxReader')
rootWindow.geometry(str(width) + 'x' + str(height))

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

#### thread calculating
def calculateMaxColumn():
    global textLength
    global calculatePointer
    global maxLine
    global text
    tempCharPixelWidth = normalFont.measure('cccc')
    tempLimit = (width - columnMargin * 2 - centerMargin) // 2
    while calculatePointer < textLength:
        tempLine = ''
        pixelFontLength = 0#tempCharPixelWidth
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
    originRow = nowRow
    xStart = rowMargin / height
    yStart = columnMargin / width
    rowHeight = (height - 2 * rowMargin) / rowLimit / height
    singlePageWidth = (width - columnMargin - centerMargin - columnMargin) / 2 / width
    while nowRow < expectedRow:
        Label(rootWindow, text = text2[maxColumn[nowRow]:maxColumn[nowRow + 1]], font = normalFont, justify = LEFT, anchor = N + W).place(relheight = rowHeight, relwidth = singlePageWidth, relx = xStart, rely = (nowRow - originRow) *  rowHeight + columnMargin / width)
        nowRow += 1

    xStart = (width / 2 + centerMargin / 2) / width
    expectedRow = min(nowRow + rowLimit, maxLine)
    originRow = nowRow
    while nowRow < expectedRow:
        Label(rootWindow, text = text2[maxColumn[nowRow]:maxColumn[nowRow + 1]], font = normalFont, justify = LEFT, anchor = N + W).place(relheight = rowHeight, relwidth = singlePageWidth, relx = xStart, rely = (nowRow - originRow) * rowHeight + columnMargin / width)
        nowRow += 1

#### Events listener
def turnLeft(event):
    global characterPointer
    global pointerListPointer
    global pointerList
    global nowRow
    rowStack.pop()
    nowRow = rowStack.pop()
    turnPage(event)

#### Environment init
welcomeMessage = "I am preparing for reading, please wait a minute..."
welcomeMessagePixelWidth = normalFont.measure(welcomeMessage)
Label(rootWindow, text = welcomeMessage, font = normalFont, justify = LEFT, anchor = N + W).place(relheight = 1, relwidth = 1, relx = (width - welcomeMessagePixelWidth) / 2 / width, rely = (height - fontSize) / 2 / height)
def closeWelcomeMessage():
    time.sleep(1)
    rootWindow.winfo_children()[0].destroy()
    turnPage(1)
_thread.start_new_thread(closeWelcomeMessage, ())

#### Events binds
rootWindow.bind('<Right>', turnPage)
rootWindow.bind('<Left>', turnLeft)

mainloop()
