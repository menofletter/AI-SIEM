import socket

def capture_and_save_packets(interface="wlp8s0b1", packet_count=10, output_file="captured_packets.bin"):
    # Create a raw socket and bind it to the specified interface
    raw_socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(3))
    raw_socket.bind((interface, 0))

    # Open a file for writing in binary mode
    with open(output_file, "wb") as file:
        # Capture and write packets
        for _ in range(packet_count):
            packet, _ = raw_socket.recvfrom(65535)
            file.write(packet)

    # Close the socket
    raw_socket.close()

# Set the network interface to monitor (replace 'enp0s3' with your actual interface)
network_interface = 'wlp8s0b1'

# Set the number of packets to capture (you can adjust this based on your needs)
packet_count = 10

# Set the output file name
output_file = 'captured_packets.bin'

# Start capturing and saving packets
capture_and_save_packets(network_interface, packet_count, output_file)
