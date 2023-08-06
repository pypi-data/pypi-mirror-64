"""
vbiz_parser.py
"""

import os
import subprocess
import json
import sys
import getopt
import pkg_resources
import requests

TEMP_FILE = '/tmp/vbiz_parser_tmp.txt'


def let_parse(input_file, output_file, upload_path):
    """let_parse"""

    ciddict_file = 'ciddict.json'
    ciddict_filepath = pkg_resources.resource_filename(__name__, ciddict_file)
    with open(ciddict_filepath) as json_file:
        ciddict = json.load(json_file)

    if input_file:
        parse_a_file(input_file, ciddict, output_file, upload_path)
    else:
        for input_file in os.listdir('.'):
            parse_a_file(input_file, ciddict, output_file, upload_path)


def parse_a_file(filename, ciddict, output_file, upload_path):
    file_name, file_ext = os.path.splitext(filename)
    del file_name
    if file_ext == '.pdf':
        print('📂 %s' % (filename))
        subprocess.check_output(['pdf2txt.py', '-o', TEMP_FILE, filename])
        _f = open(TEMP_FILE, 'r')
        inputs = _f.readlines()
        result = solution(inputs, ciddict)

        if result:
            if output_file or upload_path:
                if output_file:
                    write_to_file(result, output_file)
                if upload_path:
                    upload_to_path(result, upload_path)
            else:
                print(result)

        _f.close()


def write_to_file(result, output_file):
    result_file = open(output_file, "w")
    result_file_delimeter = ';'
    result_file.write('biz_name' + result_file_delimeter + 'biz_code' +
                      result_file_delimeter + 'biz_register_date' +
                      result_file_delimeter + 'biz_phone' +
                      result_file_delimeter + 'biz_email' +
                      result_file_delimeter + 'biz_category_id' +
                      result_file_delimeter + 'biz_address' + '\n')
    str_line = result_file_delimeter.join(map(str, result))
    result_file.write(str_line + '\n')
    result_file.close()


def upload_to_path(result, upload_path):
    post_data = {
        "vbiz_address": result[6],
        "vbiz_category_id": result[5],
        "vbiz_code": result[1],
        "vbiz_email": result[4],
        "vbiz_name": result[0],
        "vbiz_phone": result[3],
        "vbiz_register_date": result[2]
    }
    post_vbiz(upload_path, post_data)


def post_vbiz(post_url, post_data):
    """post_vbiz"""
    response = requests.post(post_url, json=post_data)
    print(response.status_code)


def solution(arr, ciddict):
    """solution"""
    address_key = (
        '(cid:264)(cid:1231)(cid:68)(cid:3)(cid:70)(cid:75)(cid:1229)(cid:3)'
        '(cid:87)(cid:85)(cid:1257)(cid:3)(cid:86)(cid:1251)(cid:3)(cid:70)'
        '(cid:75)(cid:116)(cid:81)(cid:75)')
    phone_key = ('(cid:264)(cid:76)(cid:1227)(cid:81)(cid:3)(cid:87)(cid:75)'
                 '(cid:82)(cid:1189)(cid:76)(cid:29)')
    name_key = ('(cid:69)(cid:1205)(cid:81)(cid:74)(cid:3)'
                '(cid:87)(cid:76)(cid:1219)(cid:81)(cid:74)(cid:3)'
                '(cid:57)(cid:76)(cid:1227)(cid:87)(cid:29)(cid:3)')
    name_2_key = ('(cid:69)(cid:1205)(cid:81)(cid:74)(cid:3)'
                  '(cid:87)(cid:76)(cid:1219)(cid:81)(cid:74)(cid:3)'
                  '(cid:81)(cid:1133)(cid:1247)(cid:70)(cid:3)'
                  '(cid:81)(cid:74)(cid:82)(cid:106)(cid:76)(cid:29)(cid:3)')
    email_key = '@'
    category_key = '(Chính)'
    primary_key = ('STT')
    results = []
    biz_name = ''
    biz_code = ''
    biz_register_date = ''
    biz_address = ''
    biz_phone = ''
    biz_email = ''
    biz_category_id = ''
    next_address = False
    next_name = False
    primary_zone = True
    for i, line in enumerate(arr):
        del i
        line = line.replace('\n', '')
        if primary_key in line:
            primary_zone = False

        # if i == 0:
        #     biz_name = parse_cid_2_text(ciddict, line)

        if primary_zone and name_key in line:
            line = line[line.index(name_key):]
            # biz_name = parse_cid_2_text(ciddict, line.replace(name_key, ''))
            next_name = True

        if primary_zone and name_2_key in line:
            next_name = False

        if next_name:
            biz_name += parse_cid_2_text(ciddict, line.replace(name_key, ''))

        if primary_zone and address_key in line:
            next_address = True
            continue

        if primary_zone and phone_key in line:
            next_address = False
            biz_phone = line.replace(phone_key, '')
            biz_phone = biz_phone.replace(';', '-')
            biz_phone = biz_phone.replace('.', '')
            biz_phone = biz_phone.replace(' ', '')

        if next_address:
            biz_address += parse_cid_2_text(ciddict, line.replace('\n', ''))

        if primary_zone and email_key in line:
            biz_email = line
            if '@gmail' in biz_email:
                biz_email = biz_email.split("@gmail", 1)[0] + '@gmail.com'

        if primary_zone and 10 <= len(line) < 16 and line.isdigit():
            biz_code = line

        if primary_zone and len(line) == 10 and validate_date(line):
            biz_register_date = line

        if category_key in line:
            biz_category_id = line.replace(category_key, '')

    # print(biz_code, biz_register_date)
    results.extend([
        biz_name, biz_code, biz_register_date, biz_phone, biz_email,
        biz_category_id, biz_address
    ])

    return results


def parse_cid_2_text(ciddict, cid):
    """parse_cid_2_text"""
    for key in ciddict.keys():
        cid = cid.replace(key, ciddict[key])
    return cid


def validate_date(date_text):
    """validate_date"""
    from dateutil import parser

    try:
        parser.parse(date_text)
        return True
    except:  # pylint: disable=W
        return False
