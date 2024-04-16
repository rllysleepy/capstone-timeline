import sys
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from datetime import datetime
import event_dialog
import json
import os

class MainWindow(QMainWindow):
    def __init__(self, *args, parent=None):
        super().__init__(*args, parent=parent)
        self.setWindowTitle("Timeline")
        self.resize(1000,500)
        self.readEvents()
        self.initUI()
        self.loadTimeline()

    def initUI(self):
        self.toolbar=QToolBar()
        self.toolbar.addAction("New Event",self.newEventDialog)
        self.addToolBar(self.toolbar)

    def loadTimeline(self):
        self.drawScene=QGraphicsScene()
        self.drawView=QGraphicsView()
        self.drawView.setScene(self.drawScene)
        self.setCentralWidget(self.drawView)

        unit_len=200
        winH=self.window().height()
        winW=self.window().width()
        padX=30
        padY=70
        unitPen=QPen(Qt.GlobalColor.gray)
        unitPen.setWidth(2)
        unitBrush=QBrush(Qt.GlobalColor.white)
        unitPalette=[] #Qt.GlobalColor

        self.drawView.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.drawView.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.drawView.setRenderHint(QPainter.RenderHint.Antialiasing)

        # units
        dist=0
        self.drawScene.addRect(QRectF(QPointF(0,(winH/2)-20),QPointF(dist+padX,(winH/2)+20)), QPen(Qt.GlobalColor.white), QBrush(Qt.GlobalColor.white))
        for i in range(int(self.eventList[0]['year']), int(self.eventList[-1]['year'])+1):
            year=str(i)
            r=QRectF(QPointF(padX+dist,(winH/2)-20),QPointF(padX+dist+unit_len,(winH/2)+20))
            self.drawScene.addRect(r,unitPen, unitBrush)

            path = QPainterPath()
            font=QFont("Segoe UI",12,500)
            metrics=QFontMetrics(font)
            textRect=metrics.tightBoundingRect(year)
            path.addText(QPointF(padX+dist+(unit_len/2)-textRect.width()/2, (winH/2)+textRect.height()/2),font,year)
            self.drawScene.addPath(path, QPen(Qt.GlobalColor.gray), QBrush(Qt.GlobalColor.gray))
            dist+=unit_len
        self.drawScene.addRect(QRectF(QPointF(padX+dist+2,(winH/2)-40),QPointF(padX+dist+padX,(winH/2)+120)), QPen(Qt.GlobalColor.white), QBrush(Qt.GlobalColor.white))

        for i in self.eventList:
            date=datetime.strptime(i['year'] +"."+ i['month'] +"."+ i['day'], '%Y.%m.%d')
            date=date.strftime("%b")+f" {i['day']} {i['year']}"
            name=i['name']

            placeX=(int(i['year'])-int(self.eventList[0]['year']))*unit_len + padX

            path = QPainterPath()
            font=QFont("Segoe UI",9,400)
            metrics=QFontMetrics(font)
            textRect1=metrics.tightBoundingRect(date)
            path.addText(QPointF(placeX, (winH/2)-padY+textRect1.height()/2),font,date)
            self.drawScene.addPath(path, QPen(Qt.GlobalColor.gray), QBrush(Qt.GlobalColor.gray))

            path = QPainterPath()
            font=QFont("Segoe UI",9,400)
            metrics=QFontMetrics(font)
            textRect2=metrics.tightBoundingRect(name)
            path.addText(QPointF(placeX, (winH/2)-padY+15+textRect2.height()/2),font,name) # +(unit_len/2)-textRect.width()/2
            self.drawScene.addPath(path, QPen(Qt.GlobalColor.gray), QBrush(Qt.GlobalColor.gray))

            linePen=QPen(Qt.GlobalColor.gray)
            linePen.setWidth(2)
            self.drawScene.addRect(QRectF(QPointF(),QPointF()),QPen(Qt.GlobalColor.gray))
            self.drawScene.addLine(QLineF(QPointF(placeX+textRect1.width()/2,(winH/2)-padY+20+textRect1.height()/2),QPointF(placeX+textRect1.width()/2,winH/2-20)),linePen)

    def newEventDialog(self):
        dlg=event_dialog.CustomEventDialog(self)
        if dlg.exec():
            self.eventList.append(dlg.getData())
            self.saveEvents()

    def readEvents(self):
        self.eventList=list()
        if os.path.isfile("events.json"):
            with open('events.json', 'r') as openfile:
                json_object = json.load(openfile)
            self.eventList=json_object

        self.eventList=sorted(self.eventList, key=lambda d: d['year'])

    def saveEvents(self):
        json_object = json.dumps(self.eventList, indent=4)
        with open("events.json", "w") as outfile:
            outfile.write(json_object)
        self.loadTimeline()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())