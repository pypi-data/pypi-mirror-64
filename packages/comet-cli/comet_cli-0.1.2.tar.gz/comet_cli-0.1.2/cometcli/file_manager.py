#!/usr/bin/env python3

from cometcli.utils import *
import os
import requests


@daemon_check
def add_dataset(file_path):
    try:
        config = get_comet_config()
        api = config.get('api_url')
        if os.path.exists(file_path) is not True:
            print('> File not found')
            exit(1)
        file_name = file_path.split('/')[-1]
        with open(file_path, 'r') as data_file:
            content = data_file.read()
        payload = {'name': file_name, 'content': content}
        response = requests.post(api+'/dataset', json=payload)
        if response.status_code == 200:
            print('> File added to comet')
        else:
            print('> Failed to add file to comet')
    except Exception as e:
        print('> Failed to add file to comet : '+str(e))


@daemon_check
def remove_dataset(file_name):
    try:
        config = get_comet_config()
        api = config.get('api_url')
        payload = {'name': file_name}
        response = requests.delete(api+'/dataset', json=payload)
        if response.status_code == 200:
            print('> Deleted file from Comet')
        else:
            print('> Failed to delete file from comet')
    except Exception as e:
        print('> Failed to remove dataset :'+str(e))


@daemon_check
def list_datasets():
    try:
        config = get_comet_config()
        api = config.get('api_url')
        response = requests.get(api+'/dataset')
        data = response.json()['data']
        print_table(data)
    except Exception as e:
        print('> Failed to get files : '+str(e))


def print_table(data):
    if data:
        print('\n')
        columns = list(data[0].keys())
        column_string = '\t'.join(columns)
        content_string = ''
        for each in data:
            for key, value in each.items():
                content_string += str(value)+'\t'
            content_string += '\n'
        print(column_string+'\n')
        print(content_string)
    else:
        print('> No files added to comet')
