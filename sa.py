import csv
import json

# Open the CSV file
data = []
with open('dataset.csv', mode='r', newline='') as file:
    reader = csv.reader(file)
    
    # Read each row without skipping the first one
    for row in reader:
        input=row[0].strip().strip("input:")
        output=row[1].strip().strip("output:")
        # Open the file in append mode
        data.append({"messages": [{"role": "system", "content": "You are an expert at crafting search queries for brands to find their dream brand ambassador."},  {"role": "user", "content": f"{input}"}, {"role": "assistant", "content": f"{output}."}]})





with open('data.jsonl', 'w') as f:
    # Write each item in the data list as a separate line
    for entry in data:
        json.dump(entry, f)
        f.write('\n')
