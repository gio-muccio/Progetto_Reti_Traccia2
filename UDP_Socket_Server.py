import socket as sk
import os
import select

class UDP_Socket_Server:
    
    def __init__(self, host, port):
        self.host = host
        self.port = port  
        self.sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
        self.server_address = (host, port)
        print('\n Starting up on %s port %s...' % (self.server_address))
        self.sock.bind(self.server_address)

    def file_list(self, address):
        f_list = ''
        for name in os.listdir(os.getcwd()):
            f_list = f_list + name + '\n'
        sent = self.sock.sendto(f_list.encode(), address)
        return sent
            
    def get_file(self, file, address):
        if os.path.isfile(file):
            positive_response = 'Exist'
            sent = self.sock.sendto(positive_response.encode(), address)
            f = open(file, 'rb')
            text = f.read(4096)
            while (text):
                check = self.sock.sendto(text, address)
                if (check):
                    sent = sent + check
                    text = f.read(4096)
            f.close()
        else:
            negative_response = '\nFinal status: ERROR, file not exist!\n'
            sent = self.sock.sendto(negative_response.encode(), address)
        return sent
            
    def put_file(self, file):
        accept, address = self.sock.recvfrom(4096)
        if accept.decode('utf8') == 'Exist':
            f = open(file, 'wb')
            while True:
                read = select.select([self.sock], [], [], 0.125)
                if read[0]:
                    text, address = self.sock.recvfrom(4096)
                    f.write(text)
                else:
                    f.close()
                    positive_response = 'Final status: UPLOADED!\n'
                    sent = self.sock.sendto(positive_response.encode(), address)
                    break
        else:
            negative_response = '\nFinal status: ERROR, insert an existing file with its extension!\n'
            sent = self.sock.sendto(negative_response.encode(), address)
        return sent
        
    def solve_request(self, data, address):
        print(' Received %s bytes: ' % (len(data)))
        message = data.decode('utf8')
        print(' Command  >%s<  received from %s' % (message, address))
        if message[0:4] == 'list':
            sent = self.file_list(address)
        elif message[0:3] == 'get':
            sent = self.get_file(message[4:], address)
        elif message[0:3] == 'put':
            sent = self.put_file(message[4:])
        else:
            error = 'ERROR, please enter the correct command!'
            sent = self.sock.sendto(error.encode(), address)    
        print(' Response status: OK! Sent %s bytes back to %s\n' % (sent, address))
        
    def wait_request(self):
        data, address = self.sock.recvfrom(4096)
        self.solve_request(data, address)
    
    def shutdown_server(self):
        self.sock.close()   