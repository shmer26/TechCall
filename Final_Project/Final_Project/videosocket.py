import socket

class videosocket:
    '''A special type of socket to handle the sending and receiveing of fixed
       size frame strings over ususal sockets
       Size of a packet or whatever is assumed to be less than 100MB
    '''

    def __init__(self , sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock= sock

    def connect(self,host,port):
        self.sock.connect((host,port))

    def vsend(self, framestring):
        totalsent = 0
        metasent = 0
        length =len(framestring)
        lengthstr=str(length).zfill(8)

        while metasent < 8 :
            sent = self.sock.send(lengthstr[metasent:])
            if sent == 0:
                raise RuntimeError("Socket connection broken")
                self.sock.close()
            metasent += sent
        
        
        while totalsent < length :
            sent = self.sock.send(framestring[totalsent:])
            if sent == 0:
                raise RuntimeError("Socket connection broken")
                self.sock.close()
            totalsent += sent

    def vreceive(self):
        totrec=0
        metarec=0
        msgArray = []
        metaArray = []
        while metarec < 8:
            chunk = self.sock.recv(8 - metarec)
            if chunk == '':
                raise RuntimeError("Socket connection broken")
                self.sock.close()
            metaArray.append(chunk)
            metarec += len(chunk)
        lengthstr= ''.join(metaArray)
        length=int(lengthstr)

        while totrec<length :
            chunk = self.sock.recv(length - totrec)
            if chunk == '':
                raise RuntimeError("Socket connection broken")
                self.sock.close()
            msgArray.append(chunk)
            totrec += len(chunk)
        return ''.join(msgArray)

    def vclose(self):
        self.sock.close()

   


        
