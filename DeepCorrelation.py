import numpy as np
from scipy.stats import pearsonr

# Load data from the file
file_path = "C:\\Users\\Arpit0\\Downloads\\TestData.txt"

try:
    with open(file_path, 'r') as file:
        lines = file.readlines()
except FileNotFoundError:
    print(f"File not found at: {file_path}")
    exit()

# Initialize lists to store X and Y values
x = []
y = []

# Initialize a counter to keep track of the number of data points processed
count = 0

# Loop through the data
for line in lines[1:]:  # Skip the header line
    values = line.strip().split(',')
    if len(values) >= 2:
        x.append(float(values[0]))
        y.append(float(values[1]))
        count += 1
        
        # Calculate and print correlation every 50 data points
        if count % 100 == 0:
            correlation_coefficient, _ = pearsonr(x, y)
            print(f"Pearson Correlation Coefficient after {count} data points: {correlation_coefficient:.4f}")

# Calculate and print the final correlation
correlation_coefficient, _ = pearsonr(x, y)
print(f"Final Pearson Correlation Coefficient between X and Y: {correlation_coefficient:.4f}")

if correlation_coefficient == 0:
    print("No correlation")
elif 0 < correlation_coefficient < 1:
    print("Positive Correlation")
elif correlation_coefficient == 1:
    print("Perfect Positive Correlation")
elif -1 < correlation_coefficient < 0:
    print("Negative Correlation")
elif correlation_coefficient == -1:
    print("Perfect Negative Correlation")
else:
    print("ERROR!!")
