#!/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from subprocess import Popen
from subprocess import PIPE
import os

def get_scp_back_dir(path):
    return sorted([dir_name for dir_name in os.listdir(path) if dir_name.startswith("scp_backup_from-")])

def get_scp_back_date(path):
    date_list = [file_name.split("-running-config-")[1].split("_")[0] for file_name in os.listdir(path) if "-running-config-" in file_name]
    return sorted(list(set(date_list)))

def get_file_date(f_name):
    date_str = f_name.split()[0].rsplit("-", 1)[-1][0:15]
    return datetime.strptime(date_str, '%Y%m%d_%H%M%S')

def get_file_list(file_dir, start_date, end_date):
    file_list_range = [os.path.join(file_dir, f_name) for f_name in os.listdir(file_dir)
                       if start_date <= get_file_date(f_name) <= end_date]
    return sorted(file_list_range)

def diff(file_path1, file_path2):
    cmd = f"diff --context {file_path1} {file_path2}"
    p = Popen(cmd, shell=True, stdout=PIPE)
    (ret, err) = p.communicate()
    return ret

def select_backup_files(dir_list):
    while True:
        try:
            select_num = int(input(f"비교할 네트워크 장비를 선택해 주세요 [1-{len(dir_list)}]: "))
            if select_num <= 0 or select_num > len(dir_list):
                print("잘못된 선택입니다. 다시 선택해주세요.")
                continue
            return dir_list[select_num - 1]
        except ValueError:
            print("잘못된 입력입니다. 숫자를 입력해주세요.")

def select_backup_date(date_list):
    while True:
        try:
            select_start = int(input(f"시작 기간을 선택하세요 [1-{len(date_list)}]: "))
            select_end = int(input(f"종료 기간을 선택하세요 [{select_start}-{len(date_list)}]: "))
            start_date = datetime.strptime(date_list[select_start - 1] + "_000000", '%Y%m%d_%H%M%S')
            end_date = datetime.strptime(date_list[select_end - 1] + "_235959", '%Y%m%d_%H%M%S')
            return (start_date, end_date)
        except ValueError:
            print("잘못된 입력입니다. 숫자를 입력해주세요.")
        except IndexError:
            print("선택 범위가 잘못되었습니다. 다시 선택해주세요.")

def print_list(prefix, items, item_suffix = ''):
    print(f"*****[ {prefix} ]*****")
    if not items:
        print("\t\t없음\n" + ("*" * 50))
    else:
        for i, item in enumerate(items):
            print(f"\t{i+1}){item}{item_suffix}")
        print("*" * 50 + "\n")

def get_input_data():
    dir_path = "/var/log"
    dir_list = get_scp_back_dir(dir_path)
    print_list('백업 파일이 저장된 네트워크 장비 목록', [dir_name.split("scp_backup_from-")[1] for dir_name in dir_list])

    if not dir_list:
        return None

    selected_backup = select_backup_files(dir_list)
    dir_path = os.path.join(dir_path, selected_backup)
    print(f">>> {selected_backup.split('scp_backup_from-')[1]}가 선택되었습니다")

    date_list = get_scp_back_date(dir_path)
    print_list('백업 파일이 저장된 날짜 목록', date_list)

    if not date_list:
        return None

    print("\n선택한 기간 동안의 백업 파일을 비교합니다.")
    start_date, end_date = select_backup_date(date_list)
    return (dir_path, start_date, end_date)

def main():
    input_data = get_input_data()

    if input_data is not None:
        (dir_path, start_date, end_date) = input_data
        scp_file_list = get_file_list(dir_path, start_date, end_date)
        if not scp_file_list:
            print("선택한 기간 동안 백업된 파일이 없습니다.")
        elif len(scp_file_list) == 1:
            print("선택한 기간 동안 백업된 파일이 1건이어서 변경 사항을 비교할 수 없습니다.")
        else:
            for i in range(len(scp_file_list) - 1):
                cmd_result = diff(scp_file_list[i], scp_file_list[i + 1])
                print(cmd_result)
                print("=" * 50)

if __name__ == "__main__":
    main()
