# Standard Libraries
import os
import sys
import configparser
import time
import json
import subprocess
import re
import fileinput
import random
import ipaddress
import math
# External Libraries
import requests
# ProtonVPN-CLI functions
from protonvpn_linux_gui.gui_logger import gui_logger
# Constants
from .constants import (
    USER, CONFIG_FILE, SERVER_INFO_FILE, TEMPLATE_FILE, SPLIT_TUNNEL_FILE,
    VERSION
)


def call_api(endpoint, json_format=True, handle_errors=True, gui_enabled=False):
    """Call to the ProtonVPN API."""
    
    api_domain = "https://api.protonvpn.ch"
    url = api_domain + endpoint

    headers = {
        "x-pm-appversion": "Other",
        "x-pm-apiversion": "3",
        "Accept": "application/vnd.protonmail.v1+json"
    }

    gui_logger.debug("Initiating API Call: {0}".format(url))

    # For manual error handling, such as in wait_for_network()
    if not handle_errors:
        response = requests.get(url, headers=headers)
        return response

    try:
        response = requests.get(url, headers=headers, timeout=6)
        # response = requests.get(url, headers=headers)
    except (requests.exceptions.ConnectionError,
            requests.exceptions.ConnectTimeout):
        if not gui_enabled:
            print(
                "[!] There was an error connecting to the ProtonVPN API.\n"
                "[!] Please make sure your connection is working properly!"
            )
        gui_logger.debug("Error connecting to ProtonVPN API")
        if not gui_enabled:
            sys.exit(1)
        return False
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        if not gui_enabled:
            print(
                "[!] There was an error with accessing the ProtonVPN API.\n"
                "[!] Please make sure your connection is working properly!\n"
                "[!] HTTP Error Code: {0}".format(response.status_code)
            )
        gui_logger.debug("Bad Return Code: {0}".format(response.status_code))
        if not gui_enabled:
            sys.exit(1)
        return False

    if json_format:
        gui_logger.debug("Successful json response")
        return response.json()
    else:
        gui_logger.debug("Successful non-json response")
        return response

    if gui_enabled:
        return True

def pull_server_data(force=False):
    """Pull current server data from the ProtonVPN API."""
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    if not force:
        # Check if last server pull happened within the last 15 min (900 sec)
        if int(time.time()) - int(config["metadata"]["last_api_pull"]) <= 900:
            gui_logger.debug("Last server pull within 15mins")
            return

    data = call_api("/vpn/logicals")

    with open(SERVER_INFO_FILE, "w") as f:
        json.dump(data, f)
        gui_logger.debug("SERVER_INFO_FILE written")

    change_file_owner(SERVER_INFO_FILE)
    config["metadata"]["last_api_pull"] = str(int(time.time()))

    with open(CONFIG_FILE, "w+") as f:
        config.write(f)
        gui_logger.debug("last_api_call updated")


def get_servers():
    """Return a list of all servers for the users Tier."""

    server_data = {}
    timer_start = time.time()

    while True:
        if time.time() - timer_start > 5:
            break

        with open(SERVER_INFO_FILE, "r") as f:
            gui_logger.debug("Reading servers from file")
            try:
                data = json.load(f)
                if not data == None and not len(data) == 0:
                    server_data = data
                    break
            except:
                pull_server_data(force=True)
                time.sleep(2)
                pass

        # time.sleep(2)

    if len(server_data) == 0:
        return False

    servers = server_data["LogicalServers"]

    user_tier = int(get_config_value("USER", "tier"))

    # Sort server IDs by Tier
    return [server for server in servers if server["Tier"] <= user_tier and server["Status"] == 1] # noqa


def get_server_value(servername, key, servers):
    """Return the value of a key for a given server."""
    value = [server[key] for server in servers if server['Name'] == servername]
    return value[0]


def get_config_value(group, key):
    """Return specific value from CONFIG_FILE as string"""
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    return config[group][key]


