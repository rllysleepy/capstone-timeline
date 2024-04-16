import sys
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import flow_layout
import json
import os

class CustomEventDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setWindowTitle("Create a new event")
        self.desktopSize = QApplication.primaryScreen().geometry()
        self.setFixedSize(int(self.desktopSize.width()/4),int(self.desktopSize.height()/3))
        self.appliedTags=list()
        self.readTags()

        self.newlayout = QVBoxLayout()
        self.timeLayout = QHBoxLayout()
        self.nameLayout= QHBoxLayout()
        self.tagLayout = QVBoxLayout()
        self.btnLayout = QHBoxLayout()
        self.addLayout = QHBoxLayout()


        #time section
        self.timeLabel=QLabel("Time:")
        self.timeInputYear=QLineEdit()
        self.timeInputYear.setPlaceholderText("Year")
        self.timeInputYear.setFixedWidth(int(self.size().width()/5))
        self.timeInputYear.setValidator(QIntValidator(0,9999))

        self.timeInputMonth=QLineEdit()
        self.timeInputMonth.setPlaceholderText("Month")
        self.timeInputMonth.setFixedWidth(int(self.size().width()/5))
        self.timeInputMonth.setValidator(QIntValidator(0,9999))

        self.timeInputDay=QLineEdit()
        self.timeInputDay.setPlaceholderText("Day")
        self.timeInputDay.setFixedWidth(int(self.size().width()/5))
        self.timeInputDay.setValidator(QIntValidator(0,9999))

        self.timeLayout.addWidget(self.timeLabel)
        self.timeLayout.addWidget(self.timeInputYear)
        self.timeLayout.addWidget(self.timeInputMonth)
        self.timeLayout.addWidget(self.timeInputDay)

        #name section
        self.nameLabel=QLabel("Name:")
        self.nameInput=QLineEdit()
        self.nameLabel.setFixedWidth(int(self.size().width()/3))

        self.nameLayout.addWidget(self.nameLabel)
        self.nameLayout.addWidget(self.nameInput)

        #info section
        self.infoLabel=QLabel("Description:")
        self.infoInput=QTextEdit()
        self.infoInput.setMaximumHeight(self.infoInput.fontMetrics().height()*3)

        #tag section
        self.tagLabel=QLabel("Select tags:")

        self.tagView=QScrollArea()
        self.tagViewHolder=QWidget()
        self.tagViewLayout=flow_layout.FlowLayout()
        self.tagViewHolder.setLayout(self.tagViewLayout)

        self.tagView.setMaximumHeight(int(self.size().height()/5))
        self.tagView.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        self.tagView.setWidget(self.tagViewHolder)
        self.tagView.setWidgetResizable(True)

        self.tagLayout.addWidget(self.tagLabel)
        self.tagLayout.addWidget(self.tagView)

        #add tag section
        self.addLabel=QLabel("Create new tag:")
        self.addInput=QLineEdit()
        self.addInput.setToolTip("Insert tag name")
        self.addBtn=QPushButton("+")
        self.addBtn.clicked.connect(self.newTag)
        self.addBtn.setToolTip("Add tag")

        self.delBtn=QPushButton()
        self.delBtn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogDiscardButton))
        self.delBtn.setToolTip("Delete tags")

        self.addLayout.addWidget(self.addLabel)
        self.addLayout.addWidget(self.addInput)
        self.addLayout.addWidget(self.addBtn)
        self.addLayout.addWidget(self.delBtn)

        # self.tagLayout.addWidget(self.tagLabel)
        # self.tagLayout.addWidget(self.tagInput)

        #save button section
        self.saveBtn=QPushButton("Save")
        self.saveBtn.setFixedWidth(int(self.size().width()/4))
        self.cancelBtn=QPushButton("Cancel")
        self.cancelBtn.setFixedWidth(int(self.size().width()/4))
        self.saveBtn.clicked.connect(self.accept)
        self.cancelBtn.clicked.connect(self.close)
        self.btnLayout.addItem(QSpacerItem(0,1,QSizePolicy.Policy.Expanding))
        self.btnLayout.addWidget(self.saveBtn)
        self.btnLayout.addWidget(self.cancelBtn)

        #layout loading
        self.newlayout.addLayout(self.timeLayout)
        self.newlayout.addLayout(self.nameLayout)
        self.newlayout.addWidget(self.infoLabel)
        self.newlayout.addWidget(self.infoInput)
        self.newlayout.addLayout(self.tagLayout)
        self.newlayout.addLayout(self.addLayout)
        self.newlayout.addLayout(self.btnLayout)
        self.setLayout(self.newlayout)

        self.loadTags()

    def newTag(self):
        text=self.addInput.text()
        if text not in self.tagList:
            self.tagList.append(text)
            self.saveTags()
            self.addInput.setText("")

        else:
            msgbox=QMessageBox(QMessageBox.Icon.Critical,"Error!","This label already exists.")
            msgbox.exec()

        self.loadTags()

    def readTags(self):
        self.tagList=list()
        self.appliedTags=list()
        if os.path.isfile("tags.json"):
            with open('tags.json', 'r') as openfile:
                json_object = json.load(openfile)
            self.tagList=json_object

    def loadTags(self): # recreate buttons each time, set to false
        self.buttonList=list()
        self.clearLayout(self.tagViewLayout)
        for i in reversed(self.tagList):
            btn=QPushButton(str(i))
            btn.setCheckable(True)
            if str(i) in self.appliedTags:
                btn.setChecked(True)
            width = btn.fontMetrics().boundingRect(str(i)).width() + 20
            btn.setMaximumWidth(width)
            self.tagViewLayout.addWidget(btn)
            btn.clicked.connect(lambda _, tag=i: self.applyTag(str(tag)))
            self.buttonList.append(btn)
        self.tagViewLayout.addItem(QSpacerItem(1,1,QSizePolicy.Policy.Fixed,QSizePolicy.Policy.Expanding))

    def applyTag(self, tag):
        if tag not in self.appliedTags:
            self.appliedTags.append(tag)
        else:
            self.appliedTags.remove(tag)
        print(self.appliedTags)

    def saveTags(self):
        json_object = json.dumps(self.tagList, indent=4)
        with open("tags.json", "w") as outfile:
            outfile.write(json_object)

    def getData(self):
        data = dict()
        data['year']=self.timeInputYear.text()
        data['month']=self.timeInputMonth.text()
        data['day']=self.timeInputDay.text()
        data['name']=self.nameInput.text()
        data['info']=self.infoInput.toPlainText()
        data['tags']=self.appliedTags

        #return tag info
        return data

    def clearLayout(self, layout):
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)

            if isinstance(item, QWidgetItem):
                item.widget().close()
            # else:
            #     self.clearLayout(item.layout())

            layout.removeItem(item)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CustomEventDialog()
    window.show()
    sys.exit(app.exec())


{
    "year":int(),
    "events":[{
        "month":int(),
        "day":int(),
        "name":str(),
        "info":str(),
        "tags":str()
        }]
}