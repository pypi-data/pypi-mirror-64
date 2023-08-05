import argparse
import word_polysemy.plots.visualization as vi
import word_polysemy.average as av
import word_polysemy.top_ten as top
import word_polysemy.load_csv as lo

CSV_FILE = "palabras_polysemy.csv"

def pepito(mode, average, suma, number, print_top):
    url = "https://en.wikipedia.org/wiki/Most_common_words_in_English"
    csv = lo.load_words_polysemy(url, CSV_FILE)
    vi.plots(mode, csv)
    av.calculate_metrics(csv, average, suma)
    top.calculate_top(number, csv, print_top)


if __name__ == "__main__":
    # python -m word_polysemy.main boxplot --average_yes
    parser = argparse.ArgumentParser(description='Plot words polysemy')
    parser.add_argument('type', type=str,  help='choose the type of plot: "boxplot", "scatter", "barplot"')
    parser.add_argument('--average_yes', action="store_true", help='Use this flag to compute polysemy average. Otherwise it wont be done')
    parser.add_argument('--suma_yes', action="store_true", help='Use this flag to compute polysemy summatory. Other wise it wont be done')
    parser.add_argument('--top_no', action="store_false",help='Use this flag to NOT compute polysemy top N. Otherwise it won')
    parser.add_argument('--n_top', type=int , default=10, help='Introduce the number of top words to print to screen')
    args = parser.parse_args()
    pepito(args.type, args.average_yes, args.suma_yes, args.n_top, args.top_no)


