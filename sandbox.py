import zzz_enums as enums
from classes.log import log, log_header
import pandas as pd

def modify_dataframe(df):
    # Modifying the DataFrame inside the function

    df.loc[1, 'Name'] = "chuj"

# Sample DataFrame
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 22],
    'City': ['New York', 'San Francisco', 'London']
}

df = pd.DataFrame(data)

# Display the original DataFrame
print("Original DataFrame:")
print(df)

# Call the function to modify the DataFrame
modify_dataframe(df)

# Display the DataFrame after modification
print("\nDataFrame after modification:")
print(df)