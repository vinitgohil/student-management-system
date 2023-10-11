from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QMainWindow, \
	QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QComboBox, QToolBar, QStatusBar, QMessageBox
from PyQt6.QtGui import QAction, QIcon
import sqlite3

import sys


class MainWindow(QMainWindow):
	def __init__(self):
		# inherit parent class attributes and define mainwidwow instance
		super().__init__()
		self.setWindowTitle("Student Management System")
		self.setFixedWidth(500)
		self.setFixedHeight(500)

		# define file and help main menu items
		file_menu_item = self.menuBar().addMenu("&File")
		help_menu_item = self.menuBar().addMenu("&Help")
		edit_menu_item = self.menuBar().addMenu("&Edit")

		# define subitems for the menu items
		add_student_action = QAction(QIcon("icons/add.png"),"Add Student", self)
		add_student_action.triggered.connect(self.insert)
		file_menu_item.addAction(add_student_action)

		about_action = QAction("About", self)
		help_menu_item.addAction(about_action)
		# for mac users only
		about_action.setMenuRole(QAction.MenuRole.NoRole)

		search_action = QAction(QIcon("icons/search.png"),"Search", self)
		edit_menu_item.addAction(search_action)
		search_action.triggered.connect(self.search)


		# Add table to the main window
		self.table = QTableWidget()
		self.table.setColumnCount(4)
		self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "MobileNumber"))
		self.table.verticalHeader().setVisible(False)
		self.setCentralWidget(self.table)

		# Create Toolnbar and add toolbar elements
		toolbar = QToolBar()
		toolbar.setMovable(True)
		self.addToolBar(toolbar)

		toolbar.addAction(add_student_action)
		toolbar.addAction(search_action)

		# Create status bar and add status bar elements
		self.statusbar = QStatusBar()
		self.setStatusBar(self.statusbar)

		# Detect a cell selection
		self.table.cellClicked.connect(self.cell_clicked)

	def cell_clicked(self):
		edit_button = QPushButton("Edit Record")
		edit_button.clicked.connect(self.edit)
		delete_button = QPushButton("Delete Record")
		delete_button.clicked.connect(self.delete)

		# Clean or remove any preselected cell edit/delete buttons
		children = self.findChildren(QPushButton)
		if children:
			for child in children:
				self.statusbar.removeWidget(child)

		self.statusbar.addWidget(edit_button)
		self.statusbar.addWidget(delete_button)

	def load_data(self):
		connection = sqlite3.connect("database.db")
		result = connection.execute("SELECT * FROM students")
		self.table.setRowCount(0)
		for row_number, row_data in enumerate(result):
			self.table.insertRow(row_number)
			for column_number, data in enumerate(row_data):
				self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

		connection.close()

	def insert(self):
		dialog = InsertDialog()
		dialog.exec()

	def search(self):
		dialog = SearchDialog()
		dialog.exec()

	def edit(self):
		dialog = EditDialog()
		dialog.exec()

	def delete(self):
		dialog = DeleteDialog()
		dialog.exec()


class InsertDialog(QDialog):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Insert Student Details")
		self.setFixedWidth(300)
		self.setFixedHeight(300)

		layout = QVBoxLayout()

		# Add student name widget
		self.student_name = QLineEdit()
		self.student_name.setPlaceholderText("Name")
		layout.addWidget(self.student_name)

		# Add combo box course widget
		self.course_name = QComboBox()
		courses = ["Biology", "Maths", "Chemistry", "Physics", "Art", "Economics", "History", "Astronomy"]
		self.course_name.addItems(courses)
		layout.addWidget(self.course_name)

		# Add mobile number widget
		self.mobile_number = QLineEdit()
		self.mobile_number.setPlaceholderText("Mobile#")
		layout.addWidget(self.mobile_number)

		# Add submit button
		button = QPushButton("Submit")
		button.clicked.connect(self.add_student)
		layout.addWidget(button)

		self.setLayout(layout)

	def add_student(self):
		name = self.student_name.text()
		course = self.course_name.itemText(self.course_name.currentIndex())
		mobile = self.mobile_number.text()
		connection = sqlite3.connect("database.db")
		cursor = connection.cursor()
		cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",
					   (name, course, mobile))
		connection.commit()
		cursor.close()
		connection.close()
		StudentMgtSys.load_data()


