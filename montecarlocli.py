import click
import numpy as np
import pandas as pd
import random
from scipy import stats
from colorama import Fore, Back, Style

confidence_safe = 0.95
confidence_aggressive = 0.50
confidence_hostile = 0.20


def when_will_it_be_done(trials, iterations, pd_data, original_backlog_size):
    iterations_output = []
    t = pd_data['throughput'].to_numpy()    
    for trial in range(trials):
        iterations = 0
        backlog_size = original_backlog_size
        while (backlog_size>=0):
            backlog_size = backlog_size - t[random.randint(0, t.size-1)]
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

def how_many_items(trials, iterations, pd_data):
    iterations_output = []
    t = pd_data['throughput'].to_numpy()
    for trial in range(trials):
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

@click.command()
@click.option('--trials', default=10000, help='Number of trials for the montecarlo simulation (Default: 10000).')
@click.option('--backlog_size', default=50, help='Size of the backlog to forecast (Default: 50).')
@click.option('--throughput_file', prompt='The CSV file containing the throughput', help='The CSV file containing the throughput.', default="example.csv", type=str)
@click.option('--iterations', default=3 ,prompt='please insert how many iterations you can afford', help='The number of iterations for which you are forecasting.', type=int)
@click.option('--forecast_type', prompt='please insert how many iterations you can afford', help='The number of iterations for which you are forecastin', type=str, default='2')
def cli(trials, backlog_size, throughput_file, iterations, forecast_type):
    """This software will help you to forecast when a backlog of a certain size will be 
    done or how many PBI you can do in a certain amount of iterations"""
    click.echo(f"Reading {throughput_file}.")
    pd_data = pd.read_csv(throughput_file, header=0)
    if (forecast_type == '1'):
        click.echo(f"When will it be done?")
        when_will_it_be_done(trials, iterations, pd_data, backlog_size)
    elif (forecast_type == '2'):
        click.echo(f"How many items will be done in the next {iterations} iteration(s)?")
        how_many_items(trials, iterations, pd_data)
    else:
        click.echo("out of range")
