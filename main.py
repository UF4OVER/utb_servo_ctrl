import json
import os
import sys
import datetime

import serial.tools.list_ports
from PyQt5.QtWidgets import QMessageBox, QLineEdit, QFrame, QSpinBox
from PyQt5.QtWidgets import (QGridLayout, QLabel, QComboBox, QTextEdit, QApplication,
                             QMainWindow, QWidget, QPushButton)
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtCore import Qt
import logging
import servo




# class LedIndicator(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.color = Qt.red
#         self.blink = False
#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.toggleBlink)
#         self.timer.start(500)  # 每隔500毫秒切换一次颜色
#
#     def setColor(self, color):
#         self.color = color
#         self.update()
#
#     def toggleBlink(self):
#         if self.blink:
#             self.color = Qt.yellow
#         else:
#             self.color = self.original_color
#         self.blink = not self.blink
#         self.update()
#
#     def paintEvent(self, event):
#         painter = QPainter(self)
#         painter.setRenderHint(QPainter.Antialiasing)
#         painter.setBrush(self.color)
#         painter.drawEllipse(0, 0, self.width(), self.height())


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

style_sheet = """
        QMessageBox {
            background-color: #F0F0F0;
        }

        QMessageBox QLabel {
            color: #333;
            font-size: 20px; 
        }

        QMessageBox QPushButton {
            background-color: #007ACC;
            color: white;
            border-radius: 10px; /* 圆角 */
            border: 2px solid #005C19;
            padding: 10px;
            min-width: 80px;
            border-radius: 5px;
        }

        QMessageBox QPushButton:hover {
            background-color: #005C99;
            border-radius: 10px; /* 圆角 */
        }

        QMessageBox QPushButton:pressed {
            background-color: #004477;
            border-radius: 10px; /* 圆角 */
        }
        """


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.servo = None
        self.setWindowIcon(QIcon('icon.png'))
        self.setWindowTitle('三星堆舵机控制')
        self.log_file = open('log.txt', 'w')  # 打开日志文件
        self.all_servo_data1 = []
        self.all_servo_data2 = []
        self.all_servo_data3 = []
        self.all_servo_data4 = []
        self.all_servo_data5 = []
        self.all_servo_data6 = []
        self.load_presets()
        self.setStyleSheet("background-color: #f3E6C0;")

        self.setGeometry(100, 100, 400, 300)
        self.inputs = []

        self.all_servo_data1 = []
        self.all_servo_data2 = []
        self.all_servo_data3 = []
        self.all_servo_data4 = []
        self.all_servo_data5 = []
        self.all_servo_data6 = []
        for i in range(1, 7):
            setattr(self, f'all_servo_data{i}', [])

        self.serial_connection = None

        # 创建堆叠窗口
        # self.stacked_widget = QStackedWidget(self)
        # self.setCentralWidget(self.stacked_widget)

        # main_page = QWidget()
        # main_layout = QVBoxLayout(main_page)
        # settings_button = QPushButton("设置", self)
        # settings_button.clicked.connect(self.show_settings)
        # main_layout.addWidget(settings_button)
        # self.stacked_widget.addWidget(main_page)
        #
        # settings_page = SettingsPage(self)
        # self.stacked_widget.addWidget(settings_page)

        button_style = """
            QPushButton {
                background-color: rgba(110, 0, 0, 70); /* 完全透明的背景 */
                border: 1px solid rgba(0, 0, 0, 180); /* 半透明的边框 */
                color: white;
                border-width: 2px;
                border-radius: 10px;
                border-style: solid;
                border-color: darkgray;
                padding: 10px;
                font-size:20px; 
                box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
            }
            QPushButton:hover {
                background-color: rgba(240, 240, 240, 150);
            }
            QPushButton:pressed {
                background-color: rgba(200, 200, 200, 180);
                border-style: inset;
            }
            QPushButton:focus {
                outline: none; /* 移除焦点矩形 */
            }
        """

        styles = """
        QMainWindow {
            background-color: rgba(240, 232, 255, 180); /* 灰色背景，半透明 */
            border-radius: 10px; /* 圆角 */
        }

        QLabel {
            color:0f0f0f;
            font-size: 20px; 
            font-weight: bold;
            text-align: center;
        }

        QComboBox {
            background-color: rgba(255, 233, 255, 70); /* 白色背景，半透明 */
            color: black;
            border: 1px solid gray;
            border-radius:10px; /* 圆角 */
            padding: 10px;
            font-size: 20px; 
        }
        QComboBox QAbstractItemView {
                selection-background-color: #DADADA;
                selection-color: black;
                background-color: white;
                color: #133333;
                padding: 5px;
                outline: none;
                border: -3px solid transparent; /* 添加透明边框 */
                border-radius: 5px; /* 设置圆角 */
            }
        
            QComboBox QAbstractItemView::item {
                padding: 5px; /* 给每个菜单项增加内边距 */
            }
        
            QComboBox QAbstractItemView::item:selected {
                background-color: #DADADA;
                color: black;
            }
        
            QComboBox QAbstractItemView::indicator {
                width: 16px;
                height: 16px;
            }
        
            QComboBox QAbstractItemView::indicator:alternate {
                background-color: #E0E0E0;
            }
        
            QComboBox QAbstractItemView::indicator:pressed {
                background-color: #C0C0C0;
            }
        
            QComboBox QAbstractItemView::indicator:unchecked {
                image: url(:/resources/unchecked.png);
            }
        
            QComboBox QAbstractItemView::indicator:checked {
                image: url(:/resources/checked.png);
            }
        
            QComboBox QAbstractItemView::indicator:disabled {
                image: url(:/resources/disabled.png);
            }
        """

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # 创建一个栅格布局
        self.grid_layout = QGridLayout(central_widget)

        # 标签
        label = QLabel('串口:', self)
        self.grid_layout.addWidget(label, 0, 0)

        # 串口选择下拉菜单
        self.combo_serial = QComboBox(self)
        self.populate_serial_ports()
        self.grid_layout.addWidget(self.combo_serial, 0, 1)
        self.combo_serial.setStyleSheet(styles)

        # 波特率选择标签
        label_baudrate = QLabel('波特率:', self)
        self.grid_layout.addWidget(label_baudrate, 0, 2)

        self.combo_baudrate = QComboBox(self)
        self.combo_baudrate.addItems(['115200', '19200', '38400', '就这些了', '114514'])
        self.grid_layout.addWidget(self.combo_baudrate, 0, 3)
        self.combo_baudrate.setStyleSheet(styles)

        # 刷新串口按钮
        button_refresh = QPushButton('刷新', self)
        button_refresh.setStyleSheet(button_style)
        button_refresh.clicked.connect(self.populate_serial_ports)
        self.grid_layout.addWidget(button_refresh, 0, 4)

        # 连接串口按钮
        button_connect = QPushButton('链接', self)
        button_connect.setStyleSheet(button_style)
        button_connect.clicked.connect(self.connect_serial)
        self.grid_layout.addWidget(button_connect, 0, 5)

        # 断开串口按钮
        button_disconnect = QPushButton('断开', self)
        button_disconnect.setStyleSheet(button_style)
        button_disconnect.clicked.connect(self.disconnect_serial)
        self.grid_layout.addWidget(button_disconnect, 0, 6)

        button_all_tx = QPushButton('并发', self)
        button_all_tx.setStyleSheet(button_style)
        button_all_tx.clicked.connect(self.alltx)
        self.grid_layout.addWidget(button_all_tx, 0, 7)

        button_init = QPushButton('初始化', self)
        button_init.setStyleSheet(button_style)
        button_init.clicked.connect(self.inittx)
        self.grid_layout.addWidget(button_init, 0, 8)

        button_style1 = """
            QPushButton {
                background-color: rgba(220, 0, 0, 110); /* 完全透明的背景 */
                border: 1px solid rgba(110, 110, 0, 180); /* 半透明的边框 */
                color: white;
                border-width: 2px;
                border-radius: 10px;
                border-style: solid;
                border-color: darkgray;
                padding: 10px;
                font-size: 20px; 
                box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
            }
            QPushButton:hover {
                background-color: rgba(240, 240, 240, 150);
            }
            QPushButton:pressed {
                background-color: rgba(200, 200, 200, 180);
                border-style: inset;
            }
            QPushButton:focus {
                outline: none; /* 移除焦点矩形 */
            }
        """

        button_action_log_1 = QPushButton('记录为预设一', self)
        button_action_log_1.setStyleSheet(button_style1)
        button_action_log_1.clicked.connect(lambda: self.log_action(1))
        self.grid_layout.addWidget(button_action_log_1, 21, 6)

        button_action_log_2 = QPushButton('记录为预设二', self)
        button_action_log_2.setStyleSheet(button_style1)
        button_action_log_2.clicked.connect(lambda: self.log_action(2))
        self.grid_layout.addWidget(button_action_log_2, 21, 7)

        button_action_log_3 = QPushButton('记录为预设三', self)
        button_action_log_3.setStyleSheet(button_style1)
        button_action_log_3.clicked.connect(lambda: self.log_action(3))
        self.grid_layout.addWidget(button_action_log_3, 21, 8)

        button_action_log_4 = QPushButton('记录为预设四', self)
        button_action_log_4.setStyleSheet(button_style1)
        button_action_log_4.clicked.connect(lambda: self.log_action(4))
        self.grid_layout.addWidget(button_action_log_4, 23, 6)

        button_action_log_5 = QPushButton('记录为预设五', self)
        button_action_log_5.setStyleSheet(button_style1)
        button_action_log_5.clicked.connect(lambda: self.log_action(5))
        self.grid_layout.addWidget(button_action_log_5, 23, 7)

        button_action_log_6 = QPushButton('记录为预设六', self)
        button_action_log_6.setStyleSheet(button_style1)
        button_action_log_6.clicked.connect(lambda: self.log_action(6))
        self.grid_layout.addWidget(button_action_log_6, 23, 8)

        button_style2 = """
            QPushButton {
                background-color: rgba(220, 200, 0, 110); /* 完全透明的背景 */
                border: 1px solid rgba(110, 110, 0, 180); /* 半透明的边框 */
                color: white;
                border-width: 2px;
                border-radius: 10px;
                border-style: solid;
                border-color: darkgray;
                padding: 10px;
                font-size: 20px; 
                box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
            }
            QPushButton:hover {
                background-color: rgba(240, 240, 240, 150);
            }
            QPushButton:pressed {
                background-color: rgba(200, 200, 200, 180);
                border-style: inset;
            }
            QPushButton:focus {
                outline: none; /* 移除焦点矩形 */
            }
        """

        button_active_send_1 = QPushButton('预设一发送', self)
        button_active_send_1.setStyleSheet(button_style2)
        button_active_send_1.clicked.connect(lambda: self.data_and_send(1))
        self.grid_layout.addWidget(button_active_send_1, 20, 6)

        button_active_send_2 = QPushButton('预设二发送', self)
        button_active_send_2.setStyleSheet(button_style2)
        button_active_send_2.clicked.connect(lambda: self.data_and_send(2))
        self.grid_layout.addWidget(button_active_send_2, 20, 7)

        button_active_send_3 = QPushButton('预设三发送', self)
        button_active_send_3.setStyleSheet(button_style2)
        button_active_send_3.clicked.connect(lambda: self.data_and_send(3))
        self.grid_layout.addWidget(button_active_send_3, 20, 8)

        button_active_send_4 = QPushButton('预设四发送', self)
        button_active_send_4.setStyleSheet(button_style2)
        button_active_send_4.clicked.connect(lambda: self.data_and_send(4))
        self.grid_layout.addWidget(button_active_send_4, 22, 6)

        button_active_send_5 = QPushButton('预设五发送', self)
        button_active_send_5.setStyleSheet(button_style2)
        button_active_send_5.clicked.connect(lambda: self.data_and_send(5))
        self.grid_layout.addWidget(button_active_send_5, 22, 7)

        button_active_send_6 = QPushButton('预设六发送', self)
        button_active_send_6.setStyleSheet(button_style2)
        button_active_send_6.clicked.connect(lambda: self.data_and_send(6))
        self.grid_layout.addWidget(button_active_send_6, 22, 8)

        styles = """
        QTextEdit {
            border: 2px solid #ccc;
            border-radius: 16px;  /* 设置圆角半径 */
            font-family: Arial;
            font-size: 20px; 
            padding: 5px;
            background-color: #e0f0f0;
        }
        """

        self.text_display = QTextEdit(self)
        self.text_display.setReadOnly(True)
        self.grid_layout.addWidget(self.text_display, 20, 0, 4, 6)
        self.text_display.setStyleSheet(styles)
        # 设置窗口标题
        self.setWindowTitle("Main Window")
        for i in range(16):
            self.main_loop_gui(i)
            if i < 15:
                line = QFrame(self)
                line.setFrameShape(QFrame.HLine)
                line.setFrameShadow(QFrame.Sunken)
                self.grid_layout.addWidget(line, i + 1, 0, 2, 9)

    def __del__(self):
        self.log_file.close()

    def save_presets(self):
        """保存预设数据到文件"""
        presets = {'all_servo_data1': self.all_servo_data1,
                   'all_servo_data2': self.all_servo_data2,
                   'all_servo_data3': self.all_servo_data3,
                   'all_servo_data4': self.all_servo_data4,
                   'all_servo_data5': self.all_servo_data5,
                   'all_servo_data6': self.all_servo_data6, }

        with open(os.path.join(os.getcwd(), 'presets.json'), 'w') as f:
            json.dump(presets, f)

    def load_presets(self):
        """从文件加载预设数据"""
        try:
            with open(os.path.join(os.getcwd(), 'presets.json'), 'r') as f:
                presets = json.load(f)
                self.all_servo_data1 = presets.get('all_servo_data1', [])
                self.all_servo_data2 = presets.get('all_servo_data2', [])
                self.all_servo_data3 = presets.get('all_servo_data3', [])
                self.all_servo_data4 = presets.get('all_servo_data4', [])
                self.all_servo_data5 = presets.get('all_servo_data5', [])
                self.all_servo_data6 = presets.get('all_servo_data6', [])
        except Exception as e:
            print(f"Error loading presets: {e}")

    def main_loop_gui(self, index):
        self.default_values = [
            {"name": "left_hand1", "id": 1, "angle": "120", "time": 30},
            {"name": "left_hand2", "id": 13, "angle": "30", "time": 30},
            {"name": "left_hand3", "id": 15, "angle": "120", "time": 30},

            {"name": "right_hand1", "id": 2, "angle": "125", "time": 30},
            {"name": "right_hand2", "id": 14, "angle": "210", "time": 30},
            {"name": "right_hand3", "id": 16, "angle": "120", "time": 30},

            {"name": "left_leg1", "id": 3, "angle": "117", "time": 30},
            {"name": "left_leg2", "id": 5, "angle": "105", "time": 30},
            {"name": "left_leg3", "id": 6, "angle": "130", "time": 30},
            {"name": "left_leg4", "id": 7, "angle": "120", "time": 30},
            {"name": "left_leg5", "id": 8, "angle": "116", "time": 30},

            {"name": "right_leg1", "id": 4, "angle": "108", "time": 30},
            {"name": "right_leg2", "id": 9, "angle": "135", "time": 30},
            {"name": "right_leg3", "id": 10, "angle": "120", "time": 30},
            {"name": "right_leg4", "id": 11, "angle": "135", "time": 30},
            {"name": "right_leg5", "id": 12, "angle": "148", "time": 30}
        ]

        button_style = """
            QPushButton {
                background-color: rgba(11, 120, 120, 70); /* 完全透明的背景 */
                border: 1px solid rgba(10, 220, 220, 180); /* 半透明的边框 */
                color: white;
                border-width: 2px;
                border-radius: 10px;
                border-style: solid;
                border-color: darkgray;
                padding: 10px;
                font-size: 20px; 
                box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
            }
            QPushButton:hover {
                background-color: rgba(240, 240, 240, 150);
            }
            QPushButton:pressed {
                background-color: rgba(200, 200, 200, 180);
                border-style: inset;
            }
            QPushButton:focus {
                outline: none; /* 移除焦点矩形 21*/
            }
        """

        input_style = """
        QLineEdit {
            border: 2px solid #1cc;
            border-radius: 10px;
            padding: 5px;
            background-color: #f0f0f0;
            color: #333;
            font-size: 20px; 
            selection-background-color: #3465a4;
            outline: none;
        }

        QLineEdit:focus {
            border: 4px solid #1465a4;
        }
        """

        input_style_imput_QSpinBox = """
            QSpinBox {
                color: #000000; /* 文本颜色 */
                background-color: rgba(251, 250, 250, 180); /* 背景颜色 */
                selection-background-color: #03033; /* 选中文本的背景颜色 */
                border: 2px groove rgba(22, 220, 220, 80); /* 边框样式 */
                border-radius: 16px; /* 边框圆角 */
                font-size: 20px; /* 字体大小 */
                padding: 10px; /* 内边距 */
                min-width: 10em; /* 最小宽度 */
            }

            QSpinBox::up-button {
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-style: solid;
                border-top-right-radius: 16px;
                border-bottom-right-radius: 0;
                background-color: rgba(121, 120, 172, 150);
            }

            QSpinBox::down-button {
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                width: 20px;
                border-left-width: 1px;
                border-left-style: solid;
                border-bottom-right-radius: 16px;
                border-top-right-radius: 0;
                background-color: rgba(241, 170, 120, 150);
            }

            QSpinBox::up-arrow, QSpinBox::down-arrow {
                width: 20px;
                height: 20px;
            }

            QSpinBox::up-arrow {
                image: url(arrow_up_icon.png);
            }

            QSpinBox::down-arrow {
                image: url(arrow_down_icon.png);
            }
        """

        values_for_row = self.default_values[index]  # 获取对应行的字典

        name_input = QLineEdit(values_for_row["name"], self)
        name_input.setMinimumWidth(40)
        name_input.setMaximumWidth(200)
        name_input.setStyleSheet(input_style)

        id_input = QLineEdit(str(values_for_row["id"]), self)
        id_input.setMinimumWidth(40)
        id_input.setMaximumWidth(200)
        id_input.setStyleSheet(input_style)

        angle_input = QSpinBox(self)
        angle_input.setMinimum(0)
        angle_input.setMaximum(240)
        angle_input.setValue(int(values_for_row["angle"]))
        angle_input.setSingleStep(2)
        angle_input.setMinimumWidth(40)
        angle_input.setMaximumWidth(200)
        angle_input.setStyleSheet(input_style_imput_QSpinBox)

        time_input = QSpinBox(self)
        time_input.setMinimum(0)
        time_input.setMaximum(500)
        time_input.setValue(int(values_for_row["time"]))
        time_input.setSingleStep(10)
        time_input.setMinimumWidth(40)
        time_input.setMaximumWidth(200)
        time_input.setStyleSheet(input_style_imput_QSpinBox)

        label_style = """
            QLabel {
                color: #000F00; /* 白色文本 */
                background-color: rgba(200, 200, 200, 80); /* 半透明的背景 */
                border: 2px groove rgba(180, 180, 180, 50); /* 半透明的沟槽边框 */
                border-radius: 16px; /* 圆角半径 */
                font-size: 20px; 
                padding: 10px; /* 内边距 */
                margin: 5px; /* 外边距 */
                text-align: center; /* 文本居中 */
            }
        """

        label_name = QLabel(f'名{index + 1}:')
        label_name.setStyleSheet(label_style)

        label_id = QLabel("ID:")
        label_id.setStyleSheet(label_style)

        label_angle = QLabel("角度:")
        label_angle.setStyleSheet(label_style)

        label_time = QLabel("时间:")
        label_time.setStyleSheet(label_style)

        # 文本居中
        label_name.setAlignment(Qt.AlignCenter)
        label_id.setAlignment(Qt.AlignCenter)
        label_angle.setAlignment(Qt.AlignCenter)
        label_time.setAlignment(Qt.AlignCenter)
        # 添加控件到网格布局
        self.grid_layout.addWidget(label_name, index + 1, 0)
        self.grid_layout.addWidget(name_input, index + 1, 1)
        self.grid_layout.addWidget(label_id, index + 1, 2)
        self.grid_layout.addWidget(id_input, index + 1, 3)
        self.grid_layout.addWidget(label_angle, index + 1, 4)
        self.grid_layout.addWidget(angle_input, index + 1, 5)
        self.grid_layout.addWidget(label_time, index + 1, 6)
        self.grid_layout.addWidget(time_input, index + 1, 7)

        self.inputs.append([name_input, id_input, angle_input, time_input])

        single_ctrl_connect = QPushButton('控制', self)
        single_ctrl_connect.setStyleSheet(button_style)
        single_ctrl_connect.clicked.connect(lambda: self.on_single_ctrl_connect_clicked(index))
        self.grid_layout.addWidget(single_ctrl_connect, index + 1, 8)

    # def show_settings(self):
    #     # 当点击设置按钮时，切换到设置界面
    #     self.stacked_widget.setCurrentIndex(1)

    def on_single_ctrl_connect_clicked(self, index):
        """
        单个发送
        :param index:
        :return:
        """
        if self.serial_connection is None:
            self.print_to_textbox('//请先连接串口', Qt.red)
            QMessageBox.information(
                self, '状态',
                '请先链接串口！！！嘿嘿 '
            )
            return
        name_input, id_input, angle_input, time_input = self.inputs[index]
        name = name_input.text()
        id = id_input.text()
        angle = angle_input.text()
        time = time_input.text()

        print(f'Name: {name}, ID: {id}, Angle: {angle}, Time: {time}')
        self.ctrl_servo(name, id, angle, time)
        self.print_to_textbox(f"{name}.Do({angle},{time},0,0);")

    def alltx(self, index):
        """
         一次性发送
        :param index:
        :return:
        """
        if self.serial_connection is None:
            self.print_to_textbox('//请先连接串口', Qt.red)
            QMessageBox.information(
                self, '状态',
                '请先链接串口！！！嘿嘿 '
            )
            return
        for index in range(len(self.inputs)):
            name_input, id_input, angle_input, time_input = self.inputs[index]

            name_value = name_input.text()
            id_value = id_input.text()
            angle_value = angle_input.text()
            time_value = time_input.text()

            self.print_to_textbox(f"{name_value}.Do({angle_value},{time_value},0,0);", Qt.blue)
            self.ctrl_servo(name_value, id_value, angle_value, time_value)

    def inittx(self):
        """
        初始化发送
        :return:
        """
        if self.serial_connection is None:
            self.print_to_textbox('//请先连接串口', Qt.red)
            QMessageBox.information(
                self, '状态',
                '请先链接串口！！！嘿嘿 '
            )
            return
        try:
            for values in self.default_values:
                name = values["name"]
                id = values["id"]
                angle = values["angle"]
                time = values["time"]

                self.ctrl_servo(name, id, angle, time)
                self.print_to_textbox(f"{name}.Do({angle},{time},0,0);", Qt.red)
        except Exception as e:
            print(f"Error occurred: {e}")

    def log_action(self, num):
        if num == 1:
            self.all_servo_data1 = []
            for i in range(len(self.inputs)):
                name_input, id_input, angle_input, time_input = self.inputs[i]
                name_value = name_input.text()  # 获取name的文本值
                id_value = id_input.text()  # 获取id的文本值
                angle_value = angle_input.text()  # 获取angle的文本值
                time_value = time_input.text()  # 获取time的文本值
                servo_data = {
                    'name' : name_value,
                    'id'   : id_value,
                    'angle': angle_value,
                    'time' : time_value
                }
                self.all_servo_data1.append(servo_data)
            self.print_to_textbox('//记录为预设一')
            self.save_presets()
        elif num == 2:
            self.all_servo_data2 = []
            for i in range(len(self.inputs)):
                name_input, id_input, angle_input, time_input = self.inputs[i]
                name_value = name_input.text()  # 获取name的文本值1
                id_value = id_input.text()  # 获取id的文本值
                angle_value = angle_input.text()  # 获取angle的文本值
                time_value = time_input.text()  # 获取time的文本值

                servo_data = {
                    'name' : name_value,
                    'id'   : id_value,
                    'angle': angle_value,
                    'time' : time_value
                }
                self.all_servo_data2.append(servo_data)
            self.print_to_textbox('//记录为预设二')
            self.save_presets()
        elif num == 3:
            self.all_servo_data3 = []
            for i in range(len(self.inputs)):
                name_input, id_input, angle_input, time_input = self.inputs[i]
                name_value = name_input.text()  # 获取name的文本值
                id_value = id_input.text()  # 获取id的文本值
                angle_value = angle_input.text()  # 获取angle的文本值
                time_value = time_input.text()  # 获取time的文本值

                servo_data = {
                    'name' : name_value,
                    'id'   : id_value,
                    'angle': angle_value,
                    'time' : time_value
                }
                self.all_servo_data3.append(servo_data)
            self.print_to_textbox('//记录为预设三')
            self.save_presets()

        elif num == 4:
            self.all_servo_data4 = []
            for i in range(len(self.inputs)):
                name_input, id_input, angle_input, time_input = self.inputs[i]
                name_value = name_input.text()  # 获取name的文本值
                id_value = id_input.text()  # 获取id的文本值
                angle_value = angle_input.text()  # 获取angle的文本值
                time_value = time_input.text()  # 获取time的文本值
                servo_data = {
                    'name' : name_value,
                    'id'   : id_value,
                    'angle': angle_value,
                    'time' : time_value
                }

                self.all_servo_data4.append(servo_data)
            self.print_to_textbox('//记录为预设四')
            self.save_presets()
        elif num == 5:
            self.all_servo_data5 = []
            for i in range(len(self.inputs)):
                name_input, id_input, angle_input, time_input = self.inputs[i]
                name_value = name_input.text()  # 获取name的文本值
                id_value = id_input.text()  # 获取id的文本值
                angle_value = angle_input.text()  # 获取angle的文本值
                time_value = time_input.text()  # 获取time的文本值

                servo_data = {
                    'name' : name_value,
                    'id'   : id_value,
                    'angle': angle_value,
                    'time' : time_value
                }

                self.all_servo_data5.append(servo_data)
            self.print_to_textbox('//记录为预设五')
            self.save_presets()
        elif num == 6:
            self.all_servo_data6 = []
            for i in range(len(self.inputs)):
                name_input, id_input, angle_input, time_input = self.inputs[i]
                name_value = name_input.text()  # 获取name的文本值
                id_value = id_input.text()  # 获取id的文本值
                angle_value = angle_input.text()  # 获取angle的文本值
                time_value = time_input.text()  # 获取time的文本值

                servo_data = {
                    'name' : name_value,
                    'id'   : id_value,
                    'angle': angle_value,
                    'time' : time_value
                }

                self.all_servo_data6.append(servo_data)
            self.print_to_textbox('//记录为预设六')
            self.save_presets()

    def data_and_send(self, num):
        if self.serial_connection is None:
            self.print_to_textbox('//请先连接串口', Qt.red)
            QMessageBox.information(
                self, '状态',
                '请先链接串口！！！嘿嘿 '
            )
            return
        if num == 1:
            self.load_presets()
            if not self.all_servo_data1:
                self.print_to_textbox('//预设一为空', Qt.red)
                return
            self.print_to_textbox('//发送预设一')

            for servo_data in self.all_servo_data1:
                self.ctrl_servo(servo_data['name'], servo_data['id'], servo_data['angle'], servo_data['time'])
                self.print_to_textbox(f"{servo_data['name']}.Do({servo_data['angle']}, {servo_data['time']},0,0);")



        elif num == 2:
            self.load_presets()
            if not self.all_servo_data2:
                self.print_to_textbox('//预设二为空', Qt.red)
                return
            self.print_to_textbox('//发送预设二')

            for servo_data in self.all_servo_data2:
                self.ctrl_servo(servo_data['name'], servo_data['id'], servo_data['angle'], servo_data['time'])
                self.print_to_textbox(f"{servo_data['name']}.Do({servo_data['angle']}, {servo_data['time']},0,0);")



        elif num == 3:
            self.load_presets()
            if not self.all_servo_data3:
                self.print_to_textbox('//预设三为空', Qt.red)
                return
            self.print_to_textbox('//发送预设三')

            for servo_data in self.all_servo_data3:
                self.ctrl_servo(servo_data['name'], servo_data['id'], servo_data['angle'], servo_data['time'])
                self.print_to_textbox(f"{servo_data['name']}.Do({servo_data['angle']}, {servo_data['time']},0,0);")



        elif num == 4:
            self.load_presets()
            if not self.all_servo_data4:
                self.print_to_textbox('//预设四为空', Qt.red)
                return
            self.print_to_textbox('//发送预设四')

            for servo_data in self.all_servo_data4:
                self.ctrl_servo(servo_data['name'], servo_data['id'], servo_data['angle'], servo_data['time'])
                self.print_to_textbox(f"{servo_data['name']}.Do({servo_data['angle']}, {servo_data['time']},0,0);")



        elif num == 5:
            self.load_presets()
            if not self.all_servo_data5:
                self.print_to_textbox('//预设五为空', Qt.red)
                return
            self.print_to_textbox('//发送预设五')

            for servo_data in self.all_servo_data5:
                self.ctrl_servo(servo_data['name'], servo_data['id'], servo_data['angle'], servo_data['time'])
                self.print_to_textbox(f"{servo_data['name']}.Do({servo_data['angle']}, {servo_data['time']},0,0);")



        elif num == 6:
            self.load_presets()
            if not self.all_servo_data6:
                self.print_to_textbox('//预设六为空', Qt.red)
                return
            self.print_to_textbox('//发送预设六')

            for servo_data in self.all_servo_data6:
                self.ctrl_servo(servo_data['name'], servo_data['id'], servo_data['angle'], servo_data['time'])
                self.print_to_textbox(f"{servo_data['name']}.Do({servo_data['angle']}, {servo_data['time']},0,0);")

    def ctrl_servo(self, name, id, angle, time):
        """控制舵机"""
        try:
            if self.serial_connection and self.serial_connection.is_open:
                self.servo = servo.UBT_SERVO(self.serial_connection, int(id))
                self.servo.servo_do(int(angle), int(time), 0, 0)

        except ValueError:
            self.print_to_textbox("ID 必须是一个整数")
        except Exception as e:
            print(e)
            if self.servo:
                del self.servo
                self.servo = None

    def print_to_textbox(self, text, color=Qt.black):
        """
        向文本展示框中添加文本。

        :param text: 要添加的文本字符串
        :param color: 文本的颜色，默认为黑色
        """
        cursor = self.text_display.textCursor()  # 获取当前光标
        char_format = cursor.charFormat()  # 获取当前字符格式
        char_format.setForeground(QColor(color))  # 设置文本颜色
        cursor.setCharFormat(char_format)  # 应用字符格式
        cursor.insertText(text + '\n')  # 插入文本
        self.text_display.setTextCursor(cursor)  # 更新文本框的光标
        self.text_display.ensureCursorVisible()  # 确保光标可见
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 获取当前时间
        log_message = f"[{timestamp}] {text}\n"
        self.log_file.write(log_message)  # 写入文件
        self.log_file.flush()  # 立即刷新文件缓冲区

    def populate_serial_ports(self):
        """刷新串口列表"""
        available_ports = list(serial.tools.list_ports.comports())
        self.combo_serial.clear()
        for port_info in available_ports:
            self.combo_serial.addItem(port_info.device)

    def connect_serial(self):
        """尝试连接串口"""
        if not self.serial_connection:
            try:
                selected_port = self.combo_serial.currentText()
                baud_rate = int(self.combo_baudrate.currentText())
                self.serial_connection = serial.Serial(selected_port, baud_rate)
                logger.info(f'Successfully connected to {selected_port} at baud rate {baud_rate}')
                self.print_to_textbox(f'//成功链接{selected_port} 波特率：{baud_rate}')
                # QMessageBox.information(
                #     self, '状态',
                #     f'成功链接{selected_port} 波特率：{baud_rate} '
                # )
            except serial.SerialException as e:
                logger.error(f"Serial connection failed: {e}")
                self.print_to_textbox(f'//连接失败{e}')
                # QMessageBox.warning(
                #     self, '连接错误',
                #     f'串口连接失败: {e}\n\n可能是串口被占用或设备不存在'
                # )
            except ValueError:

                logger.error("Invalid baud rate value.")
                self.print_to_textbox('//波特率值无效，请检查输入')
                # QMessageBox.warning(
                #     self, '连接错误',
                #     '波特率值无效，请检查输入'
                # )
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                # detailed_error = traceback.format_exc()
                # QMessageBox.warning(
                #     self, '连接错误',
                #     f'连接失败: {e}\n\n{detailed_error}'
                # )
                self.print_to_textbox(f'//连接失败{e}')
            finally:
                if not self.serial_connection:
                    logger.warning("Connection attempt failed, closing any open resources.")
                    if self.serial_connection and self.serial_connection.is_open:
                        self.serial_connection.close()

    def disconnect_serial(self):
        """断开串口连接"""
        if self.serial_connection and self.serial_connection.is_open:
            try:
                self.serial_connection.close()
                self.serial_connection = None
                logger.info("Serial connection closed successfully.")
                self.print_to_textbox('//已断开连接')
                # QMessageBox.information(self, '状态', '已断开连接')
            except Exception as e:
                logger.error(f"Failed to close serial connection: {e}")
                self.print_to_textbox(f'//断开失败{e}')
                # QMessageBox.warning(
                #     self, '断开错误',
                #     f'断开连接失败: {e}\n\n可能是串口正在使用中'
                # )

    # def check_serial_port_status(self):
    #     if self.serial_port.isOpen():
    #         self.led_indicator.setColor(Qt.green)
    #         self.led_indicator.original_color = Qt.green
    #     else:
    #         self.led_indicator.setColor(Qt.red)
    #         self.led_indicator.original_color = Qt.red


# class SettingsPage(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         layout = QVBoxLayout(self)
#         self.back_button = QPushButton("返回", self)
#         self.back_button.clicked.connect(self.return_to_main)
#         layout.addWidget(self.back_button)
#
#     def return_to_main(self):
#         self.parent().stacked_widget.setCurrentIndex(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
