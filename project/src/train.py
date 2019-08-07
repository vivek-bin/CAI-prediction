import numpy as np
from keras.models import Sequential
from keras import layers
from keras.optimizers import RMSprop
from keras.utils.np_utils import to_categorical
from keras.callbacks import ModelCheckpoint


import constants as CONST
import prepData as PD


TRAIN_SPLIT_PCT = 0.75

TEXT_LENGTH = 0
CATEGORY_COUNT = 0
WORD_COUNT = 0


def loadData():
	global WORD_COUNT, TEXT_LENGTH
	
	x,y1,y2 = PD.loadData()
	WORD_COUNT = max([max(rec) for rec in x]) + 1
	TEXT_LENGTH = max([len(rec) for rec in x])
	
	x = oneHotEncodeText(x)	
	
	y1 = to_categorical(y1)	
	y2 = to_categorical(y2)	
	
	return x, y1, y2

def getDataDefectInjection():
	global CATEGORY_COUNT
	
	x,y,_ = loadData()
	CATEGORY_COUNT = y.shape[1]
	TRAIN_SPLIT = int(len(x) * TRAIN_SPLIT_PCT)
	
	return x[:TRAIN_SPLIT], y[:TRAIN_SPLIT], x[TRAIN_SPLIT:], y[TRAIN_SPLIT:]


def getDataDefectCategory():
	global CATEGORY_COUNT
	
	x,_,y = loadData()
	CATEGORY_COUNT = y.shape[1]
	TRAIN_SPLIT = int(len(x) * TRAIN_SPLIT_PCT)
	
	return x[:TRAIN_SPLIT], y[:TRAIN_SPLIT], x[TRAIN_SPLIT:], y[TRAIN_SPLIT:]


def vectorizeText(x):	
	xData = np.zeros((len(x),TEXT_LENGTH))
	for i,rec in enumerate(x):
		for j,val in enumerate(rec):
			xData[(i,j)] = val
		
	return xData


def oneHotEncodeText(x):	
	xData = np.zeros((len(x),WORD_COUNT))
	for i,val in enumerate(x):
		xData[(i,val)] = 1.
	
	return xData

	
def trainCategoryModel(xTrain,yTrain):
	model = Sequential()
	#model.add(layers.Embedding(input_dim=WORD_COUNT, output_dim=4, input_length=TEXT_LENGTH))
	#model.add(layers.Flatten())
	model.add(layers.Dense(8, activation='relu', input_shape=(WORD_COUNT,)))
	#model.add(layers.Dense(2, activation='relu'))
	model.add(layers.Dense(CATEGORY_COUNT, activation='softmax'))
	
	model.summary()
	model.compile(	optimizer=RMSprop(lr=4e-4),
					loss='categorical_crossentropy',
					metrics=['acc'])
	
	callbacks = [ModelCheckpoint(CONST.MODELPATH + "defect_cat_model", monitor='val_loss', save_best_only=True, save_weights_only=False)]
	
	history = model.fit(xTrain, yTrain,
					epochs=200,
					batch_size=64,
					callbacks=callbacks,
					validation_split=0.2)
	
	
	saveModel(model, "defect_cat_model")
	
	return model
	

	
def trainInjectionModel(xTrain,yTrain):
	model = Sequential()
	model.add(layers.Dense(4, activation='relu', input_shape=(WORD_COUNT,)))
	model.add(layers.Dense(CATEGORY_COUNT, activation='softmax'))
	
	model.summary()
	model.compile(	optimizer=RMSprop(lr=4e-4),
					loss='categorical_crossentropy',
					metrics=['acc'])
	
	callbacks = [ModelCheckpoint(CONST.MODELPATH + "defect_inj_model", monitor='val_loss', save_best_only=True, save_weights_only=False)]
	
	history = model.fit(xTrain, yTrain,
					epochs=200,
					batch_size=64,
					callbacks=callbacks,
					validation_split=0.2)
	
	
	saveModel(model, "defect_inj_model")
	
	return model
	

def saveModel(model,modelName):
	# serialize model to JSON
	model_json = model.to_json()
	with open(CONST.MODELPATH + modelName + ".json", "w") as json_file:
		json_file.write(model_json)
	
	# serialize weights to HDF5
	model.save_weights(CONST.MODELPATH + modelName + ".h5")
	print("Saved model to disk")
	

	
if __name__ == "__main__":
	xTrain,yTrain,xTest,yTest = getDataDefectCategory()
	print(CATEGORY_COUNT)
	model = trainCategoryModel(xTrain,yTrain)

	scores = model.evaluate(xTest, yTest, verbose=0)
	print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
	

	xTrain,yTrain,xTest,yTest = getDataDefectInjection()
	print(CATEGORY_COUNT)
	model = trainInjectionModel(xTrain,yTrain)

	scores = model.evaluate(xTest, yTest, verbose=0)
	print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))



	