# CSCE A462 Assignment 1 - Alfred Soriano
## Dataset and Libraries

This assignment looks at San Francisco data in order to help the city in some way.
The dataset I looked at is the Graffiti dataset from `https://data.sfgov.org/City-Infrastructure/Graffiti/vg6y-3pcr/about_data`

I use Google Colab which by default already has many python libraries installed.
However if you prefer to not use Colab, the libraries needed are:
```
pandas
mlxtend
scikit-learn
folium
```

## Installation

You would just need to clone the repository the following command in a terminal.
```
git clone https://github.com/alfredsoriano/sanfrancisco.git
```
This contains the .ipynb file (the Google Colab Notebook file), which you can then open in either
Google Colab or VSCode. Installing it allows you to view the results.

To run the file, please download the latest Graffiti dataset from the link `https://data.sfgov.org/City-Infrastructure/Graffiti/vg6y-3pcr/about_data`.
This is because the .csv file is too big to push to GitHub.
Note that this changes daily, so you must go to the first code block (shown below) and change the file path in the command `df = pd.read_csv('Graffiti_20250319.csv')` to the appropriate latest version.

```
import pandas as pd #used for pre-processing and data manipulation
pd.options.mode.chained_assignment = None

#read in .csv file and create a dataframe
df = pd.read_csv('Graffiti_20250319.csv')

#drop unnecessary columns and drop rows with NaN values
df = df.drop(columns=["CaseID", "Category", "Opened", "Closed", "Updated", "Status", "Status Notes", "Responsible Agency", "Neighborhood", "Supervisor District", "Address", "Source"])
df = df.dropna()

print(df.head())
print(f"Total number of graffiti reports: {len(df)}")
```

## Documentation
