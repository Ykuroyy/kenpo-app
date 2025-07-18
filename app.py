
import os
import json
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# ログレベルを設定
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# クイズデータを読み込む
def load_quizzes():
    try:
        with open('static/data/quizzes.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error("quizzes.json file not found")
        return {"easy": [], "normal": [], "hard": []}
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing quizzes.json: {e}")
        return {"easy": [], "normal": [], "hard": []}
    except Exception as e:
        logger.error(f"Unexpected error loading quizzes: {e}")
        return {"easy": [], "normal": [], "hard": []}

@app.route('/')
def index():
    """トップページ（難易度選択画面）"""
    logger.info("Accessing index page")
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error rendering index.html: {e}")
        return "エラーが発生しました。", 500

@app.route('/quiz/<difficulty>')
def quiz(difficulty):
    """クイズページ"""
    logger.info(f"Accessing quiz page with difficulty: {difficulty}")
    try:
        return render_template('quiz.html', difficulty=difficulty)
    except Exception as e:
        logger.error(f"Error rendering quiz.html: {e}")
        return "エラーが発生しました。", 500

@app.route('/api/quizzes/<difficulty>')
def api_quizzes(difficulty):
    """指定された難易度のクイズデータを返すAPI"""
    logger.info(f"API request for difficulty: {difficulty}")
    try:
        quizzes = load_quizzes()
        if difficulty in quizzes:
            return jsonify(quizzes[difficulty])
        else:
            return jsonify({"error": "指定された難易度のクイズは見つかりません。"}), 404
    except Exception as e:
        logger.error(f"Error in api_quizzes: {e}")
        return jsonify({"error": "サーバーエラーが発生しました。"}), 500

@app.route('/result')
def result():
    """結果ページ"""
    logger.info("Accessing result page")
    try:
        # クエリパラメータからスコアと問題数を取得
        score = request.args.get('score', 0, type=int)
        total = request.args.get('total', 0, type=int)
        return render_template('result.html', score=score, total=total)
    except Exception as e:
        logger.error(f"Error rendering result.html: {e}")
        return "エラーが発生しました。", 500

@app.route('/health')
def health():
    """ヘルスチェック用エンドポイント"""
    return jsonify({"status": "healthy"}), 200

@app.errorhandler(404)
def not_found(error):
    logger.error(f"404 error: {error}")
    return "ページが見つかりません。", 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"500 error: {error}")
    return "サーバーエラーが発生しました。", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting Flask app on {host}:{port} with debug={debug}")
    app.run(debug=debug, host=host, port=port)


