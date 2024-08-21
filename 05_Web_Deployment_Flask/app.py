from flask import Flask, render_template, request, jsonify
import threading
import speech_recognition as sr
import pyttsx3
from openai import OpenAI
import os
import multiprocessing

# 设置环境变量
os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['all_proxy'] = 'socks5://127.0.0.1:7890'

app = Flask(__name__)

# 初始化 OpenAI API 用于文本交互
client = OpenAI(
    # api_key="这里填写您的API Key",
    base_url="https://aihubmix.com/v1"
)

def speak_text(text):
    """将文本转换为语音"""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()  # 启动 TTS 引擎并等待其完成说话任务

def recognize_speech_from_mic():
    """从麦克风捕获音频并进行语音识别"""
    recognizer = sr.Recognizer()  # 创建一个语音识别器类
    with sr.Microphone() as source:
        print("请说话...")
        audio = recognizer.listen(source, timeout=8, phrase_time_limit=5)

    try:
        print("语音识别中...")
        query = recognizer.recognize_google(audio, language="zh-CN")  # 美式英语：en-US 中文：zh-CN
        print(f"您刚才说的是: {query}")
        return query
    except sr.UnknownValueError:
        print("无法理解语音")
        return None
    except sr.RequestError as e:
        print(f"无法请求结果; {e}")
        return None

history = [
    {"role": "system", "content": "你是由 OpenAI 训练的高级人工智能助手 ChatGPT。你将提供关于Colorful品牌电脑的购买和维护服务。"}
]

def chat(query, max_tokens=1500):
    history.append({"role": "user", "content": query})
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=history,
        temperature=0.3,
        max_tokens=max_tokens
    )
    
    result = completion.choices[0].message.content

    # 确保移除Markdown符号
    result = result.replace("*", "").replace("**", "")

    history.append({"role": "assistant", "content": result})
    return result

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat_mode():
    welcome_message = "文本交互模式启动\nColorful品牌电脑009号客服正在为您服务......"
    welcome_message = welcome_message.replace("\n", "<br>")
    return render_template('chat.html', welcome_message=welcome_message)

@app.route('/voice')
def voice_mode():
    welcome_message = "语音交互模式启动\nColorful品牌电脑009号客服正在为您服务......"
    speak_message = "语音交互模式启动。Colorful品牌电脑009号客服正在为您服务。"
    multiprocessing.Process(target=speak_text, args=(speak_message,)).start()
    welcome_message = welcome_message.replace("\n", "<br>")
    return render_template('voice.html', welcome_message=welcome_message)

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.form['query']
    response = chat(user_input)
    return jsonify({'response': response})

@app.route('/voice_query', methods=['POST'])
def voice_query():
    query = recognize_speech_from_mic()
    if query:
        response = chat(query)
        multiprocessing.Process(target=speak_text, args=(response,)).start()
        return jsonify({'response': response, 'query': query})
    else:
        return jsonify({'response': '无法理解语音，请再试一次。', 'query': ''})

if __name__ == "__main__":
    app.run(debug=True)
