"""
OpenQuill & OpenSpell Ambient Desktop Companion (Phase 4)
Local-First Windows Desktop HUD • 100% Deterministic NLP Bridge
"""

import sys
import os
import json
import time
import threading
import urllib.request
import urllib.error
import webbrowser
import tkinter as tk
from tkinter import ttk

# API Base URL
SERVER_URL = "http://127.0.0.1:8000"

class AmbientCompanionHUD:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("OpenQuill Ambient HUD")
        self.root.geometry("460x580")
        self.root.minsize(400, 500)
        
        # Configure topmost floating behavior
        self.root.attributes("-topmost", True)
        
        # Color Theme: Twilight Slate
        self.colors = {
            "bg_app": "#0e1117",
            "bg_surface": "#161b22",
            "bg_elevated": "#1f242c",
            "bg_sunken": "#0b0e13",
            "border": "#272f3d",
            "border_focus": "#3b82f6",
            "text_primary": "#f0f3f6",
            "text_secondary": "#9aa5b5",
            "text_muted": "#64748b",
            "accent": "#3b82f6",
            "accent_hover": "#2563eb",
            "emerald": "#34d399",
            "ruby": "#fb7185",
            "amber": "#fbbf24",
            "iris": "#a78bfa"
        }
        
        self.root.configure(bg=self.colors["bg_app"])
        
        # State variables
        self.last_clipboard_text = ""
        self.watching_clipboard = True
        self.debounce_timer = None
        self.current_inspect_data = {}
        
        self._build_ui()
        self._bind_events()
        
        # Start background clipboard monitoring thread
        self.monitor_thread = threading.Thread(target=self._clipboard_monitor_loop, daemon=True)
        self.monitor_thread.start()

    def _build_ui(self):
        # 1. Header Frame
        header = tk.Frame(self.root, bg=self.colors["bg_app"], padx=14, pady=10)
        header.pack(fill="x")
        
        title_lbl = tk.Label(
            header,
            text="OpenQuill HUD",
            font=("Segoe UI", 12, "bold"),
            fg=self.colors["text_primary"],
            bg=self.colors["bg_app"]
        )
        title_lbl.pack(side="left")
        
        # Clipboard Watcher Toggle Button
        self.btn_watch = tk.Button(
            header,
            text="● Watcher: ON",
            font=("Segoe UI", 8, "bold"),
            fg=self.colors["emerald"],
            bg=self.colors["bg_surface"],
            activebackground=self.colors["bg_elevated"],
            activeforeground=self.colors["emerald"],
            relief="flat",
            bd=0,
            padx=8,
            pady=3,
            command=self._toggle_watcher,
            cursor="hand2"
        )
        self.btn_watch.pack(side="right")
        
        # 2. Quality Score & Telemetry Banner
        self.score_frame = tk.Frame(
            self.root,
            bg=self.colors["bg_surface"],
            highlightbackground=self.colors["border"],
            highlightthickness=1,
            padx=14,
            pady=10
        )
        self.score_frame.pack(fill="x", padx=12, pady=(0, 8))
        
        top_score_row = tk.Frame(self.score_frame, bg=self.colors["bg_surface"])
        top_score_row.pack(fill="x")
        
        # Score Value
        self.score_lbl = tk.Label(
            top_score_row,
            text="100",
            font=("Consolas", 18, "bold"),
            fg=self.colors["emerald"],
            bg=self.colors["bg_surface"]
        )
        self.score_lbl.pack(side="left")
        
        score_denom = tk.Label(
            top_score_row,
            text="/100",
            font=("Consolas", 10),
            fg=self.colors["text_muted"],
            bg=self.colors["bg_surface"]
        )
        score_denom.pack(side="left", padx=(2, 10))
        
        self.score_status_lbl = tk.Label(
            top_score_row,
            text="Writing Pristine",
            font=("Segoe UI", 10, "bold"),
            fg=self.colors["text_primary"],
            bg=self.colors["bg_surface"]
        )
        self.score_status_lbl.pack(side="left")
        
        self.human_badge = tk.Label(
            top_score_row,
            text="100% Human",
            font=("Segoe UI", 9, "bold"),
            fg=self.colors["emerald"],
            bg=self.colors["bg_elevated"],
            padx=7,
            pady=2
        )
        self.human_badge.pack(side="right")
        
        # Telemetry row
        telem_row = tk.Frame(self.score_frame, bg=self.colors["bg_surface"])
        telem_row.pack(fill="x", pady=(8, 0))
        
        self.issues_pill = tk.Label(
            telem_row,
            text="0 Issues",
            font=("Segoe UI", 8, "bold"),
            fg=self.colors["ruby"],
            bg=self.colors["bg_elevated"],
            padx=6,
            pady=2
        )
        self.issues_pill.pack(side="left", padx=(0, 6))
        
        self.habits_pill = tk.Label(
            telem_row,
            text="0 Habits",
            font=("Segoe UI", 8, "bold"),
            fg=self.colors["accent"],
            bg=self.colors["bg_elevated"],
            padx=6,
            pady=2
        )
        self.habits_pill.pack(side="left", padx=(0, 6))
        
        self.words_pill = tk.Label(
            telem_row,
            text="0 Words",
            font=("Segoe UI", 8),
            fg=self.colors["text_secondary"],
            bg=self.colors["bg_elevated"],
            padx=6,
            pady=2
        )
        self.words_pill.pack(side="left")
        
        # 3. Text Area
        text_container = tk.Frame(
            self.root,
            bg=self.colors["bg_surface"],
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )
        text_container.pack(fill="both", expand=True, padx=12, pady=4)
        
        self.text_editor = tk.Text(
            text_container,
            font=("Segoe UI", 10),
            bg=self.colors["bg_surface"],
            fg=self.colors["text_primary"],
            insertbackground=self.colors["accent"],
            selectbackground=self.colors["accent"],
            selectforeground="#ffffff",
            bd=0,
            padx=12,
            pady=10,
            wrap="word",
            undo=True
        )
        self.text_editor.pack(fill="both", expand=True)
        self.text_editor.insert("1.0", "Copy or paste prose anywhere on Windows to inspect...")
        
        # 4. Status Toast Line
        self.toast_lbl = tk.Label(
            self.root,
            text="Ready • Standalone Desktop Companion",
            font=("Segoe UI", 8),
            fg=self.colors["text_muted"],
            bg=self.colors["bg_app"]
        )
        self.toast_lbl.pack(fill="x", padx=14, pady=2)
        
        # 5. Action Buttons Bar
        actions_bar = tk.Frame(self.root, bg=self.colors["bg_app"], padx=12, pady=8)
        actions_bar.pack(fill="x")
        
        # Primary Action: Fix & Copy
        btn_fix = tk.Button(
            actions_bar,
            text="⚡ Fix All & Copy",
            font=("Segoe UI", 9, "bold"),
            fg="#ffffff",
            bg=self.colors["accent"],
            activebackground=self.colors["accent_hover"],
            activeforeground="#ffffff",
            relief="flat",
            bd=0,
            pady=7,
            command=self.fix_all_and_copy,
            cursor="hand2"
        )
        btn_fix.pack(side="left", fill="x", expand=True, padx=(0, 4))
        
        # De-AI Humanize
        btn_deai = tk.Button(
            actions_bar,
            text="🤖 De-AI",
            font=("Segoe UI", 9, "bold"),
            fg=self.colors["amber"],
            bg=self.colors["bg_surface"],
            activebackground=self.colors["bg_elevated"],
            activeforeground=self.colors["amber"],
            relief="flat",
            bd=0,
            pady=7,
            command=self.humanize_and_copy,
            cursor="hand2"
        )
        btn_deai.pack(side="left", padx=2)
        
        # Open Studio
        btn_studio = tk.Button(
            actions_bar,
            text="↗ Studio",
            font=("Segoe UI", 9),
            fg=self.colors["text_secondary"],
            bg=self.colors["bg_surface"],
            activebackground=self.colors["bg_elevated"],
            activeforeground=self.colors["text_primary"],
            relief="flat",
            bd=0,
            pady=7,
            command=self.open_studio,
            cursor="hand2"
        )
        btn_studio.pack(side="left", padx=(4, 0))

    def _bind_events(self):
        self.text_editor.bind("<KeyRelease>", self._on_text_change)
        self.root.bind("<Escape>", lambda e: self.root.iconify())
        self.root.bind("<Control-Return>", lambda e: self.fix_all_and_copy())

    def _toggle_watcher(self):
        self.watching_clipboard = not self.watching_clipboard
        if self.watching_clipboard:
            self.btn_watch.configure(text="● Watcher: ON", fg=self.colors["emerald"])
            self._set_toast("Clipboard watcher enabled", self.colors["emerald"])
        else:
            self.btn_watch.configure(text="○ Watcher: Off", fg=self.colors["text_muted"])
            self._set_toast("Clipboard watcher paused", self.colors["text_muted"])

    def _clipboard_monitor_loop(self):
        while True:
            time.sleep(1.2)
            if not self.watching_clipboard:
                continue
            try:
                clip = self.root.clipboard_get()
                if clip and clip.strip() and clip != self.last_clipboard_text and len(clip.strip()) > 3:
                    self.last_clipboard_text = clip
                    self.root.after(0, self._load_clipboard_text, clip)
            except Exception:
                pass

    def _load_clipboard_text(self, text):
        self.text_editor.delete("1.0", "end")
        self.text_editor.insert("1.0", text)
        self._set_toast("Detected new text from clipboard", self.colors["accent"])
        self._inspect_text(text)

    def _on_text_change(self, event=None):
        if self.debounce_timer:
            self.root.after_cancel(self.debounce_timer)
        self.debounce_timer = self.root.after(350, self._run_current_text_inspection)

    def _run_current_text_inspection(self):
        text = self.text_editor.get("1.0", "end-1c").strip()
        if text:
            self._inspect_text(text)

    def _inspect_text(self, text):
        def _fetch():
            try:
                data = json.dumps({"text": text}).encode("utf-8")
                req = urllib.request.Request(
                    f"{SERVER_URL}/api/companion/inspect",
                    data=data,
                    headers={"Content-Type": "application/json"}
                )
                res = urllib.request.urlopen(req, timeout=5)
                payload = json.loads(res.read().decode())
                self.root.after(0, self._update_metrics, payload)
            except Exception as e:
                self.root.after(0, self._set_toast, f"Server offline or error: {e}", self.colors["ruby"])

        threading.Thread(target=_fetch, daemon=True).start()

    def _update_metrics(self, data):
        self.current_inspect_data = data
        score = data.get("quality_score", 100)
        self.score_lbl.configure(text=str(score))
        
        if score < 70:
            color = self.colors["ruby"]
            status = "Needs Polishing"
        elif score < 90:
            color = self.colors["amber"]
            status = "Good Quality"
        else:
            color = self.colors["emerald"]
            status = "Writing Pristine"
            
        self.score_lbl.configure(fg=color)
        self.score_status_lbl.configure(text=status)
        
        issues = data.get("total_issues", 0)
        habits = data.get("habit_clusters_count", 0)
        words = data.get("word_count", 0)
        ai_prob = data.get("ai_probability", 0.0)
        
        self.issues_pill.configure(text=f"{issues} Issues")
        self.habits_pill.configure(text=f"{habits} Habits")
        self.words_pill.configure(text=f"{words} Words")
        
        if ai_prob > 45:
            self.human_badge.configure(
                text=f"{round(ai_prob)}% AI-Signal",
                fg=self.colors["amber"]
            )
        else:
            self.human_badge.configure(
                text=f"{round(data.get('human_probability', 100))}% Human",
                fg=self.colors["emerald"]
            )

    def fix_all_and_copy(self):
        text = self.text_editor.get("1.0", "end-1c").strip()
        if not text:
            return
            
        def _fix():
            try:
                data = json.dumps({"text": text}).encode("utf-8")
                req = urllib.request.Request(
                    f"{SERVER_URL}/api/companion/quick-fix",
                    data=data,
                    headers={"Content-Type": "application/json"}
                )
                res = urllib.request.urlopen(req, timeout=5)
                payload = json.loads(res.read().decode())
                fixed_text = payload.get("fixed_text", text)
                count = payload.get("count_fixed", 0)
                
                self.root.after(0, self._apply_fix_result, fixed_text, count)
            except Exception as e:
                self.root.after(0, self._set_toast, f"Fix failed: {e}", self.colors["ruby"])

        threading.Thread(target=_fix, daemon=True).start()

    def _apply_fix_result(self, fixed_text, count):
        self.text_editor.delete("1.0", "end")
        self.text_editor.insert("1.0", fixed_text)
        
        # Write to system clipboard
        self.root.clipboard_clear()
        self.root.clipboard_append(fixed_text)
        self.last_clipboard_text = fixed_text
        
        self._set_toast(f"✓ Fixed {count} issues & copied to clipboard!", self.colors["emerald"])
        self._inspect_text(fixed_text)

    def humanize_and_copy(self):
        text = self.text_editor.get("1.0", "end-1c").strip()
        if not text:
            return
            
        def _humanize():
            try:
                data = json.dumps({"text": text}).encode("utf-8")
                req = urllib.request.Request(
                    f"{SERVER_URL}/api/humanize",
                    data=data,
                    headers={"Content-Type": "application/json"}
                )
                res = urllib.request.urlopen(req, timeout=5)
                payload = json.loads(res.read().decode())
                humanized = payload.get("humanized_text", text)
                
                self.root.after(0, self._apply_humanize_result, humanized)
            except Exception as e:
                self.root.after(0, self._set_toast, f"Humanize failed: {e}", self.colors["ruby"])

        threading.Thread(target=_humanize, daemon=True).start()

    def _apply_humanize_result(self, humanized_text):
        self.text_editor.delete("1.0", "end")
        self.text_editor.insert("1.0", humanized_text)
        
        self.root.clipboard_clear()
        self.root.clipboard_append(humanized_text)
        self.last_clipboard_text = humanized_text
        
        self._set_toast("✓ De-AI humanized & copied to clipboard!", self.colors["amber"])
        self._inspect_text(humanized_text)

    def open_studio(self):
        text = self.text_editor.get("1.0", "end-1c").strip()
        if text:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
        webbrowser.open(SERVER_URL)
        self._set_toast("Opened Studio in browser", self.colors["accent"])

    def _set_toast(self, text, color=None):
        self.toast_lbl.configure(text=text, fg=color or self.colors["text_muted"])

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AmbientCompanionHUD()
    app.run()
