
import os
import json
from flask import Flask, render_template, jsonify, request

# アプリケーションのルートディレクトリを取得
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder=os.path.join(BASE_DIR, 'static'))

# ログレベルを設定
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 起動時のログ
logger.info(f"Application starting...")
logger.info(f"BASE_DIR: {BASE_DIR}")
logger.info(f"PORT: {os.environ.get('PORT', 'Not set')}")
logger.info(f"FLASK_ENV: {os.environ.get('FLASK_ENV', 'Not set')}")

# クイズデータを読み込む
def load_quizzes():
    try:
        quiz_file_path = os.path.join(BASE_DIR, 'static', 'data', 'quizzes.json')
        logger.info(f"Loading quizzes from: {quiz_file_path}")
        
        if not os.path.exists(quiz_file_path):
            logger.error(f"Quiz file not found at: {quiz_file_path}")
            return {"easy": [], "normal": [], "hard": []}
            
        with open(quiz_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            logger.info(f"Successfully loaded quizzes: {list(data.keys())}")
            return data
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
    logger.info("Health check requested")
    try:
        # 基本的な機能テスト
        quizzes = load_quizzes()
        return jsonify({
            "status": "healthy",
            "quizzes_loaded": len(quizzes) > 0,
            "available_difficulties": list(quizzes.keys()),
            "port": os.environ.get('PORT', 'Not set'),
            "base_dir": BASE_DIR
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

@app.route('/debug')
def debug():
    """デバッグ情報を表示"""
    logger.info("Debug info requested")
    try:
        debug_info = {
            "base_dir": BASE_DIR,
            "static_folder": app.static_folder,
            "templates_folder": app.template_folder,
            "port": os.environ.get('PORT', 'Not set'),
            "flask_env": os.environ.get('FLASK_ENV', 'Not set'),
            "files": {
                "quizzes.json": os.path.exists(os.path.join(BASE_DIR, 'static', 'data', 'quizzes.json')),
                "index.html": os.path.exists(os.path.join(BASE_DIR, 'templates', 'index.html')),
                "quiz.html": os.path.exists(os.path.join(BASE_DIR, 'templates', 'quiz.html')),
                "result.html": os.path.exists(os.path.join(BASE_DIR, 'templates', 'result.html')),
            }
        }
        return jsonify(debug_info), 200
    except Exception as e:
        logger.error(f"Debug info failed: {e}")
        return jsonify({"error": str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    logger.error(f"404 error: {error}")
    return "ページが見つかりません。", 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"500 error: {error}")
    return "サーバーエラーが発生しました。", 500

# アプリケーション起動時のログ
logger.info("Flask app configured successfully")

