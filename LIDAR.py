from river import metrics, preprocessing, compose, stream
from deep_river import classification
from torch import nn
from torch import optim
import matplotlib.pyplot as plt  
from torch import manual_seed

import numpy as np
from river.stream import iter_array
from sklearn.model_selection import train_test_split
from tqdm import tqdm
from river.metrics import Accuracy

_ = manual_seed(42)

class MyModule(nn.Module):
     def __init__(self, n_features):
         super(MyModule, self).__init__()
         self.dense0 = nn.Linear(n_features, 6)
         self.nonlin = nn.ReLU()
         self.dense1 = nn.Linear(6, 20)
         self.nonlin = nn.ReLU()
         self.dense2 = nn.Linear(20,60)
         self.nonlin = nn.ReLU()
         self.dense3 = nn.Linear(60,100)
         self.nonlin = nn.ReLU()
         self.dense4 = nn.Linear(100,40)
         self.nonlin = nn.ReLU()
         self.dense5 = nn.Linear(40,14)
         self.softmax = nn.Softmax(dim=-1)

     def forward(self, X, **kwargs):
         X = self.nonlin(self.dense0(X))
         X = self.nonlin(self.dense1(X))
         X = self.nonlin(self.dense2(X))
         X = self.nonlin(self.dense3(X))
         X = self.nonlin(self.dense4(X))
         X = self.nonlin(self.dense5(X))
         X = self.softmax(X)
         return X

model_pipeline = compose.Pipeline(
     preprocessing.StandardScaler(),
     classification.Classifier(module=MyModule, loss_fn='cross_entropy', optimizer_fn='adam')
 )


dataset = stream.iter_csv(r"D:\Shree\LiDAR_TAAL_TXT\txt_files\E276N1559_LAZ_PL1_GHV.txt") #generator "dataset" in iterable format, can print the values only when iterated.
metric = metrics.Accuracy()
accuracies = []
counter = 0
point_counts = []
#print(len(dataset))
for x, y in tqdm(dataset):
    data_list = list(x.values())
    key_list = list(x.keys())

    x1 = {}
    y1 = float(x.pop("Classification"))

    for k, v in x.items():
        x1[k] = float(v)

    y_pred = model_pipeline.predict_one(x1)
    metric = metric.update(y1, y_pred)
    model_pipeline = model_pipeline.learn_one(x1, y1)
    
    counter += 1
    
    if counter % 1000 == 0:
        accuracy = metric.get()
        print(f"Processed {counter} points. Accuracy: {accuracy:.4f}")
        
        # Store accuracy and point count for plotting
        accuracies.append(accuracy)
        point_counts.append(counter)

# Plot the accuracy graph
plt.figure(figsize=(8, 6))
plt.plot(point_counts, accuracies, marker='o', linestyle='-', color='b')
plt.title("Accuracy vs. Number of Points Processed")
plt.xlabel("Number of Points Processed")
plt.ylabel("Accuracy")
plt.grid(True)
plt.show()


print(f"cross_entropy, adam, 5 Layers_100,40,14 nuerons Accuracy: {metric.get():.4f}")
