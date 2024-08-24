#!/usr/bin/env python3

'''module: dataLoader'''

import psutil
import os
from cryptography.fernet import Fernet

data_path = '../data/data.cpmpd'                           # load data path
platform_path = '../data/platform.cpmpd'

def check_data_file():
    global data_path
    global platform_path

    if not os.path.exists(data_path):
        data_path = 'data/data.cpmpd'
        platform_path = 'data/platform.cpmpd'
        
        if not os.path.exists(data_path):
            return False
    return True

def check_key_connection():                                # check if key is connected and return mount point
    for partition in psutil.disk_partitions():
        if 'removable' in partition.opts:
            if os.path.exists(partition.mountpoint + 'derypt.cdk'):
                return partition.mountpoint
    return False

def check_connected_usb():
    usb_list = []
    for patrition in psutil.disk_partitions():
        if 'removable' in patrition.opts:
            usb_list.append(patrition.mountpoint)
    if usb_list:
        return usb_list
    else:
        return False

class DataManagement():
    def __init__(self):

        self.load_from_files()
    
    def load_from_files(self):

        with open(data_path, 'rb') as file:
            self.data = file.read().split(b'\n')    #data (crypted)

        with open(platform_path, 'r') as file:
            self.platform_list = file.read().split('\n')    #platform list

    def get_key(self):
        if check_key_connection():
            key_path = check_key_connection() + 'derypt.cdk'
            with open(key_path, 'rb') as file:
                return file.read()    #key
        else:
            return False
        
    def remove_record(self, id):
        self.data.pop(id)
        self.platform_list.pop(id)

        temp_data = b'\n'.join(self.data)
        temp_platforms = '\n'.join(self.platform_list)

        with open(data_path, 'wb') as file:
            file.write(temp_data)
        with open(platform_path, 'w') as file:
            file.write(temp_platforms)

    def edit_record(self, id, record):
        temp_record = ';'.join(record).encode()
        
        key = self.get_key()
        cipher_suite = Fernet(key)

        temp_record = cipher_suite.encrypt(temp_record)

        self.data[id] = temp_record
        temp_data = b'\n'.join(self.data)

        with open(data_path, 'wb') as file:
            file.write(temp_data)

        del key
        del cipher_suite
        del record

    def add_record(self, record):
        with open(platform_path, 'r') as file:
            beg = file.readline()
        if beg:
            beg = '\n'

        key = self.get_key()
        cipher_table = Fernet(key)

        encrypted_record = ';'.join(record).encode()
        encrypted_record = cipher_table.encrypt(encrypted_record)

        with open(platform_path, 'a') as file:
            file.write(beg + record[0])

        with open(data_path, 'ab') as file:
            file.write(beg.encode() + encrypted_record)

        self.load_from_files()

        del key
        del cipher_table
        del record

    def show_by_id(self, id):
        key = self.get_key()
        cipher_table = Fernet(key)

        result = cipher_table.decrypt(self.data[id])
        result = result.decode().split(';')

        del key
        del cipher_table

        return result
        
    def show_active(self, active_platform):
        
        decrypted = []

        key = self.get_key()
        cipher_table = Fernet(key)

        for i, platform in enumerate(self.platform_list):
            if platform in active_platform:
                temp_record = cipher_table.decrypt(self.data[i]).decode()
                temp_record = temp_record.split(';')
                decrypted.append(temp_record)

        del key
        del cipher_table
        del temp_record

        return decrypted

    def count_records(self, active_platform):
        counter = 0
        if self.platform_list[0]:
            for platform in self.platform_list:
                if platform in active_platform:
                    counter += 1
        return counter
    
    def show_all(self):
        
        if len(self.data) == 0:
            return False
        else:
            decrypted = []

            key = self.get_key()
            cipher_table = Fernet(key)

            for record in self.data:
                temp_record = cipher_table.decrypt(record).decode()
                temp_record = temp_record.split(';')
                temp_record = temp_record[:2]
                decrypted.append(temp_record)

            del temp_record
            del key
            del cipher_table

            return decrypted