#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
加密/解密GUI工具

使用tkinter创建的图形界面，方便快速进行加密和解密操作
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import json
import sys
import os
import subprocess
import urllib.request
import ssl
import io

# 修复Windows控制台编码问题
if sys.platform == 'win32':
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except:
        pass

# WASM模块配置
WASM_URL = "https://fes.zuchecdn.com/cdn/h/vd/zuche/carfes/taishan/components/1.2.7/assets/sign_wasm-4bba901b.js"
WASM_LOCAL = "sign_wasm-4bba901b.js"

class EncryptDecryptGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("加密/解密工具")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # 设置样式
        style = ttk.Style()
        style.theme_use('clam')
        
        # 创建主框架
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # 标题
        title_label = ttk.Label(main_frame, text="加密/解密工具", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # 创建Notebook（标签页）
        notebook = ttk.Notebook(main_frame)
        notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # 加密标签页
        encrypt_frame = ttk.Frame(notebook, padding="10")
        notebook.add(encrypt_frame, text="加密")
        self.setup_encrypt_tab(encrypt_frame)
        
        # 解密标签页
        decrypt_frame = ttk.Frame(notebook, padding="10")
        notebook.add(decrypt_frame, text="解密")
        self.setup_decrypt_tab(decrypt_frame)
        
        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # 检查WASM模块
        self.check_wasm_module()
    
    def setup_encrypt_tab(self, parent):
        """设置加密标签页"""
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(1, weight=1)
        parent.rowconfigure(3, weight=1)
        
        # 输入标签
        input_label = ttk.Label(parent, text="输入JSON数据:", font=("Arial", 10, "bold"))
        input_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        # 输入文本框
        self.encrypt_input = scrolledtext.ScrolledText(parent, height=10, wrap=tk.WORD, font=("Consolas", 10))
        self.encrypt_input.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        self.encrypt_input.insert("1.0", '{"status": 1}')
        
        # 按钮框架
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=2, column=0, pady=10)
        
        # 加密按钮
        encrypt_btn = ttk.Button(button_frame, text="加密", command=self.encrypt_data, width=15)
        encrypt_btn.pack(side=tk.LEFT, padx=5)
        
        # 清空按钮
        clear_btn = ttk.Button(button_frame, text="清空", command=self.clear_encrypt, width=15)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # 示例按钮
        example_btn = ttk.Button(button_frame, text="加载示例", command=self.load_encrypt_examples, width=15)
        example_btn.pack(side=tk.LEFT, padx=5)
        
        # 输出标签
        output_label = ttk.Label(parent, text="加密结果:", font=("Arial", 10, "bold"))
        output_label.grid(row=3, column=0, sticky=tk.W, pady=(0, 5))
        
        # 输出文本框
        self.encrypt_output = scrolledtext.ScrolledText(parent, height=8, wrap=tk.WORD, font=("Consolas", 10))
        self.encrypt_output.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # 复制按钮
        copy_encrypt_btn = ttk.Button(parent, text="复制结果", command=self.copy_encrypt_result, width=15)
        copy_encrypt_btn.grid(row=5, column=0, pady=5)
    
    def setup_decrypt_tab(self, parent):
        """设置解密标签页"""
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(1, weight=1)
        parent.rowconfigure(3, weight=1)
        
        # 输入标签
        input_label = ttk.Label(parent, text="输入加密字符串:", font=("Arial", 10, "bold"))
        input_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        # 输入文本框
        self.decrypt_input = scrolledtext.ScrolledText(parent, height=5, wrap=tk.WORD, font=("Consolas", 10))
        self.decrypt_input.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # 按钮框架
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=2, column=0, pady=10)
        
        # 解密按钮
        decrypt_btn = ttk.Button(button_frame, text="解密", command=self.decrypt_data, width=15)
        decrypt_btn.pack(side=tk.LEFT, padx=5)
        
        # 清空按钮
        clear_btn = ttk.Button(button_frame, text="清空", command=self.clear_decrypt, width=15)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # 输出标签
        output_label = ttk.Label(parent, text="解密结果:", font=("Arial", 10, "bold"))
        output_label.grid(row=3, column=0, sticky=tk.W, pady=(0, 5))
        
        # 输出文本框
        self.decrypt_output = scrolledtext.ScrolledText(parent, height=12, wrap=tk.WORD, font=("Consolas", 10))
        self.decrypt_output.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # 复制按钮
        copy_decrypt_btn = ttk.Button(parent, text="复制结果", command=self.copy_decrypt_result, width=15)
        copy_decrypt_btn.grid(row=5, column=0, pady=5)
    
    def check_wasm_module(self):
        """检查WASM模块是否存在"""
        if not os.path.exists(WASM_LOCAL):
            self.status_var.set("WASM模块不存在，首次使用时会自动下载...")
        else:
            self.status_var.set("就绪")
    
    def download_wasm(self):
        """下载WASM模块"""
        if os.path.exists(WASM_LOCAL):
            return True
        
        self.status_var.set("正在下载WASM模块...")
        self.root.update()
        
        try:
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            
            with urllib.request.urlopen(WASM_URL, context=ssl_context) as response:
                with open(WASM_LOCAL, 'wb') as f:
                    f.write(response.read())
            
            self.status_var.set("WASM模块下载完成")
            return True
        except Exception as e:
            messagebox.showerror("错误", f"下载WASM模块失败: {e}")
            self.status_var.set("WASM模块下载失败")
            return False
    
    def encrypt_data(self):
        """加密数据"""
        try:
            # 获取输入
            input_text = self.encrypt_input.get("1.0", tk.END).strip()
            if not input_text:
                messagebox.showwarning("警告", "请输入要加密的JSON数据")
                return
            
            # 下载WASM模块
            if not self.download_wasm():
                return
            
            self.status_var.set("正在加密...")
            self.root.update()
            
            # 尝试解析JSON
            try:
                content_dict = json.loads(input_text)
            except json.JSONDecodeError as e:
                # 尝试自动修复（类似encrypt_simple.py的逻辑）
                if ':' in input_text and '{' in input_text:
                    import re
                    pattern = r'\{([^}]+)\}'
                    match = re.search(pattern, input_text)
                    if match:
                        content = match.group(1)
                        fixed_pairs = []
                        for pair in content.split(','):
                            pair = pair.strip()
                            if ':' in pair:
                                key, value = pair.split(':', 1)
                                key = key.strip()
                                value = value.strip()
                                if not (key.startswith('"') and key.endswith('"')):
                                    key = f'"{key}"'
                                if not (value.startswith('"') and value.endswith('"')):
                                    try:
                                        json.loads(value)
                                    except:
                                        value = f'"{value}"'
                                fixed_pairs.append(f'{key}: {value}')
                        fixed_json = '{' + ', '.join(fixed_pairs) + '}'
                        try:
                            content_dict = json.loads(fixed_json)
                        except:
                            raise Exception(f"JSON格式错误: {e}")
                    else:
                        raise Exception(f"JSON格式错误: {e}")
                else:
                    raise Exception(f"JSON格式错误: {e}")
            
            # 转换为JSON字符串
            if isinstance(content_dict, dict):
                content = json.dumps(content_dict, ensure_ascii=False, separators=(',', ':'))
            else:
                content = str(content_dict)
            
            # 调用加密函数
            encrypted = self.call_encrypt(content)
            
            # 显示结果
            self.encrypt_output.delete("1.0", tk.END)
            self.encrypt_output.insert("1.0", encrypted)
            
            self.status_var.set("加密成功")
            messagebox.showinfo("成功", "加密完成！")
            
        except Exception as e:
            self.status_var.set("加密失败")
            messagebox.showerror("错误", f"加密失败: {e}")
    
    def decrypt_data(self):
        """解密数据"""
        try:
            # 获取输入
            input_text = self.decrypt_input.get("1.0", tk.END).strip()
            if not input_text:
                messagebox.showwarning("警告", "请输入要解密的字符串")
                return
            
            # 下载WASM模块
            if not self.download_wasm():
                return
            
            self.status_var.set("正在解密...")
            self.root.update()
            
            # 调用解密函数
            result = self.call_decrypt(input_text)
            
            # 格式化输出
            if isinstance(result, dict):
                output = json.dumps(result, ensure_ascii=False, indent=2)
            else:
                output = str(result)
            
            # 显示结果
            self.decrypt_output.delete("1.0", tk.END)
            self.decrypt_output.insert("1.0", output)
            
            self.status_var.set("解密成功")
            messagebox.showinfo("成功", "解密完成！")
            
        except Exception as e:
            self.status_var.set("解密失败")
            messagebox.showerror("错误", f"解密失败: {e}")
    
    def call_encrypt(self, content):
        """调用加密函数"""
        wasm_path = os.path.abspath(WASM_LOCAL).replace('\\', '/')
        escaped_content = content.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
        
        code = f'''
(async () => {{
    const m = await import("file:///{wasm_path}");
    await m.__tla;
    const encrypted = m.encrypt("{escaped_content}");
    console.log(encrypted);
}})();
'''
        
        result = subprocess.run(
            ['node', '--input-type=module', '-e', code],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=30
        )
        
        if result.returncode != 0:
            raise Exception(f"加密失败: {result.stderr}")
        
        return result.stdout.strip()
    
    def call_decrypt(self, encrypted_content):
        """调用解密函数"""
        wasm_path = os.path.abspath(WASM_LOCAL).replace('\\', '/')
        
        code = f'''
(async () => {{
    const m = await import("file:///{wasm_path}");
    await m.__tla;
    console.log(JSON.stringify(JSON.parse(m.decrypt("{encrypted_content}"))));
}})();
'''
        
        result = subprocess.run(
            ['node', '--input-type=module', '-e', code],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=30
        )
        
        if result.returncode != 0:
            raise Exception(f"解密失败: {result.stderr}")
        
        return json.loads(result.stdout.strip())
    
    def clear_encrypt(self):
        """清空加密输入输出"""
        self.encrypt_input.delete("1.0", tk.END)
        self.encrypt_output.delete("1.0", tk.END)
        self.status_var.set("就绪")
    
    def clear_decrypt(self):
        """清空解密输入输出"""
        self.decrypt_input.delete("1.0", tk.END)
        self.decrypt_output.delete("1.0", tk.END)
        self.status_var.set("就绪")
    
    def copy_encrypt_result(self):
        """复制加密结果"""
        result = self.encrypt_output.get("1.0", tk.END).strip()
        if result:
            self.root.clipboard_clear()
            self.root.clipboard_append(result)
            messagebox.showinfo("成功", "已复制到剪贴板")
        else:
            messagebox.showwarning("警告", "没有可复制的内容")
    
    def copy_decrypt_result(self):
        """复制解密结果"""
        result = self.decrypt_output.get("1.0", tk.END).strip()
        if result:
            self.root.clipboard_clear()
            self.root.clipboard_append(result)
            messagebox.showinfo("成功", "已复制到剪贴板")
        else:
            messagebox.showwarning("警告", "没有可复制的内容")
    
    def load_encrypt_examples(self):
        """加载加密示例"""
        examples = [
            '{"status": 1}',
            '{"status": 2}',
            '{"code": 0, "roundInventory": 833, "skuNo": "SKU202510200003"}',
        ]
        
        # 创建示例选择窗口
        example_window = tk.Toplevel(self.root)
        example_window.title("选择示例")
        example_window.geometry("400x200")
        
        ttk.Label(example_window, text="选择要加载的示例:", font=("Arial", 10)).pack(pady=10)
        
        for i, example in enumerate(examples):
            btn = ttk.Button(
                example_window,
                text=f"示例 {i+1}: {example[:50]}...",
                command=lambda e=example: self.load_example(e, example_window)
            )
            btn.pack(pady=5, padx=20, fill=tk.X)
    
    def load_example(self, example, window):
        """加载示例"""
        self.encrypt_input.delete("1.0", tk.END)
        self.encrypt_input.insert("1.0", example)
        window.destroy()


def main():
    """主函数"""
    # 检查Node.js
    try:
        result = subprocess.run(
            ['node', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode != 0:
            messagebox.showerror("错误", "未找到Node.js，请先安装: https://nodejs.org/")
            return
    except FileNotFoundError:
        messagebox.showerror("错误", "未找到Node.js，请先安装: https://nodejs.org/")
        return
    except Exception:
        pass
    
    # 创建GUI
    root = tk.Tk()
    app = EncryptDecryptGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

