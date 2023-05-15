from import_requests_concat import process_csv_from_api

def main():
    start_date = "2023-05-01"
    end_date = "2023-05-15"
    start_time = "T03%3A00%3A00" #html encoding for 3am
    end_time = "T03%3A00%3A00"
    co2_url_template = "https://eif-research.feit.uts.edu.au/api/csv/?rFromDate={}{}&rToDate={}{}&rFamily=wasp&rSensor={}&rSubSensor=CO2"

    sensor_codes=[
        "ES_B_12_431_7BC2",
        "ES_B_08_422_7BDC",
        "ES_B_08_423_7BE2",
        "ES_B_04_415_7BD1",
        "ES_B_06_419_7C09",
        "ES_C_13_302_C88E",
        "ES_B_11_428_3EA4",
        "ES_B_07_420_7E1D",
        "ES_B_05_416_7C15",
        "ES_B_01_411_7E39"]
    
    def create_api_urls(sensor_codes, url_template):
        api_urls = []
        for sensor_code in sensor_codes:
            api_urls.append(url_template.format(start_date, start_time, end_date, end_time, sensor_code))
        return api_urls

    api_urls = create_api_urls(sensor_codes, co2_url_template)

    output_folder_name = "output"

    process_csv_from_api(api_urls, sensor_codes, output_folder_name)

if __name__ == "__main__":
    main()


