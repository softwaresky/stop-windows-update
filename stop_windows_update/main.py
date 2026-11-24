import logging
import logging.config
import sys
import servicemanager
import win32serviceutil

from stop_windows_update.core.config.logger import get_logging_config
from stop_windows_update.service_stop_windows_update import ServiceStopWindowsUpdates

logging.config.dictConfig(get_logging_config())

logger = logging.getLogger()

if __name__ == "__main__":
    try:
        if len(sys.argv) == 1:
            servicemanager.Initialize()
            servicemanager.PrepareToHostSingle(ServiceStopWindowsUpdates)
            servicemanager.StartServiceCtrlDispatcher()
        else:
            win32serviceutil.HandleCommandLine(ServiceStopWindowsUpdates)
    except Exception:
        logger.exception("Fatal error in service entry point.")
        raise
