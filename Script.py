#%%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#%%
# 3. Import it as pandas.DataFrame and explore the data :
# %%
df = pd.read_table("CLRTAP_NVFR19_V23_1_GF_csv.csv", sep="\\t", header=0)
# %%
df.head()
# %%
# print all the name of the columns
for col in df.columns : print(col)
# %%
# print (number of rows, number of columns)
df.shape
# %%
# print the type of each column variable
df.info()
# %%
df.isna().sum()
# %%
df.describe()

#%%
# 4. Drop all other air pollutants except the one that is your own project topic.
  # Export and save the smaller dataset. 
  # Include the pollutant name in the file name.
# %%
df["Pollutant_name"].unique()
# %%
df_nm = df[df["Pollutant_name"]=="NMVOC"]
# %%
df_nm.head()
# %%
df_nm.shape
# %%
df_nm.to_excel('CLRTAP_NMVOC.xlsx')


#%%
# PHASE II : 

#%%
# 5. Import the CLRTAP data including only your own pollutant 
# as a DataFrame (Shape: 146 506, 12) :
#%%
df = pd.read_excel("CLRTAP_NMVOC.xlsx")

#%%
# 6. Explore the data and calculate some summary statistics 
# of the “Emissions” -variable :
#%%
df.shape
# %%
df.info()
# %%
df.describe()
# %%
df.nunique()
# %%
pd.unique(df["Sector_name"])
# %%
df["Emissions"].describe()
# %%
df["Emissions"].sum()
# %%
df["Emissions"].median()

#%%
# 7. Check the number of missing values of each variable :
     # Consider how to deal with them (or how would you deal with them 
     # if there were any missing values). Could you treat them as zeros?
# %%
df.head()

# %%
# Checking the amount of missing values
df.isna().sum()

# %%
# Dropping the rows with missing emission values
df_nona = df.dropna(subset = "Emissions")

# %%
#Checking the shape
df_nona.shape

# %%
# Dropping the rows with a sector code of national total
df_nona = df_nona[df_nona["Sector_code"] != "NATIONAL TOTAL"]

#%%
#Finding all the unique country names in the dataset
df_nona["Country"].unique()

# %%
#Creating two dataframes. One for the emissions in EU27 and one for EEA32
df_EU27 = df_nona[df_nona["Country"] == "EU27"]
df_EEA32 = df_nona[df_nona["Country"] == "EEA32"]

# %%
#Creating a dataframe without EU27 and EEA32 to prevent double counting of emissions
df_countries = df_nona.drop(df_nona[df_nona["Country"] == "EU27"].index)
df_countries = df_countries.drop(df_countries[df_countries["Country"] == "EEA32"].index)

# %%
#Checking if EU27 and EEA32 were dropped correctly
df_countries["Country"].unique()

#%%
# 8. Create a new geographical variable dividing Europe 
# to four different regions: North, East, South, West :
# %%
# Creating lists of what countries are in what region
north =["Denmark","Finland","Ireland","Sweden","Estonia","Lithuania",
        "Latvia","Iceland","Norway"]
south = ["Greece","Italy","Portugal","Spain","Croatia","Malta","Slovenia"]
east = ["Bulgaria","Cyprus","Czech Republic","Hungary","Poland","Romania",
        "Slovakia","Türkiye"]
west = ["Austria","Belgium","France","Germany","Luxembourg","Netherlands",
        "Switzerland","Liechtenstein"]
# Creating a new column for region. Using country as a temporary value
df_countries["Region"] = df_countries["Country"]

# %%
#Replacing the country name in the region column with the corresponding region based on region lists
df_countries["Region"].replace(["Denmark","Finland","Ireland","Sweden","Estonia","Lithuania",
        "Latvia","Iceland","Norway"], "North", inplace=True)
df_countries["Region"].replace(["Austria","Belgium","France","Germany","Luxembourg","Netherlands",
        "Switzerland","Liechtenstein"], "West", inplace=True)
df_countries["Region"].replace(["Greece","Italy","Portugal","Spain","Croatia","Malta","Slovenia"], "South", inplace=True)
df_countries["Region"].replace(["Bulgaria","Cyprus","Czech Republic","Hungary","Poland","Romania",
        "Slovakia","Türkiye"], "East", inplace=True)

# %%
# Checking if the regions are correctly incorporated
df_countries

#%%
# 9. Calculate and print the total sum of emissions (cumulative over years).
     # Note that Pandas sum() -method treats missing values 
     # as zeros for default (skipna=True).
     # Is it fine or a problem in this case?

# %%
# When finding total emissions we assume that EU27 covers all the countries in EU
# This is not the truth but a simplification
# Grouping by year and emissions
emissions_year_EU27 = df_EU27.groupby("Year")["Emissions"].sum()

# %%
# Finding the cumulative emissions from EU27
emissions_year_cum_EU27 = emissions_year_EU27.cumsum()

# %%
# Printing to see if the results were as wanted and to compare total emissions for later
print(emissions_year_cum_EU27)

#%%
# 10. Calculate the sum of emissions by region and year,
# make it a new DataFrame (Shape: 186 rows, 3 columns):

# %%
# Grouping the emissions by country and year for comparison reasons
emissions_year_country = df_countries.groupby(["Country", "Year"])["Emissions"].sum()

# %%
# Printing to check if it worked
print(emissions_year_country)

# %%
# Grouping emissions by region and year
emissions_reg = df_countries.groupby(["Region", "Year"])["Emissions"].sum()
# %%
# Inspecting the results
emissions_reg

# %%
# Grouping emissions by only year. 
emissions_year = df_countries.groupby(["Year"])["Emissions"].sum()
# %%
# Double checking to see if grouping worked
emissions_year

