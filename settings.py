from PyQt4.QtCore import *
from PyQt4.QtGui import *

class SettingsDlg (QDialog):

	def __init__(self, parent):
		super (SettingsDlg, self).__init__(parent)
		self.parent = parent
		self.setWindowTitle ('Preferences')

		self.autoLogin = QCheckBox ('Auto login on startup')
		self.autoLogin.setChecked (parent.settings.auto_login)
		
		loginIntervalLabel = QLabel ('Re-login after every:')
		self.loginSpin = QSpinBox ()
		self.loginSpin.setSuffix (' minutes')
		self.loginSpin.setRange (1, 60)
		self.loginSpin.setValue (parent.settings.relogin_after/60)
		
		quotaIntervalLabel = QLabel ('Refresh Quota usage after every:')
		self.quotaSpin = QSpinBox()
		self.quotaSpin.setSuffix (' minutes')
		self.quotaSpin.setRange (1, 60)
		self.quotaSpin.setValue (parent.settings.update_quota_after/60)
		
		grid = QGridLayout()
		grid.addWidget (loginIntervalLabel, 0, 0)
		grid.addWidget (self.loginSpin, 0, 1)
		grid.addWidget (quotaIntervalLabel, 1, 0)
		grid.addWidget (self.quotaSpin, 1, 1)
		
		self.autoSwitchCheck = QCheckBox ('Enable Auto Switch to next account in the list')
		
		self.usageCheck = QCheckBox ('When usage reaches')
		self.usageCheck.setChecked (parent.settings.switch_on_critical or parent.settings.switch_on_limit)
		
		self.quotaSwitchCheck = QRadioButton ('Data Transfer Limit', self)
		self.quotaSwitchCheck.setChecked (parent.settings.switch_on_critical)
		
		self.criticalSwitchCheck = QRadioButton ('Critical quota:', self)
		self.criticalSwitchCheck.setChecked (parent.settings.switch_on_critical)
		self.criticalSpin = QDoubleSpinBox()
		self.criticalSpin.setSuffix (' MB')
		self.criticalSpin.setRange (5, 100)
		self.criticalSpin.setValue (parent.settings.critical_quota_limit/1024)
		hbox = QHBoxLayout()
		hbox.addWidget (self.criticalSwitchCheck)
		hbox.addWidget (self.criticalSpin)

		self.wrongPassCheck = QCheckBox ('When wrong password encountered')
		self.wrongPassCheck.setChecked (parent.settings.switch_on_wrongPass)
		self.autoSwitchCheck.setChecked (self.usageCheck.isChecked() or self.wrongPassCheck.isChecked())
		self.wrongPassCheck.setEnabled ( self.autoSwitchCheck.isChecked() )
		self.usageCheck.setEnabled (self.autoSwitchCheck.isChecked())
		self.quotaSwitchCheck.setEnabled ( self.usageCheck.isChecked() and self.autoSwitchCheck.isChecked() )
		self.criticalSwitchCheck.setEnabled ( self.usageCheck.isChecked() and self.autoSwitchCheck.isChecked() )
		self.criticalSpin.setEnabled (self.criticalSwitchCheck.isChecked() and self.autoSwitchCheck.isChecked() and self.usageCheck.isChecked())
		
		self.balloonPopups = QCheckBox ( 'Enable balloon popups' )
		self.balloonPopups.setChecked ( parent.settings.balloons )

		buttonBox = QDialogButtonBox ( QDialogButtonBox.Ok | QDialogButtonBox.Cancel )
		
		vbox = QVBoxLayout()
		vbox.addWidget (self.autoLogin)
		vbox.addWidget ( QLabel() )
		vbox.addLayout (grid)
		vbox.addWidget ( QLabel() )
		vbox.addWidget ( QLabel() )
		vbox.addWidget (self.autoSwitchCheck)
		vbox.addWidget (self.usageCheck)
		vbox.addWidget (self.quotaSwitchCheck)
		vbox.addLayout (hbox)
		vbox.addWidget (self.wrongPassCheck)
		vbox.addWidget ( QLabel() )
		vbox.addWidget ( QLabel() )
		vbox.addWidget ( self.balloonPopups )
		vbox.addWidget (buttonBox)
		self.setLayout (vbox)
		
		self.connect (buttonBox, SIGNAL('accepted()'), self, SLOT('accept()'))
		self.connect (buttonBox, SIGNAL('rejected()'), self, SLOT('reject()'))
		self.connect (self.autoSwitchCheck, SIGNAL('toggled(bool)'), self.box1)
		self.connect (self.usageCheck, SIGNAL('toggled(bool)'), self.box2)
		self.connect (self.criticalSwitchCheck, SIGNAL('toggled(bool)'), self.criticalSpin.setEnabled)
		
		if not self.quotaSwitchCheck.isChecked() and not self.criticalSwitchCheck.isChecked():
			self.quotaSwitchCheck.setChecked (True)

	def box1 (self, state):
		self.usageCheck.setEnabled ( state )
		self.box2 (state and self.usageCheck.isChecked())
		self.wrongPassCheck.setEnabled ( state )

	def box2 (self, state):
		self.quotaSwitchCheck.setEnabled ( state )
		self.criticalSwitchCheck.setEnabled ( state )
		self.criticalSpin.setEnabled ( self.criticalSwitchCheck.isChecked() and state )

