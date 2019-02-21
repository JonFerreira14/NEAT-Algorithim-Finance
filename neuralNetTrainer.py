#Imports
from __future__ import print_function
import neat, sys, pickle
from backtester.backtester import backtester
import visualize

#Load backtesting instance
instance = backtester()

## Genome evalueation; need to create list of nets and pass to backtester
def eval_genomes(genomes, config):
    ## list to pass to backtester
    neuralNetList = []
    ## For each genome create neural net
    for genome_id, genome in genomes:
        net = neat.nn.RecurrentNetwork.create(genome, config)
        neuralNetList.append(net)
   
    ## Pass list to backtest function to get fitness list
    results = instance.backtest(neuralNetList)
    
    ## Update fitnes based on results
    counterVal=0
    for genome_id, genome in genomes:
        genome.fitness = results[counterVal]
        counterVal +=1


## Load configuration.
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     'config')

## Stats to visualize
stats = neat.StatisticsReporter()

## Create the population, which is the top-level object for a NEAT run.
p = neat.Population(config)

## Add statistics reporter
p.add_reporter(stats)

## Add a stdout reporter to show progress in the terminal.
p.add_reporter(neat.StdOutReporter(False))



## Run until a solution is found.
winner = p.run(eval_genomes, n=20)

## Display the winning genome.
print('\nBest genome:\n{!s}'.format(winner))

## Print winner to .txt
f = open('BestGenome.txt','w')
f.write('\nBest genome:\n{!s}'.format(winner))
f.close()

## Dump winner into pickle file
pickle.dump(winner, open('winner.pkl', 'wb'))


## Plot results
visualize.plot_stats(stats, ylog=True, view=True, filename="feedforward-fitness.svg")
visualize.plot_species(stats, view=True, filename="feedforward-speciation.svg")
