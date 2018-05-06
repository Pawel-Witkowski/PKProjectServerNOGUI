import socket
import json


def fillNumberTo10digits(number):
    size = ''.join('0' for i in range(10 - len(str(number))))
    size += str(number)
    return json.dumps(size).encode()



# next create a socket object
s = socket.socket()
print ("Socket successfully created")

# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 12345
dictA = {"first": 1, "second": 2}
dictB = {"third": 3, "fourth": 4}

dictAToSend = json.dumps(dictA).encode()
sizeA = fillNumberTo10digits(len(dictAToSend))

print (sizeA)
dictBToSend = json.dumps(dictB).encode()
sizeB = fillNumberTo10digits(len(dictBToSend))



# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests
# coming from other computers on the network
s.bind(('', port))
print ("socket binded to %s" %(port))
# # put the socket into listening mode
s.listen()
print ("socket is listening")

# Establish connection with client.
c, addr = s.accept()
print ('Got connection  ', addr)


# send a thank you message to the client.
c.sendall(sizeA)
c.sendall(dictAToSend)

c.sendall(sizeB)
c.sendall(dictBToSend)

print(json.loads(c.recv(8)))
# Close the connection with the client
c.close()




