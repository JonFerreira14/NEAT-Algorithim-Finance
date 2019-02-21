#Imports
from __future__ import print_function
import neat, sys, pickle
from backtester.backtester import backtester

#Load backtesting instance
instance = backtester()

# Load configuration.
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     'config')

# load wining genome
winGenome = pickle.load(open('winner.pkl', 'rb'))
net = neat.nn.RecurrentNetwork.create(winGenome, config)
results = instance.backtest([net])

#print results
print(results)

# Display the winning genome.
print('\nBest genome:\n{!s}'.format(winGenome))

