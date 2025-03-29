# Imports
import socket
from urllib.parse import urlparse

#   Finals
# Header
MESSAGE_ID = b"00"
QR_UNTIL_RCODE = b"00"
QDCOUNT = b"01"
ANCOUNT = b"00"
NSCOUNT = b"00"
ARCOUNT = b"00"

HEADER = MESSAGE_ID + QR_UNTIL_RCODE + QDCOUNT + ANCOUNT + NSCOUNT + ARCOUNT

# Question
QTYPE = b"01"
QCLASS = b"01"

client_socket = None
file_urls = None
file_ips = None


def main():  # The main Function
    global file_urls
    global file_ips
    global client_socket

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    file_urls = open("urls.txt", 'r')
    file_ips = open("Text3.txt", 'w')

    urls_list = file_urls.read().splitlines()

    for url in urls_list:
        process_request(url)

    file_urls.close()
    file_ips.close()
    client_socket.close()


def process_request(url):  # Processes a DNS interaction
    request = create_request(url)  # Creates the request
    print(request)
    client_socket.sendto(request, ("10.200.226.11", 1800))  # Sends the information to the Server
    data, addr = client_socket.recvfrom(8)  # Gets the information from the server
    print(data)
    ip = convert_to_IP(data.decode)  # Gets the real IP
    write_to_file(ip)  # Write the information to the file accordingly


def create_request(url):  # Creates the DNS request
    request = HEADER
    QName = convert_url_to_hex(url)
    request += QName.encode()
    request += QTYPE + QCLASS   
    return request


def convert_url_to_hex(url):  # Converts the present URL into Hexadecimal
    # Remove "http://" or "https://"
    clean_domain = url.split("/")[2]

    # Convert domain to QNAME format
    qname_parts = clean_domain.split(".")  # Split domain into labels
    qname_parts[1].upper()
    qname_str = "".join(f"{len(part):02}{part}" for part in qname_parts) + '0'

    return qname_str  # Returns raw bytes, not hex


def convert_to_IP(hex_ip):  # Converts the hexadecimal IP into regular ip
    ip_address = ".".join(str(int(hex_ip[i:i + 2], 16)) for i in range(0, 8, 2))
    return ip_address


def write_to_file(ip):  # Gets the ip, and writes to Text3.txt by the instructions
    # Split the IP address and get the last octet
    last_octet = int(ip.split(".")[-1])

    # Convert to ASCII character and write to file
    file_ips.write(chr(last_octet))

main()