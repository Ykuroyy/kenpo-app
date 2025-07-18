
import json
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# クイズデータを読み込む
def load_quizzes():
    with open('static/data/quizzes.json', 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/')
def index():
    """トップページ（難易度選択画面）"""
    return render_template('index.html')

@app.route('/quiz/<difficulty>')
def quiz(difficulty):
    """クイズページ"""
    return render_template('quiz.html', difficulty=difficulty)

@app.route('/api/quizzes/<difficulty>')
def api_quizzes(difficulty):
    """指定された難易度のクイズデータを返すAPI"""
    quizzes = load_quizzes()
    if difficulty in quizzes:
        return jsonify(quizzes[difficulty])
    else:
        return jsonify({"error": "指定された難易度のクイズは見つかりません。"}), 404

@app.route('/result')
def result():
    """結果ページ"""
    # クエリパラメータからスコアと問題数を取得
    score = request.args.get('score', 0, type=int)
    total = request.args.get('total', 0, type=int)
    return render_template('result.html', score=score, total=total)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)
