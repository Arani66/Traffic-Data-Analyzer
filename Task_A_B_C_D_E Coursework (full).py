import csv 
import os
import datetime
from collections import Counter
import tkinter as tk

# Task A: Input Validation
def validate_date_input_prompt(input_prompt, min_value, max_value, range_msg):
    while True:
        try:
            value = int(input(input_prompt))
            if min_value <= value <= max_value:
                return value
            else:
                print(range_msg)
        except ValueError:
            print("Integer required")

def leap_check(year):
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        return True

def validate_date_input(): 
    current_year = datetime.datetime.now().year
    
    while True:
        day = validate_date_input_prompt("Please enter the day of the survey in the format dd : ", 1, 31,
                                         "Out of range - values must be in the range 1 and 31.")                            
        month = validate_date_input_prompt("Please enter the month of the survey in the format MM : ", 1, 12,
                                           "Out of range - values must be in the range 1 to 12.")
        
        if month in [4, 6, 9, 11] and day == 31:
            print("This month cannot have 31 days. Please try again")
            return validate_date_input()
            
        if month == 2 and day > 29:
            print("February cannot have more than 29 days. Please try again")    
            return validate_date_input()
            
        year = validate_date_input_prompt(f"Please enter the year of the survey in the format YYYY : ", 2000, current_year,
                                          f"Out of range - values must range from 2000 to {current_year}.")
        
        if month == 2:
            if leap_check(year):
                pass
            elif day > 28:
                print(f"February in the year {year} is not a leap year so it only has 28 days. Please try again")
                return validate_date_input()
                
        global input_date 
        input_date = f"{day} / {month:02d} / {year}"  
        print(f"Your input date is {input_date}")
    
        return day, month, year    

def validate_continue_input():
    while True: 
        choice = input("Do you want to enter another data set? (Y/N): ").strip().upper()
        if choice == "Y":
            return True
        elif choice == "N":
            print("Exiting code")
            return False
        else: 
            print("Invalid input. Enter Y for yes or N for no.")
    
