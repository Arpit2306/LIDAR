# Define the paths to the input and output files
input_file_path = "C:\\Users\\Arpit0\\Downloads\\TestData.txt"
output_file_path = "D:\\LIDAR\\2CLASS.txt"

# Open the input file for reading
with open(input_file_path, 'r') as input_file:
    # Read all lines from the input file
    lines = input_file.readlines()

# Create a list to store filtered rows (include the header row)
filtered_rows = []

# Extract the header row (the first line)
header = lines[0]

# Remove double quotes from the header
header = header.replace('"', '')

# Append the modified header row to the filtered rows list
filtered_rows.append(header)

# Iterate through the data rows and filter rows with '2' or '5' in the "Classification" column
for line in lines[1:]:  # Skip the header row
    # Split the line into columns based on a comma delimiter
    columns = line.strip().split(',')
    
    # Check if the "Classification" column (index 3) contains '2' or '5'
    if columns[3] in ['2', '5']:
        filtered_rows.append(line)

# Open the output file for writing and write the modified header and filtered rows
with open(output_file_path, 'w') as output_file:
    output_file.writelines(filtered_rows)

print(f"Filtered rows containing '2' or '5' in the 'Classification' column have been written to {output_file_path}")