#%%
# 11. Draw line plots of the total emissions of your pollutant
#  in the four European regions and in Europe in total :
# %%
# Plotting the total EU emissions per year
plt.plot(emissions_year)
plt.title("EU27 emissions Over Time")
plt.xlabel("Year")
plt.ylabel("Emissions")
plt.legend()

plt.show()

# %%
# Creating a pandas dataframe out of the series
df2 = pd.DataFrame(emissions_reg)
#%%
# Checking if the conversion worked
df2

#%%
# Creating a list of the regions
regions = df2.index.get_level_values("Region").unique()

# Plotting the emissions by year in four seperate lines for each region
for region in regions:
    region_data = df2.xs(region, level="Region")
    plt.plot(region_data.index.get_level_values("Year"), region_data["Emissions"], label=region)

plt.title("Cumulative Emissions by Region Over Time")
plt.xlabel("Year")
plt.ylabel("Emissions")
plt.legend()

plt.show()

# %%
# PART 3 : Finding and adding new data

#%%
# Task 13. : Find out, what is the largest emission source of your pollutant :

#%%
# Creating a dataframe grouped by sector names
df_sectors = pd.DataFrame(df_nona.groupby("Sector_name")["Emissions"].sum())
# %%
# Sorting the sectors by emissions
df_sectors = df_sectors.sort_values(by='Emissions',ascending=False)

# %%
# Printing sorted list to see which sectors were the most emiting
df_sectors

#%%
# Task 14. : Create a new DataFrame including only the main sector 
# and excluding all other sectors. Keep all variables (columns) :

# %%
# Creating a dataframe for the passenger car sector
df_passenger_cars = df[df["Sector_name"] == "Road transport: Passenger cars"]
# %%
# Inspecting the passenger car dataframe
df_passenger_cars
# %%
# Creating a dataframe for EU passenger car emissions
df_cars_EU27 = df_EU27[df_EU27["Sector_name"] == "Road transport: Passenger cars"]
# %%
# Inspecting the dataframe of EU passenger car emissions
df_cars_EU27

#%%
# Task 15. : Calculate the sum of emissions in the main sector in the EU27 
# by year and put it in a smaller DataFrame (Shape: 31, 3) :

# %%
# Creating a dataframe of the yearly emissions of cars int he EU
EU27_cars_by_year = pd.DataFrame(df_cars_EU27.groupby(["Year"])["Emissions"].sum())
# %%
# Inspecting the dataframe
EU27_cars_by_year
# %%
# Looking at the shape of the dataframe
EU27_cars_by_year.shape

# %%
# Task 17. : Process the new dataset so that you can combine it 
# with the emissions DataFrame in Python :

#%%
# Extracting a seperate dataset of emissions from EU passenger cars
CO2_cars_EU = pd.read_excel("eu-sdg-12-30_2000-2022_v01_r00.xlsx", sheet_name=1)

# %%
# Inspecting the dataset
CO2_cars_EU.head()

# %%
# Dropping the first 8 rows and the 10th row because they dont matter
CO2_cars_EU = CO2_cars_EU.drop([0,1,2,3,4,5,6,7,9])

# %%
# Inspecting the resulting database
CO2_cars_EU.head()

# %%
# Modify the header :
new_header = CO2_cars_EU.iloc[0]
CO2_cars_EU.columns = new_header #set the header row as the df header
CO2_cars_EU = CO2_cars_EU[1:] #take the data less the header row

#%%
# Inspecting the new dataset
CO2_cars_EU.head()

#%%
# Replacing the : with NaN
CO2_cars_EU = CO2_cars_EU.replace(to_replace=":", value=np.NaN)
CO2_cars_EU.head()

# %%
# Extracting the wanted rows
CO2_cars_EU = CO2_cars_EU.iloc[1]

# %%
# Inspecting the resulting dataset
CO2_cars_EU

# %%
# Extracting the wanted rows from the dataset
CO2_cars_EU =CO2_cars_EU.iloc[3:]

# %%
# Inspecting the result
CO2_cars_EU

# %%
# Looking at the infor of the dataset. This is where we realised we had a series and not a df
CO2_cars_EU.info()

#%%
# 18. Make a plot comparing the other indicator and 
# the emissions of your pollutant in the sector that causes 
# the highest emissions of your pollutant in the EU27. 

# This gives you an additional indication about the success 
# of policies restricting the emissions of your pollutant.

# %%
# If we take the row for EU27, there are missing values from 2000 to 2006
# so the values begin on the 2007 which is quite sad compared to
# the other dataset where the data begin on the 1990...

# Let's see if it's still interesting :

#%%
# Making the previous dataset values into numeric values rather than objects
df3 = pd.to_numeric(CO2_cars_EU, errors='coerce')

#%% 
# Making the index of the dataset int64 to match the dataset from task 10-11
df3.index = df3.index.astype(int)

#%%
# Inspecting the dataset
df3

#%%
# Comparing the info of this series to the dataframe of emissions_year
df3.info()

#%%
# Comparing this info to the df3 info
emissions_year.info()

# %%
# Plotting the total NMVOC emissions and the CO2 emissions from new passenger cars against each other
fig,ax = plt.subplots()

ax.plot(emissions_year, color = "red")
ax.set_xlabel("Years")
ax.set_ylabel("Emissions of NMVOC", color = "red")
ax.set_title("NMVOC and CO2 emissions in new passengers cars")

ax2 = ax.twinx()

ax2.plot(df3, color = "blue")
ax2.set_ylabel("Average CO2 emissions per km from new passenger cars", color = "blue")

plt.show()