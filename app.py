from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

@app.route('/')
def home():
    return '🏟️ Betman 배당 API 서버입니다.'

@app.route('/odds')
def odds():
    url = "https://www.betman.co.kr/main/mainPage/gamebuy/gameSlip.do?gmId=G101&gmTs=250048"

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    matches = []
    rows = soup.select('tr[data-matchseq]')
    for row in rows:
        teams = row.select('div.scoreDiv span')
        buttons = row.select('div.btnChkBox button')
        if len(teams) >= 3 and len(buttons) >= 3:
            try:
                home = teams[0].text.strip()
                away = teams[2].text.strip()
                odds_values = [float(btn.select_one('span.db').contents[0].strip()) for btn in buttons]
                match = {
                    "경기번호": row.get("data-matchseq", ""),
                    "홈팀": home,
                    "원정팀": away,
                    "배당": {
                        "승": odds_values[0],
                        "무": odds_values[1],
                        "패": odds_values[2]
                    }
                }
                matches.append(match)
            except:
                continue
    return jsonify(matches)
