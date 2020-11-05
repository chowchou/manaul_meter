import os
import subprocess
import sys
import re
import datetime

import func_timeout
from PyQt5.QtCore import QThread,pyqtSignal,Qt
from func_timeout import func_set_timeout


class Get_result(QThread):
    #  通过类成员对象定义信号对象
    _signal = pyqtSignal(list)
    def __init__(self):
        super(Get_result, self).__init__()
        self.rev_data = ''
    def __del__(self):
        self.wait()

    @func_set_timeout(35)
    def test_start(self):
        main = "cctt_simulator_sta_control.exe"
        if os.path.exists(main):
            rc, out = subprocess.getstatusoutput(main)
            # print(out)
            fail_re = re.compile('(\d) : fail')
            self.fail_list = re.findall(fail_re, out)
            # print(self.fail_list)
            print(datetime.datetime.now())
            pass_num = re.compile(
                "success count:(\d*).*fail count:(\d*).*total count:(\d*).*success ratio: (\d*\.\d*%)")
            res_list = re.findall(pass_num, out)
            # print(res_list)
            res_list = list(res_list[0])
            res_list.append(self.fail_list)
            # print(res_list)
            self._signal.emit(res_list)
            print('进程完成')
            return
    def run(self):
        try:
            print(datetime.datetime.now())
            print('进程开始启动')
            try:
                self.test_start()
            except func_timeout.exceptions.FunctionTimedOut:
                rev_data = ['F01']
                self._signal.emit(rev_data)
                return
            except Exception as e:
                print(e)
            # finally:
            #     sys.exit()
        except Exception as e:
            self.rev_data = ['F00']
            self.rev_data.append(e)
            self._signal.emit(self.rev_data)
            return
        # else:
        #     self.rev_data = 'end'
