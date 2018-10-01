# -*- coding: utf-8 -*-

import subprocess, time, os, json
from lib import com

def print_warning(args):
    print("{}{}{}".format(com.color.WARNING,args,com.color.END))

# TODO 2 Refactor JSONProcess class
class JSONProcess:
    """ If anything wrong happens, only preserve 4KB output from the output"""
    PROCESS_BUF_SIZE = 1024*256
    MAX_JSON_PROCESS_RESULT_LENGTH = 4096
    
    def __init__(self, name, cmdline, cwd=None):
        self.name = name
        self.cmdline = cmdline
        self.cwd = cwd
        self.out, self.err = '', ''
        self.result = None
        self.proc = None

    def _loadJsonDump_(self):
        """Pulls a JSON file returns the data.
        Used primarily for debugging"""
        with open(_lsblkDataFile_) as json_data:
            return json.load(json_data)

    def start(self):
        """Start the subprocess"""
        self.proc = subprocess.Popen(self.cmdline, stdout=subprocess.PIPE,stderr=subprocess.PIPE, cwd=self.cwd, bufsize=JSONProcess.PROCESS_BUF_SIZE)

    def is_finished(self):
        """
        Check if the process is finished
        :return: True if the process is terminated, not started or finished normally
        """
        if self.proc is None: return True
        self.out += non_block_read(self.proc.stdout)
        self.err += non_block_read(self.proc.stderr)
        return self.proc.poll() is not None

    def terminate(self):
        if self.proc is not None:
            self.proc.terminate()
            self.proc = None
            self.result = {}

    def get_result(self):
        """
        Retrieve the result of the JSON process
        :return:
        None if not finished or not started;
        an empty dict if the process is terminated;
        a dict with only stdout and stderr if failed to parse JSON from the process stdout;
        a dict with parsed JSON from the process stdout
        """
        # terminated or the result is already parsed
        if self.result is not None: return self.result
        # not started
        if self.proc is None: return None
        # still running
        if not self.is_finished(): return None
        out, err = self.out, self.err
        try:
            self.result = json.loads(out)
        except ValueError:
            print_warning('failed to parse JSON from a JSONProcess: {}'.format(self.name))
            self.result = {'stderr': truncate_string(err, JSONProcess.MAX_JSON_PROCESS_RESULT_LENGTH),
                           'stdout': truncate_string(out, JSONProcess.MAX_JSON_PROCESS_RESULT_LENGTH)}
        print_emph(self.result)
        return self.result

    def wait_task(self, timeout):
        """ Wait until the JSON process is finished, with a timeout
        :param timeout: in seconds
        :return: status (True is successful), result (result object from the process)
        """
        status, result = True, None
        while not self.is_finished():
            time.sleep(1)
            timeout -= 1
            if timeout < 0:
                self.terminate()
                status = False
                break
        result = self.get_result()
        return status, result