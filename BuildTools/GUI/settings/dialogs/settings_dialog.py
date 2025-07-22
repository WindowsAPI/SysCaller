from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTabWidget,
                           QPushButton, QWidget)
from PyQt5.QtCore import QSettings

from settings.tabs.general_tab import GeneralTab
from settings.tabs.obfuscation_tab import ObfuscationTab
from settings.tabs.integrity_tab import IntegrityTab
from settings.tabs.profile_tab import ProfileTab
from features.stub_mapper import StubMapperDialog
from settings.utils import get_ini_path

class SysCallerSettings(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("SysCaller - Settings")
        self.setMinimumWidth(500)
        self.setMinimumHeight(600)
        self.setStyleSheet("""
            QDialog {
                background: #252525;
                color: white;
            }
            QTabWidget::pane {
                border: 1px solid #333333;
                border-radius: 5px;
                background: #1E1E1E;
            }
            QTabBar::tab {
                background: #333333;
                color: white;
                padding: 8px 20px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
            QTabBar::tab:selected {
                background: #0b5394;
            }
            QGroupBox {
                border: 1px solid #333333;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
                color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QSpinBox {
                background: #333333;
                border: none;
                border-radius: 3px;
                padding: 5px;
                color: white;
            }
            QPushButton {
                background: #0b5394;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                color: white;
            }
            QPushButton:hover {
                background: #67abdb;
            }
            QCheckBox, QRadioButton {
                color: white;
            }
            QLabel {
                color: white;
            }
            QListWidget {
                background: #333333;
                color: white;
                border-radius: 5px;
                padding: 5px;
            }
            QLineEdit {
                background: #333333;
                border: 1px solid #444444;
                border-radius: 5px;
                padding: 8px;
                color: white;
            }
            QScrollArea {
                border: none;
                background: transparent;
            }
        """)
        self.settings = QSettings(get_ini_path(), QSettings.IniFormat)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        tabs = QTabWidget()
        self.general_tab = GeneralTab(self.settings)
        self.obfuscation_tab = ObfuscationTab(self.settings)
        self.integrity_tab = IntegrityTab(self.settings)
        self.profile_tab = ProfileTab(self.settings)
        tabs.addTab(self.general_tab, "General")
        tabs.addTab(self.integrity_tab, "Integrity")
        tabs.addTab(self.obfuscation_tab, "Obfuscation")
        tabs.addTab(self.profile_tab, "Profile")
        layout.addWidget(tabs)
        button_layout = QHBoxLayout()
        stub_mapper_btn = QPushButton("Stub Mapper")
        stub_mapper_btn.setToolTip("Customize obfuscation settings for individual syscalls")
        stub_mapper_btn.clicked.connect(self.open_stub_mapper)
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_settings)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(stub_mapper_btn)
        button_layout.addStretch()
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)

    def save_settings(self):
        self.general_tab.save_settings()
        self.obfuscation_tab.save_settings()
        self.integrity_tab.save_settings()
        self.profile_tab.save_settings()
        self.accept()
        
    def open_stub_mapper(self):
        dialog = StubMapperDialog(self)
        dialog.exec_() 
