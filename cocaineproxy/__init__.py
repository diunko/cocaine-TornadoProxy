import atexit
import pwd
import time
import os
import sys
import json
from functools import partial
from signal import SIGTERM

class Daemon(object):

    def __init__(self, pidfile, userid=None, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile
        self.userid = userid

    def daemonize(self):
        """Double-fork magic"""
        if self.userid:
            uid = pwd.getpwnam(self.userid).pw_uid
            os.seteuid(uid)
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError, err:
            sys.stderr.write("First fork failed: %d (%s)\n" % (err.errno, err.strerror))
            sys.exit(1)
        # decouple from parent environment
        os.chdir("/")
        os.setsid()
        os.umask(0)

        # Second fork
        
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError, err:
            sys.stderr.write("Second fork failed: %d (%s)\n" % (err.errno, err.strerror))
            sys.exit(1)
            
        sys.stdout.flush()
        sys.stderr.flush()
        si = file(self.stdin, 'r')
        so = file(self.stdout, 'w')
        se = file(self.stderr, 'w')
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        #write PID file
        atexit.register(self.delpid)
        pid = str(os.getpid())
        file(self.pidfile,'w').write("%s\n" % pid)

    def delpid(self):
        try:
            os.remove(self.pidfile)
        except Exception, err:
            pass

    def start(self, *args):
        """
        Start  the daemon
        """

        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if pid:
            msg = "pidfile %s exists. Exit.\n"
            sys.stderr.write(msg % self.pidfile)
            sys.exit(1)

        self.daemonize()
        self.run(*args)

    def stop(self):
        """
        Stop daemon.
        """
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if not pid:
            msg = "pidfile %s doesn't exist. Exit.\n"
            sys.stderr.write(msg % self.pidfile)
            sys.exit(1)

        #Kill
        try:
            while True:
                os.kill(pid, SIGTERM)
                time.sleep(0.5)
        except OSError, err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
                sys.stdout.write("Process %d stoped successfully\n" % pid)
            else:
                print str(err)
                sys.exit(1)

    def status(self):
        try:
            with file(self.pidfile, 'r') as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None

        if not pid:
            msg = "Stopped\n"
            sys.stderr.write(msg)
            sys.exit(1)

        try:
            os.kill(pid, 0)
        except OSError as err:
            msg = "Stopped\n"
            sys.stderr.write(msg)
            sys.exit(1)

        sys.stdout.write("Running. PID %d\n" % pid)
        sys.exit(0)

    def restart(self, *args):
        self.stop()
        self.start(*args)

    def run(self, *args):
        pass


def load_config(path):
    with open(path, 'r') as cfg:
        return json.load(cfg)


def coroutine(func):
    def start(*args,**kwargs):
        cr = func(*args,**kwargs)
        cr.next()
        return cr
    return start
