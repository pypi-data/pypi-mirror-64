import requests
from bs4 import BeautifulSoup
import pandas as pd

def load_words_polysemy(url, csv_file):
    print("loading words and polysemy")
    palabras = requests.get(url)
    soup = BeautifulSoup(palabras.content, 'html.parser')
    celdas = soup.find_all("td")

    lista_palabras = []
    lista_polysemy = []

    for idx, celda in enumerate(celdas):
        if idx % 6 == 0:
            lista_palabras.append(celda)
        elif (idx + 1) % 6 == 0:
            lista_polysemy.append(celda)

    palabras_polysemy = {}

    for palabra, poly in zip(lista_palabras, lista_polysemy):
        palabras_polysemy[palabra.text] = int(poly.text.strip())

    palabras_polysemy

    df = pd.DataFrame.from_dict(palabras_polysemy, orient='index')

    df.columns = ["polysemy"]
    df.to_csv(csv_file)
    print("Finished")
    return csv_file

if __name__ == "__main__":
    load_words_polysemy("https://en.wikipedia.org/wiki/Most_common_words_in_English")