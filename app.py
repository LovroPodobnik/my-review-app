from flask import Flask, render_template, request, jsonify, send_from_directory
from app_store_scraper import AppStore
import re
import json
import os
import openai

app = Flask(__name__)

def extract_app_id(url):
    regex = r'/id(\d+)'
    match = re.search(regex, url)
    return match.group(1) if match else None

def save_reviews_to_file(reviews):
    reviews_to_save = []

    for review in reviews:
        review_copy = review.copy()
        review_copy['date'] = review_copy['date'].strftime('%Y-%m-%d %H:%M:%S')
        reviews_to_save.append(review_copy)

    with open('reviews.json', 'w', encoding='utf-8') as f:
        json.dump(reviews_to_save, f, ensure_ascii=False, indent=4)

def generate_suggestions(reviews):
    openai.api_key = "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"

    # Combine the review texts into a single string
    review_texts = " ".join([review["review"] for review in reviews])

    prompt = f"Act as UX/UI designer. Analize user Based on the following user reviews:\n\n{review_texts}\n\n"

    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.8,
    )

    suggestion = response.choices[0].text.strip()
    return suggestion

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form.get('url')
    app_id = extract_app_id(url)

    if not app_id:
        return jsonify({'error': 'Invalid App Store URL'})

    app_scraper = AppStore(country="nz", app_name="", app_id=app_id)
    app_scraper.review(how_many=20)
    reviews = app_scraper.reviews

    save_reviews_to_file(reviews)

    suggestion = generate_suggestions(reviews)

    return jsonify({'reviews': reviews, 'suggestion': suggestion})

@app.route('/reviews.json')
def reviews_json():
    return send_from_directory(os.getcwd(), 'reviews.json', as_attachment=False)

if __name__ == '__main__':
    app.run(debug=True)
