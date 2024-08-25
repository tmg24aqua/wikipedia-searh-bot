from flask import Flask, render_template, request
import wikipediaapi
from langdetect import detect, LangDetectException

app = Flask(__name__)

def get_language_from_text(text):
    try:
        lang = detect(text)
        if lang == 'ru':
            return 'ru'
        else:
            return 'en'
    except LangDetectException:
        return 'en'  # Если язык не удалось определить, используем английский

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query', '').strip()

    if not query:
        error_message = "Please enter a search query."
        return render_template('index.html', error_message=error_message)

    language = get_language_from_text(query)

    wiki = wikipediaapi.Wikipedia(
        language=language,
        user_agent="YourAppName/1.0 (https://yourwebsite.com; your-email@example.com)"
    )

    page = wiki.page(query)
    if page.exists():
        # Берем первые 2000 символов текста для краткого описания
        summary = page.text[:2000].rsplit(' ', 1)[0] + '...'

        # Безопасная работа с изображениями страницы
        images = []
        if hasattr(page, 'images'):
            images = list(page.images.keys())[:2]
        
        return render_template('result.html', title=page.title, summary=summary, url=page.fullurl, images=images)
    else:
        return render_template('result.html', title="Page not found", summary="Sorry, no matching article found.", url=None)

if __name__ == '__main__':
    app.run(debug=True)
