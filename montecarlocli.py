import click
import numpy as np
import pandas as pd
import random
import sys
import rich.progress
from rich.progress import track

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
@click.option('-p', '--percentiles', help='The percentiles you want to look at default (0.20, 0.50, 0.85) all should be smaller or equal to 1', default=[0.20, 0.50, 0.85], type=float, multiple=True)
@pass_config
def cli(config, trials, file, percentiles):
    """This software will help you to forecast when a backlog of a certain size will be 
    done or how many PBI you can do in a certain amount of iterations"""
    np_percentiles = np.array(percentiles)
    if np.any(np_percentiles <= 0) or np.any(np_percentiles > 1):
         print("Percentiles should be between 0 excluded and 1 included")
         sys.exit(1)
    click.echo(f"Reading {file}.")
    with rich.progress.open(file, "rb") as rich_file:
        config.data = pd.read_csv(rich_file, header=0)
    config.trials = trials
    config.percentiles = -np.sort(-np_percentiles)

@cli.command(help='Command to forecast when a certain amount of pbi can be done.')
@click.option('-b', '--backlog_size', default=50, help='Size of the backlog to forecast (Default: 50).')
@pass_config
def when(config, backlog_size,):
    iterations_output = []
    t = config.data['values'].to_numpy()    
    percentiles = config.percentiles
    for trial in track(range(config.trials), description='Processing...'):
        iterations = 0
        b_size = backlog_size
        while (b_size>=0):
            v = t[random.randint(0, t.size-1)]
            b_size = b_size - v
            iterations = iterations+1
        iterations_output.append(iterations)
    min = np.min(iterations_output)
    max = np.max(iterations_output)
    avg = np.average(iterations_output)
    std = np.std(iterations_output)
    print(f"* Forecast for {backlog_size} pbi on {config.trials} trials *")
    for p in percentiles:
        print(f'''* Number of iterations forecasted with {p*100}% confidence: {np.percentile(iterations_output, (p)*100, method="closest_observation")}''')
    print(f'* Min iterations {min:.2f} *')
    print(f'* Max iterations {max:.2f} *')
    print(f"* Avg iterations {avg:.2f} *")
    print(f"* Standard deviations  {std:.2f} *")

@cli.command(help='Command to forecast how many pbi can be don ein a certain amount of time.')
@click.option('-i', '--iterations', default=3, help='The number of iterations for which you are forecasting.', type=int)
@pass_config
def howmany(config, iterations):
    iterations_output = []
    t = config.data['values'].to_numpy()
    percentiles = config.percentiles
    for trial in track(range(config.trials), description='Processing...'):
        iteration = np.random.choice(t, iterations)
        iterations_output.append(iteration)
    expected_output = np.array(np.sum(iterations_output, axis=1))
    min = np.min(expected_output)
    max = np.max(expected_output)
    avg = np.average(expected_output)
    std = np.std(expected_output)
    print(f"* Forecast for {iterations} with {config.trials} trials *")
    for p in percentiles:
        print(
            f"""* Number of pbi forecasted with {p*100}% confidence: {np.percentile(expected_output, (1-p)*100, method="closest_observation")}"""
        )
    print(f"* Min pbi {min:.0f} *")
    print(f"* Max pbi {max:.0f} *")
    print(f"* Avg pbi {avg:.0f} *")
    print(f"* Standard deviations  {std:.0f} *")