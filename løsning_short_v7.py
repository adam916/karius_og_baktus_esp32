import time
import ir_test_works
import network_test_1
#import buzzer
import _thread
import ldr_reading
import led_ring
import socket_buzz

# socket thread
_thread.start_new_thread(socket_buzz.init_socket, ())

# network thread
_thread.start_new_thread(network_test_1.net_work_test,())

# IR sensor
MLX90614_TOBJ1 = 0x07  # Object temperature address
MLX90614_TA = 0x06  # Ambient temperature address

# count
count=0

# taking a base light sample
base_light = ldr_reading.ldr_reading()
print(f'base light : {base_light}')
base_light_timer_start = time.time() 

# timer start
start_time = time.time()

# variable for toothbrushing start
brush_time_start = 0

# completed brushes
brushes_completed = 0
brushes_completed_reset_timer = time.time()

# list of data to be sent
list_of_data_to_send = []
                
while True:        
    # get sensor reading
    light_value = ldr_reading.ldr_reading()
    #print('light value: ', light_value)
    time.sleep(0.1)
    
    # base light sample reset 
    base_light_timer_reset = time.time()
    if base_light_timer_reset - base_light_timer_start > 240:
        base_light = ldr_reading.ldr_reading()
        print(f'new base light: {base_light}')
        base_light_timer_start = time.time()

    # variable to reset LED ring color from green to red after some time
    brush_timer = time.time()
    if brush_timer - brushes_completed_reset_timer > 300:
        brushes_completed = 0
        brushes_completed_reset_timer = time.time()
        print('ring turns red - brush_completed reset to 0')
        # led ring turns red
        led_ring.led_red()
        
    # if toothbrush is removed from stand 
    #print('light_value', light_value)
    if light_value>base_light*1.2: # ændret fra 1.3
        
        # tooth brush timer
        current_time = time.time()
        # check if time brushed timer has started or not
        if brush_time_start == 0:
            brush_time_start = time.time()
            print('brushing started..')
            # turn led ring off
            led_ring.led_off()
        
        
        #print('light value after lift: ',light_value,' ',count)
        if current_time - start_time > 1 and count < 12:
            start_time = time.time()
            count=count+1
            print(f'count: {count}')
            
        # led ring lights up as time passes 
        led_ring.led_brush(count) 
     
        # if the 12 seconds have passed blink blue
        if count == 12:
            led_ring.led_blink()
                
    # when toothbrush is placed back           
    if light_value < base_light*1.2 and brush_time_start > 0 or light_value == 0 and brush_time_start > 0: # ændret fra 1.3, indsat or light_value == 0 and brush_time_start > 0
        
        brush_time_finish = time.time()
        total_time_brushed = (brush_time_finish - brush_time_start)
        #print('light value after placed back: ',light_value, ' base_light after placed back: ', base_light)
        #print('toothbrush placed back, brush time start: ', brush_time_start,' brush time finish:',brush_time_finish, ' time brushed was: ', total_time_brushed,'seconds')
        print('brushing finished..')
        print(f'total time brushed: {total_time_brushed} seconds')
          
        # take new base light reading
        time.sleep(0.5)
        base_light = ldr_reading.ldr_reading()
        print(f'new base light : {base_light}') 
        
        # turn off led ring again
        led_ring.led_off()
        
        #  check if total time brushed was long enough. if yes, turn green, if no turn red
        if total_time_brushed > 11 or brushes_completed == 1:
            brushes_completed = 1
            led_ring.led_green()
            
        if total_time_brushed > 11:  
            # temp check
            time.sleep(1)
            object_temp = ir_test_works.read_temperature(MLX90614_TOBJ1)
            ambient_temp = ir_test_works.read_temperature(MLX90614_TA)
            print('object temp:',object_temp)
            print('ambient temp:',ambient_temp)
            #tooth_brush_temp = object_temp-ambient_temp
            if object_temp > ambient_temp:
                tooth_brush_temp = object_temp-ambient_temp
                print(f'tootbrush has been touched, its {tooth_brush_temp} *C hotter')
                
                # try to send data to server
                list_of_data_to_send.append(total_time_brushed)
                list_of_data_to_send.append(f"tandbørste berørt og {tooth_brush_temp}*C varmere")
                
                #print('list of data to send',list_of_data_to_send)
                if total_time_brushed > 11:
                    print(f'simuleret send: {list_of_data_to_send[-1]},{list_of_data_to_send[-2]}')
                    network_test_1.init_data(list_of_data_to_send[-2],list_of_data_to_send[-1])
            else:
                if total_time_brushed > 11:
                    print('tandbørsten var måske ikke holdt i hånd')
                    network_test_1.init_data(total_time_brushed,'tandbørste var muligvis ikke holdt i hånd')
        # if brush time is too short and one fully completed brush haven't been done since reset, turn led ring red
        if total_time_brushed < 11 and brushes_completed == 0:        
            led_ring.led_red()
            print("didn't brush long enough") 
               
        # reset brush timer, count and start time
        brush_time_start = 0
        count = 0
        start_time = time.time()
        
