import win32serviceutil
import win32service
import win32event
import win32con
import servicemanager
import socket
import time
import sys
import os
import tempfile
import logging

from stop_windows_update import stop_windows_services_update

logging.basicConfig(
    filename="c:\\Temp\\stop_windows_updates.log",
    level=logging.INFO,
    format='%(asctime)s [%(name)s] %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

logger = logging.getLogger("StopWindowsUpdates")

class StopWindowsUpdates(win32serviceutil.ServiceFramework):
    _svc_name_ = "StopWindowsUpdates"
    _svc_display_name_ = "Stop Windows Updates"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.stop_requested = False

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
                stop_windows_services_update(logger=logger)
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