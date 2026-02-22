import pandas as pd

# Load dataset
df = pd.read_csv("fake reviews dataset.csv")

# Show the number of unique label values
print("Unique values in the label column:")
print(df["label"].unique())

# Show how many times each label appears
print("\nLabel value counts:")
print(df["label"].value_counts())