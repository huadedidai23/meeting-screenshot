# -*- coding: utf-8 -*-
"""配置管理模块"""
import json
import os
import sys


def _get_config_dir():
    """获取配置文件目录（打包后和开发时都能用）"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


CONFIG_FILE = os.path.join(_get_config_dir(), "config.json")

DEFAULT_CONFIG = {
    "screenshot_mode": "fullscreen",
    "region": None,
    "threshold": 5.0,
    "interval": 1.5,
    "last_save_folder": ""
}


def load_config():
    """加载配置，文件不存在或损坏时返回默认配置"""
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
            for key, val in DEFAULT_CONFIG.items():
                if key not in config:
                    config[key] = val
            return config
    except Exception:
        return DEFAULT_CONFIG.copy()


def save_config(config):
    """保存配置到文件"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
    except Exception:
        pass
