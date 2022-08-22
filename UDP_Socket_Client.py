import socket as sk
import os
import select
import time

class UDP_Socket_Client:
    
    def __init__(self):
        self.sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
                    
    def get_file(self, file, server_address):
        print('\nWaiting to receive response...')
        time.sleep(0.5)
        response, server_address = self.sock.recvfrom(4096)
        if response.decode('utf8') == 'Exist':
            print('\n...downloading file...')
            f = open(file, 'wb')
            while True:
                read = select.select([self.sock], [], [], 0.125)
                if read[0]:
                    text, address = self.sock.recvfrom(4096)
                    f.write(text)
                else:
                    f.close()
                    break
            time.sleep(1.5)
            print('Final status: DOWNLOADED!\n')
        else:
            print(response.decode('utf8'))
    
    def put_file(self, file, server_address):
        print('\nWaiting to receive response...')
        time.sleep(0.5)
        if os.path.isfile(file):
            positive_response = 'Exist'
            self.sock.sendto(positive_response.encode(), server_address)
            print('\n...uploading file...')
            f = open(file, 'rb')
            text = f.read(4096)
            while (text):
                if (self.sock.sendto(text, server_address)):
                    text = f.read(4096)
                else:
                    f.close()
                    break
            time.sleep(1.5)
        else:
            negative_response = 'File not exist'
            self.sock.sendto(negative_response.encode(), server_address)
        data, server = self.sock.recvfrom(4096)
        print(data.decode('utf8'))
       
    def handle_request(self, server_address):
        try:
            options = 'Possible request:\n 1) list \n 2) get \n 3) put \n\n>'
            message = input(options) 
            print('Command request:  >%s< ' % message)
            print('Sending message  "%s"  to socket server %s' % (message, server_address))
            time.sleep(1.5)
            self.sock.sendto(message.encode(), server_address)
            command = message[0:3]               
            if command == 'get':
                self.get_file(message[4:], server_address)
            elif command == 'put':
                self.put_file(message[4:], server_address)
            else:
                print('\nWaiting to receive response...\n')
                time.sleep(2)
                data, server = self.sock.recvfrom(4096)
                output = data.decode('utf8')
                print('Response from the server: \n%s' % output)               
        except Exception as info:
            print(info)
        finally:
            print("Ending the client's request...")
            time.sleep(1.5)
            print('Client end.')
            self.sock.close()

def main():
    print('Client start: ')
    client = UDP_Socket_Client()
    client.handle_request(('127.0.0.1', 10000))

if __name__ == '__main__':
    main()