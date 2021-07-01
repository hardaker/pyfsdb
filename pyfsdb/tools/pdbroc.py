"""Plots a ROC curve from a given FSDB file with a confidence and true column

This requires both matplotlib and sklearn to function.
"""

import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, plot_roc_curve, auc
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, FileType
from logging import debug, info, warning, error, critical
import logging
import sys
import pyfsdb

def parse_args():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter,
                            description=__doc__,
                            epilog="Exmaple Usage: pdbroc in_file.fsdb out_file.png")

    parser.add_argument("-t", "--truth-column", default="true", type=str,
                        help="Specifies the column name that marks the true rows")

    parser.add_argument("-T", "--truth-value", default="1", type=str,
                        help="Specifies the truth column value that should be used to indicate 'true'")

    parser.add_argument("-c", "--confidence-column", default="confidence", type=str,
                        help="The column name holding the confidence value")

    parser.add_argument("-i", "--invert-false-truths", action="store_true",
                        help="If specified, a 0 confidence for a false row will be considered a true negative (and a good classification) -- otherwise the confidence is supposed to respect the confidence of the truth value, higher always being better.")

    parser.add_argument("-l", "--label", default="ROC", type=str,
                        help="The label to put on the legend")

    parser.add_argument("-a", "--output-auc", action="store_true",
                        help="Output the AUC value to the terminal as well")

    parser.add_argument("--log-level", default="info",
                        help="Define the logging verbosity level (debug, info, warning, error, fotal, critical).")

    parser.add_argument("input_file", type=FileType('r'), nargs='?', default=sys.stdin,
                        help="The input FSDB file to plot")

    parser.add_argument("output_file", type=str, nargs='?', default="",
                        help="The output (PNG) file to write; if not specified plot in a window; if NONE don't plot at all (useful to just print AUC)")

    args = parser.parse_args()
    log_level = args.log_level.upper()
    logging.basicConfig(level=log_level,
                        format="%(levelname)-10s:\t%(message)s")
    return args


# taken from
# https://www.codespeedy.com/how-to-plot-roc-curve-using-sklearn-library-in-python/
def plot_roc(fpr, tpr, label="ROC"):
    plt.plot([0, 1], [0, 1], linestyle=':', color='black')
    plt.plot(fpr, tpr, color='blue', label=label)
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.legend()
    return plt


def main():
    args = parse_args()

    inh = pyfsdb.Fsdb(file_handle=args.input_file,
                      return_type=pyfsdb.RETURN_AS_DICTIONARY)

    confidence_column = args.confidence_column
    true_column = args.truth_column
    true_value = args.truth_value

    trues = []
    confidence = []
    for row in inh:
        if row[true_column] == true_value:
            trues.append(1)
            confidence.append(float(row[confidence_column]))
        else:
            trues.append(0)
            if args.invert_false_truths:
                confidence.append(1.0-float(row[confidence_column]))
            else:
                confidence.append(float(row[confidence_column]))

    (tpr, fpr, thresholds) = roc_curve(trues, confidence)
    plot_roc(fpr, tpr, label=args.label)

    if args.output_auc:
        print(f"AUC: {auc(fpr, tpr)}")

    if args.output_file:
        if args.output_file != "NONE":
            plt.savefig(args.output_file)
    else:
        plt.show()


if __name__ == "__main__":
    main()

