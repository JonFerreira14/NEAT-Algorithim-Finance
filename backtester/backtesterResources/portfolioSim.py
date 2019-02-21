import pandas as pd
import numpy as np
import os

class portfolioSim(object):

	def __init__(self, inputneuralnet):
		## Initial account settings
		self.neuralnet = inputneuralnet
		self.accountValue = 10000
		self.longShortFlat = 0 
		self.positionBasis = 0 
		## Trading settings
		self.stopLossFactor = 6
		self.takeProfitFactor = 3
		self.tickSize = 0.25
		self.commision = 0.85
		self.tickVal = 12.50

		
		
	## Check current value of held positions
	## Close if TP or SL hit (assume TP&SL were limit orders and no slip)
	## Calculate and update mark-to-market value 
	## Update portfolio if position is closed
	def portfolioUpdate(self, level1Bid, level1Ask):
		## Check if we have position and if so, what is gain/loss and check if stopped or take profit (update if sl or tp and update acct val)
		## If we are long
		if self.longShortFlat == 1:
			## Calc TP and SL
			takeProfit = self.positionBasis + self.takeProfitFactor*self.tickSize
			stopLoss = self.positionBasis - self.stopLossFactor*self.tickSize
			
			## Check curr position value
			currPositionVal = level1Bid
			markToMarket = (currPositionVal - self.positionBasis)*self.tickVal/self.tickSize
			
			## Close position if needed and chng acct val
			if currPositionVal <= stopLoss:
				self.longShortFlat = 0
				self.positionBasis = 0
				self.accountValue += (markToMarket-self.commision*2)

			elif currPositionVal >= takeProfit:
				self.longShortFlat = 0
				self.positionBasis = 0
				self.accountValue += (markToMarket-self.commision*2)

			
		## If we are short
		elif self.longShortFlat == -1:
			## Calc TP and SL
			takeProfit = self.positionBasis - self.takeProfitFactor*self.tickSize
			stopLoss = self.positionBasis + self.stopLossFactor*self.tickSize
			
			## Check curr position value
			currPositionVal = level1Ask
			markToMarket = (self.positionBasis - currPositionVal)*self.tickVal/self.tickSize
			
			## Close position if needed and chng acct val
			if currPositionVal >= stopLoss:
				self.longShortFlat = 0
				self.positionBasis = 0
				self.accountValue += (markToMarket-self.commision*2)

			elif currPositionVal <= takeProfit:
				self.longShortFlat = 0
				self.positionBasis = 0
				self.accountValue += (markToMarket-self.commision*2)
		
		return

	
	## If no position, place long or short order w/
	## consideration for slippage, commisions, etc
	def placeOrder(self, direction, level1Bid, level1Ask):
		## Get max val of list
		orderType = direction.index(max(direction))
		
		if orderType == 0:
			self.longShortFlat = 1
			self.positionBasis = level1Ask
			#print("long")
		
		elif orderType == 1:
			self.longShortFlat = -1
			self.positionBasis = level1Bid
			#print("short")
		return


	def getPerformance(self):
		
		if self.accountValue != 10000:
			return self.accountValue-10000
		else:
			return -10000
			

	