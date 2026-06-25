# Деплой на Oracle Cloud Free (24/7 бесплатно)

## Шаг 1: Аккаунт Oracle Cloud
1. Перейди на https://cloud.oracle.com/free
2. Зарегистрируйся (нужна карта, но ничего не списывается)
3. Выбери **"Always Free"** при создании аккаунта

## Шаг 2: Создай VM Instance
1. В консоли нажми **"Create a VM instance"**
2. Настрой:
   - **Name:** vizitka-bot
   - **Image:** Ubuntu 22.04 (или Ubuntu 24.04)
   - **Shape:** VM.Standard.A1.Flex (ARM — бесплатно)
   - **OCPU:** 4
   - **Memory:** 24 GB
   - **SSH Keys:** сгенерируй или загрузи свой публичный ключ
3. Нажми **"Create"**
4. Запиши **Public IP** (например: `129.154.xx.xx`)

## Шаг 3: Подключись к серверу
```bash
ssh ubuntu@129.154.xx.xx
```

## Шаг 4: Загрузи код
На своей машине:
```bash
cd vizitka
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/vizitka.git
git push -u origin main
```

На сервере:
```bash
git clone https://github.com/YOUR_USERNAME/vizitka.git
cd vizitka
```

## Шаг 5: Создай .env на сервере
```bash
nano .env
```
Вставь:
```
BOT_TOKEN=ТВОЙ_ТОКЕН
YOUR_TELEGRAM_ID=868677585
```

## Шаг 6: Запусти бота
```bash
chmod +x deploy.sh
./deploy.sh
```

## Полезные команды
```bash
# Статус бота
sudo systemctl status vizitka

# Перезапуск
sudo systemctl restart vizitka

# Логи в реальном времени
sudo journalctl -u vizitka -f

# Остановка
sudo systemctl stop vizitka
```

## Автозапуск после перезагрузки
Бот уже настроен на автозапуск через systemd (сделано в deploy.sh)
