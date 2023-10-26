import pandas as pd
import numpy as np

data = pd.read_csv('E:/generation_facility_data/new_csv/output.csv')

def remove_duplicates():

    data.loc[data['Facility Name'] == 'Challicum Hills Wind Farm ', 'Power_Per_unit'] = 1.5
    data.loc[data['Facility Name'] == 'Challicum Hills Wind Farm', 'Power_Per_unit'] = 1.5
    data.loc[data['Facility Name'] == 'Clements Gap Wind Farm', 'Power_Per_unit'] = 2.1
    data.loc[data['Facility Name'] == 'Clements Gap Wind Farm ', 'Power_Per_unit'] = 2.1
    data.loc[data['Facility Name'] == 'Yambuk Wind Farm', 'Power_Per_unit'] = 1.3
    data.loc[data['Facility Name'] == 'Yambuk Wind Farm ', 'Power_Per_unit'] = 1.3
    data.loc[data['Facility Name'] == 'Starfish Hill Wind Farm', 'Power_Per_unit'] = 1.6
    data.loc[data['Facility Name'] == 'Windy Hill Wind Farm', 'Power_Per_unit'] = 0.6
    data.loc[data['Facility Name'] == 'Codrington Wind Farm', 'Power_Per_unit'] = 1.3
    data.loc[data['Facility Name'] == 'Codrington Wind Farm ', 'Power_Per_unit'] = 1.3
    data.loc[data['Facility Name'] == 'Wonthaggi Wind Farm', 'Power_Per_unit'] = 2
    data.loc[data['Facility Name'] == 'Clements Gap Wind Farm', 'Power_Per_unit'] = 2.1
    data.loc[data['Facility Name'] == 'Waterloo Wind Farm', 'Power_Per_unit'] = 3
    data.loc[data['Facility Name'] == 'Cathedral Rocks Wind Farm', 'Power_Per_unit'] = 2
    data.loc[data['Facility Name'] == 'Cathedral Rocks Wind Farm', 'Power_Per_unit'] = 2
    data.loc[data['Facility Name'] == 'Cathedral Rocks Wind Farm', 'Power_Per_unit'] = 2
    data.loc[data['Facility Name'] == 'Cathedral Rocks Wind Farm', 'Power_Per_unit'] = 2
    data.to_csv('E:/generation_facility_data/new_csv/data_process.csv', index=False)

def change_format():
    # Check the datatype of the "Total emissions (t CO2-e)" column
    column_dtype = data["Total_emissions"].dtype
    # Apply the string operation only if the column is of object (string) type
    if column_dtype == 'object':
        data["Total_emissions"] = pd.to_numeric(data["Total_emissions"].str.replace(',', ''), errors='coerce')
    data.to_csv('E:/generation_facility_data/new_csv/data_process.csv', index=False)

def rename():
    data.rename(columns={"Total emissions (t CO2-e)": "Total_emissions"}, inplace=True)
    data.rename(columns={"Power Per unit": "Power_Per_unit"}, inplace=True)
    data.rename(columns={"scope 1": "scope_1"}, inplace=True)
    data.rename(columns={"scope 2": "scope_2"}, inplace=True)
    data.to_csv('E:/generation_facility_data/new_csv/data_process.csv', index=False)

def missing_emission():
    scope1_dtype = data["scope_1"].dtype
    scope2_dtype = data["scope_2"].dtype
    if scope1_dtype == 'object':
        data["scope_1"] = pd.to_numeric(data["scope_1"].str.replace(',', ''), errors='coerce')
    if scope2_dtype == 'object':
        data["scope_2"] = pd.to_numeric(data["scope_2"].str.replace(',', ''), errors='coerce')
    # Update the "Total emissions (t CO2-e)" column for rows where "year" is 2013
    rows_2013 = data[(data["year"] == 2013) & (data["Total_emissions"].isna())]
    # Update "Total_emissions" to be the sum of "scope 1" and "scope 2" for these rows
    for idx in rows_2013.index:
        data.at[idx, "Total_emissions"] = data.at[idx, "scope_1"] + data.at[idx, "scope_2"]
    data.to_csv('E:/generation_facility_data/new_csv/data_process.csv', index=False)

def missing_turbine():
    data = pd.read_csv('E:/generation_facility_data/new_csv/data_process.csv')

    filtered_rows_new = data[(data["numbers"].isna()) | (data["Power_Per_unit"].isna())]

    reference_data_new = data.dropna(subset=["numbers", "Power_Per_unit", "Total_emissions"])

    for idx, row in filtered_rows_new.iterrows():
        differences = abs(reference_data_new["Total_emissions"] - row["Total_emissions"])

        if differences.isna().all():
            continue

        closest_idx = differences.idxmin()

        if pd.isna(row["numbers"]):
            data.at[idx, "numbers"] = reference_data_new.at[closest_idx, "numbers"]
        if pd.isna(row["Power_Per_unit"]):
            data.at[idx, "Power_Per_unit"] = reference_data_new.at[closest_idx, "Power_Per_unit"]
    data.to_csv('E:/generation_facility_data/new_csv/data_process.csv', index=False)

def nonnumeric_data_processing():
    data = pd.read_csv('E:/generation_facility_data/new_csv/data_process.csv')
    # Filter rows where "numbers" is not numeric
    non_numeric_numbers_rows = data[pd.to_numeric(data["numbers"], errors='coerce').isna()]

    reference_data_numbers = data.dropna(subset=["numbers", "Power_Per_unit", "Total_emissions"])
    reference_data_numbers = reference_data_numbers[
        pd.to_numeric(reference_data_numbers["numbers"], errors='coerce').notna()]

    for idx, row in non_numeric_numbers_rows.iterrows():
        differences = abs(reference_data_numbers["Total_emissions"] - row["Total_emissions"])

        if differences.isna().all():
            continue

        closest_idx = differences.idxmin()

        if pd.isna(row["numbers"]) or not isinstance(row["numbers"], (int, float)):
            data.at[idx, "numbers"] = reference_data_numbers.at[closest_idx, "numbers"]
        if pd.isna(row["Power_Per_unit"]):
            data.at[idx, "Power_Per_unit"] = reference_data_numbers.at[closest_idx, "Power_Per_unit"]

    data.to_csv('E:/generation_facility_data/new_csv/data_process.csv', index=False)


def all_data_process():
    rename()
    remove_duplicates()
    change_format()
    missing_emission()
    missing_turbine()
    nonnumeric_data_processing()
    print("Data Processing Finished")
