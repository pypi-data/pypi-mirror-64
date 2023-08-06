import os, sys
try:
    from setproctitle import setproctitle
except ImportError:
    setproctitle = None

from . import daemon
import time
from .. import pathtool
from ..termcolor import tc
if os.name == "nt":
    import win32serviceutil

class Service:
    def __init__ (self, name, working_dir, lockpath = None, win32service = None):
        self.name = name
        self.working_dir = working_dir
        self.lockpath = lockpath or working_dir
        self.win32service = win32service
        setproctitle and setproctitle (name)
        pathtool.mkdir (working_dir)
        if lockpath:
            pathtool.mkdir (lockpath)
        os.chdir (working_dir)

    def start (self):
        if os.name == "nt":
            set_service_config (['start'])
        else:
            from . import Daemonizer
            if not Daemonizer (self.working_dir, self.name, lockpath = self.lockpath).runAsDaemon ():
                pid = daemon.status (self.lockpath, self.name)
                print ("{} {}".format (tc.debug (self.name), tc.error ("[already running:{}]".format (pid))))
                sys.exit ()

    def stop (self):
        if os.name == "nt":
            set_service_config (['stop'])
        else:
            daemon.kill (self.lockpath, self.name, True)

    def status (self, verbose = True):
        pid = daemon.status (self.lockpath, self.name)
        if verbose:
            if pid:
                print ("{} {}".format (tc.debug (self.name), tc.warn ("[running:{}]".format (pid))))
            else:
                print ("{} {}".format (tc.debug (self.name), tc.secondary ("[stopped]")))
        return pid

    def execute (self, cmd):
        if cmd == "stop":
            self.stop ()
            return False
        elif cmd == "status":
            self.status ()
            return False
        elif cmd == "start":
            self.start ()
        elif cmd == "restart":
            self.stop ()
            time.sleep (2)
            self.start ()
        elif cmd == "install":
            self.install ()
            return False
        elif cmd == "update":
            self.update ()
            return False
        elif cmd == "remove":
            self.remove ()
            return False
        else:
            raise AssertionError ('unknown command: %s' % cmd)

        if os.name == "nt":
            return False
        return True

    if os.name == "nt":
        def set_service_config (self, argv = []):
            argv.insert (0, "")
            script = os.path.join (os.getcwd (), sys.argv [0])
            win32serviceutil.HandleCommandLine(self.win32service, "%s.%s" % (script [:-3], self.win32service.__name__), argv)

        def install (self):
            self.set_service_config (['--startup', 'auto', 'install'])

        def remove (self):
            self.set_service_config (['remove'])

        def update (self):
            self.set_service_config (['update'])

    else:
        def install (self, update = False):
            name = self.name.split ('/')[-1]
            service_script = '/etc/systemd/system/{}.service'.format (name)
            if not update and os.path.exists (service_script):
                raise SystemError ('service {} is already exists. use update command'.format (name))
            user = os.getenv("SUDO_USER") or 'nobody'
            args = sys.argv [1:]
            if args and hasattr (self, args [-1]):
                args = args [:-1]

            if self.name == 'skitai/smtpda':
                import skitai
                serve = os.path.join (os.path.dirname (skitai.__file__), 'scripts', 'commands', 'smtpda.py')
            else:
                serve = os.path.abspath (sys.argv [0])

            script = SERVICE_TEMPLATE.format (
                name = name.title (),
                user = user,
                executable = sys.executable,
                serve = serve,
                args = " ".join (['"{}"'.format (each) for each in args])
            )
            with open (service_script, 'w') as f:
                f.write (script)
            os.chmod (service_script, 0o755)

            os.system ("systemctl daemon-reload")
            os.system ("systemctl enable {}".format (name))
            print ("service {} installed".format (name))
            print ("  sudo systemctl start {}".format (name))

        def remove (self):
            name = self.name.split ('/')[-1]
            service_script = '/etc/systemd/system/{}.service'.format (name)
            if not os.path.exists (service_script):
                return
            os.remove (service_script)

        def update (self):
            self.install (True)

    uninstall = remove

SERVICE_TEMPLATE = '''[Unit]
Description=Skitai {name} Service

[Service]
Type=simple
User={user}
Group={user}
StandardOutput=syslog+console
StandardError=syslog+console
Restart=on-failure
WorkingDirectory=/var/tmp
ExecStart={executable} {serve} {args}
ExecStop=/bin/kill -s TERM $MAINPID
ExecReload=/bin/kill -s HUP $MAINPID

[Install]
WantedBy=multi-user.target
'''

