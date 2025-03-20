#CSCE A462 Assignment 1
#Alfred Soriano

#IMPORTANT: The best way to view and run this code is to open it under a Google Colab notebook.
#Each block is a new code snippet, which helps to separate all folium maps and outputs.

#BLOCK 1----------------------------------------------------------------------------------
import pandas as pd #used for pre-processing and data manipulation
pd.options.mode.chained_assignment = None

#read in .csv file and create a dataframe
df = pd.read_csv('Graffiti_20250319.csv')

#drop unnecessary columns and drop rows with NaN values
df = df.drop(columns=["CaseID", "Category", "Opened", "Closed", "Updated", "Status", "Status Notes", "Responsible Agency", "Neighborhood", "Supervisor District", "Address", "Source"])
df = df.dropna()

print(df.head())
print(f"Total number of graffiti reports: {len(df)}")
#BLOCK 1----------------------------------------------------------------------------------

#BLOCK 2----------------------------------------------------------------------------------
#ASSOCIATION RULES
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

#only get "not_offensive" and "offensive" types
df_apriori = df[df['Request Type'].isin(['not_offensive', 'offensive'])]
print(f"Total number of not_offensive & offensive graffiti reports: {len(df_apriori)}")

#target columns
transactions = df_apriori[['Request Type', 'Request Details']].values.tolist()

#apply transaction encoder (turns string data into boolean data)
te = TransactionEncoder()
te_ary = te.fit_transform(transactions)
df_apriori = pd.DataFrame(te_ary, columns=te.columns_)

#apriori algorithm
frequent_itemsets = apriori(df_apriori, min_support=0.03, use_colnames=True)

#generate association rules
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.3)

#filter out leverage, conviction, zhangs_metric, etc.
rules = rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']]

#print rules
rules

#SUPPORT is the frequency of a rule in a data set. Ex.) Rule 1: 3% of graffiti is on a commerical building and is offensive
#CONFIDENCE is the frequency that a rule is True. Ex.) Rule 0 & 1: For graffiti on commericial buildings, 65% of the time it's not offensive, 35% of the time it's offensive
#LIFT is the likelihood that the consequent will occur, given the antecedent. Ex.) Rule 1: If there is offensive graffiti, it's more likely that it will appear given that the offensive graffiti is on a commerical building.
#BLOCK 2----------------------------------------------------------------------------------

#BLOCK 3----------------------------------------------------------------------------------
#FOLIUM VISUALIZATION
import folium

#only get "not_offensive" and "offensive" types
df_folium = df[df['Request Type'].isin(['not_offensive', 'offensive'])]

#initialize a map at San Francisco
sf_map = folium.Map(location=[37.7749, -122.4194], zoom_start=12)

#extract latitude, longitude from Point column and drop unnecessary columns
df_folium['Coordinates'] = df_folium['Point'].str.replace("POINT (", "").str.replace(")", "")
df_folium[['Latitude', 'Longitude']] = df_folium['Coordinates'].str.split(' ', expand=True).astype(float)
df_folium = df_folium.drop(columns=['Point', 'Coordinates', 'Request Details'])

#plot points
for index, row in df_folium.iterrows():
    #get colors
    if row['Request Type'] == 'not_offensive':
        color = 'green'
    else:
        color = 'red'

    #add markers w/ color based on Request Type
    folium.CircleMarker(
        location=[row['Longitude'], row['Latitude']],
        radius=1,
        scale_radius=True,
        color=color,
    ).add_to(sf_map)

display(sf_map)

print(df_folium.head())
print(f"Total number of not_offensive & offensive graffiti reports: {len(df_folium)}")
#BLOCK 3----------------------------------------------------------------------------------

#BLOCK 4----------------------------------------------------------------------------------
#HEATMAP VISUALIZATION
from folium import plugins
from folium.plugins import HeatMap

#only get "not_offensive" and "offensive" types
df_heatmap = df[df['Request Type'].isin(['not_offensive', 'offensive'])]

#initialize heatmap starting coordinates and zoom level
sf_heatmap = folium.Map(location=[37.7749, -122.4194], zoom_start=12)

#extract latitude, longitude from Point column and drop unnecessary columns
df_heatmap['Coordinates'] = df_heatmap['Point'].str.replace("POINT (", "").str.replace(")", "")
df_heatmap[['Latitude', 'Longitude']] = df_heatmap['Coordinates'].str.split(' ', expand=True).astype(float)
df_heatmap = df_heatmap.drop(columns=['Point', 'Coordinates', 'Request Details'])

#creates a list of heat data points
heat_data = [[row['Longitude'],row['Latitude']] for index, row in df_heatmap.iterrows()]

#adds heat data points to map, according to specific display parameters
HeatMap(data=heat_data,
        radius=15,
        blur=14,
        min_opacity=0.15,
        ).add_to(sf_heatmap)

sf_heatmap
#BLOCK 4----------------------------------------------------------------------------------

#BLOCK 5----------------------------------------------------------------------------------
#CLUSTERING
from sklearn.cluster import DBSCAN

#only get "not_offensive" and "offensive" types
df_clustering = df[df['Request Type'].isin(['not_offensive', 'offensive'])]

#initialize cluster map
sf_clustermap = folium.Map(location=[37.7749, -122.4194], zoom_start=12)

#extract latitude, longitude from Point column and drop unnecessary columns
df_clustering['Coordinates'] = df_clustering['Point'].str.replace("POINT (", "").str.replace(")", "")
df_clustering[['Latitude', 'Longitude']] = df_clustering['Coordinates'].str.split(' ', expand=True).astype(float)
df_clustering = df_clustering.drop(columns=['Point', 'Request Details'])

#10% sample of the data (too much data causes crashes due to exceeding RAM limit)
df_clustering = df_clustering.sample(frac=0.1, random_state=2)

Coordinates = df_clustering[['Latitude', 'Longitude']].values

#need a low eps/min_samples to filter out noise, but need it high enough to provide signifiant cluster data
dbscan = DBSCAN(eps=0.0015, min_samples=10)
clusters = dbscan.fit_predict(Coordinates)


for i, (lat, lon) in enumerate(Coordinates):
    cluster_id = clusters[i]

    #handle noise
    if cluster_id == -1:
        continue #TOGGLE: Show noise or not
        color = 'gray'

    else:
        #assign a color to cluster
        colors = ['blueviolet', 'orangered', 'goldenrod', 'seagreen', 'dodgerblue', 'darkslategrey', 'mediumvioletred']
        color = colors[cluster_id % len(colors)]

    folium.CircleMarker(location=[lon, lat],
                        radius=5,
                        color=color,
                        fill=True,
                        fill_color=color).add_to(sf_clustermap)

sf_clustermap
#BLOCK 5----------------------------------------------------------------------------------