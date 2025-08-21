# Travel Assistant Telegram Botu

Bu proje, bir Telegram botu ile [ucuzabilet.com](https://www.ucuzabilet.com/) üzerinden uçuş araması yaparak gidiş/dönüş için en uygun uçuşları ve fiyatları kullanıcıya sunar. Kullanıcıdan aldığı şehir ve tarih bilgileriyle web scraping yapar ve sonuçları Telegram üzerinden iletir.

## Özellikler

- Telegram üzerinden uçuş arama komutu ile kolay kullanım.
- Gidiş ve dönüş uçuşları için en uygun fiyatları bulur.
- Tüm fiyat ve uçuş detaylarını listeler.
- Fiyat grafiği üzerinden minimum ücretli alternatifleri gösterir.
- Birden fazla yolcu desteği.

## Kurulum

### Gereksinimler

- Python 3.8+
- Google Chrome ve [ChromeDriver](https://chromedriver.chromium.org/downloads)
- Telegram Bot Token
- .env dosyası

### Bağımlılıklar

```bash
pip install python-telegram-bot selenium pandas python-dotenv
```

### .env Dosyası

Ana dizinde `.env` dosyası oluşturun ve aşağıdaki satırı ekleyin:

```
TOKEN=telegram-bot-tokenunuz
```

### ChromeDriver

- [ChromeDriver](https://chromedriver.chromium.org/downloads) indirin.
- Sürümünüzün Chrome ile uyumlu olduğundan emin olun.
- `chromedriver` dosyasını PATH'a ekleyin veya proje dizinine koyun.

## Kullanım

Botu başlatmak için:

```bash
python bot.py
```

Botu çalıştırdıktan sonra Telegram'da Text'i aşağıdaki formatta gönderin:

```
20.09.2025-22.09.2025-İstanbul-Antalya-2
```

**Parametreler:**

- `20.09.2025`: Gidiş tarihi
- `22.09.2025`: Dönüş tarihi
- `İstanbul`: Kalkış şehri
- `Antalya`: Varış şehri
- `2`: Yolcu sayısı (isteğe bağlı; belirtilmezse 1)

**Örnek Mesaj:**

```
10.10.2025-15.10.2025-Ankara-İzmir
05.12.2025-12.12.2025-İstanbul-Antalya-3
```

### Yanıt Formatı

Bot, gidiş ve dönüş için en uygun uçuşun detaylarını ve fiyatlarını, minimum fiyatlı alternatif tarihleri ve toplam ücreti gösterir.

## Kod Açıklaması

- **Selenium** ile ucuzabilet.com'da arama yapılır, sonuçlar çekilir.
- **Telegram Bot API** ile kullanıcının mesajına yanıt verilir.
- **Pandas** ile fiyat verileri işlenir ve en düşük fiyatlar tespit edilir.
- **dotenv** ile bot token'ı .env dosyasından çekilir.
- Hatalar yakalanır ve kullanıcıya iletilir.

## Notlar

- Web scraping işlemleri zaman zaman site güncellemeleri nedeniyle bozulabilir. Selektörleri gerektiğinde güncelleyin.
- ChromeDriver'ın sistemde kurulu ve PATH'ta olduğundan emin olun.
- Telegram botunu eklemeden önce [BotFather](https://t.me/BotFather) ile bir bot oluşturun ve TOKEN alın.

## Lisans

MIT
