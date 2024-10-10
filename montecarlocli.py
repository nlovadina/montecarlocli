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
@click.option('-f', '--file', help='The CSV file containing the the input data (look at the github page).', default="./example.csv", type=str)
@pass_config
def cli(config, trials, file):
    """This software will help you to forecast when a backlog of a certain size will be 
    done or how many PBI you can do in a certain amount of iterations"""
    click.echo(f"Reading {file}.")
    config.data = pd.read_csv(file, header=0)
    config.trials = trials
    

@cli.command(help='Command to forecast when a certain amount of pbi can be done.')
@click.option('--backlog_size', default=50, help='Size of the backlog to forecast (Default: 50).')
@pass_config
def when(config, backlog_size):
    iterations_output = []
    t = config.data['throughput'].to_numpy()    
    for trial in range(config.trials):
        iterations = 0
        b_size = backlog_size
        while (b_size>=0):
            b_size = b_size - t[random.randint(0, t.size-1)]
            iterations = iterations+1
        iterations_output.append(iterations)
        print(iterations_output)
    forecasted_iterations_number_safe = np.percentile(iterations_output, (confidence_safe)*100, method='closest_observation')
    forecasted_iterations_number_aggressive = np.percentile(iterations_output, (confidence_aggressive)*100, method='closest_observation')
    forecasted_iterations_number_hostile = np.percentile(iterations_output, (confidence_hostile)*100, method='closest_observation')
    left_align_main = 46
    alignment_numbers = 19
    box_borders = left_align_main+alignment_numbers+3
    center_align =9
    right_align = 15
    print(f"*-{'':-^{box_borders}}*")
    print("* "+Fore.GREEN+f'Number of iterations forecasted with {confidence_safe*100}% confidence:_{forecasted_iterations_number_safe:_>{alignment_numbers}.0f}'+Fore.RESET+" *")
    print("* "+f'Number of iterations forecasted with {confidence_aggressive*100}% confidence:_{forecasted_iterations_number_aggressive:_>{alignment_numbers}.0f}'+" *")
    print("* "+Fore.RED+f'Number of iterations forecasted with {confidence_hostile*100}% confidence:_{forecasted_iterations_number_hostile:_>{alignment_numbers}.0f}'+Fore.RESET+" *")
    print(f"*-{'':-^{box_borders}}*")

@cli.command(help='Command to forecast how many pbi can be don ein a certain amount of time.')
@click.option('-i', '--iterations', default=3, help='The number of iterations for which you are forecasting.', type=int)
@pass_config
def howmany(config, iterations):
    iterations_output = []
    t = config.data['throughput'].to_numpy()
    for trial in range(config.trials):
        iteration = np.random.choice(t, iterations)
        iterations_output.append(iteration)
    expected_output = np.array(np.sum(iterations_output, axis=1))
    forecasted_items_number_safe = np.percentile(expected_output, (1-confidence_safe)*100, method='closest_observation')
    forecasted_items_number_aggressive = np.percentile(expected_output, (1-confidence_aggressive)*100, method='closest_observation')
    forecasted_items_number_hostile = np.percentile(expected_output, (1-confidence_hostile)*100, method='closest_observation')
    left_align_main = 46
    alignment_numbers = 19
    box_borders = left_align_main+alignment_numbers+3
    center_align =9
    right_align = 15
    print(f"*-{'':-^{box_borders}}*")
    print("* "+Back.GREEN+f'Number of pbi forecasted with {confidence_safe*100}% confidence:_{forecasted_items_number_safe:_>{alignment_numbers}.0f}'+Back.RESET+" *")
    print("* "+Back.YELLOW+f'Number of pbi forecasted with {confidence_aggressive*100}% confidence:_{forecasted_items_number_aggressive:_>{alignment_numbers}.0f}'+Back.RESET+" *")
    print("* "+Back.RED+f'Number of pbi forecasted with {confidence_hostile*100}% confidence:_{forecasted_items_number_hostile:_>{alignment_numbers}.0f}'+Back.RESET+" *")
    print(f"*-{'':-^{box_borders}}*")