import pprint
import os
import subprocess
import logging

def execute_command(command=""):

    with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.DEVNULL) as process:
        std_out, std_err = process.communicate()
        return std_out.decode()

def parse_service_output(input_string=""):

    dict_data = {}
    lst_lines = []

    for line_ in input_string.split("\r\n"):
        line_ = line_.strip()
        split_line_ = line_.split(":")
        if len(split_line_) == 2:
            key, value = split_line_
            value = value.strip()
            value = value.replace("  ", " ")
            if " " in value:
                value_1, value_2 = value.split(" ")
                if str(value_1).isdigit():
                    value_1 = int(value_1)
                value = (value_1, value_2)
            dict_data[key.strip()] = value
        else:
            lst_lines.append(line_)

    return " ".join(lst_lines) if "FAILED" in input_string else dict_data

class WinService:

    def __init__(self, service_name=""):
        self.service_name = service_name

    def query(self):
        output = execute_command(f"sc query {self.service_name}")
        return parse_service_output(output)

    def state(self):
        dict_data = self.query()
        return dict_data.get("STATE")

    def start(self):
        output = execute_command(f"sc start {self.service_name}")
        return parse_service_output(output)

    def stop(self):
        output = execute_command(f"sc stop {self.service_name}")
        return parse_service_output(output)

    def __str__(self):
        return " | ".join([f"{key}={value}" for key, value in self.query().items() if isinstance(self.query(), dict)])

def stop_windows_services_update(logger = None, lst_add_services=[]):

    for service_ in list(set(["wuauserv", "WaaSMedicSvc", "LicenseManager"] + lst_add_services)):
        try:
            win_service = WinService(service_)
            if win_service.state()[0] == 4:
                result = win_service.stop()
                if isinstance(result, dict):
                    if logger:
                        logger.info(f"Successfully {service_} stopped. {win_service}")
                else:
                    if logger:
                        logger.error(f"{service_}: {result}")
        except Exception as err:
            if logger:
                logger.error(err)

# def main():
#     logging.basicConfig(
#         filename="c:\\Temp\\stop_windows_updates.log",
#         level=logging.INFO,
#         format='%(asctime)s [%(name)s] %(levelname)s | %(message)s',
#         datefmt='%Y-%m-%d %H:%M:%S',
#     )
#
#     logger = logging.getLogger("StopWindowsUpdatesScripts")
#     stop_windows_services_update(logger)
#
# if __name__ == '__main__':
#     main()