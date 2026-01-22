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
  total_questions_answered: number;
  overall_accuracy: number;
  current_streak_days: number;
  longest_streak_days: number;
  last_activity_date: string;
  last_updated: string;
  stats_by_category: Record<string, CategoryStats>;
  weakest_topics: TopicRanking[];
  strongest_topics: TopicRanking[];
}

export interface CategoryStats {
  total: number;
  correct: number;
  accuracy: number;
}

export interface TopicRanking {
  topic_id: string;
  topic_name: string;
  accuracy: number;
}

export interface UserProfile {
  user_id: string;
  email: string;
  name?: string;
  created_at: string;
  last_login: string;
}
