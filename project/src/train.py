import numpy as np
from keras.models import Sequential
from keras import layers
from keras.optimizers import RMSprop
from keras.utils.np_utils import to_categorical
from keras.callbacks import ModelCheckpoint


import constants as CONST
import prepData as PD


TRAIN_SPLIT_PCT = 0.75

PATH = CONST.PATH
MODEL_PATH = PATH + "models\\"

CATEGORY_COUNT = 0
WORD_COUNT = 0


def getDataDefectInjection():
	global CATEGORY_COUNT, WORD_COUNT
	
	x,y1,y2 = PD.loadData()
	
	CATEGORY_COUNT = max(y2) + 1
	WORD_COUNT = max([max(rec) for rec in x]) + 1
	
	
	TRAIN_SPLIT = int(len(x) * TRAIN_SPLIT_PCT)
	
	xTrain = vectorizeText(x[:TRAIN_SPLIT])
	xTest = vectorizeText(x[TRAIN_SPLIT:])
	
	yTrain = to_categorical(y2[:TRAIN_SPLIT])
	yTest = to_categorical(y2[TRAIN_SPLIT:])
	
	
	return xTrain,yTrain,xTest,yTest

def getDataDefectCategory():
	global CATEGORY_COUNT, WORD_COUNT
	
	x,y1,y2 = PD.loadData()
	
	CATEGORY_COUNT = max(y2) + 1
	WORD_COUNT = max([max(rec) for rec in x]) + 1
	
	
	TRAIN_SPLIT = int(len(x) * TRAIN_SPLIT_PCT)
	
	xTrain = vectorizeText(x[:TRAIN_SPLIT])
	xTest = vectorizeText(x[TRAIN_SPLIT:])
	
	yTrain = to_categorical(y2[:TRAIN_SPLIT])
	yTest = to_categorical(y2[TRAIN_SPLIT:])
	
	
	return xTrain,yTrain,xTest,yTest


def vectorizeText(x):
	xData = np.zeros((len(x),WORD_COUNT))
	
	for i,val in enumerate(x):
		xData[(i,val)] = 1.
	
	return xData

	
def trainDenseModel(xTrain,yTrain):	
	
	model = Sequential()
	model.add(layers.Dense(32, activation='relu', input_shape=(WORD_COUNT,)))
	model.add(layers.Dense(32, activation='relu'))
	model.add(layers.Dense(CATEGORY_COUNT, activation='softmax'))
	
	model.summary()
	model.compile(	optimizer=RMSprop(lr=4e-4),
					loss='categorical_crossentropy',
					metrics=['acc'])
	
	callbacks = [ModelCheckpoint("defect_cat_model", monitor='val_loss', save_best_only=True, save_weights_only=False)]
	
	history = model.fit(xTrain, yTrain,
					epochs=25,
					batch_size=16,
					callbacks=callbacks,
					validation_split=0.2)
	
	
	saveModel(model, "defect_cat_model")
	
	return model
	

def saveModel(model,modelName):
	# serialize model to JSON
	model_json = model.to_json()
	with open(MODEL_PATH + modelName + ".json", "w") as json_file:
		json_file.write(model_json)
	
	# serialize weights to HDF5
	model.save_weights(MODEL_PATH + modelName + ".h5")
	print("Saved model to disk")
	

	
if __name__ == "__main__":
	
	xTrain,yTrain,xTest,yTest = getDataDefectCategory()
	print(CATEGORY_COUNT)
	model = trainDenseModel(xTrain,yTrain)

	#scores = model.evaluate(xTest, yTest, verbose=0)
	#print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))



	