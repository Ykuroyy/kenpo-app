
document.addEventListener('DOMContentLoaded', () => {
    // クイズコンテナが存在する場合のみ以下の処理を実行
    if (!document.getElementById('quiz-container')) return;

    // --- 要素の取得 ---
    const quizHeader = document.getElementById('quiz-header');
    const progressText = document.getElementById('progress-text');
    const questionGenre = document.getElementById('question-genre');
    const questionText = document.getElementById('question-text');
    const optionsArea = document.getElementById('options-area');
    const feedbackArea = document.getElementById('feedback-area');
    const explanationArea = document.getElementById('explanation-area');
    const explanationText = document.getElementById('explanation-text');
    const nextBtn = document.getElementById('next-btn');

    // --- 変数の初期化 ---
    let quizzes = [];
    let currentQuizIndex = 0;
    let score = 0;
    let isAnswered = false;

    // --- ヘッダーのテキストを設定 ---
    const difficultyMap = {
        easy: 'かんたん',
        normal: 'ふつう',
        hard: 'むずかしい'
    };
    quizHeader.textContent = `けんぽうクイズ - ${difficultyMap[DIFFICULTY] || 'Unknown'} -`;

    // --- クイズデータをサーバーから取得 ---
    async function fetchQuizzes() {
        try {
            const response = await fetch(`/api/quizzes/${DIFFICULTY}`);
            if (!response.ok) {
                throw new Error('クイズデータの取得に失敗しました。');
            }
            quizzes = await response.json();
            if (quizzes.length > 0) {
                // クイズをランダムに並び替え
                quizzes.sort(() => Math.random() - 0.5);
                displayQuiz();
            } else {
                questionText.textContent = 'このレベルのクイズはまだありません。ごめんなさい！😢';
            }
        } catch (error) {
            console.error(error);
            questionText.textContent = 'エラーが発生しました。ページを再読み込みしてください。';
        }
    }

    // --- クイズを表示する関数 ---
    function displayQuiz() {
        // UIをリセット
        resetState();
        isAnswered = false;

        const quiz = quizzes[currentQuizIndex];
        progressText.textContent = `第${currentQuizIndex + 1}問 / ${quizzes.length}問`;
        questionGenre.textContent = quiz.genre;
        questionText.textContent = quiz.question;

        // 選択肢を作成
        quiz.options.forEach(option => {
            const button = document.createElement('button');
            button.textContent = option;
            button.classList.add('btn');
            button.addEventListener('click', () => checkAnswer(option, button));
            optionsArea.appendChild(button);
        });
    }

    // --- 回答をチェックする関数 ---
    function checkAnswer(selectedOption, selectedButton) {
        if (isAnswered) return; // 回答済みの場合は何もしない
        isAnswered = true;

        const quiz = quizzes[currentQuizIndex];
        const isCorrect = selectedOption === quiz.answer;

        // フィードバックを表示
        feedbackArea.style.display = 'block';
        if (isCorrect) {
            score++;
            feedbackArea.textContent = '🎉 正解！';
            feedbackArea.className = 'correct';
        } else {
            feedbackArea.textContent = '😢 不正解...';
            feedbackArea.className = 'incorrect';
        }

        // 解説を表示
        explanationText.textContent = quiz.explanation;
        explanationArea.style.display = 'block';

        // 次へボタンを表示
        nextBtn.style.display = 'block';

        // 選択肢のボタンを無効化
        Array.from(optionsArea.children).forEach(btn => {
            btn.disabled = true;
            if (btn.textContent === quiz.answer) {
                // 正解の選択肢をハイライト
                btn.style.backgroundColor = '#a8e6cf'; // ミントグリーン
                btn.style.borderColor = '#a8e6cf';
            }
        });
    }

    // --- 次の問題へ進む or 結果画面へ ---
    nextBtn.addEventListener('click', () => {
        currentQuizIndex++;
        if (currentQuizIndex < quizzes.length) {
            displayQuiz();
        } else {
            // クイズ終了、結果ページへリダイレクト
            window.location.href = `/result?score=${score}&total=${quizzes.length}`;
        }
    });

    // --- UIの状態をリセットする関数 ---
    function resetState() {
        feedbackArea.style.display = 'none';
        explanationArea.style.display = 'none';
        nextBtn.style.display = 'none';
        while (optionsArea.firstChild) {
            optionsArea.removeChild(optionsArea.firstChild);
        }
    }

    // --- 最初のクイズを取得して開始 ---
    fetchQuizzes();
});