def set_config_value(group, key, value):
    """Write a specific value to CONFIG_FILE"""

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    config[group][key] = str(value)

    gui_logger.debug(
        "Writing {0} to [{1}] in config file".format(key, group)
    )

    with open(CONFIG_FILE, "w+") as f:
        config.write(f)


def get_ip_info(gui_enabled=False):
    """Return the current public IP Address"""
    gui_logger.debug("Getting IP Information")
    ip_info = call_api("/vpn/location", gui_enabled=gui_enabled)

    if ip_info == None or ip_info == False:
        return False

    ip = ip_info["IP"]
    isp = ip_info["ISP"]

    if gui_enabled == True:
        return ip, isp, ip_info["Country"]
    return ip, isp


def get_country_name(code):
    """Return the full name of a country from code"""

    from .country_codes import country_codes
    return country_codes.get(code, code)


def get_fastest_server(server_pool):
    """Return the fastest server from a list of servers"""

    # Sort servers by "speed" and select top n according to pool_size
    fastest_pool = sorted(
        server_pool, key=lambda server: server["Score"]
    )
    if len(fastest_pool) >= 50:
        pool_size = 4
    else:
        pool_size = 1
    gui_logger.debug(
        "Returning fastest server with pool size {0}".format(pool_size)
    )
    fastest_server = random.choice(fastest_pool[:pool_size])["Name"]
    return fastest_server


def get_default_nic():
    """Find and return the default network interface"""
    default_route = subprocess.run(
        "ip route show | grep default",
        stdout=subprocess.PIPE, shell=True
    )

    # Get the default nic from ip route show output
    default_nic = default_route.stdout.decode().strip().split()[4]
    return default_nic


def is_connected():
    """Check if a VPN connection already exists."""
    ovpn_processes = subprocess.run(["pgrep", "--exact", "openvpn"],
                                    stdout=subprocess.PIPE)
    ovpn_processes = ovpn_processes.stdout.decode("utf-8").split()

    gui_logger.debug(
        "Checking connection Status. OpenVPN processes: {0}"
        .format(len(ovpn_processes))
        )
    return True if ovpn_processes != [] else False


def wait_for_network(wait_time):
    """Check if internet access is working"""

    print("Waiting for connection...")
    start = time.time()

    while True:
        if time.time() - start > wait_time:
            gui_logger.debug("Max waiting time reached.")
            print("Max waiting time reached.")
            sys.exit(1)
        gui_logger.debug("Waiting for {0}s for connection...".format(wait_time))
        try:
            call_api("/test/ping", handle_errors=False)
            time.sleep(2)
            print("Connection working!")
            gui_logger.debug("Connection working!")
            break
        except (requests.exceptions.ConnectionError,
                requests.exceptions.ConnectTimeout):
            time.sleep(2)


def cidr_to_netmask(cidr):
    subnet = ipaddress.IPv4Network("0.0.0.0/{0}".format(cidr))
    return str(subnet.netmask)


