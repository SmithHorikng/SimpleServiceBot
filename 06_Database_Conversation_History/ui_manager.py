import tkinter as tk
from tkinter import scrolledtext, Listbox, Toplevel, PhotoImage, messagebox
import threading
import sqlite3
from chat_manager import ChatManager
from voice_manager import VoiceManager
from db_manager import DBManager

class ServiceRobotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Colorful客服机器人")
        
        self.chat_manager = ChatManager()
        self.voice_manager = VoiceManager()
        self.db_manager = DBManager()

        # 设置右上角按钮框架
        self.top_right_frame = tk.Frame(root)
        self.top_right_frame.pack(side=tk.TOP, anchor='ne', padx=10, pady=10)
        
        # 设定图标大小为相同的像素值，确保显示一致
        icon_size = 40
        
        # 加载图标
        history_icon = PhotoImage(file="resources/history.png")
        clear_icon = PhotoImage(file="resources/clear.png")

        # 计算缩放比例并缩放图标
        history_icon = history_icon.subsample(history_icon.width() // icon_size)
        clear_icon = clear_icon.subsample(clear_icon.width() // icon_size)
        
        # 清理历史记录按钮
        self.clear_history_button = tk.Button(self.top_right_frame, image=clear_icon, command=self.clear_history)
        self.clear_history_button.image = clear_icon  # 保存引用
        self.clear_history_button.pack(side=tk.RIGHT, padx=5)        
        
        # 历史记录按钮
        self.history_button = tk.Button(self.top_right_frame, image=history_icon, command=self.show_history)
        self.history_button.image = history_icon  # 保存引用
        self.history_button.pack(side=tk.RIGHT, padx=5)

        # 设置交互模式选择框架在窗口的中央
        self.mode_frame = tk.Frame(root)
        self.mode_frame.pack(side=tk.TOP, pady=10)
        
        self.label = tk.Label(self.mode_frame, text="请选择交互模式：", font=("Arial", 16))
        self.label.pack(pady=10)
        
        self.text_button = tk.Button(self.mode_frame, text="文本交互", font=("Arial", 14), command=self.start_text_mode)
        self.text_button.pack(pady=5)
        
        self.voice_button = tk.Button(self.mode_frame, text="语音交互", font=("Arial", 14), command=self.start_voice_mode)
        self.voice_button.pack(pady=5)
        
        # 将清屏和退出按钮放在“语音交互”按钮下面，每个按钮占一行
        self.clear_screen_button = tk.Button(self.mode_frame, text="清屏", font=("Arial", 14), command=self.clear_screen)
        self.clear_screen_button.pack(pady=5)

        self.exit_button = tk.Button(self.mode_frame, text="退出", font=("Arial", 14), command=root.quit)
        self.exit_button.pack(pady=5)
        
        # 对话框
        self.dialog = scrolledtext.ScrolledText(root, state='disabled', width=80, height=20, font=("Arial", 12))
        self.dialog.pack(pady=10)

    def append_dialog(self, text):
        self.dialog.config(state='normal')
        self.dialog.insert(tk.END, text + "\n")
        self.dialog.config(state='disabled')
        self.dialog.yview(tk.END)
        
    def clear_screen(self):
        """清空对话框内容"""
        self.dialog.config(state='normal')
        self.dialog.delete(1.0, tk.END)
        self.dialog.config(state='disabled')

    def clear_history(self):
        """清理历史记录"""
        if messagebox.askyesno("确认", "您确定要清理所有历史记录吗？"):
            with sqlite3.connect(self.db_manager.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM history')
                conn.commit()
            messagebox.showinfo("提示", "历史记录已清理！")
        
    def start_text_mode(self):
        self.append_dialog("文本交互模式启动...\nColorful品牌电脑009号客服正在为您服务......")
        prompt_base = self.chat_manager.construct_prompt(self.chat_manager.prompt1_parts, self.chat_manager.scenarios)
        self.chat_manager.history.append({"role": "system", "content": prompt_base})
        
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(pady=5)
        
        self.input_label = tk.Label(self.input_frame, text="请输入您的问题：", font=("Arial", 12))
        self.input_label.pack(side=tk.LEFT)
        
        self.input_entry = tk.Entry(self.input_frame, width=50, font=("Arial", 12))
        self.input_entry.pack(side=tk.LEFT, padx=5)
        
        self.send_button = tk.Button(self.input_frame, text="发送", font=("Arial", 12), command=self.send_query)
        self.send_button.pack(side=tk.LEFT)

    def send_query(self):
        query = self.input_entry.get()
        if query:
            self.append_dialog("用户: " + query)
            threading.Thread(target=self._process_text_query, args=(query,)).start()
            self.input_entry.delete(0, tk.END)

    def _process_text_query(self, query):
        result = self.chat_manager.chat(query)
        self.append_dialog("客服: " + result)
        
        # 保存历史记录
        full_chat = "\n".join([
            f"{entry['role']}: {entry['content']}" for entry in self.chat_manager.history 
            if entry['role'] != 'system'
        ])
        self.db_manager.add_history(query, full_chat)
        
        self.append_dialog("=" * 70)  # 添加分割线
        
    def start_voice_mode(self):
        self.append_dialog("语音交互模式启动...\nColorful品牌电脑009号客服正在为您服务......")
        prompt_base = self.chat_manager.construct_prompt(self.chat_manager.prompt2_parts, self.chat_manager.scenarios)
        self.chat_manager.history.append({"role": "system", "content": prompt_base})
        
        self.voice_manager.start_speaking_thread("Colorful品牌电脑009号客服正在为您服务......请问有什么可以帮助您的？")
        
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(pady=5)
        
        self.speak_button = tk.Button(self.input_frame, text="按住说话", font=("Arial", 12), command=self.speak_query)
        self.speak_button.pack(side=tk.LEFT)

    def speak_query(self):
        self.voice_manager.start_recognizing_thread(self._process_voice_query)

    def _process_voice_query(self, query):
        self.append_dialog("用户: " + query)
        result = self.chat_manager.chat(query)
        self.append_dialog("客服: " + result)
        
        # 保存历史记录
        full_chat = "\n".join([
            f"{entry['role']}: {entry['content']}" for entry in self.chat_manager.history 
            if entry['role'] != 'system'
        ])
        self.db_manager.add_history(query, full_chat)
        
        self.append_dialog("=" * 70)  # 添加分割线
        self.voice_manager.start_speaking_thread(result)

    def show_history(self):
        history_window = Toplevel(self.root)
        history_window.title("历史记录")
        
        history_listbox = Listbox(history_window, font=("Arial", 12))
        history_listbox.pack(fill=tk.BOTH, expand=True)
        
        histories = self.db_manager.get_all_history()
        for record in histories:
            history_listbox.insert(tk.END, f"{record[1]} ({record[2]})")

        def on_select(event):
            selected_index = history_listbox.curselection()
            if selected_index:
                record_id = histories[selected_index[0]][0]
                full_chat = self.db_manager.get_history_by_id(record_id)
                
                # 过滤掉 system 角色的消息
                filtered_chat = "\n".join([
                    line for line in full_chat.splitlines()
                    if not line.startswith("system:")
                ])
                
                self.append_dialog(filtered_chat)
        
        history_listbox.bind('<<ListboxSelect>>', on_select)
