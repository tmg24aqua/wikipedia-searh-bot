from flask import Flask, render_template, request
import wikipediaapi

app = Flask(__name__)

# Укажите ваш user-agent
wiki = wikipediaapi.Wikipedia(
    language='en',
    user_agent="YourAppName/1.0 (https://yourwebsite.com; ezerskijn9@gmail.com)"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    page = wiki.page(query)
    if page.exists():
        return f"<h1>{page.title}</h1><p>{page.summary}</p>"
    else:
        return "<p>Page not found</p>"

if __name__ == '__main__':
    app.run(debug=True)
