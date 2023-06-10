import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import Perceptron
from sklearn.naive_bayes import GaussianNB
from sklearn import svm

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """

    # Read data in from file
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)
        months = {
            "jan" : 0,
            "feb" : 1,
            "mar" : 2,
            "apr" : 3,
            "may" : 4,
            "june" : 5,
            "jul" : 6,
            "aug" : 7,
            "sep" : 8,
            "oct" : 9,
            "nov" : 10,
            "dec" : 11
        }
        evidence = list()
        labels = list()
        for row in reader:
            
            evidence.append([
                int(row[0]),
                float(row[1]),
                int(row[2]),
                float(row[3]),
                int(row[4]),
                float(row[5]),
                float(row[6]),
                float(row[7]),
                float(row[8]),
                float(row[9]),
                int(months[row[10].lower()]),
                int(row[11]),
                int(row[12]),
                int(row[13]),
                int(row[14]),
                int(1 if row[15].lower() == "returning_visitor" else 0),
                int(1 if row[16].lower() == "true" else 0)
            ])

            labels.append(int(1 if row[-1].lower() == "true" else 0))

    # X_training, X_testing, y_training, y_testing = train_test_split(
    #     evidence, labels, test_size=0.4
    # )

    return (evidence,labels)
    raise NotImplementedError


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """

    # model = Perceptron()
    # model = svm.SVC()
    # model = KNeighborsClassifier(n_neighbors=1)
    model = GaussianNB()

    # Fit model
    model.fit(evidence, labels)

    return model
    raise NotImplementedError


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    actual_Plabels = 0
    predict_Plabels = 0
    actual_Nlabels = 0
    predict_Nlabels = 0

    for label , prediction in zip(labels , predictions):
        if label:
            actual_Plabels += 1
            if prediction: predict_Plabels += 1
        else:
            actual_Nlabels += 1
            if not prediction: predict_Nlabels += 1

    sensitivity = predict_Plabels/actual_Plabels
    specificity = predict_Nlabels/actual_Nlabels

    return (sensitivity , specificity)

    raise NotImplementedError


if __name__ == "__main__":
    main()
