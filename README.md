# Raspberri test pipeline

## Цель

Создать комплексный пайплайн с собственным раннером и разными машинами для тестов и продуктива

## Задача

* Система определяет температуру процессора и публикует ее на MQTT сервере
* Разработка ведется на VS Code (Windows 10) через Remote-SSH на Raspberry PI 4
* После тестов из IDE выполняется commit / git push, что запускает github actions 
* Запускается это на локальном runner (ARM на Raspberry Pi 4)
* Устанавливается виртуальное окружение python3 и т.п.
* Выполняются проверки линтером для директории `src/`
* Запускается основная программа (в фоне), считывает показания температуры процессора (в будущем и внешних датчиков) и публикует на mqtt сервере
* Запускается тестовая программа, подписывается на соответствующие топики mqtt, получает 2 сообщения в указанном диапазоне (из файла настроек)
* Если все хорошо, завершает основную программу и завершается сама
* Копирует (scp) программу и настройки на Raspberry Pi Zero W (продуктивную) и запускает ее там, предварительно остановив "старую" копию

## master

### v0.00

Первоначальный commit и настройка

### v0.10

Пробный запуск deploy

### v0.12

На целевой машине создан сервис `/etc/systemd/system/self_monitoring.service`

    [Unit]
    Description=Self monitoring
    After=network.target

    [Service]
    Restart=always
    RestartSec=20
    User=pi
    ExecStart=/bin/bash -c "cd /home/pi/bin; ./self_monitoring.py" &

    [Install]
    WantedBy=multi-user.target

Также заданы необходимые переменные окружения по типу `sudo systemctl set-environment MQTT_PORT=1883`  
После загрузки нового файла просто перезапускается сервис

### v0.20

Добавлен лог от предыдущего билда (`CI.log`)

Внесены исправления в `self_monitoring.py` согласно рекомендациям линтера

### v0.22

Обновлен CI.log (меньше ощшибок линтера)
