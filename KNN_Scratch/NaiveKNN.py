import csv
import numpy as np

months = {"jan" : 0,"feb" : 1,"mar" : 2,"apr" : 3,"may" : 4,"june" : 5,
          "jul" : 6,"aug" : 7,"sep" : 8,"oct" : 9,"nov" : 10,"dec" : 11}


class KNN:

    def __init__(self ,train_X ,Train_Y, k=1):
        self.k = k
        self.train_X = train_X 
        self.train_Y = Train_Y
    

    def distance(self , x , X):
        return np.sqrt(np.sum((x - X)**2))


    def one_predict(self , x):
        
        neighbours =[self.distance(x,X) for X in self.train_X]
        Kneighbours = np.argsort(neighbours)[:self.k]
        one_count = 0
        zero_count = 0
        for val in Kneighbours:
            if self.train_Y[val] == 1:
                one_count+=1
            else: zero_count += 1

        return 1 if (one_count > zero_count) else 0
    

    def predict(self, test_X):
        predictions = []
        for X in test_X:
            predictions.append(self.one_predict(X))

        return predictions

    

def load_data():

    filename = "Shopping.csv"

    # Read data in from file
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)
        evidence = list()
        labels = list()
        for row in reader:
            
            evidence.append([
                int(row[0]),float(row[1]),int(row[2]),float(row[3]),int(row[4]),float(row[5]),float(row[6]),
                float(row[7]),float(row[8]),float(row[9]),int(months[row[10].lower()]),int(row[11]),int(row[12]),
                int(row[13]),int(row[14]),
                int(1 if row[15].lower() == "returning_visitor" else 0),
                int(1 if row[16].lower() == "true" else 0)
            ])

            labels.append(int(1 if row[-1].lower() == "true" else 0))

    evidence = np.array(evidence)
    labels = np.array(labels)
    return evidence,labels
    raise NotImplementedError



def compare(A , B):
    correct = 0
    incorrect = 0
    for A_val , B_val in zip(A,B):
        if A_val == B_val:
            correct += 1
        else:
            incorrect += 1
    
    
    return correct , incorrect


def main():

    data , labels = load_data()
    
    # spliting data
    holdout = int(0.60 * len(data))
    test_X = data[:holdout]
    train_X = data[holdout:]
    test_Y = labels[:holdout]
    train_Y = labels[holdout:]

    #initialising the model
    model = KNN(train_X , train_Y, 3)
    predictions = model.predict(test_X)

    # Comparing the prediction
    correct , incorrect = compare(predictions , test_Y)

    # Print results
    print(f"Results for KNN model")
    print(f"Correct: {correct}")
    print(f"Incorrect: {incorrect}")
    print(f"Accuracy: {100 * correct / (correct + incorrect):.2f}%")
    

if __name__ == "__main__":
    main()
