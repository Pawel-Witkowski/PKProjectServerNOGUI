import socket
import json
import Cryptography


secondPublic = 608304910142350396698363327001812754362885774565113507467145687232890587785014631394173069824500094829807307054273835218156320703304105285660931778433496412765294560162930708921682965665533072584084877545594795640400563105158139815
myDH = Cryptography.DH()
myRSA = Cryptography.RSA()
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_name = socket.gethostname()
port_number = 1300
print ("The name of local machine", host_name)

host_port_pair = (host_name,port_number)
print (host_port_pair)
sock.bind(host_port_pair)

sock.listen(1)

conn_obj, addr = sock.accept()
print("Got a connection from ", addr, " => Thanks...")

value = json.loads(conn_obj.recv(2048))
sign = value.get('signature')
message = str(value.get('message'))
connectionVerification = Cryptography.verifySignature(sign, message, secondPublic, myRSA.N)

if connectionVerification:
    myDH.generatePrivateKey(int(message))
    package = Cryptography.packMessage(str(myDH.publicKey).encode(), myRSA.d, myRSA.N)
    conn_obj.send(package.encode())

    myAES = Cryptography.AESCipher(str(myDH.privateKey))
    while True:
        package_from_client = json.loads(conn_obj.recv(2048))

        if not package_from_client:
            print ("no reply from client")
            break
        else:
            sign = package_from_client.get('signature')
            msg_from_client = package_from_client.get('message')
            verificationOfMessage = Cryptography.verifySignature(sign, str(msg_from_client), secondPublic, myRSA.N)
            if verificationOfMessage:
                msg_from_client = myAES.decrypt(msg_from_client.encode())
                print ("message from client =>", msg_from_client)

                msg_for_client = input("message for client =>")
                msg_for_client = myAES.encrypt(msg_for_client)
                package_for_client = Cryptography.packMessage(msg_for_client, myRSA.d, myRSA.N)
                conn_obj.send(package_for_client.encode())
            else:
                print("message verification failed")
                break
else:
    print("client key verification failed")
conn_obj.close()
sock.close()
