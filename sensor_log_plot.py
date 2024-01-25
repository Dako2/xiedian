import matplotlib.pyplot as plt
import os

def parse_sensor_data(file_path):
    # List to store parsed data
    parsed_data = []

    # Open the file and read line by line
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip():  # Skip empty lines
                # Split the line into components
                parts = line.split(',')

                # Extract the timestamp and sensor type
                timestamp = parts[0].strip()
                sensor_type = parts[1].strip()

                # Extract sensor values
                values = [float(val) for val in parts[2:]]

                # Create a dictionary for this line
                sensor_data = {
                    'timestamp': timestamp,
                    'sensor_type': sensor_type,
                    'values': values
                }

                # Add the dictionary to the list
                parsed_data.append(sensor_data)

    return parsed_data

def calculate_mean(values):
    return sum(values) / len(values) if values else 0

def normalize_timestamps(timestamps):
    # Normalize timestamps to the first timestamp
    base_timestamp = timestamps[0]
    return [(t - base_timestamp) / 1000.0 for t in timestamps]  # Convert to seconds

def plot_sensor_data(parsed_data):
    # Dictionary to store data grouped by sensor type
    sensor_data = {}

    # Process each entry in the parsed data
    for entry in parsed_data:
        timestamp = int(entry['timestamp'])
        sensor_type = entry['sensor_type']
        mean_value = calculate_mean(entry['values'])

        # Add data to the dictionary
        if sensor_type not in sensor_data:
            sensor_data[sensor_type] = {'timestamps': [], 'means': []}
        sensor_data[sensor_type]['timestamps'].append(timestamp)
        sensor_data[sensor_type]['means'].append(mean_value)

    # Normalize timestamps and plot data for each sensor type
    for sensor_type, data in sensor_data.items():
        normalized_timestamps = normalize_timestamps(data['timestamps'])
        plt.plot(normalized_timestamps, data['means'], '.',label=sensor_type)

    plt.xlabel('Time Duration (seconds)')
    plt.ylabel('Mean Sensor Value')
    plt.title('Mean Sensor Value vs Time Duration')
    plt.legend()
    plt.show()

# File path
file_path = 'sensor_log.txt'

# Parse the data
parsed_data = parse_sensor_data(file_path)

# Print the parsed data
for item in parsed_data:
    print(item)


# Call the function with the parsed_data
plot_sensor_data(parsed_data)
