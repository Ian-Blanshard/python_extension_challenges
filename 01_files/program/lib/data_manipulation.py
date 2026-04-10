import os

# == INSTRUCTIONS ==
#
# Below, you'll find lots of incomplete functions.
#
# Your job: Implement each function so that it does its job effectively.
#
# Tips:
# * Use the material, Python Docs and Google as much as you want
#
# * A warning: the data you are using may not contain quite what you expect;
#   cleaning data (or changing your program) might be necessary to cope with
#   "imperfect" data

# == EXERCISES ==

# Purpose: return a boolean, False if the file doesn't exist, True if it does
# Example:
#   Call:    does_file_exist("nonsense")
#   Returns: False
#   Call:    does_file_exist("AirQuality.csv")
#   Returns: True
# Notes:
# * Use the already imported "os" module to check whether a given filename exists
def does_file_exist(filename):
    if os.path.exists(filename):
        return True
    else:
        return False
    
# Purpose: get the contents of a given file and return them; if the file cannot be
# found, return a nice error message instead
# Example:
#   Call: get_file_contents("AirQuality.csv")
#   Returns:
#     Date;Time;CO(GT);PT08.S1(CO);NMHC(GT);C6H6(GT);PT08.S2(NMHC);[...]
#     10/03/2004;18.00.00;2,6;1360;150;11,9;1046;166;1056;113;1692;1268;[...]
#     [...]
#   Call: get_file_contents("nonsense")
#   Returns: "This file cannot be found!"
# Notes:
# * Learn how to open file as read-only
# * Learn how to close files you have opened
# * Use readlines() to read the contents
# * Use should use does_file_exist()
def get_file_contents(filename):
    if does_file_exist(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            return file.readlines()
    else:
        return "This file cannot be found!"

# Purpose: fetch Christmas Day (25th December) air quality data rows, and if
# boolean argument "include_header_row" is True, return the first header row
# from the filename as well (if it is False, omit that row)
# Example:
#   Call: christmas_day_air_quality("AirQuality.csv", True)
#   Returns:
#     Date;Time;CO(GT);PT08.S1(CO);NMHC(GT);C6H6(GT);PT08.S2(NMHC);[...]
#     25/12/2004;00.00.00;5,9;1505;-200;15,6;1168;567;525;169;1447;[...]
#     [...]
#   Call: christmas_day_air_quality("AirQuality.csv", False)
#   Returns:
#     25/12/2004;00.00.00;5,9;1505;-200;15,6;1168;567;525;169;1447;[...]
#     [...]
# Notes:
# * should use get_file_contents() - N.B. as should any subsequent
# functions you write, using anything previously built if and where necessary
def christmas_day_air_quality(filename, include_header_row):
    file = get_file_contents(filename)
    data = []
    if include_header_row:
        data.append(file[0])
    for row in file:
        if row[0:10] == '25/12/2004':
            data.append(row)
    return data
#####################################################################
######## my own function to process data into a useable format ######
#####################################################################
def process_data(filename):
    """
    returns dictionaries for each line of data 
    nested into an array
    """
    # open file and read contents
    file = get_file_contents(filename)

    # list to hold row data dictionaries
    processed_data = []

    # create list of headers
    headers = file[0].split(';')
    headers = headers[:-2]
    
    # create list for each row of data
    data_lists = []
    for row in file[1:]:
        seperate_data = row.split(';')
        seperate_data = seperate_data[:-2]   
        data_lists.append(seperate_data)
    
    # create dict for each row and add to processed data array
    for row in data_lists:
        row_dict = {k: v for k, v in zip(headers,row)}
        processed_data.append(row_dict)
    # function returns processed data
    return processed_data
 

# Purpose: fetch Christmas Day average of "PT08.S1(CO)" values to 2 decimal places
# Example:
#   Call: christmas_day_average_air_quality("AirQuality.csv")
#   Returns: 1439.21
# Data sample:
# Date;Time;CO(GT);PT08.S1(CO);NMHC(GT);C6H6(GT);PT08.S2(NMHC);NOx(GT);PT08.S3(NOx);NO2(GT);PT08.S4(NO2);PT08.S5(O3);T;RH;AH;;
# 10/03/2004;18.00.00;2,6;1360;150;11,9;1046;166;1056;113;1692;1268;13,6;48,9;0,7578;;
def christmas_day_average_air_quality(filename):

    data = process_data(filename)
    # filter all rows from christmas
    christmas = list(filter(lambda x: x['Date'][0:5] == '25/12', data))
    # create list of all the co values from christmas row
    christmas_co = [int(x['PT08.S1(CO)']) for x in christmas]
    # return average of co values 
    return round(sum(christmas_co) / len(christmas_co), 2)
    
    
    

# Purpose: scrape all the data and calculate average values for each of the 12 months
#          for the "PT08.S1(CO)" values, returning a dictionary of keys as integer
#          representations of months and values as the averages (to 2 decimal places)
# Example:
#   Call: get_averages_for_month("AirQuality.csv")
#   Returns: {1: 1003.47, [...], 12: 948.71}
# Notes:
# * Data from months across multiple years should all be averaged together
def get_averages_for_month(filename):

    data = process_data(filename)

    months = {}

    for i in range(1,13):

        if i < 10:
            i = '0' + str(i)
        else:
            i = str(i)

        month = list(filter(lambda x: x['Date'][3:5] == i, data))
        months[int(i)] = round(sum([int(x['PT08.S1(CO)']) for x in month]) / len(month),2)
    
    return months

# Purpose: write only the rows relating to March (any year) to a new file, in the same
# location as the original, including the header row of labels
# Example
#   Call: create_march_data("AirQuality.csv")
#   Returns: nothing, but writes header + March data to file called
#            "AirQualityMarch.csv" in same directory as "AirQuality.csv"
def create_march_data(filename):
    my_csv = ''

    # get header
    data = get_file_contents(filename)
    my_csv += data[0]

    # get march data
    data = process_data(filename)
    march = list(filter(lambda x: x['Date'][3:5] == '03', data))
    
    # add march data to csv string
    for d in march:
        line = ''
        for v in d.values():
            line += f'{v};'
        my_csv += line + ';\n'
    
    # write data to file
    f = open('AirQualityMarch.csv', 'w')
    f.write(my_csv)
    

# Purpose: write monthly responses files to a new directory called "monthly_responses",
# in the same location as AirQuality.csv, each using the name format "mm-yyyy.csv",
# including the header row of labels in each one.
# Example
#   Call: create_monthly_responses("AirQuality.csv")
#   Returns: nothing, but files such as monthly_responses/05-2004.csv exist containing
#            data matching responses from that month and year
def create_monthly_responses(filename):

    # create dir, if exists do nothing
    os.makedirs('monthly_responses', exist_ok=True)

    def build_csv(month_dictionary):
        """
        when passed a dict containing a months
        data build the csv and return it
        """
        # get header
        data = get_file_contents(filename)
        month_csv = data[0]
        # add month data to csv string
        for d in month_dictionary:
            line = ''
            for v in d.values():
                line += f'{v};'
            month_csv += line + ';\n'
        # return built csv
        return month_csv


    # get/process data
    data = process_data(filename)
    #loop through each year 2004/2005
    for year in range(2004,2006):
        # filter data for loops current year
        years_data = list(filter(lambda x: x['Date'][6:10] == str(year), data))
        # loop through that years data and create csv for each month
        for month in range(1,13):
            if month < 10:
                month = '0' + str(month)
            else:
                month = str(month)
            month_dict = list(filter(lambda x: x['Date'][3:5] == month, years_data))
            # if there is data for the month build csv and write to dir
            if month_dict:
                month_csv = build_csv(month_dict)
                with open(f'monthly_responses/{month}-{year}.csv', 'w') as f:
                    f.write(month_csv)

