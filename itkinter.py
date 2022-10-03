import os
import subprocess
import threading
import tkinter.messagebox
import tkinter
from tkinter import *
import config
from equipment_mode import *
from response_code import *
# from iweb import *
from itelnet import *
from iexcel import *
from tkinter import ttk


class UI(object):
    def __init__(self, height, width):
        self.excel = Excel()
        self.tn = TelnetClient()
        self.window = tkinter.Tk()
        self.ui(height, width)

    # 模式选择窗口
    def ui(self, height, width):
        self.window.title("自动化")
        screenwidth = self.window.winfo_screenwidth()
        screenheight = self.window.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.window.geometry(alignstr)
        x = list(equipment_mode.keys())
        y = list(equipment_mode.values())
        for i in range(0, len(x)):
            self.lable = Label(self.window, text=x[i], width=20)
            self.lable.grid(row=0, column=i, stick=W)
            for m in range(0, len(y[i].values())):
                self.button = Button(self.window, text=list(y[i].values())[m], width=20,
                                     command=lambda m=m, i=i: self.mode_ui(list(y[i].values())[m]))
                self.button.grid(row=m + 1, column=i, stick=W)
        self.window.mainloop()

    # 功能窗口
    def mode_ui(self, mode):
        self.window.destroy()
        self.mode_window = tkinter.Tk()
        self.mode_window.title('模式')
        self.mode_window.geometry('1000x1000')

        self.ip_Lable = Label(self.mode_window, text="输入ip:", height=3, width=10)
        self.ip_Lable.grid(row=0, sticky=W)
        self.ip_text = Entry(self.mode_window, width=15)
        self.ip_text.grid(row=0, column=1, sticky=W)
        if mode == equipment_mode["mtk"][4] or mode == equipment_mode["mtk"][5] or (
                mode in list(equipment_mode["rtl"].values())) or (
                mode in list(equipment_mode["博通"].values())):
            self.ip_text.insert(0, "192.168.0.1")
        elif (mode in list(equipment_mode["mtk"].values())) or (mode in list(equipment_mode["创达特"].values())):
            self.ip_text.insert(0, "192.168.1.1")
        self.port_Lable = Label(self.mode_window, text="输入port:")
        self.port_Lable.grid(row=0, column=2, sticky=W)
        self.port_text = Entry(self.mode_window, width=15)
        self.port_text.grid(row=0, column=3, sticky=W)
        self.port_text.insert(0, "23")

        self.mode_lable = Label(self.mode_window, text="型号:")
        self.mode_lable.grid(row=0, column=4)
        self.mode_text = Entry(self.mode_window)
        self.mode_text.grid(row=0, column=5)
        self.mode_text.insert(0, mode)
        self.mode_text.config(state="readonly")

        self.link_Lable = Label(self.mode_window, text="连接情况", height=3, width=10)
        self.link_Lable.grid(row=1, sticky=W)
        self.link_text = Entry(self.mode_window, width=50)
        self.link_text.grid(row=1, column=1, columnspan=2, sticky=E)
        self.link_text.insert(0, response_code[3])
        self.link_text.config(state='readonly')
        self.link_button = Button(self.mode_window, text="连接", width=10,
                                  command=lambda: self.linkTelnet(self.ip_text.get(), self.port_text.get(), mode))
        self.link_button.grid(row=1, column=3, sticky=E)
        if self.mode_text.get() not in list(equipment_mode['创达特'].values()):
            self.cmd_lable = Label(self.mode_window, text="输入命令", height=3)
            self.cmd_lable.grid(row=2, column=0)
            self.cmd_entry = Entry(self.mode_window, width=50)
            self.cmd_entry.grid(row=2, column=1, columnspan=2, sticky=W)
            self.cmd_button = Button(self.mode_window, text="执行命令", width=10,
                                     command=lambda: self.execute_cmd(self.cmd_entry.get()))
            self.cmd_button.grid(row=2, column=3, sticky=E)

            self.showcmd_lable = Label(self.mode_window, text="显示结果")
            self.showcmd_lable.grid(row=3, column=0)
            self.cmdShow_text = Text(self.mode_window, height=20, width=100)
            self.cmdShow_text.grid(row=3, column=1, columnspan=5)
            self.cmdShow_text.config(state="disable")

        self.basics_function = Label(self.mode_window, text="基础功能", height=3)
        self.basics_function.grid(row=4, column=0)

        self.produce_write = Button(self.mode_window, text="产测写入", width=10,
                                    command=lambda: self.produce_write_window())
        self.produce_write.grid(row=4, column=1)

        self.produce_read = Button(self.mode_window, text="产测读取结果", width=10,
                                   command=lambda: self.produce_read_window())
        self.produce_read.grid(row=4, column=2)

        self.protocol_Lable = Label(self.mode_window, text="协议", height=3)
        self.protocol_Lable.grid(row=6, column=0)

        self.wan_dhcp_button = Button(self.mode_window, text="wan_dhcp")
        self.wan_dhcp_button.grid(row=6, column=1)

        self.wan_pppoe_button = Button(self.mode_window, text="wan_pppoe")
        self.wan_pppoe_button.grid(row=6, column=2)

        self.wan_static_button = Button(self.mode_window, text="wan_static")
        self.wan_static_button.grid(row=6, column=3)

        self.lan_dhcp_button = Button(self.mode_window, text="lan_dhcp")
        self.lan_dhcp_button.grid(row=6, column=4)

        self.tr069_1_button = Button(self.mode_window, text="tr069-1")
        self.tr069_1_button.grid(row=7, column=0)
        self.tr069_2_button = Button(self.mode_window, text="tr069-2")
        self.tr069_2_button.grid(row=7, column=1)

        self.fota_Lable = Label(self.mode_window, text="fota与cfota升级", height=3)
        self.fota_Lable.grid(row=8, column=0)

        self.old_cfota_button = Button(self.mode_window, text="老cfota")
        self.old_cfota_button.grid(row=8, column=1)

        self.new_cfota_button = Button(self.mode_window, text="新cfota")
        self.new_cfota_button.grid(row=8, column=2)

        self.new_fota_button = Button(self.mode_window, text="我们平台上的fota")
        self.new_fota_button.grid(row=8, column=3)

        self.mode_window.mainloop()

    # 开启telnet
    def linkTelnet(self, ip, port, mode):
        if mode in list(equipment_mode["mtk"].values()) or (
                mode in list(equipment_mode["博通"].values())):
            url = "curl -X POST \"http://" + ip + "/factory/telnet?open=1&token=b26bbb9407b20d92c5b7dd071a108dcc\""
            os.system(url)

            if mode in list(equipment_mode["博通"].values()):
                result = self.tn.link_telnet(ip, 'admin', 'admin', port, mode)
            elif mode == equipment_mode['mtk'][0] or mode == equipment_mode['mtk'][1]:
                result = self.tn.link_telnet(ip, 'root', '', port, mode)
            elif mode == equipment_mode['mtk'][2] or mode == equipment_mode['mtk'][3]:
                result = self.tn.link_telnet(ip, 'root', 'root', port, mode)
            elif mode == equipment_mode['mtk'][4] or mode == equipment_mode['mtk'][5]:
                result = self.tn.link_telnet(ip, 'root', 'nE7n$8q%5m', port, mode)


        elif mode in list(equipment_mode["rtl"].values()):
            url = "curl -d ''  http://" + ip + "//boafrm/formTelnetfortest"
            os.system(url)
            result = self.tn.link_telnet(ip, 'root', 'nE7n$8q%5m', port, mode)

        elif mode in list(equipment_mode["创达特"].values()):
            result = self.tn.link_telnet(ip, 'root', 'trid', port, mode)
        self.link_text.config(state='normal')
        self.link_text.delete(0, "end")
        self.link_text.insert(0, response_code[result])
        self.link_text.config(state="readonly")
        if result == 2:
            self.again_user_passwd()

    # 执行指令
    def execute_cmd(self, cmd):
        if self.link_text.get() == response_code[1]:
            result = self.tn.execute_command(cmd, self.mode_text.get())
            config.add_telnet_cmd_counnt()
            self.cmdShow_text.config(state='normal')
            self.cmdShow_text.delete(1.0, "end")
            self.cmdShow_text.insert(1.0, result)
            self.cmdShow_text.config(state='disable')
        else:
            tkinter.messagebox.showinfo('提示', response_code[3])

    # 产测写窗口
    def produce_write_window(self):
        self.t1 = tkinter.Toplevel()
        self.create_window(self.t1, "产测写入", 500, 500)
        if (self.mode_text.get() in list(equipment_mode["mtk"].values())) or (
                self.mode_text.get() in list(equipment_mode["rtl"].values())) or (
                self.mode_text.get() in list(equipment_mode["博通"].values())):
            self.macrw_Lable = Label(self.t1, text="macrw")
            self.macrw_Lable.grid(row=0, sticky=W)
            self.macrw = Entry(self.t1)
            self.macrw.grid(row=0, column=1, sticky=E)
            self.macformat = Label(self.t1, text="mac格式：(xxxxxxxxxxxx)")
            self.macformat.grid(row=0, column=2, sticky=W)

            self.adminPasswd_Lable = Label(self.t1, text="adminPasswd")
            self.adminPasswd_Lable.grid(row=1, sticky=W)
            self.adminPasswd = Entry(self.t1)
            self.adminPasswd.grid(row=1, column=1, sticky=E)

            if self.mode_text.get() not in list(equipment_mode["rtl"].values()):
                self.ssid_2g_Lable = Label(self.t1, text="ssid_2g")
                self.ssid_2g_Lable.grid(row=2, sticky=W)
                self.ssid_2g = Entry(self.t1)
                self.ssid_2g.grid(row=2, column=1, sticky=E)

                self.ssid_5g_Lable = Label(self.t1, text="ssid_5g")
                self.ssid_5g_Lable.grid(row=4, sticky=W)
                self.ssid_5g = Entry(self.t1)
                self.ssid_5g.grid(row=4, column=1, sticky=E)

            self.ssidpsk_2g_Lable = Label(self.t1, text="ssidpsk_2g")
            self.ssidpsk_2g_Lable.grid(row=3, sticky=W)
            self.ssidpsk_2g = Entry(self.t1)
            self.ssidpsk_2g.grid(row=3, column=1, sticky=E)

            self.ssidpsk_5g_Lable = Label(self.t1, text="ssidpsk_5g")
            self.ssidpsk_5g_Lable.grid(row=5, sticky=W)
            self.ssidpsk_5g = Entry(self.t1)
            self.ssidpsk_5g.grid(row=5, column=1, sticky=E)

            self.wpspin_2g_Lable = Label(self.t1, text="wpspin_2g")
            self.wpspin_2g_Lable.grid(row=6, sticky=W)
            self.wpspin_2g = Entry(self.t1)
            self.wpspin_2g.grid(row=6, column=1, sticky=E)

            self.sn_Lable = Label(self.t1, text="sn")
            self.sn_Lable.grid(row=8, sticky=W)
            self.sn = Entry(self.t1)
            self.sn.grid(row=8, column=1, sticky=E)

            self.fotaUrl_Lable = Label(self.t1, text="fotaUrl")
            self.fotaUrl_Lable.grid(row=9, sticky=W)
            self.fotaUrl = Entry(self.t1)
            self.fotaUrl.grid(row=9, column=1, sticky=E)

            if self.mode_text.get() == equipment_mode["mtk"][4] or self.mode_text.get() == equipment_mode["mtk"][5]:
                self.produceClass_Lable = Label(self.t1, text="productClass")
                self.produceClass_Lable.grid(row=10, sticky=W)
                self.produceClass = Entry(self.t1)
                self.produceClass.grid(row=10, column=1, sticky=W)

            self.produce_write_submit = Button(self.t1, text="提交", command=self.excute_produce_write)
            self.produce_write_submit.grid(row=11, column=0)

        elif self.mode_text.get() in list(equipment_mode["创达特"].values()):
            self.mac_Lable = Label(self.t1, text="mac")
            self.mac_Lable.grid(row=0, column=0, sticky=W)
            self.mac = Entry(self.t1)
            self.mac.grid(row=0, column=1, sticky=W)
            self.mac_format = Label(self.t1, text="mac格式：(xx:xx:xx:xx:xx:xx)")
            self.mac_format.grid(row=0, column=2, sticky=W)

            self.wlan4g_Lable = Label(self.t1, text="wlan2.4 ssid")
            self.wlan4g_Lable.grid(row=1, column=0, sticky=W)
            self.wlan4g = Entry(self.t1)
            self.wlan4g.grid(row=1, column=1, sticky=W)

            self.wlan4g_pass_Lable = Label(self.t1, text="wlan2.4 pass")
            self.wlan4g_pass_Lable.grid(row=2, column=0, sticky=W)
            self.wlan4g_pass = Entry(self.t1)
            self.wlan4g_pass.grid(row=2, column=1, sticky=W)

            self.wlan4g_pin_Lable = Label(self.t1, text="pin2.4")
            self.wlan4g_pin_Lable.grid(row=3, column=0, sticky=W)
            self.wlan4g_pin = Entry(self.t1)
            self.wlan4g_pin.grid(row=3, column=1, sticky=W)

            self.wlan5g_Lable = Label(self.t1, text="wlan5 ssid")
            self.wlan5g_Lable.grid(row=4, column=0, sticky=W)
            self.wlan5g = Entry(self.t1)
            self.wlan5g.grid(row=4, column=1, sticky=W)

            self.wlan5g_pass_Lable = Label(self.t1, text="wlan5 pass")
            self.wlan5g_pass_Lable.grid(row=5, column=0, sticky=W)
            self.wlan5g_pass = Entry(self.t1)
            self.wlan5g_pass.grid(row=5, column=1, sticky=W)

            self.wlan5g_pin_Lable = Label(self.t1, text="pin5")
            self.wlan5g_pin_Lable.grid(row=6, column=0, sticky=W)
            self.wlan5g_pin = Entry(self.t1)
            self.wlan5g_pin.grid(row=6, column=1, sticky=W)

            self.produce_write_submit = Button(self.t1, text="提交", command=self.excute_produce_write)
            self.produce_write_submit.grid(row=10, column=0)

    # 执行产测写
    def excute_produce_write(self):
        data = {}
        if self.mode_text.get() == equipment_mode["mtk"][4] or self.mode_text.get() == equipment_mode["mtk"][5]:
            data = {self.macrw_Lable['text']: self.macrw.get(), self.adminPasswd_Lable['text']: self.adminPasswd.get(),
                    self.ssid_2g_Lable['text']: self.ssid_2g.get(),
                    self.ssidpsk_2g_Lable['text']: self.ssidpsk_2g.get(),
                    self.ssid_5g_Lable['text']: self.ssid_5g.get(),
                    self.ssidpsk_5g_Lable['text']: self.ssidpsk_5g.get(),
                    self.wpspin_2g_Lable['text']: self.wpspin_2g.get(), self.sn_Lable['text']: self.sn.get(),
                    self.fotaUrl_Lable['text']: self.fotaUrl.get(),
                    self.produceClass_Lable['text']: self.produceClass.get()}
        elif (self.mode_text.get() in list(equipment_mode["mtk"].values())) or (
                self.mode_text.get() in list(equipment_mode["博通"].values())):
            data = {self.macrw_Lable['text']: self.macrw.get(), self.adminPasswd_Lable['text']: self.adminPasswd.get(),
                    self.ssid_2g_Lable['text']: self.ssid_2g.get(),
                    self.ssidpsk_2g_Lable['text']: self.ssidpsk_2g.get(),
                    self.ssid_5g_Lable['text']: self.ssid_5g.get(),
                    self.ssidpsk_5g_Lable['text']: self.ssidpsk_5g.get(),
                    self.wpspin_2g_Lable['text']: self.wpspin_2g.get(), self.sn_Lable['text']: self.sn.get(),
                    self.fotaUrl_Lable['text']: self.fotaUrl.get()}
        elif self.mode_text.get() in list(equipment_mode["rtl"].values()):
            data = {self.macrw_Lable['text']: self.macrw.get(), self.adminPasswd_Lable['text']: self.adminPasswd.get(),
                    self.ssidpsk_2g_Lable['text']: self.ssidpsk_2g.get(),
                    self.ssidpsk_5g_Lable['text']: self.ssidpsk_5g.get(),
                    self.wpspin_2g_Lable['text']: self.wpspin_2g.get(), self.sn_Lable['text']: self.sn.get(),
                    self.fotaUrl_Lable['text']: self.fotaUrl.get()}
        elif self.mode_text.get() in list(equipment_mode["创达特"].values()):
            data = {self.mac_Lable['text']: self.mac.get(), self.wlan4g_Lable['text']: self.wlan4g.get(),
                    self.wlan4g_pass_Lable['text']: self.wlan4g_pass.get(),
                    self.wlan4g_pin_Lable['text']: self.wlan4g_pin.get(), self.wlan5g_Lable['text']: self.wlan5g.get(),
                    self.wlan5g_pass_Lable['text']: self.wlan5g_pass.get(),
                    self.wlan5g_pin_Lable['text']: self.wlan5g_pin.get()}
        self.excel.write_excel(self.mode_text.get() + '-produce.xlsx', 'write', data, 'produce_write')
        if self.link_text.get() == response_code[1]:
            self.tn.del_produce_write_flag(data, self.mode_text.get())
            if self.mode_text.get() in list(equipment_mode['创达特'].values()):
                tkinter.messagebox.showinfo('提示', response_code[5])
            self.telnet_link_disconnect()
        else:
            tkinter.messagebox.showinfo('提示', response_code[3])

        self.t1.destroy()

    # 产测读窗口
    def produce_read_window(self):
        self.t2 = tkinter.Toplevel()
        self.create_window(self.t2, "读取产测", 600, 600)
        if (self.mode_text.get() in list(equipment_mode["mtk"].values())) or (
                self.mode_text.get() in list(equipment_mode["rtl"].values())) or (
                self.mode_text.get() in list(equipment_mode["博通"].values())):
            self.macrwRead_Lable = Label(self.t2, text="macrw")
            self.macrwRead_Lable.grid(row=0, column=0, sticky=W)
            self.macrwRead = Entry(self.t2, width=30)
            self.macrwRead.grid(row=0, column=1, sticky=W)
            self.macrwRead.config(state="readonly")
            self.macrwRead_button = Button(self.t2, text="读取mac",
                                           command=lambda: self.produceRead_one(self.macrwRead_Lable['text'],
                                                                                self.macrwRead))
            self.macrwRead_button.grid(row=0, column=2, sticky=W)

            if self.mode_text.get() not in list(equipment_mode['rtl'].values()):
                self.ssid_2gRead_Lable = Label(self.t2, text="ssid_2g")
                self.ssid_2gRead_Lable.grid(row=1, column=0, sticky=W)
                self.ssid_2gRead = Entry(self.t2, width=30)
                self.ssid_2gRead.grid(row=1, column=1, sticky=W)
                self.ssid_2gRead.config(state="readonly")
                self.ssid_2gRead_button = Button(self.t2, text="读取ssid_2g",
                                                 command=lambda: self.produceRead_one(self.ssid_2gRead_Lable['text'],
                                                                                      self.ssid_2gRead))
                self.ssid_2gRead_button.grid(row=1, column=2, sticky=W)

                self.ssid_5gRead_Lable = Label(self.t2, text="ssid_5g")
                self.ssid_5gRead_Lable.grid(row=2, column=0, sticky=W)
                self.ssid_5gRead = Entry(self.t2, width=30)
                self.ssid_5gRead.grid(row=2, column=1, sticky=W)
                self.ssid_5gRead.config(state="readonly")
                self.ssid_5gRead_button = Button(self.t2, text="读取ssid_5g",
                                                 command=lambda: self.produceRead_one(self.ssid_5gRead_Lable['text'],
                                                                                      self.ssid_5gRead))
                self.ssid_5gRead_button.grid(row=2, column=2, sticky=W)

            self.ssidpsk_2gRead_Lable = Label(self.t2, text="ssidpsk_2g")
            self.ssidpsk_2gRead_Lable.grid(row=3, column=0, sticky=W)
            self.ssidpsk_2gRead = Entry(self.t2, width=30)
            self.ssidpsk_2gRead.grid(row=3, column=1, sticky=W)
            self.ssidpsk_2gRead.config(state="readonly")
            if self.mode_text.get() in list(equipment_mode['rtl'].values()):
                self.ssidpsk_2gRead_button = Button(self.t2, text="读取ssidpsk_2g", command=lambda: self.produceRead_one(
                    'read ' + self.ssidpsk_2gRead_Lable['text'], self.ssidpsk_2gRead))
            else:
                self.ssidpsk_2gRead_button = Button(self.t2, text="读取ssidpsk_2g", command=lambda: self.produceRead_one(
                    self.ssidpsk_2gRead_Lable['text'], self.ssidpsk_2gRead))
            self.ssidpsk_2gRead_button.grid(row=3, column=2, sticky=W)

            self.ssidpsk_5gRead_Lable = Label(self.t2, text="ssidpsk_5g")
            self.ssidpsk_5gRead_Lable.grid(row=4, column=0, sticky=W)
            self.ssidpsk_5gRead = Entry(self.t2, width=30)
            self.ssidpsk_5gRead.grid(row=4, column=1, sticky=W)
            self.ssidpsk_5gRead.config(state="readonly")
            if self.mode_text.get() in list(equipment_mode['rtl'].values()):
                self.ssidpsk_5gRead_button = Button(self.t2, text="读取ssidpsk_5g", command=lambda: self.produceRead_one(
                    'read ' + self.ssidpsk_5gRead_Lable['text'], self.ssidpsk_5gRead))
            else:
                self.ssidpsk_5gRead_button = Button(self.t2, text="读取ssidpsk_5g", command=lambda: self.produceRead_one(
                    self.ssidpsk_5gRead_Lable['text'], self.ssidpsk_5gRead))
            self.ssidpsk_5gRead_button.grid(row=4, column=2, sticky=W)

            self.wpspin_2gRead_Lable = Label(self.t2, text="wpspin_2g")
            self.wpspin_2gRead_Lable.grid(row=5, column=0, sticky=W)
            self.wpspin_2gRead = Entry(self.t2, width=30)
            self.wpspin_2gRead.grid(row=5, column=1, sticky=W)
            self.wpspin_2gRead.config(state="readonly")
            self.wpspin_2gRead_button = Button(self.t2, text="读取wpspin_2g",
                                               command=lambda: self.produceRead_one(self.wpspin_2gRead_Lable['text'],
                                                                                    self.wpspin_2gRead))
            self.wpspin_2gRead_button.grid(row=5, column=2, sticky=W)

            self.adminPasswdRead_Lable = Label(self.t2, text="adminPasswd")
            self.adminPasswdRead_Lable.grid(row=6, column=0, sticky=W)
            self.adminPasswdRead = Entry(self.t2, width=30)
            self.adminPasswdRead.grid(row=6, column=1, sticky=W)
            self.adminPasswdRead.config(state="readonly")
            self.adminPasswdRead_button = Button(self.t2, text="读取adminPasswd",
                                                 command=lambda: self.produceRead_one(
                                                     self.adminPasswdRead_Lable['text'],
                                                     self.adminPasswdRead))
            self.adminPasswdRead_button.grid(row=6, column=2, sticky=W)

            self.snRead_Lable = Label(self.t2, text="sn")
            self.snRead_Lable.grid(row=7, column=0, sticky=W)
            self.snRead = Entry(self.t2, width=30)
            self.snRead.grid(row=7, column=1, sticky=W)
            self.snRead.config(state="readonly")
            self.snRead_button = Button(self.t2, text="读取sn",
                                        command=lambda: self.produceRead_one(
                                            self.snRead_Lable['text'],
                                            self.snRead))
            self.snRead_button.grid(row=7, column=2, sticky=W)

            self.fotaUrlRead_Lable = Label(self.t2, text="fotaUrl")
            self.fotaUrlRead_Lable.grid(row=8, column=0, sticky=W)
            self.fotaUrlRead = Entry(self.t2, width=30)
            self.fotaUrlRead.grid(row=8, column=1, sticky=W)
            self.fotaUrlRead.config(state="readonly")
            self.fotaUrlRead_button = Button(self.t2, text="读取fotaUrl",
                                             command=lambda: self.produceRead_one(
                                                 self.fotaUrlRead_Lable['text'],
                                                 self.fotaUrlRead))
            self.fotaUrlRead_button.grid(row=8, column=2, sticky=W)

            self.swVersionRead_Lable = Label(self.t2, text="swVersion")
            self.swVersionRead_Lable.grid(row=9, column=0, sticky=W)
            self.swVersionRead = Entry(self.t2, width=30)
            self.swVersionRead.grid(row=9, column=1, sticky=W)
            self.swVersionRead.config(state="readonly")
            self.swVersionRead_button = Button(self.t2, text="读取swVersion",
                                               command=lambda: self.produceRead_one(
                                                   self.swVersionRead_Lable['text'],
                                                   self.swVersionRead))
            self.swVersionRead_button.grid(row=9, column=2, sticky=W)

            self.allledon_Lable = Label(self.t2, text="allledon")
            self.allledon_Lable.grid(row=10, column=0)
            self.allledon = Entry(self.t2, width=30)
            self.allledon.grid(row=10, column=1)
            self.allledon.config(state="readonly")
            self.allledon_button = Button(self.t2, text="点亮所有灯",
                                          command=lambda: self.produceRead_one(self.allledon_Lable['text'],
                                                                               self.allledon))
            self.allledon_button.grid(row=10, column=2)

            self.allledoff_Lable = Label(self.t2, text="allledoff")
            self.allledoff_Lable.grid(row=11, column=0)
            self.allledoff = Entry(self.t2, width=30)
            self.allledoff.grid(row=11, column=1)
            self.allledoff.config(state="readonly")
            self.allledoff_button = Button(self.t2, text="熄灭所有灯",
                                           command=lambda: self.produceRead_one(self.allledoff_Lable['text'],
                                                                                self.allledoff))
            self.allledoff_button.grid(row=11, column=2)

            self.configckeckRead_Lable = Label(self.t2, text="configckeck")
            self.configckeckRead_Lable.grid(row=20, column=0, sticky=W)
            self.configckeckRead = Entry(self.t2, width=30)
            self.configckeckRead.grid(row=20, column=1, sticky=W)
            self.configckeckRead.config(state="readonly")
            self.configckeckRead_button = Button(self.t2, text="读取configckeck",
                                                 command=lambda: self.produceRead_one(
                                                     self.configckeckRead_Lable['text'],
                                                     self.configckeckRead))
            self.configckeckRead_button.grid(row=20, column=2, sticky=W)

        elif (self.mode_text.get() in list(equipment_mode["创达特"].values())):
            self.flash2Read_Lable = Label(self.t2, text="flash2")
            self.flash2Read_Lable.grid(row=0, column=0)
            self.flash2Read = Entry(self.t2, width=50)
            self.flash2Read.grid(row=0, column=1)
            self.flash2Read.config(state="readonly")
            self.flash2Read_button = Button(self.t2, text="读取flash2",
                                            command=lambda: self.produceRead_one(self.flash2Read_Lable['text'],
                                                                                 self.flash2Read))
            self.flash2Read_button.grid(row=0, column=2)

            self.memoryRead_Lable = Label(self.t2, text="memory")
            self.memoryRead_Lable.grid(row=1, column=0)
            self.memoryRead = Entry(self.t2, width=50)
            self.memoryRead.grid(row=1, column=1)
            self.memoryRead.config(state="readonly")
            self.memoryRead_button = Button(self.t2, text="读取memory",
                                            command=lambda: self.produceRead_one(self.memoryRead_Lable['text'],
                                                                                 self.memoryRead))
            self.memoryRead_button.grid(row=1, column=2)

            self.macRead_Lable = Label(self.t2, text="mac get")
            self.macRead_Lable.grid(row=2, column=0)
            self.macRead = Entry(self.t2, width=50)
            self.macRead.grid(row=2, column=1)
            self.macRead.config(state="readonly")
            self.macRead_button = Button(self.t2, text="读取mac",
                                         command=lambda: self.produceRead_one(self.macRead_Lable['text'],
                                                                              self.macRead))
            self.macRead_button.grid(row=2, column=2)

            self.ledonRead_Lable = Label(self.t2, text="led on")
            self.ledonRead_Lable.grid(row=3, column=0)
            self.ledonRead = Entry(self.t2, width=50)
            self.ledonRead.grid(row=3, column=1)
            self.ledonRead.config(state="readonly")
            self.ledonRead_button = Button(self.t2, text="点亮所有灯",
                                           command=lambda: self.produceRead_one(self.ledonRead_Lable['text'],
                                                                                self.ledonRead))
            self.ledonRead_button.grid(row=3, column=2)

            self.ledoffRead_Lable = Label(self.t2, text="led off")
            self.ledoffRead_Lable.grid(row=4, column=0)
            self.ledoffRead = Entry(self.t2, width=50)
            self.ledoffRead.grid(row=4, column=1)
            self.ledoffRead.config(state="readonly")
            self.ledoffRead_button = Button(self.t2, text="熄灭所有灯",
                                            command=lambda: self.produceRead_one(self.ledoffRead_Lable['text'],
                                                                                 self.ledoffRead))
            self.ledoffRead_button.grid(row=4, column=2)

            self.ledendRead_Lable = Label(self.t2, text="led end")
            self.ledendRead_Lable.grid(row=5, column=0)
            self.ledendRead = Entry(self.t2, width=50)
            self.ledendRead.grid(row=5, column=1)
            self.ledendRead.config(state="readonly")
            self.ledendRead_button = Button(self.t2, text="恢复所有灯",
                                            command=lambda: self.produceRead_one(self.ledendRead_Lable['text'],
                                                                                 self.ledendRead))
            self.ledendRead_button.grid(row=5, column=2)

            self.wlan2ssidRead_Lable = Label(self.t2, text="wlan2.4 ssid get")
            self.wlan2ssidRead_Lable.grid(row=6, column=0)
            self.wlan2ssidRead = Entry(self.t2, width=50)
            self.wlan2ssidRead.grid(row=6, column=1)
            self.wlan2ssidRead.config(state="readonly")
            self.wlan2ssidRead_button = Button(self.t2, text="读取wlan2.4ssid",
                                               command=lambda: self.produceRead_one(self.wlan2ssidRead_Lable['text'],
                                                                                    self.wlan2ssidRead))
            self.wlan2ssidRead_button.grid(row=6, column=2)

            self.wlan2passRead_Lable = Label(self.t2, text="wlan2.4 pass get")
            self.wlan2passRead_Lable.grid(row=7, column=0)
            self.wlan2passRead = Entry(self.t2, width=50)
            self.wlan2passRead.grid(row=7, column=1)
            self.wlan2passRead.config(state="readonly")
            self.wlan2passRead_button = Button(self.t2, text="读取wlan2.4pass",
                                               command=lambda: self.produceRead_one(self.wlan2passRead_Lable['text'],
                                                                                    self.wlan2passRead))
            self.wlan2passRead_button.grid(row=7, column=2)

            self.wlan5ssidRead_Lable = Label(self.t2, text="wlan5 ssid get")
            self.wlan5ssidRead_Lable.grid(row=8, column=0)
            self.wlan5ssidRead = Entry(self.t2, width=50)
            self.wlan5ssidRead.grid(row=8, column=1)
            self.wlan5ssidRead.config(state="readonly")
            self.wlan5ssidRead_button = Button(self.t2, text="读取wlan5ssid",
                                               command=lambda: self.produceRead_one(self.wlan5ssidRead_Lable['text'],
                                                                                    self.wlan5ssidRead))
            self.wlan5ssidRead_button.grid(row=8, column=2)

            self.wlan5passRead_Lable = Label(self.t2, text="wlan5 pass get")
            self.wlan5passRead_Lable.grid(row=9, column=0)
            self.wlan5passRead = Entry(self.t2, width=50)
            self.wlan5passRead.grid(row=9, column=1)
            self.wlan5passRead.config(state="readonly")
            self.wlan5passRead_button = Button(self.t2, text="读取wlan5pass",
                                               command=lambda: self.produceRead_one(self.wlan5passRead_Lable['text'],
                                                                                    self.wlan5passRead))
            self.wlan5passRead_button.grid(row=9, column=2)

            self.pinRead_Lable = Label(

                self.t2, text="pin get")
            self.pinRead_Lable.grid(row=10, column=0)
            self.pinRead = Entry(self.t2, width=50)
            self.pinRead.grid(row=10, column=1)
            self.pinRead.config(state="readonly")
            self.pinRead_button = Button(self.t2, text="读取pin ",
                                         command=lambda: self.produceRead_one(self.pinRead_Lable['text'],
                                                                              self.pinRead))
            self.pinRead_button.grid(row=10, column=2)

            # self.button_Lable=Label(self.t2,text="button")
            # self.button_Lable.grid(row=11,column=0)

            # button_value=['wps','reset','wlan']
            # self.button_combobox=ttk.Combobox(self.t2,height=10,width=10,state="readonly",values=button_value)
            # self.button_combobox.set(button_value[0])
            # self.button_combobox.grid(row=11,column=1)

            self.VersionRead_Lable = Label(self.t2, text="version")
            self.VersionRead_Lable.grid(row=12, column=0)
            self.VersionRead = Entry(self.t2, width=50)
            self.VersionRead.grid(row=12, column=1)
            self.VersionRead.config(state="readonly")
            self.VersionRead_button = Button(self.t2, text="读取version",
                                             command=lambda: self.produceRead_one(self.VersionRead_Lable['text'],
                                                                                  self.VersionRead))
            self.VersionRead_button.grid(row=12, column=2)

            self.lan_Lable = Label(self.t2, text="lan")
            self.lan_Lable.grid(row=13, column=0)
            self.lan = Entry(self.t2, width=50)
            self.lan.grid(row=13, column=1)
            self.lan.config(state="readonly")
            self.lan_button = Button(self.t2, text="读取lan",
                                     command=lambda: self.produceRead_one(self.lan_Lable['text'], self.lan))
            self.lan_button.grid(row=13, column=2)

            self.usb_Lable = Label(self.t2, text="usb")
            self.usb_Lable.grid(row=14, column=0)
            self.usb = Entry(self.t2, width=50)
            self.usb.grid(row=14, column=1)
            self.usb.config(state="readonly")
            self.usb_button = Button(self.t2, text="读取usb")
            self.usb_button.grid(row=14, column=2)

        self.moreRead_button = Button(self.t2, text="批量读取")
        self.moreRead_button.grid(row=30, column=0)

    # 执行单个产测读
    def produceRead_one(self, value, format):
        if self.link_text.get() == response_code[1]:
            if self.mode_text.get() in list(equipment_mode['创达特'].values()):
                cmd = value
            else:
                cmd = 'produce ' + value
            result = self.tn.execute_command(cmd, self.mode_text.get())

            config.add_telnet_cmd_counnt()
            format.config(state="normal")
            format.delete(0, 'end')
            if 'led' in cmd:
                result = '请观察灯的状态'
            print(result)
            format.insert(0, result)
            format.config(state='readonly')

    def produceRead_more(self):
        print(2)

    def again_user_passwd(self):
        self.t3 = tkinter.Toplevel()
        self.create_window(self.t3, "重新输入账号密码", 400, 400)

        self.again_user_label = Label(self.t3, text="用户名", height=3)
        self.again_user_label.grid(row=0, column=0)
        self.again_user_entry = Entry(self.t3)
        self.again_user_entry.grid(row=0, column=1)

        self.again_passwd_label = Label(self.t3, text="密码", height=3)
        self.again_passwd_label.grid(row=1, column=0)
        self.again_passwd_entry = Entry(self.t3)
        self.again_passwd_entry.grid(row=1, column=1)

        self.again_user_passwd_button = Button(self.t3, text="提交",
                                               command=lambda: self.excute_again_user_passwd(self.ip_text.get(),
                                                                                   self.again_user_entry.get(),
                                                                                   self.again_passwd_entry.get(), self.port_text.get(),
                                                                                   self.mode_text.get()))
        self.again_user_passwd_button.grid(row=2, column=0)

    def excute_again_user_passwd(self,ip,username,passwd,port,mode):
        result=self.tn.link_telnet(ip, username, passwd, port, mode)
        self.link_text.config(state='normal')
        self.link_text.delete(0, "end")
        self.link_text.insert(0, response_code[result])
        self.link_text.config(state="readonly")
        if result !=2:
            self.t3.destroy()
    # 创建窗口
    def create_window(self, t, name, height, width):
        t.title(name)
        screenwidth = t.winfo_screenwidth()
        screenheight = t.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        t.geometry(alignstr)

    def telnet_link_disconnect(self):
        self.link_text.config(state="normal")
        self.link_text.delete(0, "end")
        self.link_text.insert(0, response_code[4])
        self.link_text.config(state="readonly")
