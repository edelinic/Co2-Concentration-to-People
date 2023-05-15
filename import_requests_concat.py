import requests 
import os
import csv
import pandas as pd

def process_csv_from_api(urls, sensor_codes, output_folder_name):
    # create a new folder in the current directory
    output_folder_path = os.path.join(os.getcwd(), output_folder_name)
    os.makedirs(output_folder_path, exist_ok=True)

    # create a new Excel file in the output folder
    output_file_path = os.path.join(output_folder_path, "concat_co2_sensors.xlsx")
    writer = pd.ExcelWriter(output_file_path,
                            engine="openpyxl",
                            datetime_format='mmm d yyyy hh:mm:ss',
                            date_format='mmmm dd yyyy')

    # create a list to store the resampled dataframes
    resampled_dfs = []
    
    for i, url in enumerate(urls):
        print("downloading from " + url)
        response = requests.get(url)

        if response.status_code == 200:
            # create a CSV reader object
            csv_reader = csv.reader(response.text.splitlines(), delimiter=',')

            sensor_code = sensor_codes[i]
            sheet_name = f"Sensor {sensor_code}"

            # create a new sheet for the CSV data
            sheet_name = f"Sensor {sensor_code}"
            df = pd.DataFrame(csv_reader, columns=["timestamp", f"Sensor {sensor_code}"])

            # Convert the 'timestamp' column to a datetime index
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            df.set_index("timestamp", inplace=True)

            # convert co2 concentration to numeric value
            df[f"Sensor {sensor_code}"] = pd.to_numeric(df[f"Sensor {sensor_code}"], errors='coerce')
           
            df = df.resample('10T').mean().interpolate()
            resampled_dfs.append(df)

            df.to_excel(writer, sheet_name=sheet_name)

            workbook  = writer.book
            worksheet = writer.sheets[sheet_name]
            # Hide the worksheet
            worksheet.sheet_state = 'hidden'
            
        else:
            print(f"Error retrieving CSV data from {url}")

    # combine the resampled data for all sensors into a single DataFrame
    combined_df = pd.concat(resampled_dfs, axis=1)

    combined_df['Average'] = combined_df.mean(axis=1)

    #drop tailing time (often blank after interpolation)
    combined_df.drop(combined_df.tail(1).index, inplace=True)

    # write the combined data to a single sheet in the Excel file
    combined_df.to_excel(writer, sheet_name="Combined Data")

    # save the Excel file
    writer._save()
