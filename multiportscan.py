import concurrent.futures
import nmap
import openpyxl
from tqdm import tqdm
from ipaddress import ip_network, ip_address
import socket

# Open the text file containing the IP addresses and subnets
with open('ip_ranges.txt') as f:
    ip_ranges = f.read().splitlines()

# Create a list of IP addresses to scan
ip_list = []
for ip_range in ip_ranges:
    try:
        network = ip_network(ip_range)
        ip_list.extend([str(ip) for ip in network])
    except ValueError:
        ip_list.append(ip_range)

# Create an Nmap PortScanner object
nm = nmap.PortScanner()

# Create an Excel workbook and add a worksheet
workbook = openpyxl.Workbook()
worksheet = workbook.active

# Set the column headings for the worksheet
worksheet['A1'] = 'IP Address'
worksheet['B1'] = 'Domain Name'

# Define the list of additional ports to scan
additional_ports = [21, 22, 23, 443, 80, 161, 21, 162, 5432, 1433, 135, 8080, 53, 139, 445, 1720, 5060, 3389, 3306, 123, 500, 465, 25, 69, 383, 5432, 8030]

# Set the column headings for each additional port
for port in additional_ports:
    worksheet.cell(row=1, column=len(worksheet[1]) + 1).value = f'Port {port}'

# Define a function to scan a single IP address
def scan_ip(ip):
    # Scan additional ports for the IP address
    nm.scan(ip, ','.join(map(str, additional_ports)))

    # Get the domain name for the IP address
    try:
        domain_name = socket.gethostbyaddr(ip)[0]
    except socket.herror:
        domain_name = 'unknown'

    # Initialize a list to store port statuses
    port_statuses = ['unknown'] * len(additional_ports)

    # Update the list with the status of each additional port
    for i, port in enumerate(additional_ports):
        try:
            port_status = nm[ip]['tcp'][port]['state']
            port_statuses[i] = port_status
        except KeyError:
            pass

    # Return the IP address, domain name, and port statuses as a tuple
    return (ip, domain_name) + tuple(port_statuses)

# Use multi-threading to scan IP addresses in parallel
with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    results = list(tqdm(executor.map(scan_ip, ip_list), total=len(ip_list)))

# Write the results to the Excel worksheet
for i, result in enumerate(results):
    worksheet.cell(row=i+2, column=1).value = result[0]
    worksheet.cell(row=i+2, column=2).value = result[1]
    for j, port_status in enumerate(result[2:]):
        worksheet.cell(row=i+2, column=len(worksheet[1]) + 1 + j).value = port_status

# Save the Excel workbook
workbook.save('port_scan_results.xlsx')
