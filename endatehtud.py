import random

names = ['Luikoja', 'Lepasalu', 'Smurf', 'Toomla', 'Sipelgas']
laps = 10
filename = 'Result.txt'
file_header = 'Ring;Nimi;Aeg;Sektor1;Sektor2;Sektor3;Viga\n'
results = []
minimum = 23
maximum = 26
fastest_lap = ['Unknown', 999]
three_sectors = [['Unknown', 999], ['Unknown', 999], ['Unknown', 999]]
sectors_data = []

def random_sector_time(mini, maxi):
    return random.uniform(mini, maxi)

def one_lap_time(mini, maxi, driver_name):
    sectors_data.clear()
    lap_time = 0
    for _ in range(3):
        sector_time = random_sector_time(mini, maxi)
        sectors_data.append(sector_time)
        if sector_time < three_sectors[_][1]:
            three_sectors[_] = [driver_name, sector_time]
        lap_time += sector_time
    return lap_time

def format_time(sec):
    m, s = divmod(int(sec), 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

with open(filename, 'w', encoding='utf-8') as f:
    f.write(file_header)
    for name in names:
        lap_times = 0
        errors = []
        for lap in range(laps):
            if random.randint(0, 9) == 2:
                lap_time = one_lap_time(30, 90, 'Unknown')
                errors.append(lap + 1)
            else:
                lap_time = one_lap_time(minimum, maximum, name)
                if lap_time < fastest_lap[1]:
                    fastest_lap = [name, lap_time]
            lap_times += lap_time
            sectors_data_str = ';'.join(map(str, [lap + 1, name, lap_time] + sectors_data + [int(lap_time != 0)]))
            f.write(sectors_data_str + '\n')
        results.append([name, lap_times, errors])

results.sort(key=lambda x: x[1])

for idx, (name, lap_times, errors) in enumerate(results):
    difference = format_time(lap_times - results[0][1]) if idx > 0 else ""
    fastest_lap_str = format_time(fastest_lap[1]) if name == fastest_lap[0] else ""
    lap_times_str = format_time(lap_times)
    print(name.ljust(10), lap_times_str, difference, errors, fastest_lap_str)

print('\nSektorite parimad')
total_sector_time = sum(sector[1] for sector in three_sectors)
for idx, (driver, sector_time) in enumerate(three_sectors):
    print(f"Sektor {idx+1}", driver.ljust(10), format_time(sector_time))
print("Unelmate ring", format_time(total_sector_time))
