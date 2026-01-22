import React, { useState, useEffect } from "react";
import { apiService } from "../services/api";
import type { Question, AnswerResponse } from "../types";

export const PracticePage: React.FC = () => {
  const [question, setQuestion] = useState<Question | null>(null);
  const [selectedAnswer, setSelectedAnswer] = useState<string>("");
  const [submitted, setSubmitted] = useState(false);
  const [result, setResult] = useState<AnswerResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [startTime, setStartTime] = useState<number>(Date.now());

  const loadNextQuestion = async () => {
    setLoading(true);
    try {
      const { question: nextQuestion } = await apiService.getNextQuestion();
      setQuestion(nextQuestion);
      setSelectedAnswer("");
      setSubmitted(false);
      setResult(null);
      setStartTime(Date.now());
    } catch (error) {
      console.error("Error loading question:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadNextQuestion();
  }, []);

  const handleSubmit = async () => {
    if (!selectedAnswer || !question) return;

    setLoading(true);
    const responseTime = Date.now() - startTime;

    try {
      const response = await apiService.submitAnswer({
        question_id: question.question_id,
        user_answer: selectedAnswer,
        response_time_ms: responseTime,
      });

      setResult(response);
      setSubmitted(true);
    } catch (error) {
      console.error("Error submitting answer:", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading && !question) {
    return (
      <div className="practice-page">
        <div className="loading">Chargement de la question...</div>
      </div>
    );
  }

  if (!question) {
    return (
      <div className="practice-page">
        <div className="error">Aucune question disponible</div>
      </div>
    );
  }

  return (
    <div className="practice-page">
      <div className="question-container">
        <div className="question-header">
          <div className="category-badge">{question.category}</div>
          <div className="difficulty-badge">
            Difficulté:{" "}
            {question.difficulty === 1
              ? "Facile"
              : question.difficulty === 2
              ? "Moyen"
              : "Difficile"}
          </div>
        </div>

        <h2 className="question-text">{question.question_text}</h2>

        <div className="answer-options">
          {question.answer_options?.map((option) => (
            <button
              key={option.id}
              className={`answer-option ${
                selectedAnswer === option.id ? "selected" : ""
              } ${
                submitted
                  ? result?.correct && selectedAnswer === option.id
                    ? "correct"
                    : !result?.correct && selectedAnswer === option.id
                    ? "incorrect"
                    : result?.correct_answer === option.id
                    ? "show-correct"
                    : ""
                  : ""
              }`}
              onClick={() => !submitted && setSelectedAnswer(option.id)}
              disabled={submitted}
            >
              <span className="option-id">{option.id.toUpperCase()}</span>
              <span className="option-text">{option.text}</span>
            </button>
          ))}
        </div>

        {!submitted ? (
          <div className="action-buttons">
            <button
              className="btn btn-primary"
              onClick={handleSubmit}
              disabled={!selectedAnswer || loading}
            >
              {loading ? "Soumission..." : "Soumettre la réponse"}
            </button>
          </div>
        ) : (
          <div className="result-section">
            <div
              className={`result-indicator ${
                result?.correct ? "correct" : "incorrect"
              }`}
            >
              {result?.correct ? "✓ Correct!" : "✗ Incorrect"}
            </div>

            <div className="explanation">
              <h3>Explication:</h3>
              <p>{result?.explanation}</p>
            </div>

            <div className="source-reference">
              <h4>Source:</h4>
              <p>
                {result?.source_reference.document}, page{" "}
                {result?.source_reference.page}
                {result?.source_reference.section &&
                  ` - ${result.source_reference.section}`}
              </p>
            </div>

            <div className="action-buttons">
              <button className="btn btn-primary" onClick={loadNextQuestion}>
                Question suivante →
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
