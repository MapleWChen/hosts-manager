# -*- coding: utf-8 -*-
"""
Hosts 管理器 - tkinter GUI
功能：添加/删除 hosts 记录，左右布局
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
import socket
import subprocess
import shutil


HOSTS_PATH = os.path.join(
    os.environ.get('SystemRoot', r'C:\Windows'),
    r'System32\drivers\etc\hosts'
)
BACKUP_PATH = HOSTS_PATH + '.backup'


class HostsManager:
    def __init__(self, root):
        self.root = root
        self.root.title('Hosts 管理器')
        self.root.geometry('900x560')
        self.root.minsize(780, 480)
        self.root.configure(bg='#f0f2f5')

        self.setup_styles()
        self.setup_ui()
        self.refresh_hosts_content()

    def _set_sash(self, paned):
        try:
            paned.sash_place(0, 350, 0)
        except:
            pass

    def setup_styles(self):
        self.colors = {
            'bg': '#f0f2f5',
            'card_bg': '#ffffff',
            'title': '#1a1a2e',
            'accent_green': '#27ae60',
            'accent_green_hover': '#2ecc71',
            'accent_red': '#c0392b',
            'accent_red_hover': '#e74c3c',
            'accent_blue': '#2980b9',
            'accent_blue_hover': '#3498db',
            'accent_gray': '#7f8c8d',
            'accent_gray_hover': '#95a5a6',
            'text': '#2c3e50',
            'muted': '#95a5a6',
            'border': '#dcdde1',
            'terminal_bg': '#1e1e1e',
            'terminal_fg': '#d4d4d4',
            'warning_bg': '#fdebd0',
            'warning_fg': '#b7950b',
            'success_bg': '#d5f5e3',
            'success_fg': '#1e8449',
            'danger_bg': '#fadbd8',
            'danger_fg': '#c0392b',
            'info_bg': '#d4e6f1',
            'info_fg': '#1a5276',
        }

        self.font_title = ('Microsoft YaHei', 16, 'bold')
        self.font_section = ('Microsoft YaHei', 11, 'bold')
        self.font_label = ('Microsoft YaHei', 10)
        self.font_btn = ('Microsoft YaHei', 11, 'bold')
        self.font_btn_small = ('Microsoft YaHei', 10)
        self.font_status = ('Microsoft YaHei', 9)
        self.font_terminal = ('Consolas', 10)

    def setup_ui(self):
        # ===== 主容器 =====
        main = tk.Frame(self.root, bg=self.colors['bg'])
        main.pack(fill='both', expand=True, padx=16, pady=16)

        # ===== PanedWindow 左右布局 =====
        paned = tk.PanedWindow(main, orient='horizontal', bg=self.colors['bg'],
                               sashwidth=4, sashrelief='flat', opaqueresize=True)
        paned.pack(fill='both', expand=True)

        # ===== 左侧：操作区 =====
        left = tk.Frame(paned, bg=self.colors['bg'])
        paned.add(left, minsize=280, width=340)

        # 标题
        tk.Label(left, text='Hosts 记录管理', font=self.font_title,
                 bg=self.colors['bg'], fg=self.colors['title']).pack(pady=(0, 16))

        # 输入组
        input_frame = tk.LabelFrame(left, text=' 记录配置 ', font=self.font_label,
                                     bg=self.colors['card_bg'], fg=self.colors['text'],
                                     bd=1, relief='groove', padx=12, pady=12)
        input_frame.pack(fill='x', padx=4)

        # 域名行
        row1 = tk.Frame(input_frame, bg=self.colors['card_bg'])
        row1.pack(fill='x', pady=6)
        tk.Label(row1, text='域名:', font=self.font_label,
                 bg=self.colors['card_bg'], fg=self.colors['text'], width=6, anchor='w').pack(side='left')
        self.domain_var = tk.StringVar(value='')
        self.domain_entry = tk.Entry(row1, textvariable=self.domain_var,
                                     font=self.font_label, relief='solid', bd=1,
                                     highlightthickness=2, highlightcolor='#3498db')
        self.domain_entry.pack(side='left', fill='x', expand=True, ipady=4)
        self.domain_var.trace_add('write', lambda *_: self.update_status())

        # IP行
        row2 = tk.Frame(input_frame, bg=self.colors['card_bg'])
        row2.pack(fill='x', pady=6)
        tk.Label(row2, text='IP:', font=self.font_label,
                 bg=self.colors['card_bg'], fg=self.colors['text'], width=6, anchor='w').pack(side='left')
        self.ip_var = tk.StringVar(value='')
        self.ip_entry = tk.Entry(row2, textvariable=self.ip_var,
                                  font=self.font_label, relief='solid', bd=1,
                                  highlightthickness=2, highlightcolor='#3498db')
        self.ip_entry.pack(side='left', fill='x', expand=True, ipady=4)

        # 按钮组
        btn_frame = tk.LabelFrame(left, text=' 操作 ', font=self.font_label,
                                   bg=self.colors['card_bg'], fg=self.colors['text'],
                                   bd=1, relief='groove', padx=12, pady=12)
        btn_frame.pack(fill='x', padx=4, pady=(12, 0))

        # 添加按钮
        self.add_btn = tk.Button(btn_frame, text='添 加 记 录', font=self.font_btn,
                                  bg=self.colors['accent_green'], fg='white',
                                  activebackground=self.colors['accent_green_hover'],
                                  activeforeground='white', cursor='hand2',
                                  relief='flat', bd=0, pady=8)
        self.add_btn.pack(fill='x', pady=4)
        self.add_btn.bind('<Enter>', lambda e: self.add_btn.configure(bg=self.colors['accent_green_hover']))
        self.add_btn.bind('<Leave>', lambda e: self.add_btn.configure(bg=self.colors['accent_green']))
        self.add_btn.configure(command=self.add_record)

        # 删除按钮
        self.del_btn = tk.Button(btn_frame, text='删 除 记 录', font=self.font_btn,
                                  bg=self.colors['accent_red'], fg='white',
                                  activebackground=self.colors['accent_red_hover'],
                                  activeforeground='white', cursor='hand2',
                                  relief='flat', bd=0, pady=8)
        self.del_btn.pack(fill='x', pady=4)
        self.del_btn.bind('<Enter>', lambda e: self.del_btn.configure(bg=self.colors['accent_red_hover']))
        self.del_btn.bind('<Leave>', lambda e: self.del_btn.configure(bg=self.colors['accent_red']))
        self.del_btn.configure(command=self.delete_record)

        # 解析IP按钮
        self.resolve_btn = tk.Button(btn_frame, text='自动解析 IP', font=self.font_btn_small,
                                      bg=self.colors['accent_blue'], fg='white',
                                      activebackground=self.colors['accent_blue_hover'],
                                      activeforeground='white', cursor='hand2',
                                      relief='flat', bd=0, pady=6)
        self.resolve_btn.pack(fill='x', pady=4)
        self.resolve_btn.bind('<Enter>', lambda e: self.resolve_btn.configure(bg=self.colors['accent_blue_hover']))
        self.resolve_btn.bind('<Leave>', lambda e: self.resolve_btn.configure(bg=self.colors['accent_blue']))
        self.resolve_btn.configure(command=self.resolve_ip)

        # 状态栏
        self.status_frame = tk.Frame(left, bg=self.colors['info_bg'], bd=0)
        self.status_frame.pack(fill='x', padx=4, pady=(12, 0))

        self.status_label = tk.Label(self.status_frame, text='', font=self.font_status,
                                     bg=self.colors['info_bg'], fg=self.colors['info_fg'],
                                     wraplength=280, justify='left', padx=10, pady=8,
                                     anchor='w')
        self.status_label.pack(fill='x')
        self.update_status()

        # ===== 右侧：Hosts 内容预览 =====
        right = tk.Frame(paned, bg=self.colors['bg'])
        paned.add(right, minsize=400, width=560)

        tk.Label(right, text='当前 Hosts 文件内容', font=self.font_section,
                 bg=self.colors['bg'], fg=self.colors['title'], anchor='w').pack(fill='x', pady=(0, 6))

        # 终端风格文本框
        text_frame = tk.Frame(right, bg=self.colors['terminal_bg'], bd=0,
                              highlightthickness=1, highlightbackground='#555')
        text_frame.pack(fill='both', expand=True)

        self.hosts_text = tk.Text(text_frame, font=self.font_terminal,
                                    bg=self.colors['terminal_bg'], fg=self.colors['terminal_fg'],
                                    insertbackground='white', selectbackground='#264f78',
                                    relief='flat', bd=0, wrap='none',
                                    padx=10, pady=10, state='disabled')
        
        scrollbar_y = tk.Scrollbar(text_frame, orient='vertical', command=self.hosts_text.yview)
        scrollbar_x = tk.Scrollbar(right, orient='horizontal', command=self.hosts_text.xview)
        self.hosts_text.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        scrollbar_y.pack(side='right', fill='y')
        self.hosts_text.pack(side='left', fill='both', expand=True)
        scrollbar_x.pack(fill='x', pady=(2, 0))

        # 刷新按钮
        self.refresh_btn = tk.Button(right, text='刷新内容', font=self.font_btn_small,
                                      bg=self.colors['accent_gray'], fg='white',
                                      activebackground=self.colors['accent_gray_hover'],
                                      activeforeground='white', cursor='hand2',
                                      relief='flat', bd=0, pady=4)
        self.refresh_btn.pack(fill='x', pady=(6, 0))
        self.refresh_btn.bind('<Enter>', lambda e: self.refresh_btn.configure(bg=self.colors['accent_gray_hover']))
        self.refresh_btn.bind('<Leave>', lambda e: self.refresh_btn.configure(bg=self.colors['accent_gray']))
        self.refresh_btn.configure(command=self.refresh_hosts_content)

        # 延迟设置分割位置
        self.root.after(50, lambda: self._set_sash(paned))

    def update_status(self):
        domain = self.domain_var.get().strip()
        if domain:
            record = self.find_record(domain)
            if record:
                self.status_label.configure(
                    text=f'已存在记录:\n{record.strip()}\n\n点击「添加」将更新，点击「删除」将移除',
                    bg=self.colors['warning_bg'], fg=self.colors['warning_fg']
                )
            else:
                self.status_label.configure(
                    text=f'域名 {domain}\n当前无 Hosts 记录\n点击「添加记录」将添加新条目',
                    bg=self.colors['success_bg'], fg=self.colors['success_fg']
                )
        else:
            self.status_label.configure(
                text='请输入域名', bg=self.colors['info_bg'], fg=self.colors['info_fg']
            )

    def find_record(self, domain):
        try:
            with open(HOSTS_PATH, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    if domain in line and not line.strip().startswith('#'):
                        return line
        except:
            pass
        return None

    def read_hosts(self):
        try:
            with open(HOSTS_PATH, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception as e:
            return f'读取 hosts 文件失败: {e}'

    def refresh_hosts_content(self):
        content = self.read_hosts()
        self.hosts_text.configure(state='normal')
        self.hosts_text.delete('1.0', 'end')
        self.hosts_text.insert('1.0', content)
        self.hosts_text.configure(state='disabled')
        self.update_status()

    def backup_hosts(self):
        try:
            shutil.copy2(HOSTS_PATH, BACKUP_PATH)
            return True
        except:
            return False

    def flush_dns(self):
        try:
            subprocess.run(
                ['ipconfig', '/flushdns'],
                capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW
            )
        except:
            pass

    def resolve_ip(self):
        domain = self.domain_var.get().strip()
        if not domain:
            messagebox.showwarning('提示', '请先输入域名')
            return

        self.resolve_btn.configure(state='disabled', text='解析中...')
        self.root.update_idletasks()

        try:
            ip = socket.gethostbyname(domain)
            self.ip_var.set(ip)
            self.status_label.configure(
                text=f'解析成功:\n{domain}  ->  {ip}',
                bg=self.colors['success_bg'], fg=self.colors['success_fg']
            )
        except socket.gaierror:
            messagebox.showerror('解析失败', f'无法解析域名: {domain}')
            self.status_label.configure(
                text=f'解析失败: {domain}',
                bg=self.colors['danger_bg'], fg=self.colors['danger_fg']
            )
        finally:
            self.resolve_btn.configure(state='normal', text='自动解析 IP')

    def add_record(self):
        domain = self.domain_var.get().strip()
        ip = self.ip_var.get().strip()

        if not domain or not ip:
            messagebox.showwarning('提示', '请填写域名和 IP 地址')
            return

        record = self.find_record(domain)
        if record:
            action = '更新'
            msg = (f'域名 {domain} 已有以下记录：\n\n{record.strip()}\n\n'
                   f'将更新为：\n{ip}    {domain}\n\n确认操作？')
        else:
            action = '添加'
            msg = f'即将添加以下记录：\n\n{ip}    {domain}\n\n确认操作？'

        if not messagebox.askyesno(f'确认{action}', msg):
            return

        try:
            self.backup_hosts()

            with open(HOSTS_PATH, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            new_lines = [line for line in lines if domain not in line]
            new_lines.append(f'\n{ip}\t{domain}\n')

            with open(HOSTS_PATH, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)

            self.flush_dns()
            self.refresh_hosts_content()
            messagebox.showinfo('成功', f'已{action}记录并刷新 DNS 缓存')
        except PermissionError:
            messagebox.showerror('权限不足',
                                  '请以管理员身份运行本程序！\n\n右键程序 -> 以管理员身份运行')
        except Exception as e:
            messagebox.showerror('操作失败', f'错误: {e}')

    def delete_record(self):
        domain = self.domain_var.get().strip()

        if not domain:
            messagebox.showwarning('提示', '请填写域名')
            return

        record = self.find_record(domain)
        if not record:
            messagebox.showinfo('提示', f'域名 {domain} 无 Hosts 记录，无需删除')
            return

        if not messagebox.askyesno('确认删除',
                                    f'即将删除以下记录：\n\n{record.strip()}\n\n确认删除？'):
            return

        try:
            self.backup_hosts()

            with open(HOSTS_PATH, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            new_lines = [line for line in lines if domain not in line]

            with open(HOSTS_PATH, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)

            self.flush_dns()
            self.refresh_hosts_content()
            messagebox.showinfo('成功', '已删除记录并刷新 DNS 缓存')
        except PermissionError:
            messagebox.showerror('权限不足',
                                  '请以管理员身份运行本程序！\n\n右键程序 -> 以管理员身份运行')
        except Exception as e:
            messagebox.showerror('操作失败', f'错误: {e}')


def main():
    root = tk.Tk()
    app = HostsManager(root)
    root.mainloop()


if __name__ == '__main__':
    main()
