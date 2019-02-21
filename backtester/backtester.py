import pandas as pd
import numpy as np 
import os
from random import randint
from ast import literal_eval
## Import custom classes
from backtester.backtesterResources.portfolioSim import portfolioSim

class backtester(object):
	
	def __init__(self):
		## Load book data
		print("Loading data...")
		global bookData
		bookData = pd.read_csv(os.path.join("backtester\cleanData","{}.csv".format(str("cleanBookData"))), converters={"book": literal_eval},nrows=500000)
		print("Data loaded")


	def backtest(self, neuralnet):
		portfolioList = []
		portfolioReturns = []
		
		#Initiate array of portfolios
		for i in neuralnet:
			portfolioList.append(portfolioSim(i))
		
		## Main backtest loop
		for row in bookData.itertuples():
			
			for j in portfolioList:
				## Update portfolio if we have a position
				if j.longShortFlat != 0:
					j.portfolioUpdate(row[1], row[2])
					
				## Decide to enter a position if we are flat
				else:
					direction = j.neuralnet.activate(row[3])
					j.placeOrder(direction, row[1], row[2])	

		## Append to and return portfolio performace list
		for j in portfolioList:
			portfolioReturns.append(j.getPerformance())
		
		return portfolioReturns
