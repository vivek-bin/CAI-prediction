import random
import pandas
import re

import constants as CONST


def loadData():
	file = pandas.ExcelFile(CONST.DATAPATH + "input.xlsx").parse("input")
	
	for col in ["Category","Type","Stage of defect injection","Defect category"]:
		with open(CONST.ENCODINGS + col +"Map.txt","r") as iFile:
			unique = iFile.readlines()
		
		uniqueDict = {val.strip():i+1 for i,val in enumerate(unique)}
		
		for i,val in enumerate(file[col]):
			file[col][i] = uniqueDict[val]
			
	wordDict = {}
	with open(CONST.ENCODINGS + "WordMap.txt","r") as iFile:
		wordList = iFile.readlines()
		wordDict = {val.strip():i+1 for i,val in enumerate(wordList)}
	
	for col in ["Summary","Description"]:
		cleanColumnText(file, col)
		for i in range(len(file[col])):
			for j,val in enumerate(file[col][i]):
				try:
					file[col][i][j] = wordDict[val]
				except KeyError:
					file[col][i][j] = 0
	
	file["Input Text"] = [s+d for s,d in zip(file["Summary"],file["Description"])]
	file["Input Text"] = [[v for v in rec if v]+[0] for rec in file["Input Text"]]
	
	print(file["Input Text"][0])
	
	
	vecRecords = list(zip(file["Category"],file["Type"],file["Stage of defect injection"],file["Defect category"],file["Input Text"]))
	
	random.shuffle(vecRecords)
	
	x = [i3 for (i1,i2,o1,o2,i3) in vecRecords]
	y1 = [o1 for (i1,i2,o1,o2,i3) in vecRecords]
	y2 = [o2 for (i1,i2,o1,o2,i3) in vecRecords]
	
	return x,y1,y2
	
	
def generateMapping():
	file = pandas.ExcelFile(CONST.DATAPATH + "input.xlsx").parse("input")
	
	for col in ["Category", "Type", "Stage of defect injection", "Defect category"]:
		unique = set(file[col])
		with open(CONST.ENCODINGS + col+"Map.txt","w") as oFile:
			oFile.writelines("\n".join(unique))
	
	
	allWords = set()
	for col in ["Summary","Description"]:
		cleanColumnText(file, col)
		allWords = allWords | getUniqueWords(file[col])		#union on sets
	
	
	filteredWords = wordFrequency(file,allWords)
	with open(CONST.ENCODINGS + "WordMap.txt","w") as oFile:
		oFile.writelines("\n".join(filteredWords))

	
	
	
def cleanColumnText(file, colName):
	for i,val in enumerate(file[colName]):
		# file[colName][i] = cleanStr(val).split()
		file[colName][i] = re.split(r"\W", cleanStr(val))
	
def getUniqueWords(col):
	allWords = set()
	for rec in col:
		allWords.update(rec)
			
	return allWords
	
def cleanStr(inputStr):
	inputStr = str(inputStr).lower().replace("-","")
	strList = list(inputStr)
	
	toSpace = "+*/$&;:.,!?'\"#(){}[]_=<>\\\u201c\\i201c\u2018\u2019"
	toRemove = "-"
	toN = "0123456789"
	
	for i,ch in enumerate(strList):
		# if ch in toSpace:
		# 	strList[i] = " "
		if ch in toRemove:
			strList[i] = ""
		if ch in toN:
			strList[i] = "N"
	
	ouputLine = "".join(strList)
	
	return ouputLine

def wordFrequency(file,allWords):
	wordFreq = {val: 0 for val in allWords}
	
	for col in ["Summary","Description"]:
		for rec in file[col]:
			for word in allWords:
				if word in rec:
					wordFreq[word] = wordFreq[word] + 1 
	
	#ignore words that are too rare or too common
	wordList = [k for k,v in wordFreq.items() if v > CONST.MIN_VOCAB_FREQ and v < CONST.MAX_VOCAB_FREQ]
	
	return sorted(wordList)
	
	
if __name__ == "__main__":
	generateMapping()




