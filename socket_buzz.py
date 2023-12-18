import socket
import buzzer


#This sectio opens a socket connection. Once a connection has been detected, it takes the data and decodes it.
def init_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("", 3000))
    print("Listening...")
    s.listen()
    while True:
        try:
            clientsocket, address = s.accept()
            print(f"Connection from {address} has been established")
            call_back="Your call has been recieved."
            clientsocket.send(call_back.encode())
            
            
            # buzzer
            buzzer.buzzer_play()

            '''
            sentdata=[str(i) for i in clientsocket.recv(2048).decode("utf-8").split("\n")]
            print(sentdata)
            check_pass(sentdata)

            call_back="Data has been recieved."
            clientsocket.send(call_back.encode())
            '''
        except Exception as e:
            print(f"Exception{e}")
        finally:
            s.close()
            init_socket_thread()
            break


#Starts a thread for the function above.
def init_socket_thread():
    th = Thread(target=init_socket)
    th.start()
    print("New thread started")
    
    
