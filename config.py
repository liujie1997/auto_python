telnet_cmd_counnt = 0


def add_telnet_cmd_counnt():
    global telnet_cmd_counnt
    telnet_cmd_counnt = telnet_cmd_counnt + 1


def telnet_cmd_counnt_get():
    return telnet_cmd_counnt
