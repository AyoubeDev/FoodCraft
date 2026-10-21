import socket 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SQL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("localhost", 8888))


while True:
    
    cliente_socket, addr = server.accept()
    print(f"Connection form {addr} has been established")

    client_socket.send(bytes("Welcome to the calculator Server", "utf-8"))

    while True:
        data = client_socket.recv(1024)
        if not data: 
            break

        number_1, number_2, operation = data.decode("utf-8").split(" ;")
        print(f"{number_1} {operation} {number_2}")

        if operation.strip() == "+":
            result = int(number_1) + int(number_2)
        elif operation.strip() == "-":
            result = int(number_1) - int(number_2)
        elif operation.strip() == "*":
            result = int(number_1) * int(number_2)
        elif operation.strip() == "/":
            result = int(number_1) / int(number_2)
        client_socket.send(bytes())

        # 2;3;+

        print(f"Recived data: {data}")
        client_socket.close()