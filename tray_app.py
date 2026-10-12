"""
Custom Discord Rich Presence - Tray Control Panel & GUI
Author: Fameboyq (https://github.com/Fameboyq)
License: MIT
"""

import os
import sys
import json
import threading
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageDraw
import pystray

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')

DEFAULT_CONFIG = {
    "client_id": "1440730997460172810",
    "enabled": True,
    "language": "en",
    "interval_seconds": 6,
    "buttons": [
        {"label": "Website", "url": "https://fameboyq.fun"},
        {"label": "Telegram", "url": "https://t.me/fameboyq"}
    ]
}

I18N = {
    "en": {
        "title": "⚡ Custom Discord RPC - Control Panel",
        "status_active": "● ACTIVE",
        "status_off": "● OFF",
        "lang_switch": "Language / Язык:",
        "sec_general": "  General Settings  ",
        "client_id": "Client ID:",
        "interval": "Animation Interval (sec):",
        "sec_buttons": "  Discord Profile Buttons  ",
        "btn1_label": "Button 1 Label:",
        "btn1_url": "Button 1 URL:",
        "btn2_label": "Button 2 Label:",
        "btn2_url": "Button 2 URL:",
        "save_btn": "💾 Save & Apply Changes",
        "tray_open": "Open Control Panel",
        "tray_toggle": "Toggle RPC",
        "tray_lang": "Language",
        "tray_exit": "Exit",
        "saved_msg": "Configuration saved successfully!"
    },
    "ru": {
        "title": "⚡ Кастомный Discord RPC - Панель управления",
        "status_active": "● ВКЛЮЧЕН",
        "status_off": "● ВЫКЛЮЧЕН",
        "lang_switch": "Язык / Language:",
        "sec_general": "  Основные настройки  ",
        "client_id": "Client ID:",
        "interval": "Интервал анимации (сек):",
        "sec_buttons": "  Кнопки в профиле Discord  ",
        "btn1_label": "Текст кнопки 1:",
        "btn1_url": "Ссылка кнопки 1:",
        "btn2_label": "Текст кнопки 2:",
        "btn2_url": "Ссылка кнопки 2:",
        "save_btn": "💾 Сохранить и применить",
        "tray_open": "Открыть панель",
        "tray_toggle": "Вкл/Выкл RPC",
        "tray_lang": "Язык",
        "tray_exit": "Выход",
        "saved_msg": "Настройки успешно сохранены!"
    }
}

def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return DEFAULT_CONFIG.copy()

