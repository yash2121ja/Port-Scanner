# Port Scanner
This is a Python script that scans a list of IP addresses and subnets for open ports 80 and 443. It also retrieves the domain name for each IP address.

# Usage
1. Create a text file named ip_ranges.txt in the same directory as the Python script.
2. Add the IP addresses and subnets to scan in the ip_ranges.txt file, one per line.
3. Run the Python script using python port_scanner.py.
4. The results will be saved to an Excel file named port_scan_results.xlsx in the same directory as the Python script.

# Dependencies
This Python script requires the following dependencies:

* `concurrent.futures`
* `nmap`
* `enpyxl`
* `tqdm`
* `ipaddress`
* `socket`
These dependencies can be installed using pip:


`pip install -r requirements.txt`

# License
This Python script is released under the MIT License. See the LICENSE file for details.
