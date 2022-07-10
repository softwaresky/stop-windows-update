import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import time
import sys
import os
import logging
from logging.handlers import TimedRotatingFileHandler
from stop_windows_update import stop_windows_services_update

P_DATA_DIR = os.environ.get("ALLUSERSPROFILE")

# logging.basicConfig(
#     filename=os.path.join(P_DATA_DIR, "stop_windows_updates.log"),
#     level=logging.INFO,
#     format='%(asctime)s [%(name)s] %(levelname)s | %(message)s',
#     datefmt='%Y-%m-%d %H:%M:%S',
# )

## Here we define our formatter
formatter = logging.Formatter(fmt='%(asctime)s [%(name)s] %(levelname)s | %(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')

logHandler = TimedRotatingFileHandler(os.path.join(P_DATA_DIR, "stop_windows_updates.log"),
                                      when='D',
                                      interval=15,
                                      backupCount=8)
logHandler.setLevel(logging.INFO)
logHandler.setFormatter(formatter)

logger = logging.getLogger("StopWindowsUpdates")
logger.setLevel(logging.INFO)
logger.addHandler(logHandler)

class StopWindowsUpdates(win32serviceutil.ServiceFramework):
    _svc_name_ = "StopWindowsUpdates"
    _svc_display_name_ = "Stop Windows Updates"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.stop_requested = False
        self.lst_args = list(args)[1:] if args else []


    def SvcStop(self):
        logger.info('Stopping service ...')
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        self.stop_requested = True

    def SvcDoRun(self):
        logger.info("Start service ...")

        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )
        self.main()

    def main(self):
        while not self.stop_requested:
            try:
                stop_windows_services_update(logger=logger, lst_add_services=self.lst_args)
            except Exception as err:
                logger.error(err)

            time.sleep(60)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(StopWindowsUpdates)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(StopWindowsUpdates)

# pyinstaller -F --hidden-import=win32timezone service_stop_windows_update.py