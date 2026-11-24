# Stop Windows Updates Service

A lightweight Windows service written in Python (`pywin32`) that runs in the background and periodically stops Windows Update–related services (`BITS`, `wisvc`, `wuauserv`, and `UsoSvc`).

## Requirements

* Windows (Administrator privileges required to install/manage services)
* Python 3.10+
* `pywin32`
* `pyinstaller`

## Installation

Install Python dependencies from the project root:

```cmd
pip install -U -r .\requirements\stop_windows_update.txt
```

## Build

Compile the service executable using `build_service.py`, which invokes PyInstaller with `service_stop_windows_update.spec`:

```bash
python build_service.py
```

The built binary will be output to the `dist/` directory (`service_stop_windows_update.exe`).

## Usage (Run as Administrator)

### Debug in Console

```cmd
service_stop_windows_update.exe debug
```

### Install & Start Service

```cmd
service_stop_windows_update.exe --startup auto install
service_stop_windows_update.exe start
```

### Stop & Remove Service

```cmd
service_stop_windows_update.exe stop
service_stop_windows_update.exe remove
```

## Logs

Service logs are written with 15-day rotation to:

```text
C:\ProgramData\stop_windows_updates.log
```