
def synchronizedCommunication():
    myDH, myRSA, hisRSA = initializeCryptography()

    loadPrivateData(myRSA, myDH)

    loadPublicData(hisRSA)

    sock = initializeSocket()

    sock.listen(1)
    conn_obj, addr = sock.accept()
    print("Got a connection from ", addr, " => Thanks...")
    value = json.loads(conn_obj.recv(2048))
    print ("received " + json.dumps(value, indent=1))
    sign = value.get('signature')
    message = str(value.get('message'))
    connectionVerification = Cryptography.verifySignature(sign, message, hisRSA.e, hisRSA.N)

    if connectionVerification:
        myDH.generatePrivateKey(int(message))
        package = Cryptography.packMessage(str(myDH.publicKey).encode(), myRSA.d, myRSA.N)
        answer = input("Do you want to send package \n %s \n 'n' to abort protocol\n" % (package))
        if (answer == 'n'):
            closeConnection(conn_obj, sock)
            return
        conn_obj.send(package.encode())
        myAES = Cryptography.AESCipher(str(myDH.privateKey))
        while True:
            package_from_client = json.loads(conn_obj.recv(2048))
            print("received" + json.dumps(package_from_client, indent=1))
            if not package_from_client:
                print ("no reply from client")
                break
            else:
                sign = package_from_client.get('signature')
                msg_from_client = package_from_client.get('message')
                messageVerification = Cryptography.verifySignature(sign, str(msg_from_client), hisRSA.e, hisRSA.N)
                if messageVerification:
                    msg_from_client = myAES.decrypt(msg_from_client.encode())
                    print ("message from client =>", msg_from_client)
                    msg_for_client = input("message for client =>")
                    msg_for_client = myAES.encrypt(msg_for_client)
                    package_for_client = Cryptography.packMessage(msg_for_client, myRSA.d, myRSA.N)
                    print("sent " + json.dumps(package_for_client, indent=1))
                    conn_obj.send(package_for_client.encode())
                else:
                    print("message verification failed")
                    break
    else:
        print("client key verification failed")
    closeConnection(conn_obj, sock)

def initializeCryptography():
    myDH = Cryptography.DH()
    myRSA = Cryptography.RSA()
    hisRSA = Cryptography.RSA()
    return myDH, myRSA, hisRSA

def loadPrivateData(myRSA, myDH):
    serverPrivateData = sys.argv[1]
    temp = []
    with open(serverPrivateData, "r") as file:
        for line in file:
            temp.append(line)
    ## (p, q, N, e, d)
    myRSA.setRSA(int(temp[0]), int(temp[1]), int(temp[2]), int(temp[3]), int(temp[4]))
    ## (p, g)
    myDH.setPG(int(temp[5], 16), int(temp[6], 16))

def loadPublicData(hisRSA):
    clientPublicData = sys.argv[2]
    temp = []
    with open(clientPublicData, "r") as file:
        for line in file:
            temp.append(line)
    # (N, e)
    hisRSA.setPublicKey(int(temp[0]), int(temp[1]))

def initializeSocket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_name = socket.gethostname()
    port_number = 1300
    print ("The name of local machine", host_name)
    host_port_pair = (host_name,port_number)
    print (host_port_pair)
    sock.bind(host_port_pair)
    return sock

def closeConnection(conn_obj, sock):
    conn_obj.close()
    sock.close()

if __name__ == "__main__":
    import socket
    import json
    import Cryptography
    import sys
    if (len(sys.argv) == 3):
        synchronizedCommunication()
    else:
        print ("Please, provide two parameters!")



