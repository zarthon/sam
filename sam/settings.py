from PyQt4.QtCore import *
from PyQt4.QtGui import *

class SettingsDlg (QDialog):

	def __init__(self, parent):
		super (SettingsDlg, self).__init__(parent)
		self.parent = parent
		self.setWindowTitle ('Preferences')

		#grid1
		ipLabel = QLabel ('Server:')
		portLabel = QLabel ('Port:')
		self.ipEdit = QLineEdit (parent.getSetting('Conf', 'Server').toString())
		colonLabel = QLabel (':')
		self.portEdit = QLineEdit (parent.getSetting('Conf', 'Port').toString())
		checkButton = QPushButton ('&Check')
		self.servLabel = QLabel()
		grid1 = QGridLayout()
		grid1.addWidget (ipLabel, 0, 0)
		grid1.addWidget (portLabel, 0, 2, 1, 2)
		grid1.addWidget (self.ipEdit, 1, 0)
		grid1.addWidget (colonLabel, 1, 1)
		grid1.addWidget (self.portEdit, 1, 2)
		grid1.addWidget (checkButton, 1, 3)
		grid1.addWidget (self.servLabel, 2, 0)

		#domainBox
		domainLabel = QLabel ('Domain:')
		self.domainEdit = QLineEdit (parent.getSetting('Conf', 'Domain').toString())
		domainBox = QHBoxLayout()
		domainBox.addWidget (domainLabel)
		domainBox.addWidget (self.domainEdit)

		#Misc opts
		self.autoLogin = QCheckBox ('Auto login on startup')
		self.autoLogin.setChecked (parent.getSetting('Conf', 'AutoLogin').toBool())
		self.balloonPopups = QCheckBox ( 'Enable balloon popups' )
		self.balloonPopups.setChecked ( parent.getSetting('Conf', 'Balloons').toBool() )

		#grid
		loginIntervalLabel = QLabel ('Re-login after every:')
		self.loginSpin = QSpinBox ()
		self.loginSpin.setSuffix (' minutes')
		self.loginSpin.setRange (1, 500)
		self.loginSpin.setValue (parent.getSetting('Conf', 'ReloginAfter').toInt()[0]/60)
		
		quotaIntervalLabel = QLabel ('Refresh Quota usage after every:')
		self.quotaSpin = QSpinBox()
		self.quotaSpin.setSuffix (' minutes')
		self.quotaSpin.setRange (1, 60)
		self.quotaSpin.setValue (parent.getSetting('Conf', 'UpdateQuotaAfter').toInt()[0]/60)
		
		grid = QGridLayout()
		grid.addWidget (loginIntervalLabel, 0, 0)
		grid.addWidget (self.loginSpin, 0, 1)
		grid.addWidget (quotaIntervalLabel, 1, 0)
		grid.addWidget (self.quotaSpin, 1, 1)

		#autoSwitch CheckBox
		self.autoSwitchCheck = QCheckBox ('Enable Auto Switch')
		self.autoSwitchCheck.setChecked (parent.getSetting('Conf', 'AutoSwitch').toBool())
		self.autoSwitchCheck.setToolTip ('Enable/Disable auto-switching to next account in list,\nif any error is encountered\n(wrong password or data transfer limit exceeds)')

		#hbox
		self.criticalCheck = QCheckBox ('Switch when usage reaches:')
		self.criticalCheck.setChecked (parent.getSetting('Conf', 'SwitchOnCritical').toBool() and parent.getSetting('Conf', 'AutoSwitch').toBool())
		self.criticalCheck.setEnabled (self.autoSwitchCheck.isChecked())
		self.criticalCheck.setToolTip ('This will switch to next account if the\nspecified usage is reached.')
		self.criticalSpin = QDoubleSpinBox()
		self.criticalSpin.setSuffix (' MB')
		self.criticalSpin.setRange (5, 100)
		self.criticalSpin.setValue (parent.getSetting('Conf', 'CriticalQuotaLimit').toInt()[0]/1024)
		self.criticalSpin.setEnabled (self.criticalCheck.isChecked())
		hbox = QHBoxLayout()
		hbox.addWidget (self.criticalCheck)
		hbox.addWidget (self.criticalSpin)

		#buttonBox
		buttonBox = QDialogButtonBox ( QDialogButtonBox.Ok | QDialogButtonBox.Cancel )
		
		vbox = QVBoxLayout()
		vbox.addLayout (grid1)
		vbox.addLayout (domainBox)
		vbox.addWidget (self.autoLogin)
		vbox.addWidget ( self.balloonPopups )
		vbox.addWidget ( QLabel() )
		vbox.addLayout (grid)
		vbox.addWidget ( QLabel() )
		vbox.addWidget ( QLabel() )
		vbox.addWidget (self.autoSwitchCheck)
		vbox.addLayout (hbox)
		vbox.addWidget ( QLabel() )
		vbox.addWidget (buttonBox)
		self.setLayout (vbox)
		
		self.connect (checkButton, SIGNAL('clicked()'), self.check)
		self.connect (buttonBox, SIGNAL('accepted()'), self, SLOT('accept()'))
		self.connect (buttonBox, SIGNAL('rejected()'), self, SLOT('reject()'))
		self.connect (self.autoSwitchCheck, SIGNAL('toggled(bool)'), self.updateUi)
		self.connect (self.criticalCheck, SIGNAL('toggled(bool)'), self.criticalSpin.setEnabled)
		
	def updateUi (self, state):
		self.criticalCheck.setEnabled ( state )
		self.criticalSpin.setEnabled ( state and self.criticalCheck.isChecked() )

	def check (self):
		addr = str ( self.ipEdit.text() )
		try: port = int ( self.portEdit.text() )
		except ValuError: port = 80
		import socket
		serv = socket.socket()
		try:
			serv.connect ( (addr, port) )
			self.servLabel.setText ('<font color="green">Server Found</font>')
		except: self.servLabel.setText ('<font color="red">Server not found</font>')
		serv.close()
