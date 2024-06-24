import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# Load the spreadsheet data
df = pd.read_excel("my_spreadsheet.xlsx")

# Create a linear regression model
model = LinearRegression()

# Fit the model to the data
model.fit(df["x"], df["y"])

# Make predictions
predictions = model.predict(df["x"])

# Evaluate the model
print(model.score(df["x"], df["y"]))
