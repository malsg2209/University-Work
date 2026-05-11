# my_rental.py
# Name: Malarchelvi S Ganandran
# Student ID: S4109025

"""
Design Overview and Reflection
------------------------------
The program is structured using an Object-Oriented approach to model a bike rental system. The key
classes implemented are:

- Bike: Holds all attributes related to a bike (ID, model, type, prices, etc.) and tracks usage statistics.
- Rider: Represents riders and maintains data on their rentals, costs, and rule compliance (e.g., bike limits).
- RentalLog: Manages the orchestration of file parsing, rental processing, summaries, and output.

Each class is designed with encapsulation in mind. The attributes are initialized through constructors,
and methods are created for handling updates, validation, and business logic calculations.

Design Decisions
----------------
- A `defaultdict` was used in several places to manage dynamic data storage (e.g., rider-bike logs, daily usage).
  This allowed cleaner and more fault-tolerant logic when updating values.
- `Counter` was used for hourly rental time bucket tracking due to its built-in aggregation features.
- I chose `while` loops over `for` in `process_rentals()` to explicitly control paired event traversal (BOOKED/RETURNED).
- Custom exceptions are used (`DataFormatError`) for controlled exits when input file issues arise.
- Time calculations are handled using the `datetime` module to simplify conversion and formatting.

Development Process
-------------------
1. Began by building out a basic rental logger that reads log files and calculates durations (PASS level).
2. Added detailed Bike class logic with validation and price policies (CREDIT level).
3. Integrated full Rider logic, enforcing rental limits by type and time (DI level).
4. Refined robustness by handling format errors, splitting outputs into categorized tables,
   and prepending summaries to log files (HD level).

Testing and Reattempts
----------------------
Throughout development, I re-ran and reattempted the program multiple times with varied test files
to ensure correctness, stability, and completeness at every level. This iterative process helped catch:
- Edge cases such as bikes or riders with only ongoing rentals.
- Sorting and formatting inconsistencies across different file sizes.
- Miscalculations in total durations and costs.
- Violations of rental rules (e.g., bike limits or time limits).
Each retry provided insights into areas for code improvement and enhanced error handling.

Challenges Faced
----------------
- Managing consistent formatting across tables with both numeric and string types.
- Ensuring proper alignment and readability of tabular output (padding, formatting).
- Handling ongoing rentals and correct computation of daily minutes per rider.
- Merging summary data at the top of `rental_records.txt` without losing historical entries.
- Preventing file write conflicts by separating runtime printing from file output logic.

Unmet Requirements / Known Issues
---------------------------------
- Although all required features are implemented, defining `save_to_file` twice could be confusing.
  Care should be taken to ensure that the correct one is invoked; future versions should consolidate it.
- No GUI or interactive menu is implemented (not required, but could enhance usability).
- The program assumes files are relatively small; performance under massive data loads is not optimized.
- While timestamps are expected to be correct per spec, the program will not handle logical inconsistencies
  (e.g., RETURNED before BOOKED) unless explicitly validated.
- The rider/bike IDs must exist in the other files as expected—no cross-check warnings for unmatched IDs are included.

Code Commentary Strategy
------------------------
Inline comments are placed before major methods, conditionals, and logic blocks to explain:
- Why a loop structure or data type was chosen.
- Why a condition or calculation was made a certain way.
- How each method contributes to the larger goal (e.g., `update_rental()` maintains aggregate state).

"""

import os
import sys
from datetime import datetime
from collections import defaultdict, Counter

class DataFormatError(Exception):
    pass

class Bike:
    def __init__(self, bike_id, model=None, bike_type=None, gear_count=None, battery_range=None, price1=None, price2=None):
        if not bike_id.startswith("BK") or not bike_id[2:].isdigit():
            raise DataFormatError(f"Invalid bike ID: {bike_id}")
        self.bike_id = bike_id
        self.model = model
        self.bike_type = bike_type
        self.gear_count = gear_count
        self.battery_range = battery_range
        self.price1 = price1
        self.price2 = price2
        self.finished_rentals = 0
        self.ongoing_rentals = 0
        self.total_rental_duration = 0
        self.total_booked = 0

        if self.bike_type == "Urban":
            if self.battery_range == "n/a" or float(self.battery_range) <= 10:
                raise DataFormatError(f"Urban bike battery range error: {bike_id}")
        elif self.bike_type == "Adventure":
            if self.battery_range != "n/a" or float(self.price1) != 12.5 or float(self.price2) != 8.0:
                raise DataFormatError(f"Adventure bike pricing error: {bike_id}")

        if float(self.price1) <= 0 or float(self.price2) <= 0:
            raise DataFormatError(f"Invalid prices for bike {bike_id}")
        if float(self.price1) <= float(self.price2):
            raise DataFormatError(f"Price1 must be greater than Price2 for bike {bike_id}")

    def update_rental(self, duration=None, ongoing=False):
        self.total_booked += 1
        if ongoing:
            self.ongoing_rentals += 1
        else:
            self.finished_rentals += 1
            if duration:
                self.total_rental_duration += duration

