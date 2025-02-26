import socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("10.200.226.11", 1800))
text = open("cheval.txt", "w")

def is_right(response): # Check if the response is proper
    ind_l = int(response[0])
    l = len(response)

    ind = response[1 : 1+ind_l]

    ind1 = ind[:ind_l // 2]
    ind2 = ind[ind_l // 2:]

    if ind_l % 2 != 0:
        ind2 = ind[(ind_l // 2) + 1:]
    ind1 = sorted(ind1)
    ind2 = sorted(ind2)

    return ind1 == ind2

def create_code():
    char = client_socket.recv(1).decode()
    code = ""

    l = int(char) + 3

    j = 0
    while j < l:
        code += char
        char = client_socket.recv(1).decode()
        j += 1

    return code

i = 1
while i < 70:
    inline = True

    while inline:
        client_socket.send(f"{i:03d}".encode())

        l = client_socket.recv(1).decode()
        recv = create_code()
        inline = is_right(recv)

        if inline and recv[0].isnumeric:
            text.write(recv[-3:])

    text.write("\n")
    i += 1

client_socket.close()
text.close()