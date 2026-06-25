# Деплой на Google Cloud Free (24/7 бесплатно)

## Шаг 1: Аккаунт Google Cloud
1. Перейди на https://cloud.google.com/free
2. Войди через Google аккаунт
3. Получи **$300 кредит на 90 дней** + всегда бесплатный e2-micro

## Шаг 2: Создай VM Instance
1. В консоли: https://console.cloud.google.com/compute
2. Нажми **"Create Instance"**
3. Настрой:
   - **Name:** vizitka-bot
   - **Region:** us-central1 (или ближайший)
   - **Zone:** us-central1-a
   - **Machine type:** e2-micro (всегда бесплатно)
   - **Boot disk:** Ubuntu 22.04 LTS
   - **Firewall:** Allow HTTP, Allow HTTPS
4. Нажми **"Create"**
5. Запиши **External IP** (например: `34.xx.xx.xx`)

## Шаг 3: Подключись к серверу
```bash
gcloud compute ssh vizitka-bot --zone=us-central1-a
```
Или через веб-интерфейс: нажми **SSH** рядом с инстансом

## Шаг 4: Установи Python и зависимости
```bash
sudo apt update && sudo apt install -y python3 python3-pip python3-venv git
```

## Шаг 5: Загрузи код
```bash
cd /home/YOUR_USERNAME
git clone https://github.com/YOUR_USERNAME/vizitka.git
cd vizitka

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Шаг 6: Создай .env
```bash
nano .env
```
Вставь:
```
BOT_TOKEN=ТВОЙ_ТОКЕН
YOUR_TELEGRAM_ID=868677585
```

## Шаг 7: Запусти бота
```bash
nohup python bot.py &
```

## Автозапуск (опционально)
```bash
sudo tee /etc/systemd/system/vizitka.service > /dev/null <<EOF
[Unit]
Description=Telegram Bot Vizitka
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/home/YOUR_USERNAME/vizitka
ExecStart=/home/YOUR_USERNAME/vizitka/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable vizitka
sudo systemctl start vizitka
```

## Полезные команды
```bash
# Статус
sudo systemctl status vizitka

# Логи
sudo journalctl -u vizitka -f

# Перезапуск
sudo systemctl restart vizitka
```

## Важно!
- e2-micro: 0.25 vCPU, 1 GB RAM — хватит для бота
- Всегда бесплатно, без лимита времени
- Кредит $300 на 90 дней для других сервисов
