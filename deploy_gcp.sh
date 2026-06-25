#!/bin/bash
echo "=== Установка Python и зависимостей ==="
sudo apt update && sudo apt install -y python3 python3-pip python3-venv git

echo "=== Клонирование проекта ==="
cd /home/$USER
git clone https://github.com/YOUR_USERNAME/vizitka.git
cd vizitka

echo "=== Создание виртуального окружения ==="
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

echo "=== Создание systemd сервиса ==="
sudo tee /etc/systemd/system/vizitka.service > /dev/null <<EOF
[Unit]
Description=Telegram Bot Vizitka
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=/home/$USER/vizitka
ExecStart=/home/$USER/vizitka/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

echo "=== Запуск сервиса ==="
sudo systemctl daemon-reload
sudo systemctl enable vizitka
sudo systemctl start vizitka

echo "=== Готово! ==="
echo "Статус: sudo systemctl status vizitka"
echo "Логи: sudo journalctl -u vizitka -f"
