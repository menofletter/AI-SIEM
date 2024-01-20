from scapy.all import ARP, Ether, sniff, conf, srp
import threading
import json
import csv
import time

def scan_and_save_devices(ip_range="192.168.1.1/24", output_file="scanned_devices.json"):
    try:
        # Set L3socket as the socket type
        conf.L3socket = conf.L3socket6

        # Create ARP request packet
        arp_request = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip_range)

        # Send and receive packets
        result = srp(arp_request, timeout=3, verbose=0)[0]

        # Extract devices from response
        devices = [{'ip': received.psrc, 'mac': received.hwsrc} for sent, received in result]

        # Save devices to a JSON file
        with open(output_file, "w") as json_file:
            json.dump(devices, json_file, indent=4)

        print(f"Scanned devices saved to {output_file}")
    except Exception as e:
        print(f"Error during device scanning: {str(e)}")

def packet_handler(packet, output_file="captured_packets.csv"):
    try:
        # Define your packet handling logic here
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(packet.time))
        packet_info = {
            'timestamp': timestamp,
            'source': packet.src,
            'destination': packet.dst,
            'protocol': packet.payload.name,
            'length': len(packet),
        }

        # Write packet information to a CSV file
        with open(output_file, mode='a', newline='') as csv_file:
            fieldnames = ['timestamp', 'source', 'destination', 'protocol', 'length']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            # Write header if the file is empty
            if csv_file.tell() == 0:
                writer.writeheader()

            writer.writerow(packet_info)

        print(packet.summary())  # Example: Print a summary of each packet
    except Exception as e:
        print(f"Error handling packet: {str(e)}")

def capture_packets(output_file="captured_packets.csv"):
    try:
        # Start capturing packets using Scapy's sniff function
        sniff(prn=lambda packet: packet_handler(packet, output_file), store=0)
    except Exception as e:
        print(f"Error during packet capturing: {str(e)}")

# Specify your network range (replace with your actual subnet)
network_range = input("Enter the IP range (e.g., 192.168.1.1/24): ")

# Set the output file name for scanned devices
devices_output_file = 'scanned_devices.json'

# Set the output file name for captured packets
packets_output_file = 'captured_packets.csv'

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
