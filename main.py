import csv
import threading
import requests
from config import api_key

res_all_vals = []

def extract_num_details(num):
    try:
        url = f"http://apilayer.net/api/validate?access_key={api_key}&number={num}"
        r = requests.get(url)
        print("response:- ", r, "number:- ", num)
        if r.status_code != 200:
            return ["", "", "", "", "", "", "", "", ""]
        result = r.json()
        if result.get('valid') == True:
            number = result.get("number")
            local_format = result.get("local_format")
            international_format = result.get("international_format")
            country_prefix = result.get("country_prefix")
            country_code = result.get("country_code")
            country_name = result.get("country_name")
            location = result.get("location")
            carrier = result.get("carrier")
            line_type = result.get("line_type")
            return [number, local_format, international_format, country_prefix, country_code, country_name, location, carrier, line_type]

        else:
            return ["", "", "", "", "", "", "", "", ""]

    except Exception as e:
        print("Error", e, "num:-", num)
    
    return ["", "", "", "", "", "", "", "", ""]

def call_func(all_nums):
    global res_all_vals
    all_vals = []
    for num in all_nums:
        res = extract_num_details(num)
        all_vals.append([num] + res)
    res_all_vals+=all_vals

if __name__ == "__main__":
    # all_val = []
    # input_list = []
    # with open('get_numverified.csv', mode ='r')as file:
    #     csvFile = csv.reader(file)
    #     i = 0
    #     for lines in csvFile:
    #         num = "".join(lines[0].split())
    #         res = extract_num_details(num)
    #         all_val.append([num] + res)

    all_val = []
    input_list = []
    with open('get_numverified.csv', mode ='r')as file:
        csvFile = csv.reader(file)
        i = 0
        temp_list = []
        for lines in csvFile:
            num = "".join(lines[0].split())
            i+=1
            temp_list.append(num)
            if i == 5000:
                i = 0
                input_list.append(temp_list)
                temp_list = []
    
    if temp_list:
        input_list.append(temp_list)
    

    all_threads = []
    for lst in input_list:
        thread = threading.Thread(target= call_func, args= (lst,))
        thread.start()
        all_threads.append(thread)

    for thread in all_threads:
        thread.join()
        
           
    fields  = ["Input Number", "Number", "Local Format", "International Format", "Country Prefix", "Country Code", "Country Name", "Location", "Carrier", "Line Type"]
    filename = "numbers_done.csv"
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow(fields)
        csvwriter.writerows(res_all_vals)