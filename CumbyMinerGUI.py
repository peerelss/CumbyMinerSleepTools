import sys
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QTableWidget, QTableWidgetItem,
    QFileDialog, QLineEdit, QLabel
)
import re
from utils.miner_util_tools import parse_time_to_seconds, sleep_all_miner, wake_up_all_miner


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("机器控制面板")
        self.setGeometry(100, 100, 900, 600)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # === 上半部分 ===
        top_layout = QHBoxLayout()

        self.excel_path_input = QLineEdit()
        self.excel_path_input.setPlaceholderText("请选择 Excel 文件...")
        self.excel_path_input.setReadOnly(True)

        self.btn_select_excel = QPushButton("选择Excel")
        self.btn_select_excel.clicked.connect(self.select_excel)

        self.btn_wake = QPushButton("唤醒机器")
        self.btn_sleep = QPushButton("休眠机器")
        self.btn_sleep.clicked.connect(self.sleep_all_miner)
        self.btn_low_power = QPushButton("切换低功耗")

        top_layout.addWidget(self.excel_path_input)
        top_layout.addWidget(self.btn_select_excel)
        top_layout.addWidget(self.btn_wake)
        top_layout.addWidget(self.btn_sleep)
        top_layout.addWidget(self.btn_low_power)

        layout.addLayout(top_layout)

        # === 下半部分 ===
        bottom_layout = QHBoxLayout()

        # 左边文本框：IP输入
        self.ip_text = QTextEdit()
        self.ip_text.setPlaceholderText("请输入IP列表，每行一个IP")

        # 右边表格：显示Excel内容
        self.table = QTableWidget()

        bottom_layout.addWidget(self.ip_text, 1)
        bottom_layout.addWidget(self.table, 2)

        layout.addLayout(bottom_layout)

        self.setLayout(layout)

    def sleep_all_miner(self):
        if self.df is None:
            print("未加载数据")
            return

            # 新建一列：运行时长（秒）
        self.df["运行时长（秒）"] = self.df["启动时间"].astype(str).apply(parse_time_to_seconds)

        # 过滤出运行大于1秒的记录
        filtered_df = self.df[self.df["运行时长（秒）"] > 1]

        self.show_df(filtered_df)
        wake_up_all_miner(filtered_df)

    def wake_up_miner(self):
        pass

    def select_excel(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "选择文件", "", "表格文件 (*.xlsx *.xls *.csv);;所有文件 (*)"
        )
        if file_name:
            self.excel_path_input.setText(file_name)
            self.load_excel(file_name)

    def load_excel(self, file_path):
        try:
            if file_path.endswith((".xlsx", ".xls")):
                self.df = pd.read_excel(file_path)
            elif file_path.endswith(".csv"):
                self.df = pd.read_csv(file_path)
            else:
                print("不支持的文件格式")
                return
            self.show_df(self.df)
        except Exception as e:
            print("读取文件出错：", e)

    def show_df(self, df):
        self.table.setRowCount(len(df))
        self.table.setColumnCount(len(df.columns))
        self.table.setHorizontalHeaderLabels(df.columns.astype(str).tolist())

        for i in range(len(df)):
            for j in range(len(df.columns)):
                item = QTableWidgetItem(str(df.iat[i, j]))
                self.table.setItem(i, j, item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
