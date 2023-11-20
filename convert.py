import csv

# Define the input and output file paths
input_file_path = "C:\\Users\\Arpit0\\Downloads\\ADAGANT.txt"  # Replace with the actual file path
output_file_path = "D:\\CSV.csv"  # Specify the desired CSV file name

# Open the input text file and create a CSV writer for the output file
with open(input_file_path, 'r', encoding='latin-1') as input_file, open(output_file_path, 'w', newline='', encoding='utf-8') as output_file:
    # Create a CSV writer with a comma as the delimiter
    csv_writer = csv.writer(output_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    
    # Initialize a flag to skip the header rows
    skip_header = True
    
    # Process each line in the text file
    for line in input_file:
        # Remove leading and trailing whitespace and split the line into columns based on spaces
        columns = line.strip().split()
        
        # Check if the line contains data (not just headers)
        if len(columns) > 0:
            # Write the columns to the CSV file
            csv_writer.writerow(columns)
        else:
            # Skip empty lines and header rows
            continue

print(f"Text file '{input_file_path}' has been converted to '{output_file_path}'")