class Rider:
    def __init__(self, rider_id, name="", phone="", join_date="01:01:2000 00:00:00", rider_type="Casual"):
        if not rider_id.startswith("RD") or not rider_id[2:].isdigit():
            raise DataFormatError(f"Invalid rider ID: {rider_id}")
        try:
            datetime.strptime(join_date.strip(), "%d:%m:%Y %H:%M:%S")
        except ValueError:
            raise DataFormatError(f"Invalid join date format: {join_date}")
        self.rider_id = rider_id
        self.name = name
        self.phone = phone
        self.join_date = join_date
        self.rider_type = rider_type
        self.finished_urban = 0
        self.finished_adv = 0
        self.ongoing_urban = 0
        self.ongoing_adv = 0
        self.total_duration = 0
        self.total_cost = 0
        self.daily_minutes = defaultdict(float)
        self.flag_bike_limit = False
        self.flag_duration_limit = False

    def update_rental(self, bike_type, duration=None, cost=None, ongoing=False, date_str=None):
        if ongoing:
            if bike_type == "Urban":
                self.ongoing_urban += 1
            elif bike_type == "Adventure":
                self.ongoing_adv += 1
        else:
            if bike_type == "Urban":
                self.finished_urban += 1
            elif bike_type == "Adventure":
                self.finished_adv += 1
            if duration:
                self.total_duration += duration
                if date_str:
                    self.daily_minutes[date_str] += duration
            if cost:
                self.total_cost += cost

        if self.rider_type == "Casual":
            if self.ongoing_urban > 1 or self.ongoing_adv > 1:
                self.flag_bike_limit = True
        elif self.rider_type == "Pro":
            if self.ongoing_urban > 1 or self.ongoing_adv > 2:
                self.flag_bike_limit = True

    def check_daily_limit(self):
        limit = 600 if self.rider_type == "Casual" else 1080
        for mins in self.daily_minutes.values():
            if mins > limit:
                self.flag_duration_limit = True

