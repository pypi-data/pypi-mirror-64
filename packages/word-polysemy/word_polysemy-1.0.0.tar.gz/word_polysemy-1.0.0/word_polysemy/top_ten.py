import pandas as pd

def calculate_top(number, file, print_top):
    df = pd.read_csv(file)
    top = df.nlargest(number, "polysemy").values
    if print_top:
        print(top)
    return top