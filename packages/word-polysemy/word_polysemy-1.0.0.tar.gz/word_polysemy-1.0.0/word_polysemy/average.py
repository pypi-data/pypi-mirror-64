import pandas as pd
import numpy as np

def calculate_metrics(file, print_average, print_suma):
    df = pd.read_csv(file)
    column_values = df["polysemy"].values
    average = np.mean(column_values)
    suma = sum(column_values)
    if print_average:
        print(average)
    if print_suma:
        print(suma)

    return average, suma




