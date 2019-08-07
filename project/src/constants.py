from inspect import getsourcefile
from os.path import abspath
from os.path import dirname

#paths
PATH = dirname(dirname(dirname(abspath(getsourcefile(lambda:0))))) + "/"
PROJECT = dirname(dirname(abspath(getsourcefile(lambda:0)))) + "/"

DATAPATH = PATH + "data/"
ENCODINGS = DATAPATH + "encodings/"
MODELPATH = PATH + "models/"



MIN_VOCAB_FREQ = 5
MAX_VOCAB_FREQ = 100