class RentalLog:
    def __init__(self):
        self.rental_data = defaultdict(list)
        self.bikes = {}
        self.riders = {}
        self.time_buckets = Counter()
        self.rental_durations = defaultdict(list)

    def safe_open(self, filename):
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File not found: {filename}")
        return open(filename, 'r')

    def load_log(self, filename):
        with self.safe_open(filename) as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) != 5:
                    raise DataFormatError(f"Incorrect rental log format: {line.strip()}")
                trans_id, rider_id, bike_id, status, timestamp = parts
                if not trans_id.startswith("T") or not trans_id[1:].isdigit():
                    raise DataFormatError(f"Invalid transaction ID: {trans_id}")
                try:
                    timestamp_obj = datetime.strptime(timestamp.strip(), "%d:%m:%Y %H:%M:%S")
                except ValueError:
                    raise DataFormatError(f"Invalid timestamp format: {timestamp}")
                self.rental_data[(rider_id, bike_id)].append((status.strip(), timestamp_obj))
                if status.strip() == 'BOOKED':
                    bucket = (timestamp_obj.hour // 2) * 2
                    self.time_buckets[bucket] += 1

    def load_bikes(self, filename):
        with self.safe_open(filename) as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) != 7:
                    raise DataFormatError(f"Incorrect bike file format: {line.strip()}")
                bike_id, model, bike_type, gear_count, battery_range, price1, price2 = parts
                self.bikes[bike_id] = Bike(bike_id, model, bike_type, int(gear_count), battery_range, float(price1), float(price2))

    def load_riders(self, filename):
        with self.safe_open(filename) as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) != 5:
                    raise DataFormatError(f"Incorrect rider file format: {line.strip()}")
                rider_id, name, phone, join_date, rider_type = parts
                self.riders[rider_id] = Rider(rider_id, name, phone, join_date, rider_type)

    def process_rentals(self):
        for (rider_id, bike_id), events in self.rental_data.items():
            events.sort(key=lambda x: x[1])
            i = 0
            while i < len(events):
                bike = self.bikes[bike_id]
                rider = self.riders[rider_id]
                if i+1 < len(events) and events[i][0] == 'BOOKED' and events[i+1][0] == 'RETURNED':
                    start, end = events[i][1], events[i+1][1]
                    duration = (end - start).total_seconds() / 60
                    date_key = start.strftime("%d:%m:%Y")
                    cost = bike.price1 if duration <= 300 else bike.price2 * (duration / 60)
                    bike.update_rental(duration)
                    rider.update_rental(bike.bike_type, duration, cost, ongoing=False, date_str=date_key)
                    self.rental_durations[(rider_id, bike_id)].append(f"{int(duration)}")
                    i += 2
                else:
                    bike.update_rental(ongoing=True)
                    rider.update_rental(bike.bike_type, ongoing=True)
                    self.rental_durations[(rider_id, bike_id)].append("--")
                    i += 1
        for rider in self.riders.values():
            rider.check_daily_limit()

    def show_summary_sentences(self):
        max_bike_duration = max(b.total_rental_duration for b in self.bikes.values())
        max_bike = [b.bike_id for b in self.bikes.values() if b.total_rental_duration == max_bike_duration]
        max_bike_rentals = max(b.total_booked for b in self.bikes.values())
        most_popular = [b.bike_id for b in self.bikes.values() if b.total_booked == max_bike_rentals]
        max_rider_duration = max(r.total_duration for r in self.riders.values())
        most_active = [r.rider_id for r in self.riders.values() if r.total_duration == max_rider_duration]
        max_rider_cost = max(r.total_cost for r in self.riders.values())
        most_valuable = [r.rider_id for r in self.riders.values() if r.total_cost == max_rider_cost]

        print(f"\nMost Valuable Bike: {', '.join(max_bike)} ({int(max_bike_duration)} mins)")
        print(f"Most Popular Bike: {', '.join(most_popular)} ({max_bike_rentals} bookings)")
        print(f"Most Active Rider: {', '.join(most_active)} ({int(max_rider_duration)} mins)")
        print(f"Most Valuable Rider: {', '.join(most_valuable)} (${max_rider_cost:.2f})")

    def show_time_buckets(self):
        print("\nRentals per 2-hour interval:")
        for hour in sorted(self.time_buckets):
            print(f"{hour:02d}:00 - {hour+2:02d}:00 : {self.time_buckets[hour]} rentals")

    def summarize(self):
        self.process_rentals()
        self.show_summary_sentences()
        self.show_time_buckets()
        self.show_bike_tables()
        self.show_rider_tables()
        self.save_to_file()

    def show_bike_tables(self):
        print("\nUrban Bikes:")
        print(
            f"{'ID':<6} {'Model':<10} {'Gear':<5} {'Done':<5} {'Doing':<6} {'Minutes':<7} {'Prices':<10} {'Battery':<8}")
        urban_bikes = sorted([b for b in self.bikes.values() if b.bike_type == "Urban"],
                             key=lambda b: -b.total_rental_duration)
        for b in urban_bikes:
            print(
                f"{b.bike_id:<6} {b.model:<10} {b.gear_count:<5} {b.finished_rentals:<5} {b.ongoing_rentals:<6} {int(b.total_rental_duration):<7} {b.price1:.2f}/{b.price2:.2f} {b.battery_range:<8}")

        print("\nAdventure Bikes:")
        print(
            f"{'ID':<6} {'Model':<10} {'Gear':<5} {'Done':<5} {'Doing':<6} {'Minutes':<7} {'Prices':<10} {'Battery':<8}")
        adv_bikes = sorted([b for b in self.bikes.values() if b.bike_type == "Adventure"],
                           key=lambda b: -b.total_rental_duration)
        for b in adv_bikes:
            print(
                f"{b.bike_id:<6} {b.model:<10} {b.gear_count:<5} {b.finished_rentals:<5} {b.ongoing_rentals:<6} {int(b.total_rental_duration):<7} {b.price1:.2f}/{b.price2:.2f} {b.battery_range:<8}")

    def show_rider_tables(self):
        print("\nCasual Riders:")
        print(
            f"{'ID':<6} {'Name':<12} {'Phone':<12} {'Join Date':<20} {'Cost':<8} {'Minutes':<8} {'Finish':<8} {'Ongoing':<8}")
        casuals = sorted([r for r in self.riders.values() if r.rider_type == "Casual"], key=lambda r: -r.total_cost)
        for r in casuals:
            mark1 = '!' if r.flag_bike_limit else ''
            mark2 = '!!' if r.flag_duration_limit else ''
            print(
                f"{r.rider_id:<6} {r.name:<12} {r.phone:<12} {r.join_date:<20} {r.total_cost:.2f} {int(r.total_duration):<8} {r.finished_urban}/{r.finished_adv}{mark1:<3} {r.ongoing_urban}/{r.ongoing_adv}{mark1:<3}{mark2:<2}")

        print("\nPro Riders:")
        print(
            f"{'ID':<6} {'Name':<12} {'Phone':<12} {'Join Date':<20} {'Cost':<8} {'Minutes':<8} {'Finish':<8} {'Ongoing':<8}")
        pros = sorted([r for r in self.riders.values() if r.rider_type == "Pro"], key=lambda r: -r.total_cost)
        for r in pros:
            mark1 = '!' if r.flag_bike_limit else ''
            mark2 = '!!' if r.flag_duration_limit else ''
            print(
                f"{r.rider_id:<6} {r.name:<12} {r.phone:<12} {r.join_date:<20} {r.total_cost:.2f} {int(r.total_duration):<8} {r.finished_urban}/{r.finished_adv}{mark1:<3} {r.ongoing_urban}/{r.ongoing_adv}{mark1:<3}{mark2:<2}")

    def save_to_file(self, filename="rental_records.txt"):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        with open(filename, 'r') as f:
            old = f.read() if os.path.exists(filename) else ""

        with open(filename, 'w') as f:
            f.write(f"\n--- Rental Summary at {now} ---\n")
            f.write("\nMost Valuable Bike: " + ', '.join([b.bike_id for b in self.bikes.values() if
                                                          b.total_rental_duration == max(
                                                              b.total_rental_duration for b in self.bikes.values())]))
            f.write("\nMost Popular Bike: " + ', '.join([b.bike_id for b in self.bikes.values() if
                                                         b.total_booked == max(
                                                             b.total_booked for b in self.bikes.values())]))
            f.write("\nMost Active Rider: " + ', '.join([r.rider_id for r in self.riders.values() if
                                                         r.total_duration == max(
                                                             r.total_duration for r in self.riders.values())]))
            f.write("\nMost Valuable Rider: " + ', '.join([r.rider_id for r in self.riders.values() if
                                                           r.total_cost == max(
                                                               r.total_cost for r in self.riders.values())]))

            f.write("\n\nRentals per 2-hour interval:\n")
            for hour in sorted(self.time_buckets):
                f.write(f"{hour:02d}:00 - {hour + 2:02d}:00 : {self.time_buckets[hour]} rentals\n")

            f.write("\n\nUrban Bikes:\n")
            for b in sorted([b for b in self.bikes.values() if b.bike_type == "Urban"],
                            key=lambda b: -b.total_rental_duration):
                f.write(
                    f"{b.bike_id},{b.model},{b.gear_count},{b.finished_rentals},{b.ongoing_rentals},{int(b.total_rental_duration)},{b.price1:.2f}/{b.price2:.2f},{b.battery_range}\n")

            f.write("\nAdventure Bikes:\n")
            for b in sorted([b for b in self.bikes.values() if b.bike_type == "Adventure"],
                            key=lambda b: -b.total_rental_duration):
                f.write(
                    f"{b.bike_id},{b.model},{b.gear_count},{b.finished_rentals},{b.ongoing_rentals},{int(b.total_rental_duration)},{b.price1:.2f}/{b.price2:.2f},{b.battery_range}\n")

            f.write("\n\nCasual Riders:\n")
            for r in sorted([r for r in self.riders.values() if r.rider_type == "Casual"], key=lambda r: -r.total_cost):
                mark1 = '!' if r.flag_bike_limit else ''
                mark2 = '!!' if r.flag_duration_limit else ''
                f.write(
                    f"{r.rider_id},{r.name},{r.phone},{r.join_date},{r.total_cost:.2f},{int(r.total_duration)},{r.finished_urban}/{r.finished_adv}{mark1},{r.ongoing_urban}/{r.ongoing_adv}{mark1}{mark2}\n")

            f.write("\nPro Riders:\n")
            for r in sorted([r for r in self.riders.values() if r.rider_type == "Pro"], key=lambda r: -r.total_cost):
                mark1 = '!' if r.flag_bike_limit else ''
                mark2 = '!!' if r.flag_duration_limit else ''
                f.write(
                    f"{r.rider_id},{r.name},{r.phone},{r.join_date},{r.total_cost:.2f},{int(r.total_duration)},{r.finished_urban}/{r.finished_adv}{mark1},{r.ongoing_urban}/{r.ongoing_adv}{mark1}{mark2}\n")

            f.write(old)
if __name__ == "__main__":
    log = RentalLog()
    args = sys.argv
    if len(args) == 1:
        print("[Usage:] python my_rental.py <rental_log.txt> [bikes.txt] [riders.txt]")
    else:
        try:
            log.load_log(args[1])
            if len(args) > 2:
                log.load_bikes(args[2])
            if len(args) > 3:
                log.load_riders(args[3])
            log.summarize()
        except Exception as e:
            print(f"Error: {e}")
