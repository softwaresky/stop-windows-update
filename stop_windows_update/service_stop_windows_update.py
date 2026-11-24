import logging
import threading
import time
import win32event
import win32service
import win32serviceutil

from stop_windows_update.core.windows_handlers import WinServiceManager

TARGET_SERVICES = [
    "BITS",
    "wisvc",
    "wuauserv",
    "UsoSvc",
]
POLL_INTERVAL_SECONDS = 10.0

logger = logging.getLogger(__name__)


class ServiceStopWindowsUpdates(win32serviceutil.ServiceFramework):
    _svc_name_ = "StopWindowsUpdates"
    _svc_display_name_ = "Stop Windows Updates"
    _svc_description_ = "Periodically checks target Windows services and stops running ones."

    def __init__(self, args):
        super().__init__(args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self._stop_event = threading.Event()

    def SvcStop(self):
        logger.info("Stop signal received from SCM.")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self._stop_event.set()
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        logger.info("Service started (interval=%.1fs, targets=%s)", POLL_INTERVAL_SECONDS, TARGET_SERVICES)
        try:
            while not self._stop_event.is_set():
                started = time.monotonic()
                try:
                    with WinServiceManager() as manager:
                        for svc_name in TARGET_SERVICES:
                            manager.stop_if_running(svc_name)
                except Exception:
                    logger.exception("Error during service polling cycle.")

                elapsed = time.monotonic() - started
                remaining = max(0.0, POLL_INTERVAL_SECONDS - elapsed)
                self._stop_event.wait(timeout=remaining)
        finally:
            logger.info("Service loop exited cleanly.")


