#coding: utf-8
from PyQt4 import QtCore
from PyQt4 import QtGui

class target(QtGui.QWidget):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent=parent)
		self.setUI()
	
	def setUI(self):
		textbox = QtGui.QLineEdit()
		button = QtGui.QPushButton('fav')
		hbox = QtGui.QHBoxLayout()
		
		hbox.addWidget(textbox)
		hbox.addWidget(button)
		
		self.setLayout(hbox)

class user_list(QtGui.QWidget):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent=parent)
		self.setUI()
	
	def setUI(self):
		list_widget = QtGui.QListWidget()
			#Item編集部-->あとで関数化
		item1 = QtGui.QListWidgetItem()
		item1.setText('genya0407')
		item1.setIcon(QtGui.QIcon(QtGui.QPixmap('/home/yusuke/github/qt-practice/icon.jpg')))
		
		list_widget.addItem(item1)
		vbox = QtGui.QVBoxLayout()
		vbox.addWidget(list_widget)
		self.setLayout(vbox)

class auth_widget(QtGui.QWidget):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent=parent)
		self.setUI()
	
	def setUI(self):
		add_user = QtGui.QPushButton('add')
		verify_num = QtGui.QLineEdit()
		launch_auth_window = QtGui.QPushButton('auth')
		
		hbox = QtGui.QHBoxLayout()
		hbox.addWidget(launch_auth_window)
		hbox.addWidget(verify_num)
		hbox.addWidget(add_user)
		
		self.setLayout(hbox)

class main_vbox(QtGui.QWidget):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent=parent)
		self.setUI()
	
	def setUI(self):
		vbox = QtGui.QVBoxLayout()
		
		tg = target()
		ul = user_list()
		aw = auth_widget()
		
		vbox.addWidget(tg)
		vbox.addWidget(ul)
		vbox.addWidget(aw)
		
		self.setLayout(vbox)

def main():
	app = QtGui.QApplication([])
	main_window = QtGui.QMainWindow()
	
	mw = main_vbox()
	
	main_window.setCentralWidget(mw)
	main_window.show()
	
	app.exec_()

if __name__ == '__main__':
	main()
