#!/usr/bin/env python3
"""
Генератор buildozer.spec для Kivy-проектов курса.
Создаёт файл со всеми настройками, которые нужны чтобы сборка
APK прошла без типичных ошибок.

Запуск:
    python make_spec.py

Скрипт спросит название приложения и имя пакета,
остальные (проверенные) настройки подставит сам.
"""

import os
import sys

# ── Настройки по умолчанию (проверены на сборке через GitHub Actions) ──
DEFAULTS = {
    "title": "Моя Визитка",
    "package_name": "vizitka",
    "package_domain": "org.student",
    # Точные версии — без них ошибка 'long' при сборке pyjnius
    "requirements": "python3,kivy==2.3.0,pyjnius==1.6.1",
    "orientation": "portrait",
    # Версия python-for-android. КРИТИЧНО: свежие версии тянут hostpython 3.14,
    # под который pyjnius не собирается. v2024.01.21 использует hostpython 3.11.
    "p4a_branch": "v2024.01.21",
}

SPEC_TEMPLATE = """[app]

# Название приложения (видно на телефоне под иконкой)
title = {title}

# Имя пакета — только латиница, без пробелов и цифр в начале
package.name = {package_name}

# Домен пакета (можно оставить как есть)
package.domain = {package_domain}

# Папка с исходным кодом (. = текущая папка)
source.dir = .

# Какие типы файлов включать в сборку
# ВАЖНО: kv — обязательно, иначе дизайн не попадёт в APK
# jpg/jpeg/png — для картинок
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf

# Версия приложения
version = 1.0

# --- Зависимости с ТОЧНЫМИ версиями ---
# Без точных версий сборка падает с ошибкой 'long' (pyjnius)
requirements = {requirements}

# Ориентация экрана: portrait (вертикально) или landscape
orientation = {orientation}

# Заставка при запуске (необязательно)
# presplash.filename = %(source.dir)s/presplash.png

# Иконка приложения (необязательно)
# icon.filename = %(source.dir)s/icon.png

# --- Android настройки ---
# Разрешения. INTERNET нужен для AsyncImage (картинки из сети)
android.permissions = INTERNET

# Версии Android API (проверенные значения)
android.api = 33
android.minapi = 21
android.ndk = 25b

# Автоматически принять лицензию SDK (без этого сборка спросит и упадёт)
android.accept_sdk_license = True

# Архитектура процессора (arm64-v8a — современные телефоны)
android.archs = arm64-v8a

# --- САМАЯ ВАЖНАЯ СТРОКА ---
# Версия python-for-android. Без неё берётся свежая версия с hostpython 3.14,
# под который pyjnius НЕ собирается (ошибка 'undeclared name not builtin: long').
# v2024.01.21 использует hostpython 3.11 — сборка проходит успешно.
p4a.branch = {p4a_branch}


[buildozer]

# Уровень логов: 2 = подробно (удобно искать ошибки)
log_level = 2

# --- Убирает вопрос про root-пользователя ---
# В облаке (Colab/GitHub) некому ответить на этот вопрос — ставим 0
warn_on_root = 0
"""


def ask(prompt, default):
    """Спросить значение, показав значение по умолчанию."""
    answer = input(f"{prompt} [{default}]: ").strip()
    return answer if answer else default


def main():
    print("=" * 52)
    print("  Генератор buildozer.spec для Kivy")
    print("=" * 52)
    print()

    if os.path.exists("buildozer.spec"):
        overwrite = input("buildozer.spec уже существует. Перезаписать? (y/n): ").strip().lower()
        if overwrite != "y":
            print("Отменено.")
            sys.exit(0)

    title = ask("Название приложения (видно под иконкой)", DEFAULTS["title"])
    package_name = ask("Имя пакета (латиница, без пробелов)", DEFAULTS["package_name"])

    spec = SPEC_TEMPLATE.format(
        title=title,
        package_name=package_name,
        package_domain=DEFAULTS["package_domain"],
        requirements=DEFAULTS["requirements"],
        orientation=DEFAULTS["orientation"],
        p4a_branch=DEFAULTS["p4a_branch"],
    )

    with open("buildozer.spec", "w", encoding="utf-8") as f:
        f.write(spec)

    print()
    print("Файл buildozer.spec создан!")
    print()
    print("Ключевые настройки (защита от ошибок сборки):")
    print(f"  p4a.branch = {DEFAULTS['p4a_branch']}   (hostpython 3.11)")
    print(f"  requirements = {DEFAULTS['requirements']}")
    print(f"  warn_on_root = 0")
    print(f"  android.accept_sdk_license = True")
    print()
    print("Не забудь: в GitHub Actions используй runs-on: ubuntu-22.04")
    print("(не ubuntu-latest - там ломаются старые пакеты).")


if __name__ == "__main__":
    main()
