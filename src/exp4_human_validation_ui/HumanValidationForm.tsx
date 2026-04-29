"""
React component for human annotation form.

This is a basic prototype that can be deployed as a standalone web app
or integrated into a larger dashboard. It handles:
- Case display (one at a time)
- 5-point Likert scale ratings
- Progress tracking
- Auto-save to backend (Firebase/API)

For deployment, use: npm start or serve build/ directory
"""

import React, { useState, useEffect } from 'react';
import './HumanValidationForm.css';

interface Case {
  case_id: string;
  dataset: string;
  explainer: string;
  model_family: string;
  explanation_text: string;
  prediction: string;
  true_label: string;
  technical_metrics: Record<string, number>;
}

interface Rating {
  case_id: string;
  annotator_id: string;
  q1_clarity: number;
  q2_completeness: number;
  q3_concision: number;
  q4_plausibility: number;
  q5_audit_usefulness: number;
  comments: string;
  timestamp: string;
}

const QUESTIONS = [
  {
    id: 'q1_clarity',
    text: 'This explanation is easy to understand.',
    hint: 'Does it use plain language without excessive jargon?'
  },
  {
    id: 'q2_completeness',
    text: 'This explanation explains WHY the model made its decision.',
    hint: 'Does it address the actual reasons for the prediction?'
  },
  {
    id: 'q3_concision',
    text: 'This explanation is concise and not overly wordy.',
    hint: 'Is it reasonably brief or does it ramble?'
  },
  {
    id: 'q4_plausibility',
    text: 'This explanation makes practical sense in the real world.',
    hint: 'Do the reasons logically connect to the decision?'
  },
  {
    id: 'q5_audit_usefulness',
    text: 'I could use this explanation to check if the model is making fair decisions.',
    hint: 'Does it give enough info to audit model fairness?'
  }
];

interface Props {
  cases: Case[];
  annotatorId: string;
  onSubmit: (rating: Rating) => void;
  onProgress?: (current: number, total: number) => void;
}

export const HumanValidationForm: React.FC<Props> = ({
  cases,
  annotatorId,
  onSubmit,
  onProgress
}) => {
  const [caseIndex, setCaseIndex] = useState(0);
  const [ratings, setRatings] = useState<Record<string, number>>({});
  const [comments, setComments] = useState('');
  const [showGuide, setShowGuide] = useState(true);

  const currentCase = cases[caseIndex];
  const allRated = QUESTIONS.every(q => ratings[q.id] !== undefined && ratings[q.id] !== 0);

  useEffect(() => {
    if (onProgress) {
      onProgress(caseIndex, cases.length);
    }
  }, [caseIndex, cases.length, onProgress]);

  const handleRatingChange = (questionId: string, value: number) => {
    setRatings(prev => ({ ...prev, [questionId]: value }));
  };

  const handleSubmitCase = () => {
    if (!allRated) return;

    const rating: Rating = {
      case_id: currentCase.case_id,
      annotator_id: annotatorId,
      q1_clarity: ratings.q1_clarity,
      q2_completeness: ratings.q2_completeness,
      q3_concision: ratings.q3_concision,
      q4_plausibility: ratings.q4_plausibility,
      q5_audit_usefulness: ratings.q5_audit_usefulness,
      comments: comments,
      timestamp: new Date().toISOString()
    };

    onSubmit(rating);

    // Move to next case
    if (caseIndex < cases.length - 1) {
      setCaseIndex(caseIndex + 1);
      setRatings({});
      setComments('');
    } else {
      alert('✅ All cases completed! Thank you for your feedback.');
    }
  };

  const predictionLabel = currentCase.prediction === 1 ? 'YES' : 'NO';
  const trueLabel = currentCase.true_label === 1 ? 'YES' : 'NO';

  return (
    <div className="human-validation-form">
      <header className="form-header">
        <h1>XAI Evaluation Study</h1>
        <p>Rate the quality of AI explanations</p>
      </header>

      {showGuide && (
        <div className="info-banner">
          <p>
            👉 <strong>New here?</strong> Read the{' '}
            <a href="#guide" onClick={() => setShowGuide(false)}>
              annotator guide
            </a>
            {' '}for tips on how to rate each explanation.
          </p>
        </div>
      )}

      <div className="progress-bar">
        <div
          className="progress-fill"
          style={{ width: `${((caseIndex + 1) / cases.length) * 100}%` }}
        ></div>
        <p className="progress-text">
          Case {caseIndex + 1} of {cases.length}
        </p>
      </div>

      <div className="case-container">
        <div className="case-context">
          <div className="context-field">
            <strong>Dataset:</strong> {currentCase.dataset}
          </div>
          <div className="context-field">
            <strong>Model:</strong> {currentCase.model_family}
          </div>
          <div className="context-field">
            <strong>Explainer:</strong> {currentCase.explainer}
          </div>
        </div>

        <div className="prediction-box">
          <p>
            <strong>Model Prediction:</strong> The model predicts <span className="prediction-label">{predictionLabel}</span> for this record.
          </p>
          <p className="hint">(True label: {trueLabel})</p>
        </div>

        <div className="explanation-box">
          <h3>Explanation</h3>
          <p className="explanation-text">{currentCase.explanation_text}</p>
        </div>

        <div className="questions-container">
          <h3>How would you rate this explanation?</h3>
          <p className="questions-intro">
            Please rate each statement on a scale of <strong>1 (Strongly Disagree)</strong> to <strong>5 (Strongly Agree)</strong>
          </p>

          {QUESTIONS.map(q => (
            <div key={q.id} className="question-block">
              <label className="question-text">{q.text}</label>
              <p className="question-hint">{q.hint}</p>

              <div className="likert-scale">
                {[1, 2, 3, 4, 5].map(value => (
                  <button
                    key={value}
                    className={`likert-button ${ratings[q.id] === value ? 'selected' : ''}`}
                    onClick={() => handleRatingChange(q.id, value)}
                  >
                    <span className="likert-value">{value}</span>
                    <span className="likert-label">
                      {value === 1 && 'Strongly\nDisagree'}
                      {value === 2 && 'Disagree'}
                      {value === 3 && 'Neutral'}
                      {value === 4 && 'Agree'}
                      {value === 5 && 'Strongly\nAgree'}
                    </span>
                  </button>
                ))}
              </div>
            </div>
          ))}

          <div className="comments-section">
            <label htmlFor="comments">
              <strong>Optional Comments</strong> - Why did you rate this way?
            </label>
            <textarea
              id="comments"
              value={comments}
              onChange={e => setComments(e.target.value)}
              placeholder="Add any additional feedback here..."
              rows={4}
            />
          </div>
        </div>

        <div className="button-group">
          <button
            className="btn btn-primary"
            onClick={handleSubmitCase}
            disabled={!allRated}
          >
            {caseIndex === cases.length - 1 ? '✓ Finish' : '→ Next Case'}
          </button>
          <p className="help-text">
            {!allRated && '⚠️ Please rate all 5 questions before proceeding'}
          </p>
        </div>
      </div>

      <footer className="form-footer">
        <p>Questions? Contact the research team at [contact]</p>
      </footer>
    </div>
  );
};

export default HumanValidationForm;
