import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';
import type { UserStats } from '../types';

export const DashboardPage: React.FC = () => {
  const [stats, setStats] = useState<UserStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    setLoading(true);
    try {
      const { stats: userStats } = await apiService.getUserStats();
      setStats(userStats);
    } catch (error) {
      console.error('Error loading stats:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="dashboard-page">
        <div className="loading">Chargement des statistiques...</div>
      </div>
    );
  }

  if (!stats) {
    return (
      <div className="dashboard-page">
        <div className="error">Impossible de charger les statistiques</div>
      </div>
    );
  }

  return (
    <div className="dashboard-page">
      <h1>Tableau de bord</h1>

      <div className="stats-overview">
        <div className="stat-card">
          <div className="stat-value">{stats.total_questions_answered}</div>
          <div className="stat-label">Questions répondues</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{stats.overall_accuracy.toFixed(1)}%</div>
          <div className="stat-label">Précision globale</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{stats.current_streak_days}</div>
          <div className="stat-label">Série actuelle (jours)</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{stats.longest_streak_days}</div>
          <div className="stat-label">Meilleure série</div>
        </div>
      </div>

      <div className="category-stats-section">
        <h2>Performances par catégorie</h2>
        <div className="category-stats-grid">
          {Object.entries(stats.category_stats).map(([category, categoryStats]) => (
            <div key={category} className="category-stat-card">
              <h3>{category}</h3>
              <div className="progress-bar">
                <div
                  className="progress-fill"
                  style={{ width: `${categoryStats.accuracy}%` }}
                />
              </div>
              <div className="stat-details">
                <span className="accuracy">{categoryStats.accuracy.toFixed(1)}%</span>
                <span className="count">
                  {categoryStats.correct_answers}/{categoryStats.questions_answered} correct
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="topic-stats-section">
        <h2>Performances par thème</h2>
        <div className="topic-stats-list">
          {Object.entries(stats.topic_stats)
            .sort((a, b) => a[1].accuracy - b[1].accuracy)
            .map(([topicId, topicStats]) => (
              <div key={topicId} className="topic-stat-row">
                <div className="topic-info">
                  <span className="topic-id">{topicId}</span>
                  <div className="mini-progress-bar">
                    <div
                      className="mini-progress-fill"
                      style={{ width: `${topicStats.accuracy}%` }}
                    />
                  </div>
                </div>
                <div className="topic-metrics">
                  <span className="accuracy">{topicStats.accuracy.toFixed(1)}%</span>
                  <span className="count">
                    {topicStats.correct_answers}/{topicStats.questions_answered}
                  </span>
                </div>
              </div>
            ))}
        </div>
      </div>

      {stats.last_practice_date && (
        <div className="last-practice">
          Dernière pratique: {new Date(stats.last_practice_date).toLocaleDateString('fr-FR')}
        </div>
      )}
    </div>
  );
};
