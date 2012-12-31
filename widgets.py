#coding: utf-8
from PyQt4 import QtCore
from PyQt4 import QtGui

import twitter2


class target(QtGui.QWidget):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent=parent)
		self.setUI()
	
	def setUI(self):
		target_name = QtGui.QLineEdit()
		trigger_button = QtGui.QPushButton('fav')
		hbox = QtGui.QHBoxLayout()
		
		hbox.addWidget(target_name)
		hbox.addWidget(trigger_button)
		
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
		self.add_user = QtGui.QPushButton('add')
		self.verify_num = QtGui.QLineEdit()
		self.launch_auth_window = QtGui.QPushButton('auth')
		
		hbox = QtGui.QHBoxLayout()
		hbox.addWidget(self.launch_auth_window)
		hbox.addWidget(self.verify_num)
		hbox.addWidget(self.add_user)
		
		self.setLayout(hbox)

class main_widget(QtGui.QWidget):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent=parent)
		self.setUI()
	
	def setUI(self):
		vbox = QtGui.QVBoxLayout()
		
		self.tg = target()
		self.ul = user_list()
		self.aw = auth_widget()
		
		self.act = action()
		
			#connect
		self.aw.launch_auth_window.clicked.connect(self.act.open_url)
		self.aw.add_user.clicked.connect(self.pass_verifier)
		
		vbox.addWidget(self.tg)
		vbox.addWidget(self.ul)
		vbox.addWidget(self.aw)
		
		self.setLayout(vbox)
	
	def pass_verifier(self):
		pin = self.aw.verify_num.text().strip()
#		print(pin)
		self.act.create_user_dict(pin)

class action(object):
	def __init__(self):
		self.twitter = twitter()
	
	def open_url(self):
		self.request_token,self.request_token_secret = self.twitter.get_request_token()
		self.twitter.get_verifier(request_token)
	
	def get_access_token(self,verifier):
		access_token,access_token_secret,screen_name = self.twitter.get_access_token(self.request_token,self.request_token_secret,verifier)
		return [self.access_token,self.access_token_secret,screen_name]
	
	def create_user_dict(self,verifier):
		access = self.get_access_token(verifier)
		
		access_token = access[0]
		access_token_secret = access[1]
		screen_name =  access[2]
		user_dict = {
			'screen_name':screen_name,
			'access_token':access_token,
			'access_token_secret':access_token_secret
		}
		
		return user_dict

def main():
	app = QtGui.QApplication([])
	main_window = QtGui.QMainWindow()

	mw = main_widget()
	main_window.setCentralWidget(mw)
	main_window.setWindowTitle('weapons_of_mass_favoritation')
	
	main_window.show()
	
	app.exec_()

if __name__ == '__main__':
	main()