class SearchDialog(QDialog):
	def __init__(self):
		super().__init__()

		self.setWindowTitle("Search Student")
		self.setFixedWidth(300)
		self.setFixedHeight(300)

		layout = QVBoxLayout()

		# Add student name widget
		self.student_name = QLineEdit()
		self.student_name.setPlaceholderText("Name")
		layout.addWidget(self.student_name)

		# Add search button
		button = QPushButton("Search")
		button.clicked.connect(self.search_student)
		layout.addWidget(button)

		self.setLayout(layout)

	def search_student(self):
		name = self.student_name.text()
		connection = sqlite3.connect("database.db")
		cursor = connection.cursor()
		result = cursor.execute("SELECT * FROM students WHERE name = ?", (name,))
		rows = list(result)
		print(rows)
		items = StudentMgtSys.table.findItems(name, Qt.MatchFlag.MatchFixedString)
		for item in items:
			print(item)
			StudentMgtSys.table.item(item.row(), 1).setSelected(True)

		cursor.close()
		connection.close()


class EditDialog(QDialog):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Edit Student")
		self.setFixedWidth(300)
		self.setFixedHeight(300)

		layout = QVBoxLayout()

		# Get index of the selected row
		index = StudentMgtSys.table.currentRow()

		# Get Id from selected row
		self.student_id = StudentMgtSys.table.item(index, 0).text()

		# Get student name from selected row
		student_name = StudentMgtSys.table.item(index, 1).text()

		# Add student name widget
		self.student_name = QLineEdit(student_name)
		self.student_name.setPlaceholderText("Name")
		layout.addWidget(self.student_name)

		# Get default course of student based on the selection
		course_name = StudentMgtSys.table.item(index, 2).text()

		# Add combo box course widget
		self.course_name = QComboBox()
		courses = ["Biology", "Maths", "Chemistry", "Physics", "Art", "Economics", "History", "Astronomy"]
		self.course_name.addItems(courses)
		self.course_name.setCurrentText(course_name)
		layout.addWidget(self.course_name)

		# Get student mobile from selected row
		mobile_number = StudentMgtSys.table.item(index, 3).text()

		# Add mobile number widget
		self.mobile_number = QLineEdit(mobile_number)
		self.mobile_number.setPlaceholderText("Mobile#")
		layout.addWidget(self.mobile_number)

		# Add submit button
		button = QPushButton("Update")
		button.clicked.connect(self.edit_student)
		layout.addWidget(button)

		self.setLayout(layout)

	def edit_student(self):
		connection = sqlite3.connect("database.db")
		cursor = connection.cursor()
		cursor.execute("UPDATE students SET name = ?, course = ?, mobile = ?  WHERE id = ?",
					   (self.student_name.text(),
						self.course_name.itemText(self.course_name.currentIndex()),
						self.mobile_number.text(),
						self.student_id))
		connection.commit()
		cursor.close()
		connection.close()

		# Refresh the table
		StudentMgtSys.load_data()


class DeleteDialog(QDialog):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Delete Student Details")

		layout = QGridLayout()
		confirmation = QLabel("Are you sure you want to delete?")
		yes = QPushButton("Yes")
		no = QPushButton("No")

		layout.addWidget(confirmation, 0, 0, 1, 2)
		layout.addWidget(yes, 1, 0)
		layout.addWidget(no, 1, 1)

		self.setLayout(layout)

		yes.clicked.connect(self.delete_student)

	def delete_student(self):

		# Get index of the selected row
		index = StudentMgtSys.table.currentRow()

		# Get Id from selected row
		student_id = StudentMgtSys.table.item(index, 0).text()

		connection = sqlite3.connect("database.db")
		cursor = connection.cursor()
		cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
		connection.commit()
		cursor.close()
		connection.close()
		StudentMgtSys.load_data()

		self.close()

		confirmation = QMessageBox()
		confirmation.setWindowTitle("Success")
		confirmation.setText("Student details successfully deleted!")
		confirmation.exec()


app = QApplication(sys.argv)
StudentMgtSys = MainWindow()
StudentMgtSys.show()
StudentMgtSys.load_data()
sys.exit(app.exec())
