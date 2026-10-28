# -*- coding: utf-8 -*-
import threading
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton

# تنظیمات صدا برای اندروید (با استفاده از jnius)
def speak_text(text):
    print(f"TTS: {text}")
    try:
        from jnius import autoclass
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        TextToSpeech = autoclass('android.speech.tts.TextToSpeech')
        Locale = autoclass('java.util.Locale')
        tts = TextToSpeech(PythonActivity.mActivity, None)
        tts.setLanguage(Locale("fa", "IR"))
        tts.speak(text, TextToSpeech.QUEUE_FLUSH, None, "utt1")
    except Exception as e:
        print("Android TTS Error (Normal on Windows):", e)

Window.size = (400, 700)
FONT_NAME = "Vazir"

KV = '''
<PriceScreen>:
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "قیمت ابزار"
            font_name: "Vazir"
            elevation: 4
        ScrollView:
            MDList:
                id: product_list
                spacing: "10dp"
'''

class ProductCard(MDCard):
    def __init__(self, name, brand, price, on_announce, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint_y = None
        self.height = "150dp"
        self.padding = "10dp"
        self.spacing = "5dp"
        self.elevation = 2
        self.radius = [10]

        self.add_widget(MDLabel(text=name, font_name=FONT_NAME, halign="right", font_style="H6"))
        self.add_widget(MDLabel(text=brand, font_name=FONT_NAME, halign="right", theme_text_color="Secondary"))
        self.add_widget(MDLabel(text=price, font_name=FONT_NAME, halign="right", theme_text_color="Primary"))

        btn_box = MDBoxLayout(size_hint_y=None, height="40dp", spacing="10dp")
        btn_box.add_widget(MDFlatButton(text="حذف", font_name=FONT_NAME))
        btn_box.add_widget(MDRaisedButton(text="اعلام", font_name=FONT_NAME, on_release=lambda x: on_announce(name, price)))
        self.add_widget(btn_box)

class PriceScreen(MDScreen):
    def on_enter(self):
        self.load_products()

    def load_products(self):
        self.ids.product_list.clear_widgets()
        products = [
            {"name": "دریل چکشی", "brand": "برند: بوش | مدل: GSB 13", "price": "2,720,000 تومان"},
            {"name": "فرز آهنگری", "brand": "برند: مکیتا | مدل: 9557HN", "price": "2,880,000 تومان"},
        ]
        for p in products:
            card = ProductCard(name=p["name"], brand=p["brand"], price=p["price"], on_announce=self.do_announce)
            self.ids.product_list.add_widget(card)

    def do_announce(self, name, price):
        text = f"قیمت {name}، {price} می‌باشد."
        speak_text(text)
        dialog = MDDialog(
            title="اعلام قیمت",
            text=text,
            buttons=[MDFlatButton(text="باشه", font_name=FONT_NAME, on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()

class PriceYarApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Amber"
        self.theme_cls.theme_style = "Dark"
        # در اندروید، فونت باید به صورت خودکار از پوشه assets خوانده شود. 
        # ما نام فونت را ثبت می‌کنیم و فایل فونت را همراه پروژه می‌فرستیم.
        try:
            LabelBase.register(name=FONT_NAME, fn_regular="Vazir.ttf")
        except:
            print("Font not found locally, relying on Android assets.")
            
        Builder.load_string(KV)
        return PriceScreen()

if __name__ == "__main__":
    PriceYarApp().run()
