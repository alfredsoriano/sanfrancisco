# CSCE A462 Assignment 1 - Alfred Soriano
## Dataset and Libraries

This assignment looks at San Francisco data in order to help the city in some way.
The dataset I looked at is the Graffiti dataset from `https://data.sfgov.org/City-Infrastructure/Graffiti/vg6y-3pcr/about_data`

I use Google Colab which by default already has many python libraries installed.
However if you prefer to not use Colab, you can also upload the .ipynb file to VSCode and view it there. 
Note that you will need the following libraries if running in an environment other than Colab:
```
pandas   #used for data pre-processing and dataframes
mlxtend   #used for association rule extraction with the apriori algorithm
scikit-learn   #used for clustering areas of high graffiti with the DBSCAN algorithm
folium   #used for post-processing and visualization on a map of San Francisco
```

## Installation

You would just need to clone the repository the following command in a terminal.
```
git clone https://github.com/alfredsoriano/sanfrancisco.git
```
This contains the .ipynb file (the Google Colab Notebook file), which you can then open in either
Google Colab or VSCode. Installing and uploading it allows you to simply view the results and visualizations.
In case this does not work, the provided .py file allows for a manual way to install the code, however note that the program
was originally made using .ipynb features, and works best and easily as such.  

To run the code, please download the latest Graffiti dataset from the link `https://data.sfgov.org/City-Infrastructure/Graffiti/vg6y-3pcr/about_data`.
This is because the .csv file is too big to push to GitHub.
Note that this changes daily, so you must go to the first code block (shown below) and change the file path in the command `df = pd.read_csv('Graffiti_20250319.csv')` to the appropriate latest version.

```
import pandas as pd #used for pre-processing and data manipulation
pd.options.mode.chained_assignment = None

#read in .csv file and create a dataframe
df = pd.read_csv('Graffiti_20250319.csv') #IMPORTANT: CHANGE THE FILE NAME TO THE LATEST DATASET VERSION

#drop unnecessary columns and drop rows with NaN values
df = df.drop(columns=["CaseID", "Category", "Opened", "Closed", "Updated", "Status", "Status Notes", "Responsible Agency", "Neighborhood", "Supervisor District", "Address", "Source"])
df = df.dropna()

print(df.head())
print(f"Total number of graffiti reports: {len(df)}")
```

If running on Google Colab, you can simply press `ctrl + F9` to run all code blocks in sequence, which is necessary to do anyway.

## Documentation
Aim: Help San Francisco to identify areas with high amounts of graffiti, for both non offensive and offensive graffiti.
The information mined from the graffiti dataset allows San Francisco organizations and residents to look at several insights. The following are just two examples.  

1: Allows organizations to identify streets with large amounts of graffiti and target the areas with offensive graffiti (includes slurs, hate speech, or hateful visuals)  
2: Allows people to avoid areas with offensive graffiti, or even go to areas with non-offensive graffiti (includes text or artwork)  

**Association Rules**  
The following is a table of association rule extracted from the program, with explanations of how to interpret the data.  
Total number of not_offensive & offensive graffiti reports: 58222
| antecedents	| consequents	| support	| confidence	| lift | 
| ------------ | ------------ | ------------ | ------------ | ------------ |
| 0	| (building_commercial)	| (not_offensive)	| 0.065285	| 0.651414	| 0.894074 | 
| 1	| (building_commercial)	| (offensive)	| 0.034935	| 0.348586	| 1.284355 | 
| 2	| (mail_box)	| (not_offensive)	| 0.043025	| 0.778434	| 1.068410 | 
| 3	| (other)	| (not_offensive)	| 0.080571	| 0.762516	| 1.046563 | 
| 4	| (pole)	| (not_offensive)	| 0.109993	| 0.626002	| 0.859196 | 
| 5	| (sidewalk_in_front_of_property)	| (not_offensive)	| 0.131411	| 0.810917	| 1.112994 | 
| 6	| (signal_box)	| (not_offensive)	| 0.067380	| 0.766211	| 1.051634 | 
| 7	| (transit_shelter_platform)	| (not_offensive)	| 0.030933	| 0.858437	| 1.178215 | 
| 8	| (pole) | (offensive)	| 0.065714	| 0.373998	| 1.377985 | 
```
#SUPPORT is the frequency of a rule in a data set. Ex.) Rule 1: 3% of graffiti is on a commerical building and is offensive
#CONFIDENCE is the frequency that a rule is True. Ex.) Rule 0 & 1: For graffiti on commericial buildings, 65% of the time it's not offensive, 35% of the time it's offensive
#LIFT is the likelihood that the consequent will occur, given the antecedent. Ex.) Rule 1: If there is offensive graffiti, it's more likely that it will appear given that the offensive graffiti is on a commerical building.
```
  
**Clustering**  
To view the clustering map, and other visualizations such as the heatmap and non-offensive/offensive plot map,
I have included images of them in the images folder. However, they are interactive maps so the best way to view them is by opening
the included .ipynb notebook file in Google Colab or VSCode, as they are already ran and loaded into their respective code blocks.  
The images folder includes three images:
- sf_map shows the ~58,000 non-offensive/offensive points on San Francisco (useful for looking at concentrated areas of non-offensive/offensive graffiti)
- sf_heatmap shows these points in a heat map (useful for looking at high density areas, but has a bit of noise)
- sf_cluster shows these points in a DBSCAN clustered map (useful for looking at the most concentrated areas, without the noise)
