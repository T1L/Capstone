import pandas as pd
data = pd.read_csv('E:/generation_facility_data/new_csv/data_process.csv')
import numpy as np


def remove_outliers():
    import pandas as pd
    data = pd.read_csv('E:/generation_facility_data/new_csv/data_augmentation.csv')
    ratio = data['Total_emissions'] / (data['numbers'] * data['Power_Per_unit'])
    Q1 = ratio.quantile(0.25)
    Q3 = ratio.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = data[(ratio < lower_bound) | (ratio > upper_bound)]
    median_ratio = ratio[(ratio >= lower_bound) & (ratio <= upper_bound)].median()
    data.loc[outliers.index, 'Total_emissions'] = (data['numbers'] * data['Power_Per_unit']) * (median_ratio + 1)
    file_path = "E:/generation_facility_data/new_csv/data_augmentation.csv"
    data.to_csv(file_path, index=False)


def augment_data(row):
    noise_factor = 0.1
    row['Total_emissions'] = row['Total_emissions'] * (1 + noise_factor * (2 * np.random.rand() - 1))
    row['numbers'] = int(row['numbers'] + row['numbers'] * noise_factor * (2 * np.random.rand() - 1))
    row['Power_Per_unit'] = row['Power_Per_unit'] * (1 + noise_factor * (2 * np.random.rand() - 1))
    return row


def generate_data():
    data = pd.read_csv('E:/generation_facility_data/new_csv/data_process.csv')
    new_rows = []
    for _ in range(600):
        while True:
            random_row = data.sample(1).iloc[0].copy()
            augmented_row = augment_data(random_row)

            # Check if augmented values are not zero
            if augmented_row['Power_Per_unit'] != 0 and augmented_row['numbers'] != 0:
                break

        new_rows.append(augmented_row)

    # Create a DataFrame from the new rows
    new_data = pd.DataFrame(new_rows)
    augmented_data = pd.concat([data, new_data], ignore_index=True)
    augmented_data['Total_emissions'] = augmented_data['Total_emissions'].round(1)
    augmented_data['Power_Per_unit'] = augmented_data['Power_Per_unit'].round(1)
    # Save the augmented data to a new CSV file
    augmented_data = augmented_data[augmented_data['Total_emissions'] != 0]
    file_path = "E:/generation_facility_data/new_csv/data_augmentation.csv"
    augmented_data.to_csv(file_path, index=False)


def data_Augmentation():
    generate_data()
    remove_outliers()
    print("Data Augmentation Complete")

data_Augmentation()