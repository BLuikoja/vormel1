def analyze_result(file_path):
    def format_time(seconds):
        minutes = int(seconds // 60)
        seconds = seconds % 60
        milliseconds = "{:.3f}".format(seconds % 1)
        return "{:02}:{:05.3f}".format(minutes, seconds + float(milliseconds))

    def sec2time(sec,
                 n_msec=3):  # https://stackoverflow.com/questions/775049/how-do-i-convert-seconds-to-hours-minutes-and-seconds
        if hasattr(sec, '__len__'):
            return [sec2time(s) for s in sec]
        m, s = divmod(sec, 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)
        if n_msec > 0:
            pattern = '%%02d:%%02d:%%0%d.%df' % (n_msec + 3, n_msec)
        else:
            pattern = r'%02d:%02d:%02d'
        if d == 0:
            return pattern % (h, m, s)
        return ('%d days, ' + pattern) % (d, h, m, s)

    def print_analysis(results, sector_bests, dream_lap, fastest_lap_racer, fastest_lap_time):
        print("Analysis:")
        for idx, result in enumerate(results):
            driver = result[0]
            lap_time = result[1]
            accidents = result[2]
            lap_time_formatted = format_time(lap_time)
            accidents_formatted = f"[{', '.join(str(accident) for accident in accidents)}]" if accidents else "[]"
            fastest_lap_indicator = ""
            if driver == fastest_lap_racer:
                fastest_lap_indicator = format_time(fastest_lap_time)
            time_difference = format_time(lap_time - results[0][1]) if idx > 0 else ""

            print(f"{driver:<10} {lap_time_formatted} {time_difference} {accidents_formatted} {fastest_lap_indicator}")

        # Sector bests
        print("\nSektorite parimad")
        for sector, (driver, time) in sector_bests.items():
            print(f"Sektor {sector} {driver:<10} {format_time(time)}")

        # Dream lap
        print(f"\nUnelmate ring {format_time(dream_lap)}")

    def is_fastest_lap(driver_name, results):
        fastest_lap = min(results, key=lambda x: x[1])[1]
        fastest_lap_drivers = [driver for driver, lap_time, _ in results if lap_time == fastest_lap]
        if driver_name == results[0][0] and driver_name in fastest_lap_drivers:
            return sec2time(fastest_lap)
        return ""

    # Read and process the Result.txt file
    results = []
    sector_times = {1: [], 2: [], 3: []}  # Store sector times for each driver
    dream_lap = 0
    fastest_lap_racer = ""
    fastest_lap_time = float('inf')  # Set initial fastest lap time to infinity

    with open(file_path, "r") as file:
        lines = file.readlines()

    # Process each line in the file
    for line in lines[1:]:
        data = line.strip().split(";")
        lap_number = int(data[0])
        driver = data[1]
        lap_time = float(data[2])
        sector1_time = float(data[3])
        sector2_time = float(data[4])
        sector3_time = float(data[5])
        accidents = []
        if data[6].lower() == "true":
            accidents.append(lap_number)
        if not results or driver != results[-1][0]:
            results.append([driver, lap_time, accidents])
        else:
            results[-1][1] += lap_time
            results[-1][2].extend(accidents)

        # Update sector bests
        if not sector_times[1] or sector1_time < sector_times[1][1]:
            sector_times[1] = (driver, sector1_time)
        if not sector_times[2] or sector2_time < sector_times[2][1]:
            sector_times[2] = (driver, sector2_time)
        if not sector_times[3] or sector3_time < sector_times[3][1]:
            sector_times[3] = (driver, sector3_time)

        # Update dream lap time
        if lap_time > dream_lap:
            dream_lap = lap_time

        # Update fastest lap time and racer
        if lap_time < fastest_lap_time:
            fastest_lap_time = lap_time
            fastest_lap_racer = driver

    # Sort the results by lap time
    results = sorted(results, key=lambda x: x[1])

    # Print the analysis
    print_analysis(results, sector_times, dream_lap, fastest_lap_racer, fastest_lap_time)

# Usage example
analyze_result("Result.txt")