def make_ovpn_template():
    """Create OpenVPN template file."""
    pull_server_data()

    with open(SERVER_INFO_FILE, "r") as f:
        server_data = json.load(f)

    # Get the ID of the first server from the API
    server_id = server_data["LogicalServers"][0]["ID"]

    config_file_response = call_api(
        "/vpn/config?Platform=linux&LogicalID={0}&Protocol=tcp".format(server_id),  # noqa
        json_format=False
    )

    with open(TEMPLATE_FILE, "wb") as f:
        for chunk in config_file_response.iter_content(100000):
            f.write(chunk)
            gui_logger.debug("OpenVPN config file downloaded")

    # Write split tunneling config to OpenVPN Template
    try:
        if get_config_value("USER", "split_tunnel") == "1":
            split = True
        else:
            split = False
    except KeyError:
        split = False
    if split:
        gui_logger.debug("Writing Split Tunnel config")
        with open(SPLIT_TUNNEL_FILE, "r") as f:
            content = f.readlines()

        with open(TEMPLATE_FILE, "a") as f:
            for line in content:
                line = line.rstrip("\n")
                netmask = None

                if not is_valid_ip(line):
                    gui_logger.debug(
                        "[!] '{0}' is invalid. Skipped.".format(line)
                    )
                    continue

                if "/" in line:
                    ip, cidr = line.split("/")
                    netmask = cidr_to_netmask(int(cidr))
                else:
                    ip = line

                if netmask is None:
                    netmask = "255.255.255.255"

                if is_valid_ip(ip):
                    f.write(
                        "\nroute {0} {1} net_gateway".format(ip, netmask)
                    )

                else:
                    gui_logger.debug(
                        "[!] '{0}' is invalid. Skipped.".format(line)
                    )

        gui_logger.debug("Split Tunneling Written")

    # Remove all remote, proto, up, down and script-security lines
    # from template file
    remove_regex = re.compile(r"^(remote|proto|up|down|script-security) .*$")

    for line in fileinput.input(TEMPLATE_FILE, inplace=True):
        if not remove_regex.search(line):
            print(line, end="")

    gui_logger.debug("remote and proto lines removed")

    change_file_owner(TEMPLATE_FILE)


def change_file_owner(path):
    """Change the owner of specific files to the sudo user."""
    uid = int(subprocess.run(["id", "-u", USER],
                             stdout=subprocess.PIPE).stdout)
    gid = int(subprocess.run(["id", "-u", USER],
                             stdout=subprocess.PIPE).stdout)

    current_owner = subprocess.run(["id", "-nu", str(os.stat(path).st_uid)],
                                   stdout=subprocess.PIPE).stdout
    current_owner = current_owner.decode().rstrip("\n")

    # Only change file owner if it wasn't owned by current running user.
    if current_owner != USER:
        os.chown(path, uid, gid)
        gui_logger.debug("Changed owner of {0} to {1}".format(path, USER))


