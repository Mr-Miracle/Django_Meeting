#!/usr/bin/env python
"""Django's command-line utility for administrative tasks.
一种命令行工具，通过它可以与django项目进行交互。
"""
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MeetingDjiango.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "无法导入Django"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
