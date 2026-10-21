import socket

socket = socket.create_connection(("localhost", 8888))

data = socket.recv(1024) #recive el mensaje de bienvenida del servidor
print(f"> {data}")


continue_calc = y
while continue_calc == "y":
    number_1 = int(input("type the first number"))
    operation = int(input("type the operation (+, -, *, /)"))
    number_2 = int(input("type the first number"))

    socket.send(bytes(f"{number_1} ; {operation} ; {number_2}"))

    result = socket.recv(1024)
    print(f"Result: {result.decode('utf-8')}")

    continue_calc = input("Quieres seguir haciendo calculos? y/n") == "y"
    