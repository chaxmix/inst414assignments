import requests

# API endpoint and key
url = "https://holidays.abstractapi.com/v1/"
api_key = "31678cd35fb64b0d885c783381a84493"

# Parameters for the API call
params = {
    "api_key": api_key,
    "country": "US",
    "year": "2020"
}

# Make the API call
response = requests.get(url, params=params)

# Check if the API call was successful
if response.status_code == 200:
    # Create a dictionary to store the count of holidays for each month
    holiday_count = {}
    for month in range(1, 13):
        holiday_count[month] = 0

    # Count the number of holidays for each month
    holidays = response.json()
    for holiday in holidays:
        month = int(holiday["date"][:2])
        holiday_count[month] += 1

    # Print the dictionary of holiday counts by month
    print(holiday_count)

else:
    print("Error")