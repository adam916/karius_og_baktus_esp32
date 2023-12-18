import time

def time_stamp(): 
    # Get the current time in seconds since the epoch (Unix timestamp)
    timestamp = time.time()
    # Convert the timestamp to a time tuple
    time_tuple = time.localtime(timestamp)
    
    formatted_time = "{:02}:{:02} {:02}-{:02}-{:04}".format(
        time_tuple[3], # hours
        time_tuple[4], # minutes
        time_tuple[2], 
        time_tuple[1],
        time_tuple[0]    
    )
    
    return formatted_time   
    

#print("Formatted time:", time_stamp())

#print(time.localtime())