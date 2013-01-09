# coding: utf-8
import twitter,pickle,os.path
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import QtWebKit

class StarShootingWidget(QtGui.QWidget):
	def __init__(self,parent=None):
		QtGui.QWidget.__init__(self,parent=parent)
		self.setup_ui()
	
	def setup_ui(self):
		hbox = QtGui.QHBoxLayout()
		
		form = QtGui.QFormLayout()
		self.target_screen_name = QtGui.QLineEdit()
		self.favorite_number = QtGui.QLineEdit()
		form.addRow('ターゲット:',self.target_screen_name)
		form.addRow('回数:',self.favorite_number)
		
		self.trigger_button = QtGui.QPushButton('ふぁぼ')
		
		hbox.addLayout(form)
		hbox.addWidget(self.trigger_button)
		
		self.setLayout(hbox)

class AccountSettingWidget(QtGui.QWidget):
	def __init__(self,parent=None):
		QtGui.QWidget.__init__(self,parent=parent)
		self.setup_ui()
	
	def setup_ui(self):
		vbox = QtGui.QVBoxLayout()
		
		self.user_list = QtGui.QListWidget()
		
		hbox = QtGui.QHBoxLayout()
		verify_num = QtGui.QLineEdit()
		self.add_user_button = QtGui.QPushButton('認証')
		hbox.addWidget(verify_num)
		hbox.addWidget(self.add_user_button)
		
		vbox.addWidget(self.user_list)
		vbox.addLayout(hbox)
		
		self.setLayout(vbox)

class VerifyGettingWidget(QtGui.QWidget):
	def __init__(self,parent=None):
		QtGui.QWidget.__init__(self,parent=parent)
		self.setup_ui()
		self.show_authorize_window()
	
	def setup_ui(self):
		self.web = QtWebKit.QWebView()
		vbox = QtGui.QVBoxLayout()
		vbox.addWidget(self.web)
		self.setLayout(vbox)
	
	def show_authorize_window(self):
		t = twitter.twitter()
		request_token, request_token_secret = t.get_request_token()
		auth_url = t.get_verifier(request_token)
		self.web.load(QtCore.QUrl(auth_url))

def main():
	app = QtGui.QApplication([])
	
	main_window = QtGui.QMainWindow()
	
	central_widget = QtGui.QWidget()
	
	left_widget = QtGui.QWidget()
	star_shooting_widget = StarShootingWidget(parent=central_widget)
	account_setting_widget = AccountSettingWidget(parent=central_widget)
	vbox = QtGui.QVBoxLayout()
	vbox.addWidget(star_shooting_widget)
	vbox.addWidget(account_setting_widget)
	left_widget.setLayout(vbox)
	left_widget.setFixedSize(320,480)
	
	verify_getting_widget = VerifyGettingWidget()
	
	hbox = QtGui.QHBoxLayout()
	hbox.addWidget(left_widget)
	hbox.addWidget(verify_getting_widget)
	
	central_widget.setLayout(hbox)
	
	main_window.setCentralWidget(central_widget)
	main_window.setWindowTitle('大量ふぁぼ兵器')
	
	main_window.show()
	app.exec_()

if __name__ == '__main__':
	main()
	