# Task B: Processed Outcomes
def process_csv_data(file_path):
    if not os.path.exists(file_path):
        print("CSV data cannot be processed because the matching CSV file was not found.")
        return None

    total_vehicles = 0
    total_trucks = 0
    total_electric_vehicles = 0
    total_2wheeled_vehicles = 0
    total_busses_leave_Elm_north = 0
    total_vehicles_not_turn = 0
    total_vehicles_over_speed = 0
    total_vehicles_Elm = 0
    total_vehicles_Hanley = 0
    total_scooters_Elm = 0
    vehicles_Hanley_peak_hour = 0

    with open(file_path, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        content = list(reader)
        global file_name
        total_vehicles = len(content) 

        for row in content:
            if row["VehicleType"].strip().lower() == "truck":
                total_trucks += 1
            if row["elctricHybrid"].upper() == "TRUE":
                total_electric_vehicles += 1
            if row["VehicleType"].strip().lower() in ["bicycle", "motorcycle", "scooter"]: 
                total_2wheeled_vehicles += 1
            if row["JunctionName"] == "Elm Avenue/Rabbit Road" and row["travel_Direction_out"] == "N" and row["VehicleType"] == "Buss":
                total_busses_leave_Elm_north += 1
            if row["travel_Direction_in"] == row["travel_Direction_out"]:
                total_vehicles_not_turn += 1
            if float(row["VehicleSpeed"]) > float(row["JunctionSpeedLimit"]):  
                total_vehicles_over_speed += 1
            if row["JunctionName"] == "Elm Avenue/Rabbit Road":
                total_vehicles_Elm += 1
            if row["JunctionName"] == "Hanley Highway/Westway":
                total_vehicles_Hanley += 1
            if row["VehicleType"] == "Scooter" and row["JunctionName"] == "Elm Avenue/Rabbit Road":
                total_scooters_Elm += 1

        total_trucks_percentage = f"{int(round((total_trucks / total_vehicles) * 100, 0))} %" if total_vehicles else "0 %"
        total_bicycles_time = [row["timeOfDay"] for row in content if row["VehicleType"] == "Bicycle"]
        bike_hours = Counter(time.split(":")[0] for time in total_bicycles_time)
        avg_bikes_per_hour = round(len(total_bicycles_time) / len(bike_hours)) if bike_hours else 0

        scooters_Elm_percentage = f"{int((total_scooters_Elm / total_vehicles_Elm) * 100)} %" if total_vehicles_Elm else "0 %"

        total_vehicles_Hanley_time = [row["timeOfDay"] for row in content if row["JunctionName"] == "Hanley Highway/Westway"]
        vehicles_Hanley_hours = Counter(time.split(":")[0] for time in total_vehicles_Hanley_time)
        vehicles_Hanley_peak_hour = max(vehicles_Hanley_hours.values(), default=0)
        
        peak_traffic_Hanley_time = [hour for hour, count in vehicles_Hanley_hours.items() if count == vehicles_Hanley_peak_hour]
        total_rain_hours = len(set([row["timeOfDay"] for row in content if row["Weather_Conditions"] in ["Heavy Rain", "Light Rain"]]))

        outcomes = (f""" 
        *************************** Data file selected is {file_name}
        *************************** The total number of vehicles recorded for this date is {total_vehicles}
        The total number of trucks recorded for this date is {total_trucks}
        The total number of electric vehicles for this date is {total_electric_vehicles}
        The total number of two-wheeled vehicles for this date is {total_2wheeled_vehicles}
        The total number of Busses leaving Elm Avenue/Rabbit Road heading North is {total_busses_leave_Elm_north}
        The total number of Vehicles through both junctions not turning left or right is {total_vehicles_not_turn}
        The percentage of total vehicles recorded that are trucks for this date is {total_trucks_percentage}
        The average number of Bikes per hour for this date is {avg_bikes_per_hour}
        The total number of Vehicles recorded as over the speed limit for this date is {total_vehicles_over_speed}
        The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {total_vehicles_Elm}
        The total number of vehicles recorded through Hanley Highway/Westway junction is {total_vehicles_Hanley}
        {scooters_Elm_percentage} of vehicles recorded through Elm Avenue/Rabbit Road are scooters
        The number of vehicles recorded in the peak hour on Hanley Highway/Westway is {vehicles_Hanley_peak_hour}
        The time/s of peak traffic hour/s on Hanley Highway/Westway were recorded between {peak_traffic_Hanley_time[0]}:00 and {int(peak_traffic_Hanley_time[0])+1}:00
        The total number of hours of rain for this date is {total_rain_hours}
        """)
        return outcomes

def display_outcomes(outcomes):           
    print(outcomes)

# Task C: Save Results to Text File
def save_results_to_file(outcomes, file_name="results.txt"):
    with open(file_name, "a") as file:
        file.write(outcomes + "\n")

# Task D: Histogram Display
class HistogramApp:
    def __init__(self, traffic_data, input_date):
        self.traffic_data = traffic_data  
        self.date = input_date 
        self.root = tk.Tk() 
        self.canvas = None 

    def setup_window(self):
        self.root.title("Traffic Data Histogram")
        self.root.geometry("1300x700")
        self.canvas = tk.Canvas(self.root, width=1300, height=700, bg="white")
        self.canvas.pack()

    def draw_histogram(self):
        side_margin = 50
        top_margin = 140
        bottom_margin = 100
        canvas_width = 1300  
        canvas_height = 700
        bar_width = 20
        bar_spacing = 0 
        hour_spacing = (canvas_width - 2 * side_margin) / len(self.traffic_data)

        max_bar_height = canvas_height - (top_margin + bottom_margin)
        max_vehi_count = max(max(vehi_counts) for vehi_counts in self.traffic_data.values())

        for i, (hour, vehi_counts) in enumerate(self.traffic_data.items()):
            bar_start = side_margin + i * hour_spacing
            bar1_L = bar_start
            bar1_R = bar1_L + bar_width
            bar2_L = bar1_R + bar_spacing
            bar2_R = bar2_L + bar_width

            bar1_height = (vehi_counts[0] / max_vehi_count) * max_bar_height
            bar2_height = (vehi_counts[1] / max_vehi_count) * max_bar_height
            verti_base = canvas_height - bottom_margin

            # Elm Avenue/Rabbit Road Junction
            self.canvas.create_rectangle(bar1_L, (verti_base - bar1_height), bar1_R, verti_base, fill="blue")
            self.canvas.create_text(bar1_L + bar_width / 2, verti_base - bar1_height - 10, text=str(vehi_counts[0]), fill="blue")

            # Hanley Highway/Westway Junction
            self.canvas.create_rectangle(bar2_L, (verti_base - bar2_height), bar2_R, verti_base, fill="red")
            self.canvas.create_text(bar2_L + bar_width / 2, verti_base - bar2_height - 10, text=str(vehi_counts[1]), fill="red") 

            # X-axis labels
            self.canvas.create_text((bar1_L + bar2_R) / 2, verti_base + 15, text=hour, fill="black")

        self.canvas.create_text(50, 30, text=f"Histogram of Vehicle Frequency per Hour ({self.date})", 
                                font=("Helvetica", 18, "bold"), fill="black", anchor="w") 
        self.canvas.create_text(650, 650, text="Hours 00:00 to 24:00", font=("Helvetica", 12))

    def add_legend(self):
        self.canvas.create_rectangle(50, 50, 66, 66, fill="blue")
        self.canvas.create_text(71, 60, text="Elm Avenue/Rabbit Road", font=("Helvetica", 12), fill="black", anchor="w")

        self.canvas.create_rectangle(50, 80, 66, 96, fill="red")
        self.canvas.create_text(71, 90, text="Hanley Highway/Westway", font=("Helvetica", 12), fill="black", anchor="w")

    def run(self):
        self.setup_window()
        self.draw_histogram()
        self.add_legend()
        self.root.mainloop()

# Task E: Code Loops to Handle Multiple CSV Files
class MultiCSVProcessor:
    def __init__(self):
        self.current_data = None

    def load_csv_file(self, file_path):
        if not os.path.exists(file_path):
            print("Histogram cannot be drawn because the matching CSV file was not found.")
            return None

        junctions = []
        data = {str(i).zfill(2): [] for i in range(24)}

        with open(file_path, "r") as csvfile:
            content = csv.DictReader(csvfile)
            
            for row in content:
                junction_name = row["JunctionName"]
                time_of_day = row["timeOfDay"]
                hour = time_of_day.split(":")[0]

                if junction_name not in junctions:
                    junctions.append(junction_name)

                if len(data[hour]) < len(junctions):
                    data[hour].append(0)

                junction_index = junctions.index(junction_name)
                data[hour][junction_index] += 1

        self.current_data = data
        traffic_data = {hour: tuple(counts) for hour, counts in data.items()}
        return traffic_data
     
    def clear_previous_data(self):
        self.current_data = {}
        print("Your data has been cleared! Current data is", self.current_data)

def main():
    traffic_data = None
    while True:
        day, month, year = validate_date_input()
        global file_name
        file_name = f"traffic_data{day:02d}{month:02d}{year:04d}.csv"
        file_path = os.path.join(os.getcwd(), file_name)
        outcomes = process_csv_data(file_path)

        if outcomes is not None:
            display_outcomes(outcomes)
            save_results_to_file(outcomes)  
            
        processor = MultiCSVProcessor() 
        traffic_data = processor.load_csv_file(file_path)
        
        if traffic_data:
            app = HistogramApp(traffic_data, input_date)
            app.run()
            
        processor.clear_previous_data()
        
        if not validate_continue_input():
            break

if __name__ == "__main__":
    main()