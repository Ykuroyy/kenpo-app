
import os
import json
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# クイズデータを読み込む
def load_quizzes():
    try:
        with open('static/data/quizzes.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        app.logger.error("quizzes.json file not found")
        return {"easy": [], "normal": [], "hard": []}
    except json.JSONDecodeError as e:
        app.logger.error(f"Error parsing quizzes.json: {e}")
        return {"easy": [], "normal": [], "hard": []}
    except Exception as e:
        app.logger.error(f"Unexpected error loading quizzes: {e}")
        return {"easy": [], "normal": [], "hard": []}

@app.route('/')
def index():
    """トップページ（難易度選択画面）"""
    try:
        return render_template('index.html')
    except Exception as e:
        app.logger.error(f"Error rendering index.html: {e}")
        return "エラーが発生しました。", 500

@app.route('/quiz/<difficulty>')
def quiz(difficulty):
    """クイズページ"""
    try:
        return render_template('quiz.html', difficulty=difficulty)
    except Exception as e:
        app.logger.error(f"Error rendering quiz.html: {e}")
        return "エラーが発生しました。", 500

@app.route('/api/quizzes/<difficulty>')
def api_quizzes(difficulty):
    """指定された難易度のクイズデータを返すAPI"""
    try:
        quizzes = load_quizzes()
        if difficulty in quizzes:
            return jsonify(quizzes[difficulty])
        else:
            return jsonify({"error": "指定された難易度のクイズは見つかりません。"}), 404
    except Exception as e:
        app.logger.error(f"Error in api_quizzes: {e}")
        return jsonify({"error": "サーバーエラーが発生しました。"}), 500

@app.route('/result')
def result():
    """結果ページ"""
    try:
        # クエリパラメータからスコアと問題数を取得
        score = request.args.get('score', 0, type=int)
        total = request.args.get('total', 0, type=int)
        return render_template('result.html', score=score, total=total)
    except Exception as e:
        app.logger.error(f"Error rendering result.html: {e}")
        return "エラーが発生しました。", 500

@app.errorhandler(404)
def not_found(error):
    return "ページが見つかりません。", 404

@app.errorhandler(500)
def internal_error(error):
    return "サーバーエラーが発生しました。", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=False, host='0.0.0.0', port=port)
