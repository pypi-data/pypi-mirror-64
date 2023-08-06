""" Import statements """
import sqlite3
import datetime
from shutil import copyfile


def backup_db(database_name="devices.db"):
    """ Backup the current devices.db sqlite3 db file """
    now = datetime.datetime.now().strftime("%m.%d.%Y_%H.%M.%S")
    new_filename = now + "_" + database_name
    copyfile(database_name, new_filename)


def create_db(database_name="devices.db"):
    """ Create a database and a devices table

    Args:
        database_name: Name of the database
        tablename: Name of the table

    Returns: None
    """
    sql_create_devices_table = """ CREATE TABLE IF NOT EXISTS devices (
        ip text NOT NULL,
        hostname text,
        description text,
        building text,
        location text,
        username text NOT NULL,
        password text NOT NULL,
        device_type text NOT NULL,
        last_seen text,
        version_info text,
        running_config text,
        flash_info text
        ); """
    conn = sqlite3.connect(database_name)
    curs = conn.cursor()
    curs.execute(sql_create_devices_table)
    conn.commit()
    conn.close()


def get_list_of_device_ips(database_name="devices.db"):
    """ Get a list of every IP address in the db """
    conn = sqlite3.connect(database_name)
    conn.row_factory = lambda cursor, row: row[0]
    curs = conn.cursor()
    curs.execute("Select ip from devices;")
    ipadds = curs.fetchall()
    ipadds = sorted(set(ipadds))
    return ipadds


def get_list_devices_by_hostname(search_string, database_name="devices.db"):
    """ Get a list of devices that have search_string in the host name """
    conn = sqlite3.connect(database_name)
    curs = conn.cursor()
    search_string = search_string + "%"
    curs.execute(
        "SELECT ip,hostname,last_seen FROM devices WHERE hostname LIKE ?",
        (search_string,),
    )
    rows = sorted(curs.fetchall())
    return rows


def get_device_from_db(ip_add, database_name="devices.db"):
    """ Get record(s) from db that are for a particular device """
    conn = sqlite3.connect(database_name)
    curs = conn.cursor()
    curs.execute("SELECT * from devices where ip=?", (ip_add,))
    rows = curs.fetchone()
    return rows


def update_last_seen_entry(ip_add, time_stamp, database_name="devices.db"):
    """ Update device's record last_seen entry """
    conn = sqlite3.connect(database_name)
    curs = conn.cursor()
    update_query = """Update devices set last_seen = ? where ip = ?"""
    data = (time_stamp, ip_add)
    curs.execute(update_query, data)
    conn.commit()
    curs.close()


def update_show_version_entry(ip_add, ver_info, database_name="devices.db"):
    """ Update device's version information in db record """
    conn = sqlite3.connect(database_name)
    curs = conn.cursor()
    update_query = """Update devices set version_info = ? where ip = ?"""
    data = (ver_info, ip_add)
    curs.execute(update_query, data)
    conn.commit()
    curs.close()


def update_running_config_entry(ip_add, running_config, database_name="devices.db"):
    """ Update the device's running config in the db record """
    conn = sqlite3.connect(database_name)
    curs = conn.cursor()
    update_query = """Update devices set running_config = ? where ip = ?"""
    data = (running_config, ip_add)
    curs.execute(update_query, data)
    conn.commit()
    curs.close()


def update_flash_info_entry(ip_add, flash_info, database_name="devices.db"):
    """ Update the device's flash information in the db record """
    conn = sqlite3.connect(database_name)
    curs = conn.cursor()
    update_query = """Update devices set flash_info = ? where ip = ?"""
    data = (flash_info, ip_add)
    curs.execute(update_query, data)
    conn.commit()
    curs.close()


def populate_db(value_dictionary, database_name="devices.db"):
    """ Function for inserting dictionary into a sqlite database

    Args:
        value_dictionary: Dictionary to be added
        table_name: Table to be populated
        database_name: Database that contains table

    Returns: A database object
    """
    keylist = []
    for key in value_dictionary.keys():
        keylist.append(key)
    conn = sqlite3.connect(database_name)
    curs = conn.cursor()
    for key in keylist:
        query_with_param = """INSERT INTO devices (ip, hostname, description, building, location, username, password, device_type, last_seen)
                    VALUES (?,?,?,?,?,?,?,?,?)"""
        data_tuple = (
            key,
            value_dictionary[key]["hostname"],
            value_dictionary[key]["description"],
            value_dictionary[key]["building"],
            value_dictionary[key]["location"],
            value_dictionary[key]["username"],
            value_dictionary[key]["password"],
            value_dictionary[key]["device_type"],
            value_dictionary[key]["last_seen"],
        )
        curs.execute(query_with_param, data_tuple)
    conn.commit()
    conn.close()


def check_devices_table_exists(database_name: str = 'devices.db') -> bool:
    """ Check for devices table """
    conn = sqlite3.connect(database_name)
    curs = conn.cursor()
    query_tables = """ SELECT count(name) from sqlite_master WHERE type='table' and name='devices' """
    curs.execute(query_tables)
    exists = bool(curs.fetchone()[0] == 1)
    conn.commit()
    conn.close()
    return exists


def add_device_to_db(device_info: dict, database_name: str = "devices.db") -> None:
    """ Adds a device to the database """
    conn = sqlite3.connect(database_name)
    curs = conn.cursor()
    query_with_param = """INSERT INTO devices (ip, hostname, description, building, location, username, password, device_type, last_seen)
                    VALUES (?,?,?,?,?,?,?,?,?)"""
    data_tuple = (
        device_info["ip"],
        device_info["hostname"],
        device_info["description"],
        device_info["building"],
        device_info["location"],
        device_info["username"],
        device_info["password"],
        device_info["device_type"],
        device_info["last_seen"],
    )
    if not check_devices_table_exists():
        create_db(database_name)
    curs.execute(query_with_param, data_tuple)
    conn.commit()
    conn.close()


def delete_device_from_db(ip_address: str, database_name: str = "devices.db") -> None:
    """ Deletes a device from the database """
    conn = sqlite3.connect(database_name)
    curs = conn.cursor()
    query_with_parm = "DELETE from devices where ip=?"
    curs.execute(query_with_parm, (ip_address,))
    conn.commit()
    conn.close()
