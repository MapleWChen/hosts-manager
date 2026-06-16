# Hosts 管理器

一个带 GUI 界面的 Windows Hosts 文件管理工具，支持添加/删除/解析域名记录。

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Windows](https://img.shields.io/badge/Windows-10%2F11-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 功能

- **添加记录** - 向 Hosts 文件添加域名/IP 映射
- **删除记录** - 从 Hosts 文件移除指定域名记录
- **自动解析 IP** - 通过 DNS 自动解析域名对应的 IP 地址
- **实时预览** - 左右分栏布局，右侧实时显示 Hosts 文件内容
- **自动备份** - 每次修改前自动备份原始 Hosts 文件
- **DNS 刷新** - 修改后自动刷新 DNS 缓存
- **UAC 提权** - 双击运行自动请求管理员权限

## 使用方法

1. 下载 `HostsManager.exe`
2. 双击运行（会自动弹出 UAC 管理员权限提示）
3. 输入域名和 IP 地址
4. 点击「添加记录」或「删除记录」

## 开发

```bash
# 安装依赖
pip install pyinstaller

# 运行
python hosts_manager.py

# 打包为 exe
pyinstaller --onefile --windowed --uac-admin --name HostsManager hosts_manager.py
```

## 技术栈

- Python 3 + tkinter
- PyInstaller (打包)

## 许可

MIT License
