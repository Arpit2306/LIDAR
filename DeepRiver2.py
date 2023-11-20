from river import metrics, datasets, preprocessing, compose
from deep_river import classification
from torch import nn
from torch import optim
from torch import manual_seed
from itertools import islice
_ = manual_seed(42)

class MyModule(nn.Module):
    def __init__(self, n_features):
        super(MyModule, self).__init__()
        self.dense0 = nn.Linear(n_features, 5)
        self.nonlin = nn.ReLU()
        self.dense1 = nn.Linear(5, 2)
        self.softmax = nn.Softmax(dim=-1)

    def forward(self, X, **kwargs):
        X = self.nonlin(self.dense0(X))
        X = self.nonlin(self.dense1(X))
        X = self.softmax(X)
        return X

model_pipeline = compose.Pipeline(
    preprocessing.StandardScaler(),
    classification.Classifier(module=MyModule, loss_fn='binary_cross_entropy', optimizer_fn='adam')
)

dataset = datasets.Phishing()
metric = metrics.Accuracy()
window_size = 1000  # Size of the rolling window
window_counter = 0  # Counter for window number

# Create a rolling window generator
rolling_window = zip(*(islice(iter(dataset), i, None) for i in range(window_size)))

for window_data in rolling_window:
    prev_X, prev_y = zip(*window_data)
    
    # Train the model on the previous 100 points
    for prev_x, prev_y_label in zip(prev_X, prev_y):
        y_pred = model_pipeline.predict_one(prev_x)
        model_pipeline = model_pipeline.learn_one(prev_x, prev_y_label)
    
    # Calculate accuracy for the current window
    accuracy = metrics.Accuracy()
    for x_next, y_next in islice(iter(dataset), window_size, None):
        y_pred_next = model_pipeline.predict_one(x_next)
        accuracy = accuracy.update(y_next, y_pred_next)
    
    window_counter += 1
    print(f"Accuracy for {window_counter * window_size} points: {accuracy.get():.4f}")
    metric = metric.update(y_next, y_pred_next)

# Calculate and print the final accuracy
final_accuracy = metric.get()
print(f"Final Accuracy: {final_accuracy:.4f}")
