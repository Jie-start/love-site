#!/usr/bin/env python
"""Django的管理命令行工具，用于执行各种管理任务"""
import os
import sys

def main():
    """运行管理任务"""
    # 设置Django的默认配置模块
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        # 导入Django的命令行执行工具
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "无法导入Django。请确保Django已正确安装。"
        ) from exc
    # 执行命令行参数
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main() 