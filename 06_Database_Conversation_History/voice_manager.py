import speech_recognition as sr
import pyttsx3
import threading

class VoiceManager:
    def __init__(self):
        self.engine = pyttsx3.init()

    def speak_text(self, text):
        """将文本转换为语音"""
        self.engine.say(text)
        self.engine.runAndWait()

    def recognize_speech_from_mic(self):
        """从麦克风捕获音频并进行语音识别"""
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
            print("无法理解语音")
            return None
        except sr.RequestError as e:
            print(f"无法请求结果; {e}")
            return None

    def start_speaking_thread(self, text):
        threading.Thread(target=self.speak_text, args=(text,)).start()

    def start_recognizing_thread(self, callback):
        threading.Thread(target=self._process_recognition, args=(callback,)).start()

    def _process_recognition(self, callback):
        query = self.recognize_speech_from_mic()
        if query:
            callback(query)
