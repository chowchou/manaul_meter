import sys
from time import sleep
from main import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QComboBox, QRadioButton, QMessageBox, QCheckBox, \
    QLineEdit
from PyQt5.QtCore import QThread, pyqtSignal, QWaitCondition, QCoreApplication
from get_result import Get_result
class Main_ui(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(Main_ui,self).__init__()
        self.setupUi(self)
        self.init_ui()
        # self.setFixedSize(self.width(), self.height())
        self.pushButton.clicked.connect(self.work_start)
        self.pushButton.setFocus()
        self.pushButton.setShortcut('enter')
        self.flag = 1

    def work_start(self):
        # print('来信号了')
        self.pushButton.setEnabled(False)
        # self.lineEdit_1_1.setFocus()
        self.get_res = Get_result()
        self.get_res._signal.connect(self.res_work)
        self.get_res.start()
        for i in range(9):
            text = '检测中...'
            init_edit = 'self.lineEdit_%d_0.setText(text)' % i
            eval(init_edit)
            init_edit = 'self.lineEdit_%d_1.setText(text)' % i
            eval(init_edit)
            style = 'background-color:#fff;color:#000;font-family:微软雅黑'
            init_edit = 'self.lineEdit_%d_1.setStyleSheet(style)' % i
            eval(init_edit)

    def init_ui(self):
        for i in range(9):
            init_edit = 'self.textEdit_%s.setEnabled(False)' %i
            eval(init_edit)
            text = '等待命令...'
            init_edit = 'self.lineEdit_%d_0.setText(text)' % i
            eval(init_edit)
        self.textBrowser.append('检测环境...')
        self.textBrowser.append('可以开始工作...')
        print('***' * 19)
        print('*' + ' '* 15 + '软件开始运行，请勿关闭此框' + ' '* 15 + '*')
        print('***' * 19)
    def res_work(self,data):
        print(data)
        try:
            if data[0] == 'F00' or data[0] == 'F01':
                print('抄表失败')
                for i in range(9):
                    text = 'error'
                    init_edit = 'self.lineEdit_%d_1.setText(text)' % i
                    eval(init_edit)
                    style = 'background-color:red;color:#fff;font-family:微软雅黑'
                    init_edit = 'self.lineEdit_%d_1.setStyleSheet(style)' % i
                    eval(init_edit)
                    text = '抄表失败'
                    init_edit = 'self.lineEdit_%d_0.setText(text)' % i
                    eval(init_edit)
                    text = '抄表超时/线程错误,请重试!'
                    init_edit = 'self.textEdit_%d.setText(text)' % i
                    eval(init_edit)
                self.textBrowser.append('抄表失败')
            else:
                pass_num = data[0]
                self.label_101.setText(pass_num)
                fail_num = data[1]
                self.label_102.setText(fail_num)
                total_count = data[2]
                self.label_103.setText(total_count)
                success_ratio = data[3]
                self.label_104.setText(success_ratio)
                for i in range(9):
                    pass_res = 'pass'
                    init_edit = 'self.lineEdit_%d_1.setText(pass_res)' % i
                    eval(init_edit)
                    style = 'background-color:green;color:#fff;font-family:微软雅黑'
                    init_edit = 'self.lineEdit_%d_1.setStyleSheet(style)' % i
                    eval(init_edit)
                    text = '检测完成'
                    init_edit = 'self.lineEdit_%d_0.setText(text)' % i
                    eval(init_edit)
                if len(data[4]) != 0:
                    for i in range(len(data[4])):
                        num = int(data[4][i])-1
                        # print(num)
                        fail = 'fail'
                        init_edit = 'self.lineEdit_%d_1.setText(fail)' % num
                        eval(init_edit)
                        style = 'background-color:red;color:#FFF;font-family:微软雅黑'
                        init_edit = 'self.lineEdit_%d_1.setStyleSheet(style)' % num
                        eval(init_edit)
                else:
                    pass
                write_text = 'Pass : ' + pass_num + '/' + 'Fail : ' + fail_num + '/' + 'Total : ' + total_count + '/' +'Success : ' + success_ratio
                self.textBrowser.append(write_text)
        except Exception as e:
            print(e)
            print(e.__traceback__.tb_lineno)
        self.pushButton.setEnabled(True)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    a = Main_ui()
    a.show()
    sys.exit(app.exec_())