export interface Topic {
  topic_id: string;
  category: string;
  name: string;
  description: string;
  source_pages: number[];
  display_order: number;
}

export interface AnswerOption {
  id: string;
  text: string;
}

export interface Question {
  question_id: string;
  topic_id: string;
  category: string;
  question_text: string;
  question_type: string;
  answer_options?: AnswerOption[];
  difficulty: number;
}

export interface QuestionWithAnswer extends Question {
  correct_answer: string;
  explanation: string;
}

export interface AnswerSubmission {
  question_id: string;
  user_answer: string;
  response_time_ms: number;
}

export interface AnswerResponse {
  correct: boolean;
  correct_answer?: string;
  explanation: string;
  source_reference: {
    document: string;
    page: number;
    section: string;
  };
}

export interface UserStats {
  user_id: string;
  total_questions_answered: number;
  total_correct: number;
  overall_accuracy: number;
  current_streak_days: number;
  longest_streak_days: number;
  last_practice_date: string;
  category_stats: Record<string, CategoryStats>;
  topic_stats: Record<string, TopicStats>;
}

export interface CategoryStats {
  questions_answered: number;
  correct_answers: number;
  accuracy: number;
}

export interface TopicStats {
  questions_answered: number;
  correct_answers: number;
  accuracy: number;
  last_attempted: string;
}

export interface UserProfile {
  user_id: string;
  email: string;
  name?: string;
  created_at: string;
  last_login: string;
}
