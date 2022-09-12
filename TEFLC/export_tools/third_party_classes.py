# ----------------------------------------
# third_party_classes.py
# Classes for 3rd-Party Apps
# ----------------------------------------

# Imports
from openpyxl import Workbook
from openpyxl.styles import Font, Color, Alignment, Border, Side, colors

# ----------------------------------------

# Gimkit Template 1
# Must export to .CSV
class Gimkit_1:

	def __init__(self, question, 
				answer_correct, 
				answer_incorrect_1, 
				answer_incorrect_2, 
				answer_incorrect_3):

		self.question = question
		self.answer_correct = answer_correct
		self.answer_incorrect_1 = answer_incorrect_1
		self.answer_incorrect_2 = answer_incorrect_2
		self.answer_incorrect_3 = answer_incorrect_3

	def default_sheet(sheet):
		font_title = Font(name='Arial',
						size=20,
						bold=True)

		font_question = Font(name='Arial',
							size=12,
							bold=True,
							color='000000FF')

		font_answer_correct = Font(name='Arial',
							size=12,
							bold=True,
							color='00008000')

		font_answer_incorrect = Font(name='Arial',
							size=12,
							bold=True,
							color='00FF0000')

		sheet.column_dimensions['A'].width = 40 # 20 original
		sheet.column_dimensions['B'].width = 40 # ^
		sheet.column_dimensions['C'].width = 40 # 25 original
		sheet.column_dimensions['D'].width = 40 # ^
		sheet.column_dimensions['E'].width = 40 # ^

		sheet["A1"].font = font_title
		sheet["A2"].font = font_question
		sheet["B2"].font = font_answer_correct
		sheet["C2"].font = font_answer_incorrect
		sheet["D2"].font = font_answer_incorrect
		sheet["E2"].font = font_answer_incorrect

		sheet["A1"] = "Gimkit Spreadsheet Import Template"
		sheet["A2"] = "Question"
		sheet["B2"] = "Correct Answer"
		sheet["C2"] = "Incorrect Answer 1"
		sheet["D2"] = "Incorrect Answer 2"
		sheet["E2"] = "Incorrect Answer 3"

		return sheet
		
	# Update sheet with [A:E] 3 + iteration
	def add_question(sheet, count, question, 
					answer_correct, 
					answer_incorrect_1, 
					answer_incorrect_2, 
					answer_incorrect_3):

		sheet["A"+str(count+3)] = question
		sheet["B"+str(count+3)] = answer_correct
		sheet["C"+str(count+3)] = answer_incorrect_1
		sheet["D"+str(count+3)] = answer_incorrect_2
		sheet["E"+str(count+3)] = answer_incorrect_3
		
		sheet["A"+str(count+3)].alignment = Alignment(wrap_text=True)
		sheet["B"+str(count+3)].alignment = Alignment(wrap_text=True)
		sheet["C"+str(count+3)].alignment = Alignment(wrap_text=True)
		sheet["D"+str(count+3)].alignment = Alignment(wrap_text=True)
		sheet["E"+str(count+3)].alignment = Alignment(wrap_text=True)

		return sheet


	def save_workbook(workbook):
		workbook.save(filename="Gimkit Spreadsheet Import Template.xlsx")

# ----------------------------------------

# Gimkit Template 2
# Must export to .CSV
class Gimkit_2:

	def __init__(self, question, 
				answer_correct):
		
		self.question = question
		self.answer_correct = answer_correct

	def default_sheet(sheet):
		font_title = Font(name='Arial',
						size=20,
						bold=True)

		font_question = Font(name='Arial',
							size=12,
							bold=True,
							color='000000FF')

		font_answer_correct = Font(name='Arial',
							size=12,
							bold=True,
							color='00008000')

		font_default = Font(name='Arial',
						size=10)

		sheet.column_dimensions['A'].width = 40 # 20 original
		sheet.column_dimensions['B'].width = 40

		sheet["A1"].font = font_title
		sheet["A2"].font = font_question
		sheet["B2"].font = font_answer_correct

		sheet["A1"] = "Gimkit Spreadsheet Import Template 2"
		sheet["A2"] = "Question"
		sheet["B2"] = "Correct Answer"

		return sheet

	# Update sheet with [A:B] 3 + iteration
	def add_question(sheet, count, question, answer_correct):
		sheet["A"+str(count+3)] = question
		sheet["B"+str(count+3)] = answer_correct
		
		sheet["A"+str(count+3)].alignment = Alignment(wrap_text=True)
		sheet["B"+str(count+3)].alignment = Alignment(wrap_text=True)

		return sheet

	def save_workbook(workbook):
		workbook.save(filename="Gimkit Spreadsheet Import Template 2.xlsx")

# ----------------------------------------

# Kahoot Template
# Must export to .XLSX
class Kahoot:

	def __init__(self, question,
				answer_option_1,
				answer_option_2,
				answer_option_3,
				answer_option_4,
				time_limit,
				correct_answers):
		
		self.question = question # 120 characters max
		
		self.answer_option_1 = answer_option_1 # 75 characters max
		self.answer_option_2 = answer_option_2 # 75 characters max
		self.answer_option_3 = answer_option_3 # 75 characters max
		self.answer_option_4 = answer_option_4 # 75 characters max
		
		self.time_limit = time_limit # 5, 10, 20, 30, 60, 90, 120, or 240 secs
		
		self.correct_answers = correct_answers # comma separated

	def default_sheet(sheet):
		pass

	def save_workbook(workbook):
		workbook.save(filename="KahootQuizTemplate.xlsx")

# ----------------------------------------

# Quizizz Template
# Must export to .XLSX
class Quizizz:

	def __init__(self, question,
				question_type,
				answer_option_1,
				answer_option_2,
				answer_option_3,
				answer_option_4,
				answer_option_5,
				correct_answers,
				time_limit,
				img_src):
		
		self.question = question
		self.question_type = question_type # multiple choice, checkbox, fill-in, open-ended, poll
		
		self.answer_option_1 = answer_option_1 # required except open-ended
		self.answer_option_2 = answer_option_2 # required except open-ended
		self.answer_option_3 = answer_option_3 # optional
		self.answer_option_4 = answer_option_4 # optional
		self.answer_option_5 = answer_option_5 # optional

		self.correct_answers = correct_answers # comma separated

		self.time_limit = time_limit # optional, 30s default

		self.img_src = img_src # optional

	def default_sheet(sheet):
		pass

	def save_workbook(workbook):
		workbook.save(filename="QuizizzSampleSpreadsheet.xlsx")

# ----------------------------------------