#coding: utf-8
from PyQt4 import QtCore
from PyQt4 import QtGui

import twitter,pickle


class target(QtGui.QWidget):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent=parent)
		self.setUI()
	
	def setUI(self):
		self.target_name = QtGui.QLineEdit()
		self.fav_count = QtGui.QLineEdit()
		self.fav_count.setText('20')
		self.trigger_button = QtGui.QPushButton('fav')
		
		form = QtGui.QFormLayout()
		form.addRow('Target:',self.target_name)
		form.addRow('Count:',self.fav_count)
		
		hbox = QtGui.QHBoxLayout()
		hbox.addLayout(form)
		hbox.addWidget(self.trigger_button)
		
		self.setLayout(hbox)

class user_list(QtGui.QWidget):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent=parent)
		self.setUI()
	
	def setUI(self):
		self.list_widget = QtGui.QListWidget()
		vbox = QtGui.QVBoxLayout()
		vbox.addWidget(self.list_widget)
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
		self.user_list = []
	
	def setUI(self):
		vbox = QtGui.QVBoxLayout()
		
		self.tg = target()
		self.ul = user_list()
		self.aw = auth_widget()
		
			# connect
		# auth_widget #
		self.aw.launch_auth_window.clicked.connect(self.open_url)
		self.aw.add_user.clicked.connect(self.add_user_dict)
		
		# target #
		self.tg.trigger_button.clicked.connect(self.fav)
		
		vbox.addWidget(self.tg)
		vbox.addWidget(self.ul)
		vbox.addWidget(self.aw)
		
		self.setLayout(vbox)
	
	def open_url(self):
		self.twitter = twitter.twitter()
		self.request_token,self.request_token_secret = self.twitter.get_request_token()
		self.twitter.get_verifier(self.request_token) #open varifiy url
	
	def add_user_dict(self): # verifier取得 -> get_access_token
		verifier = self.aw.verify_num.text()
		user_dict = self.twitter.get_user_dict(self.request_token,self.request_token_secret,verifier)
		
		self.user_list.append(user_dict)
		
		self.aw.verify_num.clear()
		self.update_user_list_display()
		
	def update_user_list_display(self):
		item = QtGui.QListWidgetItem()
		for user_dict in self.user_list:
			item.setText(user_dict['screen_name'])
			self.ul.list_widget.addItem(item)
	
	def fav(self): 
		# target の screen_name を取得
		target = self.tg.target_name.text()
		count = self.tg.fav_count.text()
		
		# target の user_timeline の tweet_id_str の list を取得
		tweets_id = self.twitter.get_user_timeline(self.user_list[0],target,count)
		
		# self.user_list に入ってる user_dict を使って、すべてのtweets_idを fav する
		for user in self.user_list:
			for t in tweets_id:
				self.twitter.create_fav(user,t)
				print('favorited ' + target + "'s tweet by " + user['screen_name'])
		
		print('finished favoricatig')

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
