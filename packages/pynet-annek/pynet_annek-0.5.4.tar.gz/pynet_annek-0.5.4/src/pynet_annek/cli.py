""" Core module with cli """
import csv
import sys
from datetime import datetime
from pprint import pprint
from termcolor import cprint
import click
import netmiko
from pynet_annek import sqlitenet


@click.group()
def main():
    """
    Pynet is a cli tool for managing network devices. Command is a required argument. 
    Use --help to get a list of each command's options.

    Example: pynet more-help --help
    """


@main.command()
@click.option("--csvex", is_flag=True, help="Example csv")
@click.option("--helptext", is_flag=True, help="Print extra help")
def more_help(helptext, csvex):
    """ Various help options for usage information """
    result = "Use --help to view usage"
    if csvex:
        result = print_csv()
    elif helptext:
        result = print_more_help()
    print(result)


@main.command()
@click.argument("filename", type=click.Path(exists=True))
def import_devices(filename):
    """ Imports a csv of devices to the sqlite database

    FILENAME is the file to import. See the more-help command for an example
    """
    records = import_file(filename)
    sqlitenet.populate_db(records)


@main.command("create-database", short_help="Creates a new database")
@click.option("--dbname", help="Provide a custom name for the database")
def create_database(dbname):
    """ Creates a new database for storing devices """
    if dbname is None:
        dbname = 'devices.db'
    sqlitenet.create_db(dbname)


@main.command("backup-database", short_help="Backs up the current database")
@click.option(
    "--dbname",
    default="devices.db",
    help="Provide a custom name for the database to be backed up.",
)
def backup_database(dbname):
    """ Backs up the database of devices, creates a copy with today's date """
    sqlitenet.backup_db(dbname)


@main.command("find-device", short_help="Find a device in the database")
@click.argument("hostname")
@click.option(
    "--dbname",
    default="devices.db",
    help="Provide a custom name for the database to search.",
)
def find_device(hostname, dbname):
    """ Searches the database for device(s) with provided string in
    hostname.
    """
    results = sqlitenet.get_list_devices_by_hostname(hostname, dbname)
    print("Returning fields IP, Hostname, and Last_Seen for found records")
    pprint(results)


@main.command("get-device", short_help="Get all fields for a specfic device record")
@click.argument("ip-address")
@click.option(
    "--dbname",
    default="devices.db",
    help="Provide a custom name for the database to search.",
)
def get_device(ip_address, dbname):
    """ Gets all fields for a particular network device """
    results = sqlitenet.get_device_from_db(ip_address, dbname)
    pprint(results)


@main.command("update-device-info", short_help="Updates info for a specific device")
@click.argument("ip-address")
@click.option("--dbname", default="devices.db", help="Provide a custom name for the databse")
def update_device_info(ip_address, dbname):
    """ Update the version info in the db for device """
    print("")
    print("")
    cprint("***************************************", "yellow")
    print(f"Attempting to connect with device {ip_address}")
    device = sqlitenet.get_device_from_db(ip_address, database_name=dbname)
    device_inst = create_device_instance(device)
    print(f"Hostname for device is {device_inst.hostname}")
    try:
        device_inst.update_version()
        cprint("=========================================", "green")
        print(f"Updating version info in db for {ip_address}")
        device_inst.update_running_config()
        cprint("=========================================", "green")
        print(f"Updating running config info in db for {ip_address}")
        device_inst.update_flash_info()
        cprint("=========================================", "green")
        print(f"Updating flash information in db for {ip_address}")
    except EOFError as eof_err:
        print(f"Received EOF error, {eof_err}")
    except TypeError as err:
        cprint("-----------------------------------------", "red")
        print(f"Trouble connecting to {ip_address}, {err}")


@main.command("add-new-device", short_help="Add a single device to the database")
@click.argument("ip-address")
@click.argument("username")
@click.argument("password")
@click.argument("device-type")
@click.option(
    "--dbname", default="devices.db", help="Provide a custom name for the database."
)
@click.option("--hostname", default="", help="Provide a hostname.")
@click.option("--description", default="", help="Provide a description")
@click.option("--building", default="", help="Provide a building")
@click.option("--location", default="", help="Provide a location")
def add_new_device(
    ip_address,
    username,
    password,
    device_type,
    hostname,
    dbname,
    description,
    building,
    location,
):
    """ Add a single device to the database """
    device_info = {
        "ip": ip_address,
        "username": username,
        "password": password,
        "hostname": hostname,
        "device_type": device_type,
        "description": description,
        "building": building,
        "location": location,
        "last_seen": "",
    }
    sqlitenet.add_device_to_db(device_info, dbname)


