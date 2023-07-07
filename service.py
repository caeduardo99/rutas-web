import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import sys
import os
import subprocess

# Ruta al archivo manage.py de tu proyecto Django
DJANGO_PROJECT_PATH = r'C:\Users\DESA03\Desktop\Desarrollo\Python\rutas_tablet'
# Ruta al archivo de registro (log)
LOG_FILE_PATH = r'C:\Users\DESA03\Desktop\Desarrollo\Python\rutas_tablet\ruru.log'

class DjangoService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'DjangoService'
    _svc_display_name_ = 'Django Service'

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.is_running = True

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.is_running = False

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                             servicemanager.PYS_SERVICE_STARTED,
                             (self._svc_name_, ''))
        self.main()

    def main(self):
        os.chdir(DJANGO_PROJECT_PATH)
        command = [
            os.path.join(DJANGO_PROJECT_PATH, 'venv', 'Scripts', 'python.exe'),
            'manage.py',
            'runserver',
            '0.0.0.0:80'
        ]

        with open(LOG_FILE_PATH, 'a') as log_file:
            process = subprocess.Popen(
                command,
                stdout=log_file,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            process.communicate()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(DjangoService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(DjangoService)
