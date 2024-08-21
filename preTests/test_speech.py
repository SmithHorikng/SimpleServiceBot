# 文件名: test_speech.py
# 本程序将演示语音识别和文本转语音的基础使用方法
# 注意，文本转语音功能需要访问海外网络，可能会受到网络环境的影响(建议使用Clash全局代理)
# 当然也可以使用离线的 TTS 引擎pocketsphinx,尽管效果不如在线翻译服务，但也是十分不错的选择。

import speech_recognition as sr   # 用于语音识别 第三方库
import pyttsx3  # 用于文本转语音(TTS) 第三方库
import os

# 设置环境变量
os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['all_proxy'] = 'socks5://127.0.0.1:7890'

# 初始化 pyttsx3 语音引擎 (TTS)
engine = pyttsx3.init()

def speak_text(text):
    """将文本转换为语音"""
    engine.say(text)
    engine.runAndWait() # 启动 TTS 引擎并等待其完成说话任务

def recognize_speech_from_mic():
    """从麦克风捕获音频并进行语音识别"""
    recognizer = sr.Recognizer()    # 创建一个语音识别器类
    # Microphone 对象，表示使用计算机的麦克风作为音频源 
    # source 是一个局部变量，代表当前的音频输入源
    with sr.Microphone() as source: 
        print("请说话...")
        audio = recognizer.listen(source, timeout=8, phrase_time_limit=5)

    try:
        print("语音识别中...")
        query = recognizer.recognize_google(audio, language="zh-CN")    # 美式英语：en-US 中文：zh-CN
        print(f"您刚才说的是: {query}")
        return query
    except sr.UnknownValueError:
        print("无法理解语音")
        return None
    except sr.RequestError as e:
        print(f"无法请求结果; {e}")
        return None

# 使用 pyttsx3 进行文本转语音演示
text = "你好，欢迎使用语音识别和文本转语音演示程序。"
# text = "Hello, welcome to the speech recognition and text-to-speech demonstration program."
print(f"将文本转换为语音: {text}")
speak_text(text)

# 使用 SpeechRecognition 进行语音识别演示
print("请通过麦克风输入语音...")
recognized_text = recognize_speech_from_mic()
if recognized_text:
    print(f"识别到的文本: {recognized_text}")
else:
    print("未识别到任何文本")


# 拓展
# 方向一：使用开源的语音识别引擎 pocketsphinx 进行离线语音识别,需要安装第三方库，并且还需要下载语言模型等文件
# 方向二：使用百度的API进行语音识别和语音合成