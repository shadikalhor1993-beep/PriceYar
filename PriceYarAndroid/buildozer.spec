[app]
# نام و مشخصات برنامه
title = PriceYar
package.name = priceyar
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf

# نسخه برنامه
version = 0.1
requirements = python3,kivy==2.3.1,kivymd==1.1.1,pyttsx3,plyer,pyjnius,requests

# تنظیمات صفحه نمایش
orientation = portrait
fullscreen = 0
android.permissions = INTERNET

[buildozer]
log_level = 2
warn_on_root = 1