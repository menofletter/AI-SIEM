from scapy.all import ARP, Ether, sniff, conf, srp
import threading

def scan_and_save_devices(ip_range="192.168.1.1/24", output_file="scanned_devices.txt"):
    # Set L3socket as the socket type
    conf.L3socket = conf.L3socket6

    # Create ARP request packet
    arp_request = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip_range)

    # Send and receive packets
    result = srp(arp_request, timeout=3, verbose=0)[0]

    # Extract devices from response
    devices = []
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})

    # Save devices to a file
    with open(output_file, "w") as file:
        for device in devices:
            file.write(f"IP: {device['ip']}, MAC: {device['mac']}\n")

    print(f"Scanned devices saved to {output_file}")

def packet_handler(packet, output_file="captured_packets.txt"):
    # Write packet information to a file
    with open(output_file, "a") as file:
        file.write(str(packet) + "\n")

    # Define your packet handling logic here
    print(packet.summary())  # Example: Print a summary of each packet

def capture_packets(output_file="captured_packets.txt"):
    # Start capturing packets using Scapy's sniff function
    sniff(prn=lambda packet: packet_handler(packet, output_file), store=0)

# Specify your network range (replace with your actual subnet)
network_range = "192.168.1.1/24"

# Set the output file name for scanned devices
devices_output_file = 'scanned_devices.txt'

# Set the output file name for captured packets
packets_output_file = 'captured_packets.txt'

# Create a thread to scan and save devices
scan_thread = threading.Thread(target=scan_and_save_devices, args=(network_range, devices_output_file))
scan_thread.start()

# Wait for the scanning thread to complete
scan_thread.join()

# Create a thread to capture packets
capture_thread = threading.Thread(target=capture_packets, args=(packets_output_file,))
capture_thread.start()

# Allow some time for packet capturing (adjust as needed)
input("Press Enter to stop capturing...")

# Stop the packet capturing thread
capture_thread.join()

print("Packet capturing completed.")

