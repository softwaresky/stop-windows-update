# stop-windows-update

Service for stopping Windows service(s) :)

## Instruction
### Build Windows Service
1. Execute following command:
```pyinstaller  service_stop_windows_update.spec```
1. Copy from **dist/service_stop_windows_update.exe** to location that your service(s) live

### Install Windows Service
1. Open terminal with Run As Administrator
2. Change directory/navigate to **service_stop_windows_update.exe** and execute the following command: 
```service_stop_windows_update.exe --startup delayed install```

The logs from this service locate in %ALLUSERSPROFILE%/stop_windows_updates.log

## Example
### With Administrator privilges
### Install:
dist\myservice.exe install

### Start:
dist\myservice.exe start

### Install with autostart:
dist\myservice.exe --startup delayed install

### Debug:
dist\myservice.exe debug

### Stop:
dist\myservice.exe stop

### Uninstall:
dist\myservice.exe remove
