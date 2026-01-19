import axios, { AxiosInstance } from 'axios';
import { fetchAuthSession } from 'aws-amplify/auth';
import type {
  Topic,
  Question,
  AnswerSubmission,
  AnswerResponse,
  UserStats,
  UserProfile,
} from '../types';

class ApiService {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: import.meta.env.VITE_API_GATEWAY_URL,
      headers: {
        'Content-Type': 'application/json',
      },
      withCredentials: false, // We're using Authorization header, not cookies
    });

    // Add request interceptor to include JWT token
    this.client.interceptors.request.use(
      async (config) => {
        try {
          const session = await fetchAuthSession();
          const token = session.tokens?.idToken?.toString();

          if (token) {
            config.headers.Authorization = `Bearer ${token}`;
          }
        } catch (error) {
          console.error('Error getting auth token:', error);
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );
  }

  // Health check (no auth required)
  async checkHealth() {
    const response = await this.client.get('/health');
    return response.data;
  }

  // Topics
  async getTopics(category?: string): Promise<{ topics: Topic[]; count: number }> {
    const params = category ? { category } : {};
    const response = await this.client.get('/topics', { params });
    return response.data.data;
  }

  async getTopic(topicId: string): Promise<{ topic: Topic }> {
    const response = await this.client.get(`/topics/${topicId}`);
    return response.data.data;
  }

  // Questions
  async getNextQuestion(debug = false): Promise<{ question: Question; debug?: any }> {
    const params = debug ? { debug: 'true' } : {};
    const response = await this.client.get('/questions/next', { params });
    return response.data.data;
  }

  async getQuestion(questionId: string, includeAnswer = false): Promise<{ question: Question }> {
    const params = includeAnswer ? { include_answer: 'true' } : {};
    const response = await this.client.get(`/questions/${questionId}`, { params });
    return response.data.data;
  }

  async submitAnswer(submission: AnswerSubmission): Promise<AnswerResponse> {
    const response = await this.client.post('/questions/answer', submission);
    return response.data.data;
  }

  // User
  async getUserProfile(): Promise<{ user: UserProfile }> {
    const response = await this.client.get('/users/me');
    return response.data.data;
  }

  async getUserStats(): Promise<{ stats: UserStats }> {
    const response = await this.client.get('/users/me/stats');
    return response.data.data;
  }

  async getUserHistory(params?: {
    limit?: number;
    topic_id?: string;
    days?: number;
  }): Promise<any> {
    const response = await this.client.get('/users/me/history', { params });
    return response.data.data;
  }
}

export const apiService = new ApiService();
