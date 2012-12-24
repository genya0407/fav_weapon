#coding: utf-8
from PyQt4 import QtCore
from PyQt4 import QtGui
import tweepy
import webbrowser


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
		
			#結合
		self.aw.launch_auth_window.clicked.connect(self.act.open_url)
		self.aw.add_user.clicked.connect(self.pass_pin)
		
		vbox.addWidget(self.tg)
		vbox.addWidget(self.ul)
		vbox.addWidget(self.aw)
		
		self.setLayout(vbox)
	
	def pass_pin(self):
		pin = self.aw.verify_num.text()
#		print(pin)
		self.act.create_api_object(pin)

class action(object):
	def __init__(self):
		consumer_key = 'HhFnDkO26i4Ct491Q5Zeg'
		consumer_secret = 'XGNL9HqyEvO3AQtX9dMeZSsdeRY7LwjOPYnz2TcFB0'
		
		self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		self.api_list = []
	
	def open_url(self):
		webbrowser.open(self.auth.get_authorization_url())
	
	def create_api_object(self, pin):
		self.auth.get_access_token(pin)
		access_token_key = self.auth.access_token.key
		access_token_secret = self.auth.access_token.secret
		self.auth.set_access_token(access_token_key, access_token_secret)
		self.api = tweepy.API(auth_handler=self.auth)
		for i in self.api.home_timeline():
			print(i.text)
#		me = self.api.me()
#		print(me.screen_name)
#		self.api_list.append(api)
			#デバッグ用
#		for i in self.api_list:
#			i.update_status('てす')

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
