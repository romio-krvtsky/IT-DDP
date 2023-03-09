import socket
import json

filename = "data.json"
username_lst = []

with open(filename, "r") as file:
    data = json.load(file)

for i in data['clients_data']:
    username_lst.append(i['username'])


username = input("Welcome! Please enter your username:  ")
if username in username_lst:
    client_id = username
    client_index = username_lst.index(client_id)
    client_messages = data['clients_data'][client_index]['messages']
else:
    raise Exception("Error! No such client")


# create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# set server address and port
server_address = ('localhost', 12345)

if client_messages:
    print("Your previous messages:")
    for msg in client_messages:
        print("-", msg)


while True:
    # get user input for message
    message = input('Enter message: ')
    if message == "exit":
        break
    client_messages.append(message)

    # send message to server with client ID prefix
    message = f'{client_id}:{message}'
    client_socket.sendto(message.encode(), server_address)

    # receive confirmation message from server
    response, _ = client_socket.recvfrom(4096)

    # decode message and print response
    print(response.decode())


# close the socket
with open(filename, "w") as file:
    json.dump(data, file)
client_socket.close()
