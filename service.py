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
    _svc_name_ = 'DjangoService' # Nombre del Servicio que se va a crear.
    _svc_display_name_ = 'Django Service' # Descripcion del Servicio que se va a crear.

    def __init__(self, args):
        """
        Inicializa el servicio de Django.

        Args:
        args (list): Argumentos pasados al servicio.
        """
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.is_running = True

    def SvcStop(self):
        """
        Detiene el servicio de Django.
        """
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.is_running = False

    def SvcDoRun(self):
        """
        Punto de entrada principal del servicio de Django.
        """
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                             servicemanager.PYS_SERVICE_STARTED,
                             (self._svc_name_, ''))
        self.main()

    def main(self):
        """
        Método principal que ejecuta el servidor de desarrollo de Django.
        """
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
        """
        Si no se pasan argumentos en la línea de comandos,
        se inicia el administrador de servicios y se prepara
        para alojar el servicio DjangoService.
        """
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(DjangoService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        """
        Si se pasan argumentos en la línea de comandos,
        se utiliza win32serviceutil.HandleCommandLine para
        manejar los comandos específicos del servicio.
        """
        win32serviceutil.HandleCommandLine(DjangoService)

