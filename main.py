"""
test
"""

import os
import csv

from datetime import datetime

import psutil
import pandas as pd


class AppTracker:
    '''
    app tracker class
    '''
    def __init__(self) -> None:
        self.state = None
        self.process_name = None
        self.current_user = os.getlogin()
        self.log_path = "./logs"
        self.csv_file_name = "data.csv"
        self.columns = ['year', 'month', 'day', 'hour', 'minute', 'second', 'process', 'state', 'user']

        if not os.path.isdir(self.log_path):
            os.makedirs(self.log_path)

        self.csv_file_full_path = os.path.join(self.log_path, self.csv_file_name)

    def set_process_name(self, process_name):
        '''
        set process name
        '''
        self.process_name = process_name

    def get_state_from_csv_file(self):
        '''
        get latest state from csv file
        '''

        # return None if data file does not exist
        if not os.path.isfile(self.csv_file_full_path):
            return None

        dataframe = pd.read_csv(self.csv_file_full_path, header=None, names=self.columns)

        # return None if dataframe is empty
        if len(dataframe) == 0:
            return None

        # Get last row
        last_state = None

        for i in range(len(dataframe)-1, -1, -1):

            last_update = dataframe.iloc[i]

            if last_update['process'] == self.process_name:
                last_state = bool(last_update['state'])
                return last_state

        return last_state

    def set_log_path(self, path: str):
        '''
        set log path
        '''
        self.log_path = path

    def check_if_process_running(self):
        '''
        Check if there is any running process that contains the given name processName.
        '''
        # Iterate over the all the running process
        for proc in psutil.process_iter():

            try:
                # Check if process name contains the given name string.
                if self.process_name.lower() in proc.name().lower():
                    return True

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        return False

    def log_activity(self):
        '''
        not yet described
        '''
        process_state = self.check_if_process_running()
        last_state = self.get_state_from_csv_file()

        if last_state is None or process_state != last_state:
            print(f"{self.process_name}: Logging new data")
            current_time = datetime.now()

            content_csv = [
                current_time.year,
                current_time.month,
                current_time.day,
                current_time.hour,
                current_time.minute,
                current_time.second,
                self.process_name,
                process_state,
                self.current_user
            ]

            try:
                with open(self.csv_file_full_path, 'a', encoding='utf-8', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(content_csv)

            except FileNotFoundError:
                print("[ERROR]: File not found!")

            except ModuleNotFoundError:
                print("[ERROR]: File not found!")

        else:
            print("Nothing to log")


def main():
    '''
    main loop
    '''

    processes = [
        'messenger.exe',
        'firefox.exe'
    ]

    for process in processes:
        process_tracker = AppTracker()
        process_tracker.set_process_name(process)
        process_tracker.log_activity()

        # del process_tracker


if __name__ == "__main__":
    main()