@main.command("delete-device", short_help="Delete a single device from the database")
@click.argument("ip-address")
@click.option(
    "--dbname", default="devices.db", help="Provide a custom name for the database."
    )
def delete_device(ip_address, dbname):
    """ Delete a single device from the database """
    sqlitenet.delete_device_from_db(ip_address, dbname)


@main.command("update-all-devices", short_help="Update stored information for all devices")
@click.option(
    "--dbname", default="devices.db", help="Provide a custom name for the database."
    )
@click.pass_context
def update_all_devices(ctx, dbname):
    """ Update version and config info in database for all devices """
    ips = sqlitenet.get_list_of_device_ips(dbname)
    for ip_add in ips:
        ctx.invoke(update_device_info, ip_address=ip_add, dbname=dbname)


@main.command("check-connections", short_help="Check connection for every device in the database")
@click.option(
    "--dbname", default="devices.db", help="Provide a custom name for the database."
    )
def check_connections(dbname):
    """ Checks to see if a connection to the device can be made. """
    ips = sqlitenet.get_list_of_device_ips(dbname)
    for ip_add in ips:
        cprint("***************************************", "yellow")
        print(f"Attempting to connect with device {ip_add}")
        device = sqlitenet.get_device_from_db(ip_add, database_name=dbname)
        device_inst = create_device_instance(device)
        device_inst.get_conn()
        print(f"Updated last seen entry in the database for device {ip_add}.")


@main.command("run-adhoc-cmd", short_help="Run a single command against a device")
@click.argument("ip-address")
@click.argument("command")
@click.option(
    "--dbname", default="devices.db", help="Provide a custom name for the database."
    )
def run_adhoc_cmd(ip_address: str, command: str, dbname: str = "devices.db") -> None:
    """ Run a single command against a device that is in the database """
    device_properties = sqlitenet.get_device_from_db(ip_address, dbname)
    dev = create_device_instance(device_properties)
    conn = dev.get_conn()
    result = run_command(conn, command)
    pprint(result)


@main.command(
    "run-adhoc-cmds", short_help="Run a single command against multiple device"
)
@click.argument("ip-addresses", nargs=-1)
@click.argument("command", nargs=1)
@click.option(
    "--dbname", default="devices.db", help="Provide a custom name for the database."
)
def run_adhoc_cmds(ip_addresses, command, dbname):
    """ Run command against multiple devices

        Example: pynet run-adhoc-cmds 10.1.1.1 10.1.1.2 10.1.1.3 "sh run"
    """
    for ip_address in ip_addresses:
        print(f"Executing command for ip address {ip_address}")
        device_properties = sqlitenet.get_device_from_db(ip_address, dbname)
        dev = create_device_instance(device_properties)
        conn = dev.get_conn()
        result = run_command(conn, command)
        pprint(result)


class Device:
    """ Class definition for network devices """

    def __init__(
        self,
        ip_add,
        hostname,
        description="",
        building="",
        location="",
        username="mike",
        password="password",
        device_type="hp_procurve",
        last_seen="",
        version_info="",
        running_config="",
        flash_info="",
    ):
        self.ip_add = ip_add
        self.hostname = hostname
        self.description = description
        self.building = building
        self.location = location
        self.username = username
        self.password = password
        self.device_type = device_type
        self.last_seen = last_seen
        self.version_info = version_info
        self.running_config = running_config
        self.flash_info = flash_info

    def __repr__(self):
        represent = f'Device(hostname="{self.hostname}",ip="{self.ip_add}",username="{self.username}", \
                    password="{self.password}",device_type="{self.device_type}")'
        return represent

    def __eq__(self, other):
        if not isinstance(other, Device):
            return NotImplemented

        return (
            self.ip_add == other.ip_add
            and self.username == other.username
            and self.password == other.password
            and self.device_type == other.device_type
        )

    def get_conn(self):
        """ Get a ssh connection for instance """
        if self.device_type == "cisco_ios":
            connsec = "enable_password"
        else:
            connsec = self.password
        conn = netmiko.ConnectHandler(
            device_type=self.device_type,
            ip=self.ip_add,
            username=self.username,
            password=self.password,
            secret=connsec,
        )
        self.update_last_seen()
        return conn

    def get_ver(self):
        """ Get version info """
        conn = self.get_conn()
        ver = run_command(conn, "sh ver")
        ver = ver.rstrip("\n")
        return ver

    def get_running_config(self):
        """ Get running config """
        conn = self.get_conn()
        run_config = run_command(conn, "sh run")
        run_config = run_config.rstrip("\n")
        return run_config


    def get_flash_info(self):
        """ Get the flash information """
        conn = self.get_conn()
        flash_info = run_command(conn, "sh flash")
        flash_info = flash_info.rstrip("\n")
        return flash_info

    def update_version(self):
        """ Update the version_info field for db record """
        version = self.get_ver()
        sqlitenet.update_show_version_entry(self.ip_add, version)
        return version

    def update_running_config(self):
        """ Update the running_config field for db record """
        run_config = self.get_running_config()
        sqlitenet.update_running_config_entry(self.ip_add, run_config)
        return run_config

    def update_flash_info(self):
        """ Update the flash info field for db record """
        flash_info = self.get_flash_info()
        sqlitenet.update_flash_info_entry(self.ip_add, flash_info)
        return flash_info

    def update_last_seen(self):
        """ Update the last_seen field for a record in the device db """
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sqlitenet.update_last_seen_entry(self.ip_add, now)


