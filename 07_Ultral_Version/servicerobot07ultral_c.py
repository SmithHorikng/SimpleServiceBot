import sys
import threading
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QStackedWidget, QTextEdit, QHBoxLayout
)
from PyQt5.QtGui import QPixmap, QFont, QPalette, QBrush
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMovie
import speech_recognition as sr
import pyttsx3
import os
from openai import OpenAI
import pygame
import sqlite3


# 设置环境变量
os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['all_proxy'] = 'socks5://127.0.0.1:7890'

# 初始化 OpenAI API 用于文本交互
client = OpenAI(
    # api_key="这里填写您的API Key",
    base_url="https://aihubmix.com/v1"
)

# 初始化语音引擎
engine = pyttsx3.init()

# 定义前置提示词 文本客服
prompt1_parts = {
    "角色": "你是Colorful品牌电脑的客服，负责回答客户的问题。",
    "风格": "请确保语言幽默诙谐，使用合适的表情符号，不要吝啬。要十分热情，并保持友好和耐心。",
    "格式": "回答时请使用纯文本格式，不要使用任何Markdown符号。尤其是*",
    "思维链": "请通过一步一步的思考（思维链），给出更优质且正确的答案。",
    "附加": "再次充分审视并把握我们的所有要求，给出优质答案，我将会非常感激，谢谢你！"
}

# 定义前置提示词 语音客服
prompt2_parts = {
    "角色": "你是Colorful品牌电脑的客服，负责回答客户的问题。",
    "风格": "请确保语言幽默诙谐，由于某些原因，我们不可以使用任何的表情及符号。要十分热情，并保持友好和耐心。",
    "格式": "回答时请使用纯文本格式，不要使用任何Markdown符号。尤其是*",
    "思维链": "请通过一步一步的思考（思维链），给出更优质且正确的答案。",
    "附加": "再次充分审视并把握我们的所有要求，给出优质答案，我将会非常感激，谢谢你！"
}


# 场景实例
scenarios = """
场景说明
场景一：新电脑购买咨询

用户背景：潜在客户想购买Colorful品牌的新电脑，对不同型号和配置不太了解。
用户问题：
“有哪些适合游戏的Colorful电脑推荐？”
“这款Colorful电脑的处理器是什么型号？”
“Colorful的电脑可选的内存和存储配置有哪些？”
“Colorful这款电脑是否支持扩展存储？”
客服回答：
列出适合游戏的Colorful电脑型号，并介绍每款电脑的显卡、处理器等关键配置。
提供具体型号的处理器信息，并解释其性能优势。
列出Colorful电脑可选的内存和存储配置，推荐适合用户需求的配置。
介绍Colorful电脑扩展存储的支持情况，包括硬盘接口类型和最大支持容量。

场景二：硬件保修服务

用户背景：购买过Colorful电脑的客户遇到硬件故障，需要保修服务。
用户问题：
“我的Colorful电脑开不了机，可能是什么问题？”
“保修期内如何申请维修？”
“Colorful的保修覆盖哪些硬件部件？”
“我的Colorful硬盘坏了，可以免费更换吗？”
客服回答：
根据用户描述，初步判断可能的问题并建议检查的部件。
提供申请维修的流程，包括如何提交故障报告和寄送设备。
解释Colorful的保修政策，列出覆盖的硬件部件和不在保修范围内的情况。
针对硬盘故障，确认是否在保修范围内并提供更换的具体步骤。

场景三：软件安装与系统维护

用户背景：客户需要在Colorful电脑上安装新的软件或维护现有系统。
用户问题：
“如何在Colorful电脑上安装最新的操作系统？”
“可以帮我在Colorful电脑上安装办公软件吗？”
“如何升级Colorful电脑的系统？”
“可以帮我在Colorful电脑上设置多系统启动吗？”
客服回答：
提供在Colorful电脑上安装最新操作系统的详细步骤或远程协助服务。
指导用户在Colorful电脑上安装常用的办公软件，并提供软件下载链接。
解释Colorful电脑系统升级的方法，包括备份数据和升级前的准备工作。
详细介绍在Colorful电脑上设置多系统启动的方法，包括分区和引导管理。

场景四：系统升级与硬件扩展

用户背景：客户需要在Colorful电脑上升级系统或增加硬件设备。
用户问题：
“如何在Colorful电脑上升级到最新的Windows系统？”
“我可以在Colorful电脑上增加一块固态硬盘吗？”
“如何在Colorful电脑上更换操作系统？”
“可以在Colorful电脑上安装额外的内存吗？”
客服回答：
提供在Colorful电脑上升级到最新Windows系统的详细教程，包括下载和安装步骤。
指导用户如何在Colorful电脑上增加固态硬盘，包括选择合适的硬盘和安装步骤。
详细解释在Colorful电脑上更换操作系统的方法，包括备份数据和安装新系统。
提供在Colorful电脑上安装额外内存的建议和步骤，确保用户选择兼容的内存模块。

场景五：软件安装服务

用户背景：客户需要在Colorful电脑上安装各类软件，以满足不同的工作和学习需求。
用户问题：
“可以帮我在Colorful电脑上安装最新的Windows系统吗？”
“如何在Colorful电脑上安装办公软件，比如Microsoft Office？”
“我需要在Colorful电脑上安装Photoshop，用于图像处理。”
“可以帮我在Colorful电脑上安装3D设计软件，比如AutoCAD吗？”
“如何在Colorful电脑上安装影视动画制作软件？”
“我需要在Colorful电脑上安装机械设计软件，比如SolidWorks。”
“可以帮我在Colorful电脑上安装建筑设计软件，比如Revit吗？”
“我需要在Colorful电脑上安装网页设计软件，有哪些推荐？”
“如何在Colorful电脑上安装开发编程工具，比如Visual Studio？”
“可以帮我在Colorful电脑上安装数据分析软件，比如R和Python吗？”
“如何在Colorful电脑上安装仿真模拟软件？”
“我需要在Colorful电脑上安装行业专用的软件，可以提供帮助吗？”
客服回答：
提供在Colorful电脑上各类软件的安装指南，包括下载、安装和激活步骤。
根据用户需求，推荐合适的软件版本和配置要求。
提供软件下载链接和正版软件购买渠道。
远程协助用户完成软件安装，并解决安装过程中遇到的问题。

场景细节描述
为了更贴近实际应用，可以进一步细化每个场景的细节。比如：

用户购买Colorful电脑时，可以设置用户对不同品牌、用途（游戏、办公、设计等）和预算的具体需求。
用户申请硬件保修时，可以细化到具体的故障现象和使用环境，以便客服提供更精准的诊断和处理建议。
用户进行系统维护和软件安装时，可以考虑用户的操作水平和已有的软件环境，提供更有针对性的指导。
用户进行硬件扩展时，可以设置用户的具体需求，如增加存储空间、提升性能等，并提供详细的扩展方案。
"""


