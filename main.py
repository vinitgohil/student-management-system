from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QMainWindow, \
	QTableWidget
from PyQt6.QtGui import QAction
import sqlite3

import sys

class MainWindow(QMainWindow):
	def __init__(self):
		# inherit parent class attributes and define mainwidwow instance
		super().__init__()
		self.setWindowTitle("Student Management System")

		# define file and help main menu items
		file_menu_item = self.menuBar().addMenu("&File")
		help_menu_item = self.menuBar().addMenu("&Help")

		# define subitems for the menu items
		add_student_action = QAction("Add Student", self)
		file_menu_item.addAction(add_student_action)

		about_action = QAction("About", self)
		help_menu_item.addAction(about_action)
		# for mac users only
		about_action.setMenuRole(QAction.MenuRole.NoRole)

		# Add table to the main window
		self.table = QTableWidget()
		self.table.setColumnCount(4)
		self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "MobileNumber"))
		self.setCentralWidget(self.table)



app = QApplication(sys.argv)
StudentMgtSys = MainWindow()
StudentMgtSys.show()
sys.exit(app.exec())