def save_config(cfg):
    try:
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(cfg, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print("Save error:", e)

def create_tray_icon():
    img = Image.new('RGBA', (64, 64), color=(0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([(4, 4), (60, 60)], radius=14, fill=(124, 77, 255, 255), outline=(0, 229, 255, 255), width=3)
    d.polygon([(32, 14), (48, 48), (38, 48), (32, 34), (26, 48), (16, 48)], fill=(255, 255, 255, 255))
    d.rectangle([(25, 38), (39, 41)], fill=(0, 229, 255, 255))
    return img

class ControlPanelApp:
    def __init__(self):
        self.root = None
        self.tray_icon = None
        self.config = load_config()
        self.lang = self.config.get("language", "en")

    def t(self, key):
        return I18N.get(self.lang, I18N["en"]).get(key, key)

    def switch_language(self, new_lang):
        self.lang = new_lang
        self.config["language"] = new_lang
        save_config(self.config)
        if self.root:
            self.root.destroy()
            self.root = None
            self.build_gui()

    def build_gui(self):
        if self.root is not None:
            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()
            return

        self.root = tk.Tk()
        self.root.title(self.t("title"))
        self.root.geometry("490x590")
        self.root.resizable(False, False)
        self.root.configure(bg="#12131f")

        # Header Frame
        header = tk.Frame(self.root, bg="#1a1b2d", height=70)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        title_lbl = tk.Label(header, text="⚡ Custom Discord RPC", font=("Segoe UI", 13, "bold"), fg="#ffffff", bg="#1a1b2d")
        title_lbl.pack(side=tk.LEFT, padx=16, pady=10)

        # Language buttons in header
        lang_frame = tk.Frame(header, bg="#1a1b2d")
        lang_frame.pack(side=tk.RIGHT, padx=16, pady=15)

        en_btn = tk.Button(lang_frame, text="EN", font=("Segoe UI", 8, "bold"), bg="#7c4dff" if self.lang == "en" else "#26283d", fg="#ffffff", relief=tk.FLAT, padx=6, command=lambda: self.switch_language("en"))
        en_btn.pack(side=tk.LEFT, padx=2)

        ru_btn = tk.Button(lang_frame, text="RU", font=("Segoe UI", 8, "bold"), bg="#7c4dff" if self.lang == "ru" else "#26283d", fg="#ffffff", relief=tk.FLAT, padx=6, command=lambda: self.switch_language("ru"))
        ru_btn.pack(side=tk.LEFT, padx=2)

        # Main Container
        container = tk.Frame(self.root, bg="#12131f", padx=20, pady=12)
        container.pack(fill=tk.BOTH, expand=True)

        # General Settings Section
        gen_sec = tk.LabelFrame(container, text=self.t("sec_general"), font=("Segoe UI", 9, "bold"), fg="#7c4dff", bg="#1a1b2d", padx=12, pady=10, relief=tk.FLAT)
        gen_sec.pack(fill=tk.X, pady=(0, 10))

        tk.Label(gen_sec, text=self.t("client_id"), font=("Segoe UI", 8), fg="#a0a0b8", bg="#1a1b2d").grid(row=0, column=0, sticky="w", pady=2)
        self.client_id_var = tk.StringVar(value=self.config.get("client_id", "1440730997460172810"))
        client_ent = tk.Entry(gen_sec, textvariable=self.client_id_var, font=("Segoe UI", 9), bg="#26283d", fg="#ffffff", insertbackground="#ffffff", relief=tk.FLAT)
        client_ent.grid(row=0, column=1, sticky="ew", padx=8, pady=2)

        tk.Label(gen_sec, text=self.t("interval"), font=("Segoe UI", 8), fg="#a0a0b8", bg="#1a1b2d").grid(row=1, column=0, sticky="w", pady=4)
        self.interval_var = tk.StringVar(value=str(self.config.get("interval_seconds", 6)))
        interval_ent = tk.Entry(gen_sec, textvariable=self.interval_var, font=("Segoe UI", 9), bg="#26283d", fg="#ffffff", insertbackground="#ffffff", relief=tk.FLAT)
        interval_ent.grid(row=1, column=1, sticky="ew", padx=8, pady=4)
        gen_sec.grid_columnconfigure(1, weight=1)

        # Buttons Section
        btn_sec = tk.LabelFrame(container, text=self.t("sec_buttons"), font=("Segoe UI", 9, "bold"), fg="#7c4dff", bg="#1a1b2d", padx=12, pady=10, relief=tk.FLAT)
        btn_sec.pack(fill=tk.X, pady=(0, 10))

        buttons = self.config.get("buttons", [{}, {}])
        b1 = buttons[0] if len(buttons) > 0 else {}
        b2 = buttons[1] if len(buttons) > 1 else {}

        tk.Label(btn_sec, text=self.t("btn1_label"), font=("Segoe UI", 8), fg="#a0a0b8", bg="#1a1b2d").grid(row=0, column=0, sticky="w", pady=2)
        self.b1_lbl_var = tk.StringVar(value=b1.get("label", "Website"))
        tk.Entry(btn_sec, textvariable=self.b1_lbl_var, font=("Segoe UI", 9), bg="#26283d", fg="#ffffff", insertbackground="#ffffff", relief=tk.FLAT).grid(row=0, column=1, sticky="ew", padx=8, pady=2)

        tk.Label(btn_sec, text=self.t("btn1_url"), font=("Segoe UI", 8), fg="#a0a0b8", bg="#1a1b2d").grid(row=1, column=0, sticky="w", pady=2)
        self.b1_url_var = tk.StringVar(value=b1.get("url", "https://fameboyq.fun"))
        tk.Entry(btn_sec, textvariable=self.b1_url_var, font=("Segoe UI", 9), bg="#26283d", fg="#ffffff", insertbackground="#ffffff", relief=tk.FLAT).grid(row=1, column=1, sticky="ew", padx=8, pady=2)

        tk.Label(btn_sec, text=self.t("btn2_label"), font=("Segoe UI", 8), fg="#a0a0b8", bg="#1a1b2d").grid(row=2, column=0, sticky="w", pady=(8, 2))
        self.b2_lbl_var = tk.StringVar(value=b2.get("label", "Telegram"))
        tk.Entry(btn_sec, textvariable=self.b2_lbl_var, font=("Segoe UI", 9), bg="#26283d", fg="#ffffff", insertbackground="#ffffff", relief=tk.FLAT).grid(row=2, column=1, sticky="ew", padx=8, pady=(8, 2))

        tk.Label(btn_sec, text=self.t("btn2_url"), font=("Segoe UI", 8), fg="#a0a0b8", bg="#1a1b2d").grid(row=3, column=0, sticky="w", pady=2)
        self.b2_url_var = tk.StringVar(value=b2.get("url", "https://t.me/fameboyq"))
        tk.Entry(btn_sec, textvariable=self.b2_url_var, font=("Segoe UI", 9), bg="#26283d", fg="#ffffff", insertbackground="#ffffff", relief=tk.FLAT).grid(row=3, column=1, sticky="ew", padx=8, pady=2)
        btn_sec.grid_columnconfigure(1, weight=1)

        # Save Button
        save_btn = tk.Button(container, text=self.t("save_btn"), font=("Segoe UI", 10, "bold"), bg="#7c4dff", activebackground="#651fff", fg="#ffffff", activeforeground="#ffffff", relief=tk.FLAT, pady=8, cursor="hand2", command=self.on_save)
        save_btn.pack(fill=tk.X, pady=(10, 0))

        # Protocol hide to tray
        self.root.protocol("WM_DELETE_WINDOW", lambda: self.root.withdraw())

    def on_save(self):
        try:
            self.config["client_id"] = self.client_id_var.get().strip()
            self.config["interval_seconds"] = int(self.interval_var.get().strip())
        except ValueError:
            self.config["interval_seconds"] = 6

        self.config["buttons"] = [
            {"label": self.b1_lbl_var.get().strip(), "url": self.b1_url_var.get().strip()},
            {"label": self.b2_lbl_var.get().strip(), "url": self.b2_url_var.get().strip()}
        ]
        self.config["language"] = self.lang
        save_config(self.config)
        messagebox.showinfo("Success", self.t("saved_msg"), parent=self.root)

    def start_tray(self):
        icon_img = create_tray_icon()
        menu = pystray.Menu(
            pystray.MenuItem(lambda _: self.t("tray_open"), lambda: self.root.after(0, self.build_gui), default=True),
            pystray.MenuItem(lambda _: f"Lang: {self.lang.upper()}", pystray.Menu(
                pystray.MenuItem("English", lambda: self.switch_language("en")),
                pystray.MenuItem("Русский", lambda: self.switch_language("ru"))
            )),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(lambda _: self.t("tray_exit"), self.quit_app)
        )
        self.tray_icon = pystray.Icon("CustomDiscordRPC", icon_img, "Custom Discord RPC", menu)
        self.tray_icon.run()

    def quit_app(self):
        if self.tray_icon:
            self.tray_icon.stop()
        if self.root:
            self.root.after(0, self.root.destroy)
        sys.exit(0)

if __name__ == "__main__":
    app = ControlPanelApp()
    t = threading.Thread(target=app.start_tray, daemon=True)
    t.start()
    app.build_gui()
    app.root.mainloop()
