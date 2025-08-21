from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from datetime import datetime
import time
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("TOKEN değeri .env dosyasından alınamadı!")

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")

async def ucus_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        msg = update.message.text.replace("/ucus", "").strip()
        parts = msg.split("-")
        if len(parts) == 4:
            gidis_tarih_str, donus_tarih_str, kalkis, varis = parts
            yolcu_sayisi = "1"
        elif len(parts) == 5:
            gidis_tarih_str, donus_tarih_str, kalkis, varis, yolcu_sayisi = parts
        else:
            await update.message.reply_text(
                "Mesaj formatı hatalı.\nÖrnek: /ucus 20.09.2025-22.09.2025-İstanbul-Antalya-2"
            )
            return
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://www.ucuzabilet.com/")

        input_gidis = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "from_text"))
        )
        input_gidis.send_keys(kalkis)
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "ul.flight-autocomplete-list-from_text li"))
        ).click()
        time.sleep(0.5)
        
        input_varis = driver.find_element(By.ID, "to_text")
        input_varis.send_keys(varis)
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "ul.flight-autocomplete-list-to_text li"))
        ).click()
        time.sleep(0.5)
        
        driver.execute_script("document.getElementById('whereDepartDate').value = arguments[0];", gidis_tarih_str)
        driver.execute_script("document.getElementById('whereBackDate').value = arguments[0];", donus_tarih_str)
        driver.execute_script("document.querySelector('input[name=\"ADULT\"]').value = arguments[0];", yolcu_sayisi)
        
        driver.find_element(By.ID, "searchFormSubmit").click()
        time.sleep(5)
        
        flight_row_gidis = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "tr.flight-item.flights-min-price"))
        )
        gidis_firma = flight_row_gidis.find_element(By.CSS_SELECTOR, ".airline").text
        gidis_ucus_num = flight_row_gidis.find_element(By.CSS_SELECTOR, ".flight-number").text
        gidis_price = flight_row_gidis.get_attribute("data-price")
        flight_times = flight_row_gidis.find_elements(By.CSS_SELECTOR, "b.flight-time")
        gidis_time_baslangic = flight_times[0].text
        gidis_time_bitis = flight_times[1].text if len(flight_times) > 1 else "Bilinmiyor"
        gidis_airportler = flight_row_gidis.find_elements(By.CSS_SELECTOR, "div.airport")
        gidis_kalkis = gidis_airportler[0].text if len(gidis_airportler) > 0 else "Bilinmiyor"
        gidis_varis = gidis_airportler[1].text if len(gidis_airportler) > 1 else "Bilinmiyor"
        
        donus_row = driver.find_element(By.CSS_SELECTOR, "#returnFlights-1")
        donus_firma = donus_row.find_element(By.CSS_SELECTOR, ".airline").text
        donus_ucus_num = donus_row.find_element(By.CSS_SELECTOR, ".flight-number").text
        donus_price = donus_row.get_attribute("data-price")
        flight_times_donus = donus_row.find_elements(By.CSS_SELECTOR, "b.flight-time")
        donus_time_baslangic = flight_times_donus[0].text
        donus_time_bitis = flight_times_donus[1].text if len(flight_times_donus) > 1 else "Bilinmiyor"
        donus_airportler = donus_row.find_elements(By.CSS_SELECTOR, "div.airport")
        donus_kalkis = donus_airportler[0].text if len(donus_airportler) > 0 else "Bilinmiyor"
        donus_varis = donus_airportler[1].text if len(donus_airportler) > 1 else "Bilinmiyor"
        
        text = (
            f"✈️ <b>Seçili Tarihler için En Uygun Biletler</b>\n\n"
            f"🛫 <b>Gidiş:</b> {gidis_tarih_str}\n"
            f"Firma: {gidis_firma}\n"
            f"Uçuş No: {gidis_ucus_num}\n"
            f"Kalkış: {gidis_kalkis} - Varış: {gidis_varis}\n"
            f"Başlangıç: {gidis_time_baslangic} - Bitiş: {gidis_time_bitis}\n"
            f"Fiyat: {gidis_price} TL\n"
            f"Toplam Ücret: {round(float(yolcu_sayisi)*float(gidis_price))} TL\n\n"
            f"🛬 <b>Dönüş:</b> {donus_tarih_str}\n"
            f"Firma: {donus_firma}\n"
            f"Uçuş No: {donus_ucus_num}\n"
            f"Kalkış: {donus_kalkis} - Varış: {donus_varis}\n"
            f"Başlangıç: {donus_time_baslangic} - Bitiş: {donus_time_bitis}\n"
            f"Fiyat: {donus_price} TL\n"
            f"Toplam Ücret: {round(float(yolcu_sayisi)*float(donus_price))} TL"
        )

        await update.message.reply_text(text, parse_mode="HTML")
        
        data = []
        bitis_tarih = datetime.strptime("31.12.2025", "%d.%m.%Y")
        for direction in ["departure", "return"]:
            label = "Gidiş" if direction == "departure" else "Dönüş"
            while True:
                lis = driver.find_elements(By.CSS_SELECTOR, f'ul[data-direction="{direction}"] li')
                yeni_veri = False
                for li in lis:
                    tarih_str = li.get_attribute("data-flight-date")
                    fiyat_str = li.get_attribute("data-amount")
                    if not tarih_str or not fiyat_str:
                        continue
                    tarih = datetime.strptime(tarih_str, "%d.%m.%Y")
                    if tarih > bitis_tarih:
                        continue
                    fiyat = float(fiyat_str)
                    if not any(d["Tarih"] == tarih_str and d["Yön"] == label for d in data):
                        data.append({"Tarih": tarih_str, "Yön": label, "Fiyat": fiyat})
                        yeni_veri = True
                if not yeni_veri:
                    break
                try:
                    next_btn = driver.find_element(By.CSS_SELECTOR, f'span.btn-calendar-graph-next[data-direction="{direction}"]')
                    driver.execute_script("arguments[0].scrollIntoView(true);", next_btn)
                    next_btn.click()
                    time.sleep(1)
                except:
                    break
        
        if data:
            df = pd.DataFrame(data)
            df_min = df.loc[df.groupby("Yön")["Fiyat"].idxmin()]
            df_min = df_min.set_index("Yön").reindex(["Gidiş","Dönüş"]).reset_index()
            
            min_text = "📊 <b>En Düşük Fiyatlı Gidiş ve Dönüş Uçuşları</b>\n"
            for _, row in df_min.iterrows():
                min_text += f"• {row['Yön']}: <b>{row['Tarih']}</b> - <b>{row['Fiyat']} TL (Tek Kişi)</b>\n"
            await update.message.reply_text(min_text, parse_mode="HTML")


        driver.quit()
    
    except Exception as e:
        await update.message.reply_text(f"Hata oluştu: {e}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ucus_handler))
app.run_polling()