def create_device_instance(args):
    """ Create an instance of the device class """
    try:
        device = Device(*args)
        return device
    except TypeError:
        print(f"Trouble connecting to ip address")
        sys.exit(1)


def run_command(connection, command):
    """ Run a command against the provided connection """
    return connection.send_command(command)


def import_file(filename):
    """ Import a file for parsing, returns a dictionary.

    Args:
        filename: The file that is to be imported.

    Returns: A dictionary containing the values from the csv
    """
    rows = []
    imported = {}
    with open(filename, newline="") as csvfile:
        import_reader = csv.reader(csvfile, delimiter=",", quotechar="|")
        for row in import_reader:
            if (len(row)) != 9 or ("." not in row[0]):
                cprint("Warning", "yellow")
                cprint(
                    "The following row from the file will not be included in the requested operation",
                    "yellow",
                )
                print(f"Invalid row {row}")
            else:
                rows.append(row)
    for row in rows:
        imported[row[0]] = {
            "hostname": row[1],
            "description": row[2],
            "building": row[3],
            "location": row[4],
            "username": row[5],
            "password": row[6],
            "device_type": row[7],
            "last_seen": row[8],
        }
    return imported


def print_csv():
    """ Returns valid CSV example """
    validcsv = """
    Here is an example of some valid csv rows
    Note: A header is not necessary and will be discarded at run time
    Position is fixed!!! Header does not dictate position. 
    Field order must be identical to these rows.
    Script also does not permit additional data. Only the fields listed are permitted.
    --------------------------------------------------------------------------------------------------------
    ip,hostname,description,building,location,username,password,devicetype,last_seen
    10.8.1.1,Admin,,admin,datacenter,username,password,hp_procurve,
    10.8.1.13,Admin-POE-1,,admin,datacenter,username,password,hp_procurve,
    10.8.1.16,Admin-1st-Floor-Conf,,admin,1stfloorconference,username,password,hp_procurve,
    10.8.1.17,Admin-DataCenter-03,,admin,datacenter,username,password,hp_procurve,
    10.8.1.18,Lincoln-01,,lincoln,2ndfloorcloset,username,password,hp_procurve,
    10.10.1.1,RIHS,CoreLayer3Aruba,rihs,,username,password,hp_procurve,
    10.10.1.5,BClosetSwitch1,HPProcurve,rihs,,username,password,hp_procurve,

    """
    return validcsv


def print_more_help():
    """ Prints help message """
    help_text = """
    --------------------------------------------------------------------------------------------------------
    Passwords are not encrypted. The "devicetype" field for a device must match a device type from netmiko.
    Netmiko library information is here. https://github.com/ktbyers/netmiko
    IP addresses must be unique. There should not be two devices in the database with the same management IP.
    Last seen value is updated whenever a connection is made to a device to update version or config
    information that is stored in the database.

    Database configuration for the sqlite database.
    sqlite> pragma table_info(devices);
    0|ip|text|1||0
    1|hostname|text|0||0
    2|description|text|0||0
    3|building|text|0||0
    4|location|text|0||0
    5|username|text|1||0
    6|password|text|1||0
    7|device_type|text|1||0
    8|last_seen|text|0||0
    9|version_info|text|0||0
    10|running_config|text|0||0
    
    """
    return help_text


if __name__ == "__main__":
    main()
