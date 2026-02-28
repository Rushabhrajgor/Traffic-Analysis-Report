class TrafficAnalyzer:
    def __init__(self, filename):
        self.filename = filename
        self.records = []

        self.summary = {}
        self.hourly_traffic = {}

        # Flags for main report
        self.location_used = False
        self.hourly_used = False
        self.avg_used = False
        self.peak_used = False

        # Flags for risk report
        self.high_used = False
        self.low_used = False
        self.accident_used = False

    # File Handling
    def load_data(self):
        try:
            with open(self.filename, "r") as file:
                lines = file.readlines()

                for line in lines[1:]:
                    data = line.strip().split(",")

                    record = (
                        data[0].strip().title(),
                        data[1].strip(),
                        int(data[2]),
                        int(data[3])
                    )
                    self.records.append(record)

        except FileNotFoundError:
            print("File not found.")
        except ValueError:
            print("Invalid data format.")

    # Analysis
    def analyze_location(self):
        for location, time, vehicles, accidents in self.records:
            if location not in self.summary:
                self.summary[location] = [0, 0]
            self.summary[location][0] += vehicles
            self.summary[location][1] += accidents

    def analyze_hourly(self):
        for location, time, vehicles, accidents in self.records:
            hour = time.split(":")[0]
            if hour not in self.hourly_traffic:
                self.hourly_traffic[hour] = 0
            self.hourly_traffic[hour] += vehicles

    # Display
    def show_summary(self):
        self.location_used = True
        print("\nLocation-wise Summary")
        for loc, data in self.summary.items():
            print(f"{loc}: Vehicles={data[0]}, Accidents={data[1]}")

    def show_hourly_traffic(self):
        self.hourly_used = True
        print("\nHour-wise Traffic")
        for hour, vehicles in sorted(self.hourly_traffic.items()):
            print(f"{hour}:00 -> {vehicles} vehicles")

    def average_traffic_per_hour(self):
        self.avg_used = True
        total = sum(self.hourly_traffic.values())
        hours = len(self.hourly_traffic)
        if hours:
            print(f"\nAverage Traffic Per Hour: {total / hours:.2f}")

    def peak_hour(self):
        self.peak_used = True
        peak = max(self.hourly_traffic, key=self.hourly_traffic.get)
        print(f"\nPeak Hour: {peak}:00 -> {self.hourly_traffic[peak]} vehicles")

    # High / Low / Accident
    def high_traffic_locations(self, limit=300):
        self.high_used = True
        print("\nHigh Traffic Locations")
        for loc, data in self.summary.items():
            if data[0] > 300:
                print(f"{loc} -> {data[0]} vehicles")

    def low_traffic_locations(self, limit=100):
        self.low_used = True
        print("\nLow Traffic Locations")
        for loc, data in self.summary.items():
            if data[0] < 100:
                print(f"{loc} -> {data[0]} vehicles")

    def accident_prone_locations(self):
        self.accident_used = True
        print("\nAccident Prone Locations")
        for loc, data in self.summary.items():
            if data[1] > 0:
                print(f"{loc} -> {data[1]} accidents")

    # Write MAIN report
    def write_report(self):
        try:
            with open("traffic_analysis_report.txt", "a", encoding="utf-8") as file:
                file.write("\n\n Traffic Analysis Report \n")

                if self.location_used:
                    file.write("\nLocation-wise Summary:\n")
                    for loc, data in self.summary.items():
                        file.write(f"{loc}: {data[0]} vehicles, {data[1]} accidents\n")

                if self.hourly_used:
                    file.write("\nHour-wise Traffic:\n")
                    for hour, v in sorted(self.hourly_traffic.items()):
                        file.write(f"{hour}:00 -> {v} vehicles\n")

                if self.avg_used:
                    avg = sum(self.hourly_traffic.values()) / len(self.hourly_traffic)
                    file.write(f"\nAverage Traffic Per Hour: {avg:.2f}\n")

                if self.peak_used:
                    peak = max(self.hourly_traffic, key=self.hourly_traffic.get)
                    file.write(f"Peak Hour: {peak}:00 -> {self.hourly_traffic[peak]}\n")

            print("Main report appended")

        except Exception as e:
            print("Error:", e)

    # Write RISK report
    def write_risk_report(self):
        try:
            with open("traffic_risk_report.txt", "a", encoding="utf-8") as file:
                file.write("\n\n Traffic Risk Report \n")

                if self.high_used:
                    file.write("\nHigh Traffic Locations:\n")
                    for loc, data in self.summary.items():
                        if data[0] > 300:
                            file.write(f"{loc} -> {data[0]} vehicles\n")

                if self.low_used:
                    file.write("\nLow Traffic Locations:\n")
                    for loc, data in self.summary.items():
                        if data[0] < 100:
                            file.write(f"{loc} -> {data[0]} vehicles\n")

                if self.accident_used:
                    file.write("\nAccident Prone Locations:\n")
                    for loc, data in self.summary.items():
                        if data[1] > 0:
                            file.write(f"{loc} -> {data[1]} accidents\n")

            print("Risk report appended")

        except Exception as e:
            print("Error:", e)


# Menu
def main():
    analyzer = TrafficAnalyzer("traffic_data_mumbai_locations.csv")
    analyzer.load_data()
    analyzer.analyze_location()
    analyzer.analyze_hourly()

    while True:
        print("\n MENU")
        print("1. Show Location-wise Summary")
        print("2. Show Hour-wise Traffic Analysis")
        print("3. Show Average Traffic")
        print("4. Show Peak Hour")
        print("5. Show High Traffic Locations")
        print("6. Show Low Traffic Locations")
        print("7. Show Accident Prone Locations")
        print("8. Save Analysis Report")
        print("9. Save Risk Report")
        print("10. Exit")

        ch = input("Enter your choice (1-10): ")

        if ch == "1":
            analyzer.show_summary()
        elif ch == "2":
            analyzer.show_hourly_traffic()
        elif ch == "3":
            analyzer.average_traffic_per_hour()
        elif ch == "4":
            analyzer.peak_hour()
        elif ch == "5":
            analyzer.high_traffic_locations()
        elif ch == "6":
            analyzer.low_traffic_locations()
        elif ch == "7":
            analyzer.accident_prone_locations()
        elif ch == "8":
            analyzer.write_report()
        elif ch == "9":
            analyzer.write_risk_report()
        elif ch == "10":
            print("Exit")
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
