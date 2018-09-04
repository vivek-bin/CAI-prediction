import constants as CONST
import pandas




def loadInitialData():
	file = []
	
	file = pandas.ExcelFile(CONST.INPUTEXCEL)
	fileData = file.parse()

	return fileData