def check_root():
    """Check if the program was executed as root and prompt the user."""
    if os.geteuid() != 0:
        print(
            "[!] The program was not executed as root.\n"
            "[!] Please run as root."
        )
        gui_logger.debug("Program wasn't executed as root")
        sys.exit(1)
    else:
        # Check for dependencies
        dependencies = ["openvpn", "ip", "sysctl", "pgrep", "pkill"]
        for program in dependencies:
            check = subprocess.run(["which", program],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
            if not check.returncode == 0:
                gui_logger.debug("{0} not found".format(program))
                print("'{0}' not found. \n".format(program) +
                      "Please install {0}.".format(program))
                sys.exit(1)


def check_update():
    """Return the download URL if an Update is available, False if otherwise"""

    def get_latest_version():
        """Return the latest version from pypi"""
        gui_logger.debug("Calling pypi API")
        try:
            r = requests.get("https://pypi.org/pypi/protonvpn-cli/json")
        except (requests.exceptions.ConnectionError,
                requests.exceptions.ConnectTimeout):
            gui_logger.debug("Couldn't connect to pypi API")
            return False
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            gui_logger.debug(
                "HTTP Error with pypi API: {0}".format(r.status_code)
            )
            return False

        release = r.json()["info"]["version"]

        return release

    # Determine if an update check should be run
    check_interval = int(get_config_value("USER", "check_update_interval"))
    check_interval = check_interval * 24 * 3600
    last_check = int(get_config_value("metadata", "last_update_check"))

    if (last_check + check_interval) >= time.time():
        # Don't check for update
        return

    gui_logger.debug("Checking for new update")
    current_version = list(VERSION.split("."))
    current_version = [int(i) for i in current_version]
    gui_logger.debug("Current: {0}".format(current_version))

    latest_version = get_latest_version()
    if not latest_version:
        # Skip if get_latest_version() ran into errors
        return
    latest_version = latest_version.split(".")
    latest_version = [int(i) for i in latest_version]
    gui_logger.debug("Latest: {0}".format(latest_version))

    for idx, i in enumerate(latest_version):
        if i > current_version[idx]:
            gui_logger.debug("Update found")
            update_available = True
            break
        elif i < current_version[idx]:
            gui_logger.debug("No update")
            update_available = False
            break
    else:
        gui_logger.debug("No update")
        update_available = False

    set_config_value("metadata", "last_update_check", int(time.time()))

    if update_available:
        print()
        print(
            "A new Update for ProtonVPN-CLI (v{0}) ".format('.'.join(
                [str(x) for x in latest_version])
                ) +
            "is available.\n" +
            "Follow the Update instructions on\n" +
            "https://github.com/ProtonVPN/protonvpn-cli-ng/blob/master/USAGE.md#updating-protonvpn-cli\n" + # noqa
            "\n"
            "To see what's new, check out the changelog:\n" +
            "https://github.com/ProtonVPN/protonvpn-cli-ng/blob/master/CHANGELOG.md" # noqa
        )


def check_init():
    """Check if a profile has been initialized, quit otherwise."""

    try:
        if not int(get_config_value("USER", "initialized")):
            print(
                "[!] There has been no profile initialized yet. "
                "Please run 'protonvpn init'."
            )
            gui_logger.debug("Initialized Profile not found")
            sys.exit(1)
        else:
            # Check if required configuration values are set
            # If this isn't the case it will set a default value

            default_conf = {
                "USER": {
                    "username": "username",
                    "tier": "0",
                    "default_protocol": "udp",
                    "dns_leak_protection": "1",
                    "custom_dns": "None",
                    "check_update_interval": "3",
                    "killswitch": "0",
                    "split_tunnel": "0",
                },
            }

            for section in default_conf:
                for config_key in default_conf[section]:
                    try:
                        get_config_value(section, config_key)
                    except KeyError:
                        gui_logger.debug("Config {0}/{1} not found, default set"
                                     .format(section, config_key))
                        set_config_value(section, config_key,
                                         default_conf[section][config_key])

    except KeyError:
        print(
            "[!] There has been no profile initialized yet. "
            "Please run 'protonvpn init'."
        )
        gui_logger.debug("Initialized Profile not found")
        sys.exit(1)


def is_valid_ip(ipaddr):
    valid_ip_re = re.compile(
        r'^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.'
        r'(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.'
        r'(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.'
        r'(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)'
        r'(/(3[0-2]|[12][0-9]|[1-9]))?$'  # Matches CIDR
    )

    if valid_ip_re.match(ipaddr):
        return True

    else:
        return False


def get_transferred_data():
    """Reads and returns the amount of data transferred during a session
    from the /sys/ directory"""

    def convert_size(size_bytes):
        """Converts byte amounts into human readable formats"""
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")

        i = int(math.floor(math.log(size_bytes, 1000)))
        p = math.pow(1000, i)
        s = round(size_bytes / p, 2)
        return "{0} {1}".format(s, size_name[i])

    base_path = "/sys/class/net/{0}/statistics/{1}"

    if os.path.isfile(base_path.format('proton0', 'rx_bytes')):
        adapter_name = 'proton0'
    elif os.path.isfile(base_path.format('tun0', 'rx_bytes')):
        adapter_name = 'tun0'
    else:
        gui_logger.debug("No usage stats for VPN interface available")
        return '-', '-'

    # Get transmitted and received bytes from /sys/ directory
    with open(base_path.format(adapter_name, 'tx_bytes'), "r") as f:
        tx_bytes = int(f.read())

    with open(base_path.format(adapter_name, 'rx_bytes'), "r") as f:
        rx_bytes = int(f.read())

    return convert_size(tx_bytes), convert_size(rx_bytes)
