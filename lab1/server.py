import socket


# create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# set server address and port
server_address = ('localhost', 12345)
server_socket.bind(server_address)

# dictionary to store client message history
client_history = {}

while True:
    # receive message from client
    message, client_address = server_socket.recvfrom(4096)

    # decode message and extract client ID
    message = message.decode()
    client_id, client_message = message.split(':', 1)

    # check ifthis is a new client connection
    if client_id not in client_history:
        print('Waiting for client connection...')
        print(f'New client connected: {client_id}')
        # create a new message history for this client
        client_history[client_id] = []

    # add message to client history
    client_history[client_id].append(client_message)
    print(f"{client_id} - {client_message}")
    # send confirmation message to client
    srvr_msg = input('Enter a message: ')
    if srvr_msg == 'exit':
        break
    response_message = f'server: {srvr_msg}'

    # response_message = f'Message received: {client_message}'
    server_socket.sendto(response_message.encode(), client_address)

# close the socket
server_socket.close()
