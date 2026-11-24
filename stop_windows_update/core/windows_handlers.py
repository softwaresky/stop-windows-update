import logging
from typing import Any
import pywintypes
import win32service
import win32con

DESIRED_ACCESS = win32service.SERVICE_QUERY_STATUS | win32service.SERVICE_STOP

logger = logging.getLogger(__name__)

SERVICE_STATE_NAMES = {
    win32service.SERVICE_STOPPED: "stopped",
    win32service.SERVICE_START_PENDING: "start_pending",
    win32service.SERVICE_STOP_PENDING: "stop_pending",
    win32service.SERVICE_RUNNING: "running",
    win32service.SERVICE_CONTINUE_PENDING: "continue_pending",
    win32service.SERVICE_PAUSE_PENDING: "pause_pending",
    win32service.SERVICE_PAUSED: "paused",
}

CONTROL_CODE_NAMES = {
    win32service.SERVICE_CONTROL_STOP: "stop",
    win32service.SERVICE_CONTROL_PAUSE: "pause",
    win32service.SERVICE_CONTROL_CONTINUE: "continue",
    win32service.SERVICE_CONTROL_INTERROGATE: "interrogate",
}


class WinServiceHandler:

    def __init__(self, win_manager: Any, service_name: str):
        self._win_manager = win_manager
        self._service_name = service_name
        self._service_handle = None

    def __enter__(self):
        self._create_service()
        return self

    def __exit__(self, *args, **kwargs):
        self.close_service()

    @property
    def is_open(self) -> bool:
        return self._service_handle is not None

    def _create_service(self):
        try:
            self._service_handle = win32service.OpenService(
                self._win_manager, self._service_name, DESIRED_ACCESS
            )
        except pywintypes.error as err:
            logging.warning("%s: cannot open service (%s)", self._service_name, err.strerror)

    def close_service(self):
        if self._service_handle is not None:
            try:
                win32service.CloseServiceHandle(self._service_handle)
            finally:
                self._service_handle = None

    @property
    def status(self) -> int | None:
        if not self.is_open:
            return None
        try:
            return win32service.QueryServiceStatus(self._service_handle)[1]
        except pywintypes.error as err:
            logger.warning("%s: failed to query status (%s)", self._service_name, err.strerror)
            return None

    def change_status(self, control: int = win32service.SERVICE_CONTROL_STOP) -> bool:
        if not self.is_open:
            return False

        current_state = self.status
        if current_state is None:
            return False

        old_label = SERVICE_STATE_NAMES.get(current_state, f"unknown({current_state})")
        action_label = CONTROL_CODE_NAMES.get(control, f"control({control})")

        try:
            win32service.ControlService(self._service_handle, control)
            logger.info("%s: %s -> sent %s", self._service_name, old_label, action_label)
            return True
        except pywintypes.error as err:
            logger.warning("%s: failed to send %s (%s)", self._service_name, action_label, err.strerror)
            return False


class WinServiceManager:

    def __init__(self):
        self._win_manager: Any = None

    def __enter__(self):
        self._create_manager()
        return self

    def __exit__(self, *args, **kwargs):
        self.close_manager()

    def _create_manager(self):
        if not self._win_manager:
            self._win_manager = win32service.OpenSCManager(None, None, win32con.GENERIC_READ)

    def close_manager(self):
        if self._win_manager is not None:
            try:
                win32service.CloseServiceHandle(self._win_manager)
            finally:
                self._win_manager = None

    def stop_if_running(self, service_name: str) -> bool:
        with WinServiceHandler(self._win_manager, service_name) as service:
            if not service.is_open:
                return False
            if service.status == win32service.SERVICE_RUNNING:
                return service.change_status(control=win32service.SERVICE_CONTROL_STOP)

        return False
