from machine import RTC
import time_stamp



# Function to write data to a text file with timestamp
def write_data_to_file(data):
    timestamp = time_stamp.time_stamp()
    filename = "log_of_data_not_sent.txt"

    with open(filename, 'a') as file:
        file.write(f"{timestamp}: {data}\n")
    
    print(f"Data written to {filename}")


'''
# Example usage
data_to_write = ['en','to','tre']
write_data_to_file(data_to_write)
'''
