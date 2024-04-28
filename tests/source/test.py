import sys

import json

data=json.load(open(sys.argv[1]))

def most(array, apk):
    selected_date = array[1].split(":")[1]
    city_temperature_data = [(city, data[city][selected_date]["temp"]) for city in data.keys()]
    warmest_city = max(city_temperature_data, key=lambda x: x[1])
    coldest_city = min(city_temperature_data, key=lambda x: x[1])
    if apk == "warmestcity":
        print(f"city:{warmest_city[0]} {array[1]} temp:{warmest_city[1]}")
    else:
        print(f"city:{coldest_city[0]} {array[1]} temp:{coldest_city[1]}")


def value(value, apk):
    if apk == "relhum":
        return round(value * 100)
    else:
        return value
          
def high(array, apk):
    selected_city = array[1].split(":")[1]
    start_date = array[2].split(":")[1]
    end_date = array[3].split(":")[1]
    city_data = data[selected_city]
    filtered_dict = {key: val for key, val in city_data.items() if start_date <= key <= end_date}
    max_entry = max(filtered_dict.items(), key=lambda x: value(x[1][apk], apk))
    date_of_max, max_value = max_entry[0], value(max_entry[1][apk], apk)
    label = {"relhum": "humidity", "temp": "temp", "ap": "pressure"}[apk]
    print(f"city:{selected_city} date:{date_of_max} {label}:{max_value}")

def status(array, apk):
    city2 = array[1].split(":")[1]
    date2 = array[2].split(":")[1]
    value = data[city2][date2][apk]
    if apk == "relhum":
        value = round(value * 100)
        label = "humidity"
    elif apk == "ap":
        label = "pressure"
    else:
        label = "temp"
    print(f"{array[1]} {array[2]} {label}:{value}")

def aggregate_values(values, target_length):
    aggregated_values = []
    total_values = len(values)
    cur_idx = 0
    for i in range(total_values % target_length):
        avg = sum(values[cur_idx:cur_idx + (total_values // target_length) + 1]) / ((total_values // target_length) + 1)
        aggregated_values.append(avg)
        cur_idx += (total_values // target_length) + 1
    while len(aggregated_values) != target_length:
        avg = sum(values[cur_idx:cur_idx + (total_values // target_length)]) / (total_values // target_length)
        aggregated_values.append(avg)
        cur_idx += total_values // target_length
    return aggregated_values

def graph(city, startdate, enddate, what):
    desired_city = data[city]
    filtered_data = {key: val for key, val in desired_city.items() if startdate <= key <= enddate}
    values = [vals[what] for vals in filtered_data.values()]

    final_values = aggregate_values(values, 50) if len(values) > 50 else values

    step = (max(final_values) - min(final_values)) / 19
    min_temp = min(final_values)
    heights = [round((value - min_temp) / step) + 1 for value in final_values]

    for level in reversed(range(1, 21)):
        row = "".join("#" if height >= level else " " for height in heights)
        print(row)

function_map = {
    "temp": status,
    "humidity": status,
    "pressure": status,
    "maxtemp": high,
    "maxhumidity": high,
    "maxpressure": high,
    "warmestcity": most,
    "coldestcity": most,
    "graphtemp": graph,
    "graphpressure": graph
}

for line in sys.stdin:
    line = line.strip().split()
    if not line:
        continue
    d = line[0]
    try:
        if d in function_map:
            if d == "graphtemp" or d == "graphpressure":
                function_map[d](line[1].split(":")[1], line[2].split(":")[1], line[3].split(":")[1], "temp" if d == "graphtemp" else "ap")
            else:
                metric = "temp" if d.endswith("temp") else "relhum" if d.endswith("humidity") else "ap" if d.endswith("pressure") else d
                function_map[d](line, metric) 
        else:
            raise Exception
    except:
        print("Invalid input")