import click
import numpy as np
import pandas as pd
import random
from scipy import stats
from colorama import Fore, Back, Style

confidence_safe = 0.95
confidence_aggressive = 0.50
confidence_hostile = 0.20

class Config(object):
        def __init__(self):
             self.data = ""             
             self.trials = 0
        
pass_config = click.make_pass_decorator(Config, ensure = True)

@click.group()
@click.option('-t', '--trials', default=10000, help='Number of trials for the montecarlo simulation (Default: 10000).')
@click.option('-f', '--file', help='The CSV file containing the the input data (look at the github page).', default="./data/example.csv", type=str)
@pass_config
def cli(config, trials, file):
    """This software will help you to forecast when a backlog of a certain size will be 
    done or how many PBI you can do in a certain amount of iterations"""
    click.echo(f"Reading {file}.")
    config.data = pd.read_csv(file, header=0)
    config.trials = trials
    

@cli.command(help='Command to forecast when a certain amount of pbi can be done.')
@click.option('-b', '--backlog_size', default=50, help='Size of the backlog to forecast (Default: 50).')
@pass_config
def when(config, backlog_size):
    iterations_output = []
    t = config.data['values'].to_numpy()    
    for trial in range(config.trials):
        iterations = 0
        b_size = backlog_size
        while (b_size>=0):
            v = t[random.randint(0, t.size-1)]
            b_size = b_size - v
            iterations = iterations+1
        iterations_output.append(iterations)
    forecasted_iterations_number_safe = np.percentile(iterations_output, (confidence_safe)*100, method='closest_observation')
    forecasted_iterations_number_aggressive = np.percentile(iterations_output, (confidence_aggressive)*100, method='closest_observation')
    forecasted_iterations_number_hostile = np.percentile(iterations_output, (confidence_hostile)*100, method='closest_observation')
    min = np.min(iterations_output)
    max = np.max(iterations_output)
    avg = np.average(iterations_output)
    std = np.std(iterations_output)
    left_align_main = 46
    alignment_numbers = 19
    box_borders = left_align_main+alignment_numbers+3
    print(f"*-{'':-^{box_borders}}*")
    print("* " f"Forecast for {backlog_size} pbi on {config.trials} trials" " *"
    )
    print("* "+Fore.GREEN+f'Number of iterations forecasted with {confidence_safe*100}% confidence:_{forecasted_iterations_number_safe:_>{alignment_numbers}.0f}'+Fore.RESET+" *")
    print("* "+f'Number of iterations forecasted with {confidence_aggressive*100}% confidence:_{forecasted_iterations_number_aggressive:_>{alignment_numbers}.0f}'+" *")
    print("* "+Fore.RED+f'Number of iterations forecasted with {confidence_hostile*100}% confidence:_{forecasted_iterations_number_hostile:_>{alignment_numbers}.0f}'+Fore .RESET+" *")
    print(f'* Min iterations {min:_>{alignment_numbers}.0f} *')
    print(f'* Max iterations {max:_>{alignment_numbers}.0f} *')
    print(f"* Avg iterations {avg:_>{alignment_numbers}.0f} *")
    print(f"* Standard deviations  {std:_>{alignment_numbers}.0f} *")
    print(f"*-{'':-^{box_borders}}*")

@cli.command(help='Command to forecast how many pbi can be don ein a certain amount of time.')
@click.option('-i', '--iterations', default=3, help='The number of iterations for which you are forecasting.', type=int)
@pass_config
def howmany(config, iterations):
    iterations_output = []
    t = config.data['values'].to_numpy()
    for trial in range(config.trials):
        iteration = np.random.choice(t, iterations)
        iterations_output.append(iteration)
    expected_output = np.array(np.sum(iterations_output, axis=1))
    forecasted_items_number_safe = np.percentile(expected_output, (1-confidence_safe)*100, method='closest_observation')
    forecasted_items_number_aggressive = np.percentile(expected_output, (1-confidence_aggressive)*100, method='closest_observation')
    forecasted_items_number_hostile = np.percentile(expected_output, (1-confidence_hostile)*100, method='closest_observation')
    min = np.min(expected_output)
    max = np.max(expected_output)
    avg = np.average(expected_output)
    std = np.std(expected_output)
    left_align_main = 46
    alignment_numbers = 19
    box_borders = left_align_main+alignment_numbers+3
 
    print(f"*-{'':-^{box_borders}}*")
    print("* "f"Forecast for _{iterations:_>{alignment_numbers}.0f} iterations "+ Back.RESET+ " *")
    print("* "+Fore.GREEN+f'Number of pbi forecasted with {confidence_safe*100}% confidence:_{forecasted_items_number_safe:_>{alignment_numbers}.0f}'+Fore.RESET+" *")
    print("* "+f'Number of pbi forecasted with {confidence_aggressive*100}% confidence:_{forecasted_items_number_aggressive:_>{alignment_numbers}.0f} *')
    print("* "+Fore.RED+f'Number of pbi forecasted with {confidence_hostile*100}% confidence:_{forecasted_items_number_hostile:_>{alignment_numbers}.0f}'+Fore.RESET+" *")
    print(f"* Min pbi {min:_>{alignment_numbers}.0f} *")
    print(f"* Max pbi {max:_>{alignment_numbers}.0f} *")
    print(f"* Avg pbi {avg:_>{alignment_numbers}.0f} *")
    print(f"* Standard deviations  {std:_>{alignment_numbers}.0f} *")
    print(f"*-{'':-^{box_borders}}*")