# Create a CSV file with some data
data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
with open("my_data.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(data)

# Open the CSV file in Bard
with open("my_data.csv") as f:
    df = pd.read_csv(f)

# Insert the data into Bard
df.to_bard()