import click
import numpy as np
import pandas as pd

rng = np.random.default_rng()


@click.command()
@click.option("-d", "--start-date", default="1/1/2024", help="starting date")
@click.option("-s", "--size", default = 30, help='number of line to generate')
@click.option("-m", "--max-value", default=30, help="max random number to generate (inclusive) min is 0")
@click.option("-f","--file-name", default="example.csv", help="output file name, file with the same name are overwritten")
def cli(start_date, size, max_value, file_name):
    random_numbers = rng.integers(max_value+1, size=size)
    dates = pd.date_range(start=start_date, periods=size)
    values = {"dates": dates, "values":random_numbers}
    pd_data = pd.DataFrame(values)
    pd_data.to_csv(file_name, index=False)

if __name__ == "__main__":
    cli()
