import base64
import io
import tkinter as tk
from PIL import Image, ImageTk

class Captcha:
    def __init__(self, captchaData):
        self.root = tk.Tk()
        self.input = ""

        self.setup_window()
        self.setup_image(captchaData)
        self.setup_entry()
        self.setup_button()
        
    def setup_window(self):
        self.root.title = "輸入 Captcha 驗證碼"

        self.root.resizable(False, False)
        self.root.attributes("-toolwindow", True)
        self.root.attributes("-topmost", True)

        self.root.protocol("WM_DELETE_WINDOW", lambda: None)

    def setup_image(self, captchaData):
        try:
            imageData = base64.b64decode(captchaData)
            image = Image.open(io.BytesIO(imageData))
            self.tkImage = ImageTk.PhotoImage(image)

            self.imgLabel = tk.Label(self.root, image=self.tkImage)
            self.imgLabel.pack(padx=10, pady=10)
        except Exception as e:
            self.imgLabel = tk.Label(
                self.root,
                text=f"圖片載入失敗: {e}", fg="red"
            )
            self.imgLabel.pack(padx=10, pady=10)

    def setup_entry(self):
        self.entryLabel = tk.Label(self.root, text="輸入 Captcha 驗證碼")
        self.entryLabel.pack(pady=2)

        self.entry = tk.Entry(self.root, width=30)
        self.entry.pack(pady=5)
        self.entry.focus_set()

    def setup_button(self):
        self.submitButton = tk.Button(
            self.root,
            text="確認",
            command=self.on_submit
        )
        self.submitButton.pack(pady=15)

    def on_submit(self):
        self.input = self.entry.get()
        self.root.destroy()

    def show(self):
        self.root.mainloop()
        return self.input