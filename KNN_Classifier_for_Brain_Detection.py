import numpy as np
import csv
from PIL import Image

image1 = Image.open(r'C:\Users\Toni\Desktop\Proiecte\AI\Proiect\Program\data\images\000001.png').convert('L')
array1 = np.array(image1).flatten()

image2 = Image.open(r'C:\Users\Toni\Desktop\Proiecte\AI\Proiect\Program\data\images\000002.png').convert('L')
array2 = np.array(image2).flatten()
train_data = np.vstack([array1, array2])

for i in range(3, 22150):
    image3 = Image.open(rf'C:\Users\Toni\Desktop\Proiecte\AI\Proiect\Program\data\images\{ i.__str__().zfill(6) }.png').convert('L')
    array3 = np.array(image3).flatten()
    train_data = np.vstack([train_data, array3])

train_labels = []
with open(r'C:\Users\Toni\Desktop\Proiecte\AI\Proiect\Program\train_labels.txt') as f:
    for line in f:
        if(line[0] != 'i'):
            label = int(line.split(',')[1][0])
            train_labels.append(label)

class Brain_Anomaly_Detection:
    def __init__(self, k, train_data, train_labels):
        self.k = k
        self.train_data = train_data
        self.train_labels = train_labels
    
    def euclidean_distance(self, a, b):
        return np.sqrt(np.sum((a - b)**2))
    
    def predict_class(self, img):
        distances = []
        for i in range(self.train_data.shape[0]):
            distance = self.euclidean_distance(self.train_data[i], img)
            distances.append((distance, self.train_labels[i]))
        
        distances.sort(key=lambda x: x[0])
        
        neighbors = distances[:self.k]
        labels = [neighbor[1] for neighbor in neighbors]
        label_counts = np.bincount(labels)
        
        if len(label_counts) == 0:
            # no neighbors found, default to class 0
            return 0
        else:
            return np.argmax(label_counts)
    
    def predict_all(self, test_data):
        predictions = []
        for i in range(test_data.shape[0]):
            prediction = self.predict_class(test_data[i])
            predictions.append(prediction)
        return predictions
    
    def evaluate(self, test_data, test_labels):
        predictions = self.predict_all(test_data)
        accuracy = np.sum(predictions == test_labels) / test_labels.shape[0]
        return accuracy
    
    def write_to_csv(self, test_data, file_path):
        predictions = self.predict_all(test_data)
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'class'])
            for i in range(test_data.shape[0]):
                writer.writerow([f'0{i}', predictions[i]])


model = Brain_Anomaly_Detection(5, train_data[:17000], train_labels)
model.write_to_csv(train_data[17000:], rf"C:\Users\Toni\Desktop\Proiecte\AI\Proiect\Program\predictions.csv")