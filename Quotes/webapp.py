from flask import Flask, render_template
import requests
import random
import time

app = Flask(__name__)

# Список доступных API с цитатами
QUOTE_APIS = [
    {
        'name': 'ZenQuotes',
        'url': 'https://zenquotes.io/api/random',
        'parse_func': lambda data: (data[0]['q'], data[0]['a'])
    },
    {
        'name': 'QuotesLate',
        'url': 'https://quoteslate.vercel.app/api/random',
        'parse_func': lambda data: (data['content'], data['author'])
    }
]


def get_random_quote(max_retries=3):
    """Получает случайную цитату с одного из API с повторными попытками"""
    apis = QUOTE_APIS.copy()
    random.shuffle(apis)  # Перемешиваем API для балансировки нагрузки

    for api in apis:
        for attempt in range(max_retries):
            try:
                response = requests.get(
                    api['url'],
                    headers=api.get('headers', {}),
                    timeout=5  # Таймаут 5 секунд
                )
                response.raise_for_status()
                quote, author = api['parse_func'](response.json())
                return {
                    'text': quote,
                    'author': author,
                    'source': api['name']
                }
            except Exception as e:
                print(f"Attempt {attempt + 1} failed for {api['name']}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(1)  # Задержка перед повторной попыткой
                continue

    return None


@app.route('/')
def home():
    quote = get_random_quote()
    if not quote:
        # Если все API не ответили, используем запасную цитату
        quote = {
            'text': 'The best preparation for tomorrow is doing your best today.',
            'author': 'H. Jackson Brown Jr.',
            'source': 'Backup'
        }
    return render_template('quote.html', quote=quote)


if __name__ == '__main__':
    app.run(debug=True)
