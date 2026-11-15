[app]

title = Smart Irrigation System

package.name = smartirrigation

package.domain = org.mayuri

source.dir = .

source.include_exts = py,png,jpg,kv,atlas

version = 1.0

requirements = python3,kivy

orientation = portrait

fullscreen = 0

android.accept_sdk_license = True

[buildozer]

log_level = 2

warn_on_root = 1

[app:android]

android.archs = arm64-v8a, armeabi-v7a

android.api = 35

android.minapi = 23

