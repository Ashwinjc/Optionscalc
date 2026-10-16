[app]
title = CrudeCalc
package.name = crudecalc
package.domain = org.crude
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy==2.3.0,cython==0.29.36
orientation = portrait
fullscreen = 0

# Android specific configurations
android.archs = arm64-v8a
android.allow_backup = True
android.accept_sdk_license = True
android.api = 33
android.minapi = 24
android.ndk = 25b
android.ndk_api = 24

[buildozer]
log_level = 2
warn_on_root = 0
