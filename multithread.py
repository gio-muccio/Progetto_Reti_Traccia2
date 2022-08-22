import UDP_Socket_Server
import threading
import time

class multithread(UDP_Socket_Server.UDP_Socket_Server):
        
    def wait_request(self):
        try:
            while True:
                print(' ...Waiting to receive request-message from client...')
                data, address = self.sock.recvfrom(4096)
                request = (data, address)
                server = threading.Thread(target = self.solve_request, args = request)
                server.daemon_thread = True
                server.start()
                time.sleep(3) 
        except KeyboardInterrupt:
            print(' (Ctrl+C pressed)\n')
            time.sleep(1.5)
            print('Server closed.')
            self.shutdown_server()
            
def main():
    print('Opening server: ')
    server_multithread = multithread('127.0.0.1', 10000)
    server_multithread.__init_subclass__()
    server_multithread.wait_request()
    
if __name__ == '__main__':
    main()