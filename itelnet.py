import telnetlib
import time
from equipment_mode import *
import config


class TelnetClient(object):

    def __init__(self):
        self.tn = telnetlib.Telnet()

    def link_telnet(self, ip, username, passwd, port, mode):
        try:
            self.tn.open(ip, port, timeout=1)
        except:
            return 0
        # 根据不同连接方式进行连接
        if mode == equipment_mode["mtk"][0] or mode == equipment_mode["mtk"][1]:
            self.tn.read_until(b'login:')
            self.tn.write(username.encode('ascii') + b'\n')
            loging_result = self.tn.read_very_eager().decode('ascii')
            if ':~#' not in loging_result:
                return 1
            else:
                return 2
        elif mode == equipment_mode["mtk"][2] or mode == equipment_mode["mtk"][3]:
            self.tn.read_until(b'login:')
            self.tn.write(username.encode('ascii') + b'\n')
            self.tn.read_until(b'Password:')
            self.tn.write(passwd.encode('ascii') + b'\n')
            loging_result = self.tn.read_very_eager().decode('ascii')
            if ':~#' not in loging_result:
                return 1
            else:
                return 2
        elif mode in list(equipment_mode["创达特"].values()):
            self.tn.read_until(b'LOGIN#')
            self.tn.write(username.encode('ascii') + b'\n')
            self.tn.read_until(b'PASS#')
            self.tn.write(passwd.encode('ascii') + b'\n')
            self.tn.read_until(b'AMS#')
            self.tn.write('manutest'.encode('ascii') + b'\n')
            loging_result = self.tn.read_very_eager().decode('ascii')
            if 'AMS>MANUTEST#' not in loging_result:
                return 1
            else:
                return 2

    def execute_command(self, cmd, mode):
        self.tn.write(cmd.encode('ascii') + b'\n')
        time.sleep(1)
        cmd_count = config.telnet_cmd_counnt_get()

        if cmd_count == 0:
            if mode in list(equipment_mode['创达特'].values()):
                self.tn.read_until(b'AMS>MANUTEST#')
                cmd_result = self.tn.read_very_eager().decode('ascii')

            else:
                self.tn.read_until(b'#')
                cmd_result = self.tn.read_very_eager().decode('ascii')
        else:
            cmd_result = self.tn.read_very_eager().decode('ascii')
        if 'led' in cmd:
            return cmd_result
        result = self.del_data(cmd, cmd_result, mode)
        return result

    def del_data(self, cmd, result, mode):
        if mode in list(equipment_mode['创达特'].values()):
            start_str = cmd
            end_str = "AMS>MANUTEST# "
            startindex = result.index(start_str)
            if startindex > 0:
                startindex += len(start_str)
            endindex = result.index(end_str)
        elif mode in list(equipment_mode['mtk'].values()):
            start_str = cmd
            end_str = "root"
            startindex = result.index(start_str)
            if startindex > 0:
                startindex += len(start_str)
            endindex = result.index(end_str)
        return result[startindex:endindex]

    def del_produce_write_flag(self, data, mode):
        write = {}
        for k, v in data.items():
            if v != '':
                write[k] = v
        if (mode in list(equipment_mode['mtk'].values())) or (mode in list(equipment_mode['rtl'].values())) or (
                mode in list(equipment_mode['博通'].values())):
            for x, y in write.items():
                cmd = "produce " + x + " " + y
                self.tn.write(cmd.encode('ascii') + b'\n')
                time.sleep(1)
            self.tn.write('produce restoredefault'.encode('ascii') + b'\n')
        elif mode in list(equipment_mode['创达特'].values()):
            for x, y in write.items():
                cmd = x + ' set ' + y
                self.tn.write(cmd.encode('ascii') + b'\n')
                time.sleep(1)
            self.tn.write('default'.encode('ascii') + b'\n')
