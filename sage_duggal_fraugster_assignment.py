#########
## Fraugster Data Scientist Assignment
## Sage Duggal
#########
## Note: I've included several commented out print statements which I used to
## debug in a Jupyter notebook. I thought these may help you see my thought process.
#########

import pandas as pd
import numpy as np
from geopy import distance # you may have to import this with pip install geopy

# step 1
df = pd.read_csv('realestate_fraugster_case.csv', delimiter = ';')

# step 2
# requires all rows to have at least 6 non-NA values
df = df.dropna(thresh = 6)

# street column
df['street'] = df['street'].str.title() 
df['street'] = df['street'].str.replace(r'[^A-Za-z0-9 ]+', '') # remove all special characters
df['street'] = df['street'].str.replace('  ', ' ') # remove double spaces

# city column
df['city'] = df['city'].str.title()
df['city'] = df['city'].str.replace(r'[^A-Za-z ]+', '')
#print(df.city.unique()) 
# Unique value inspection shows a few interesting city names like Elver,
# Foresthill, Cool, and Galt. These I manually confirmed the accuracy by Googling.

# zip code column
df['zip'] = df['zip'].str.replace(r'[^0-9]+', '')
df['zip'] = pd.to_numeric(df['zip']) #convert from string to int
#print(df.zip.describe())
# Can inspect using describe method. Min val, max val, and dtype all are correct.

# state column
df['state'] = df['state'].str.replace(r'[^A-Za-z]+', '')
#print(df.state.unique())
# Can verify this is correct by finding unique values and seeing only 'CA'.

# Beds, baths, and square feet
#print(df.beds.unique())
#print(df.beds.describe())
#print(df.baths.unique())
#print(df.baths.describe())
#print(df.sq__ft.describe())

# Looking at the basic properties of these columns shows there are no special
# character issues. We see the minimum value for all of these columns is 0. 
# Let's look in more detail:

#print(len(df.loc[df['beds'] == 0]))
#print(len(df.loc[df['baths'] ==0]))
#print(len(df.loc[df['sq__ft'] == 0]))

#print(len(df.loc[(df['beds'] == 0) & (df['baths'] == 0) & (df['sq__ft'] == 0)]))
# Using the 4 print statements above we can see that there are 108 rows with 0
# bedrooms, 108 rows with 0 bathrooms, 171 rows with 0 sq. ft., and 108 rows 
# with 0 bedrooms, 0 bathrooms, and 0 sq. ft. The 108 rows with 0s for beds,
# baths, and sq. ft could be vacant land or other real estate oddities, so while
# it's tempting to replaces these zeros with NaN, it would not be appropriate.

# This leaves the remaining 63 rows where beds and baths are non-zero while sq.
# ft. is zero. In this case, it's impossible to have a bedroom or bath with zero
# sq. ft., so we should replace these zeros with NaN.
df.loc[((df['beds'] != 0) & (df['sq__ft'] == 0)) | ((df['baths'] != 0) & (df['sq__ft'] == 0)), 'sq__ft'] = np.nan
#print(sum(df['sq__ft'].isna() == True)) #Answer should be 63.

# type column
df['type'] = df['type'].str.replace(r'[^-A-Za-z]+', '')
#print(df.type.unique())
# This revealed an unwanted string 'Unkown' which I cleaned to NaN.
df.loc[df['type'] == 'Unkown', 'type'] = np.nan

# sale_date column
df['sale_date'] = df['sale_date'].str.replace(r'[^-:0-9 ]+', '')
df['sale_date'] = pd.to_datetime(df['sale_date'])

# price column
df['price'] = df['price'].str.replace(r'[^0-9]+', '')
df['price'] = pd.to_numeric(df['price'])

# latitude column
df['latitude'] = df['latitude'].str.replace(r'[^\.0-9]+', '')
df['latitude'] = pd.to_numeric(df['latitude'])

# longitude column
df['longitude'] = df['longitude'].str.replace(r'[^-\.0-9]+', '')
df['longitude'] = pd.to_numeric(df['longitude'])

# step 3
df.to_csv('realestate_fraugster_case_clean.csv', index = False)

# step 4a
print('Outputs:\n')
min_price_index = df['price'].idxmin()
most_recent_sale_index = df['sale_date'].idxmax()

min_price_lat = df['latitude'][min_price_index]
min_price_long = df['longitude'][min_price_index]
min_price = (min_price_lat, min_price_long)

most_recent_sale_lat = df['latitude'][most_recent_sale_index]
most_recent_sale_long = df['longitude'][most_recent_sale_index]
most_recent_sale = (most_recent_sale_lat, most_recent_sale_long)

output_1 = distance.distance(min_price, most_recent_sale).meters
print(f'4a.\nThe distance between the cheapest sale and most recent sale is: {round(output_1,2)} meters.')

# step 4b
df_4b = df[(df['sale_date'] >= '1933-11-05 00:00:00') & (df['sale_date'] <= '1998-12-03 23:59:59') & (df['city'] == 'Sacramento') & (df['type'] == 'Multi-Family')]
df_4b = df_4b['street'].str.extract(r'(\d+)')

output_2 = df_4b[0].median()
print(f'\n4b.\nThe median street number between 05/11/1933 and 03/12/1998 \n(assuming European date format) considering only Multi-Family houses in \nSacramento is: {round(output_2)}.')

# step 4c
series_4c = df.groupby(['city'])['beds'].sum().sort_values(ascending = False)
second_highest_bed_count = series_4c[1]
second_highest_bed_city = series_4c.index[1]

most_common_zips = df[df['city'] == second_highest_bed_city].zip.value_counts()

print(f'\n4c.\nThe city name with the second highest bed count is {second_highest_bed_city} with {round(second_highest_bed_count)} beds sold.')
print(f'The three most common zip codes are {most_common_zips.index[0]}, {most_common_zips.index[1]}, and {most_common_zips.index[2]}.')

print('\nThank you for reviewing my assignment for the Fraugster Data Scientist role!\n-Sage Duggal')