# 构建提示词
def construct_prompt(parts, scenarios):
    return " ".join([f"{key}：{value}" for key, value in parts.items()]) + scenarios

class LoginPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        # 初始化 pygame 并加载音乐
        pygame.mixer.init()
        pygame.mixer.music.load('audio/show.mp3')
        pygame.mixer.music.play(-1)  # -1 表示循环播放

        # 设置背景图
        self.set_background('imgs/show2.gif')

        # 创建UI元素
        layout = QVBoxLayout()

        self.label = QLabel("Colorful大模型客服在线")
        self.label.setFont(QFont("华文楷体", 28, QFont.Bold))  # 使用更有艺术感的字体
        self.label.setAlignment(Qt.AlignCenter)  # 让标签居中显示
        self.label.setStyleSheet("color: #FF5733;")  # 修改颜色为非白色，例如橙红色
        layout.addWidget(self.label)

        self.username = QLineEdit(self)
        self.username.setPlaceholderText("用户名")
        self.username.setFont(QFont("Arial", 14))
        self.username.setStyleSheet("""
            background-color: rgba(255, 255, 255, 180);
            border: 2px solid #4CAF50;
            border-radius: 10px;
            padding: 5px;
        """)
        layout.addWidget(self.username)

        self.password = QLineEdit(self)
        self.password.setPlaceholderText("密码")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setFont(QFont("Arial", 14))
        self.password.setStyleSheet("""
            background-color: rgba(255, 255, 255, 180);
            border: 2px solid #4CAF50;
            border-radius: 10px;
            padding: 5px;
        """)
        layout.addWidget(self.password)

        self.login_button = QPushButton("登录")
        self.login_button.setFont(QFont("Arial", 14, QFont.Bold))
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.login_button.clicked.connect(self.check_login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def set_background(self, image_path):
        self.background_label = QLabel(self)
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        self.background_label.setScaledContents(True)

        movie = QMovie(image_path)
        self.background_label.setMovie(movie)
        movie.start()

    def resizeEvent(self, event):
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        super().resizeEvent(event)

    def check_login(self):
        username = self.username.text()
        password = self.password.text()

        if username == "root" and password == "1234":
            pygame.mixer.music.stop()  # 停止音乐播放
            self.stacked_widget.setCurrentIndex(1)  # 跳转到主页面
        else:
            self.label.setText("用户名或密码错误")
            self.label.setStyleSheet("color: red")

class ServiceRobotApp(QWidget):
    def __init__(self):
        super().__init__()
        self.history = []  # 初始化 history 列表
        self.init_db()  # 初始化数据库
        self.initUI()

    def init_db(self):
        self.conn = sqlite3.connect('chat_history.db')  # 连接到数据库文件
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_query TEXT NOT NULL,
                assistant_response TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def initUI(self):
        # 设置背景图
        self.set_background('imgs/page2.png')

        # 创建主布局
        layout = QVBoxLayout()

        # 创建水平布局，用于放置三个按钮（历史记录、清除记录、清屏）
        button_layout = QHBoxLayout()

        # 历史记录按钮
        self.history_button = QPushButton("历史记录", self)
        self.history_button.setFont(QFont("Arial", 14, QFont.Bold))
        self.history_button.setStyleSheet(self.get_button_style("blue"))
        self.history_button.clicked.connect(self.show_history)
        button_layout.addWidget(self.history_button)

        # 清除记录按钮
        self.clear_history_button = QPushButton("清除记录", self)
        self.clear_history_button.setFont(QFont("Arial", 14, QFont.Bold))
        self.clear_history_button.setStyleSheet(self.get_button_style("red"))
        self.clear_history_button.clicked.connect(self.clear_history)
        button_layout.addWidget(self.clear_history_button)

        # 清屏按钮
        self.clear_screen_button = QPushButton("清屏", self)
        self.clear_screen_button.setFont(QFont("Arial", 14, QFont.Bold))
        self.clear_screen_button.setStyleSheet(self.get_button_style("blue"))
        self.clear_screen_button.clicked.connect(self.clear_screen)
        button_layout.addWidget(self.clear_screen_button)

        # 将按钮布局添加到主布局
        layout.addLayout(button_layout)

        # 标签
        self.label = QLabel("请选择交互模式：", self)
        self.label.setFont(QFont("Arial", 18, QFont.Bold))
        self.label.setStyleSheet("color: white; background-color: rgba(0, 0, 0, 0);")
        layout.addWidget(self.label)

        # 文本交互按钮
        self.text_button = QPushButton("文本交互", self)
        self.text_button.setFont(QFont("Arial", 14, QFont.Bold))
        self.text_button.setStyleSheet(self.get_button_style())
        self.text_button.clicked.connect(self.start_text_mode)
        layout.addWidget(self.text_button)

        # 语音交互按钮
        self.voice_button = QPushButton("语音交互", self)
        self.voice_button.setFont(QFont("Arial", 14, QFont.Bold))
        self.voice_button.setStyleSheet(self.get_button_style())
        self.voice_button.clicked.connect(self.start_voice_mode)
        layout.addWidget(self.voice_button)

        # 退出按钮
        self.exit_button = QPushButton("退出", self)
        self.exit_button.setFont(QFont("Arial", 14, QFont.Bold))
        self.exit_button.setStyleSheet(self.get_button_style("red"))
        self.exit_button.clicked.connect(QApplication.instance().quit)
        layout.addWidget(self.exit_button)

        # 对话框
        self.dialog = QTextEdit(self)
        self.dialog.setReadOnly(True)
        self.dialog.setFont(QFont("Arial", 12))
        self.dialog.setStyleSheet("""
            background-color: rgba(255, 255, 255, 150);
            border: 2px solid #4CAF50;
            border-radius: 10px;
        """)
        layout.addWidget(self.dialog)

        # 输入框和发送按钮
        self.input_frame = QWidget(self)
        self.input_frame.hide()  # 初始隐藏输入框
        input_layout = QHBoxLayout()

        self.input_entry = QLineEdit(self.input_frame)
        self.input_entry.setFont(QFont("Arial", 14))
        self.input_entry.setStyleSheet(self.get_lineedit_style())
        input_layout.addWidget(self.input_entry)

        self.send_button = QPushButton("发送", self.input_frame)
        self.send_button.setFont(QFont("Arial", 14, QFont.Bold))
        self.send_button.setStyleSheet(self.get_button_style())
        self.send_button.clicked.connect(self.send_query)
        input_layout.addWidget(self.send_button)

        self.input_frame.setLayout(input_layout)
        layout.addWidget(self.input_frame)

        # 按住说话按钮
        self.speak_button = QPushButton("按住说话", self)
        self.speak_button.setFont(QFont("Arial", 14, QFont.Bold))
        self.speak_button.setStyleSheet(self.get_button_style())
        self.speak_button.clicked.connect(self.speak_query)
        self.speak_button.hide()  # 初始隐藏按住说话按钮
        layout.addWidget(self.speak_button)

        self.setLayout(layout)


    def show_history(self):
        self.dialog.clear()
        conn = sqlite3.connect('chat_history.db')
        cursor = conn.cursor()
        cursor.execute("SELECT user_query, assistant_response, timestamp FROM chat_history")
        rows = cursor.fetchall()
        conn.close()  # 关闭连接
        for row in rows:
            self.append_dialog(f"时间: {row[2]}\n用户: {row[0]}\n客服: {row[1]}\n" + "="*50)

    def clear_history(self):
        conn = sqlite3.connect('chat_history.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM chat_history")
        conn.commit()
        conn.close()  # 关闭连接
        self.append_dialog("历史记录已清除。")

    def set_background(self, image_path):
        self.setAutoFillBackground(True)
        palette = self.palette()
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        palette.setBrush(QPalette.Window, QBrush(pixmap))
        self.setPalette(palette)

    def resizeEvent(self, event):
        self.set_background('imgs/page2.png')  # 对于LoginPage，使用page1背景
        super().resizeEvent(event)

    def clear_screen(self):
        self.dialog.clear()  # 清空对话框内容
        
    def get_button_style(self, color="green"):
        color_map = {
            "red": "rgba(255, 0, 0, 180)",
            "blue": "rgba(0, 0, 255, 180)",
            "green": "rgba(76, 175, 80, 180)"
        }
        return f"""
            QPushButton {{
                background-color: {color_map[color]};
                color: white;
                border-radius: 10px;
                padding: 10px;
            }}
            QPushButton:hover {{
                background-color: {color_map[color].replace('180', '200')};
            }}
        """

    def get_lineedit_style(self):
        return """
            background-color: rgba(255, 255, 255, 180);
            border: 2px solid #4CAF50;
            border-radius: 10px;
            padding: 5px;
        """

    def append_dialog(self, text):
        self.dialog.append(text)

    def start_text_mode(self):
        self.append_dialog("文本交互模式启动...\nColorful品牌电脑009号客服正在为您服务......")
        self.set_prompt1()
        self.input_frame.show()
        self.speak_button.hide()

    def start_voice_mode(self):
        self.append_dialog("语音交互模式启动...\nColorful品牌电脑009号客服正在为您服务......")
        self.set_prompt2()
        threading.Thread(target=self.speak_text_initial).start()
        self.input_frame.hide()
        self.speak_button.show()

    def set_prompt1(self):
        prompt_base = construct_prompt(prompt1_parts, scenarios)
        self.history.append({"role": "system", "content": prompt_base})

    def set_prompt2(self):
        prompt_base = construct_prompt(prompt2_parts, scenarios)
        self.history.append({"role": "system", "content": prompt_base})

    def send_query(self):
        query = self.input_entry.text()
        if query:
            self.append_dialog("用户: " + query)
            threading.Thread(target=self.process_text_query, args=(query,)).start()
            self.input_entry.clear()

    def process_text_query(self, query):
        result = self.chat(query)
        self.append_dialog("客服: " + result)
        self.append_dialog("=" * 95)

        # 将对话记录保存到数据库
        self.save_to_db(query, result)

    def chat(self, query, max_tokens=1500):
        self.history.append({"role": "user", "content": query})
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.history,
            temperature=0.3,
            max_tokens=max_tokens
        )
        result = completion.choices[0].message.content
        result = result.replace("*", "").replace("**", "")
        self.history.append({"role": "assistant", "content": result})
        return result

    def speak_query(self):
        threading.Thread(target=self.process_voice_query).start()

    def process_voice_query(self):
        query = self.recognize_speech_from_mic()
        if query:
            self.append_dialog("用户: " + query)
            result = self.chat(query)
            self.append_dialog("客服: " + result)
            self.append_dialog("=" * 95)
            threading.Thread(target=self.speak_text, args=(result,)).start()

            # 将对话记录保存到数据库
            self.save_to_db(query, result)

    def save_to_db(self, user_query, assistant_response):
        # 在新的线程中创建新的数据库连接
        conn = sqlite3.connect('chat_history.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO chat_history (user_query, assistant_response) VALUES (?, ?)",
            (user_query, assistant_response)
        )
        conn.commit()
        conn.close()  # 关闭连接

    def recognize_speech_from_mic(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("请说话...")
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=5)

        try:
            print("语音识别中...")
            query = recognizer.recognize_google(audio, language="zh-CN")
            print(f"您刚才说的是: {query}")
            return query
        except sr.UnknownValueError:
            self.append_dialog("无法理解语音")
        except sr.RequestError as e:
            self.append_dialog(f"无法请求结果: {e}")
        return None

    def speak_text_initial(self):
        self.speak_text("Colorful品牌电脑009号客服正在为您服务......请问有什么可以帮助您的？")

    def speak_text(self, text):
        engine.say(text)
        engine.runAndWait()

class MainWindow(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.login_page = LoginPage(self)
        self.service_robot_app = ServiceRobotApp()

        self.addWidget(self.login_page)
        self.addWidget(self.service_robot_app)

        self.setFixedSize(1200, 800)
        self.setWindowTitle("Colorful 客服机器人")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
