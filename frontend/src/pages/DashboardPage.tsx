import React, { useState, useEffect } from "react";
import { apiService } from "../services/api";
import type { UserStats } from "../types";

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
      debugger;
      setStats(userStats);
    } catch (error) {
      console.error("Error loading stats:", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="dashboard-page">
        <div className="loading">Chnpmargement des statistiques...</div>
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

  const hasStatsByCategory = Object.keys(stats.stats_by_category).length > 0;

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
          <div className="stat-value">TBA</div>
          <div className="stat-label">Réponses correctes</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{stats.current_streak_days}</div>
          <div className="stat-label">Série actuelle</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{stats.longest_streak_days}</div>
          <div className="stat-label">Meilleure série</div>
        </div>
      </div>

      {hasStatsByCategory ? (
        <div className="category-stats-section">
          <h2>Performances par catégorie</h2>
          <div className="category-stats-grid">
            {Object.entries(stats.stats_by_category).map(
              ([category, categoryStats]) => (
                <div key={category} className="category-stat-card">
                  <h3>{category}</h3>
                  <div className="progress-bar">
                    <div
                      className="progress-fill"
                      style={{ width: `${categoryStats.accuracy}%` }}
                    />
                  </div>
                  <div className="stat-details">
                    <span className="accuracy">
                      {categoryStats.accuracy.toFixed(1)}%
                    </span>
                    <span className="count">
                      {categoryStats.correct}/{categoryStats.total} correct
                    </span>
                  </div>
                </div>
              )
            )}
          </div>
        </div>
      ) : null}

      {(stats.weakest_topics.length > 0 ||
        stats.strongest_topics.length > 0) && (
        <div className="topic-rankings-section">
          {stats.weakest_topics.length > 0 && (
            <div className="topic-ranking">
              <h2>🎯 Thèmes à améliorer</h2>
              <div className="topic-list">
                {stats.weakest_topics.map((topic) => (
                  <div key={topic.topic_id} className="topic-rank-item weak">
                    <div className="topic-info">
                      <span className="topic-name">{topic.topic_name}</span>
                      <div className="mini-progress-bar">
                        <div
                          className="mini-progress-fill weak"
                          style={{ width: `${topic.accuracy}%` }}
                        />
                      </div>
                    </div>
                    <span className="topic-accuracy">
                      {topic.accuracy.toFixed(1)}%
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {stats.strongest_topics.length > 0 && (
            <div className="topic-ranking">
              <h2>⭐ Vos meilleurs thèmes</h2>
              <div className="topic-list">
                {stats.strongest_topics.map((topic) => (
                  <div key={topic.topic_id} className="topic-rank-item strong">
                    <div className="topic-info">
                      <span className="topic-name">{topic.topic_name}</span>
                      <div className="mini-progress-bar">
                        <div
                          className="mini-progress-fill strong"
                          style={{ width: `${topic.accuracy}%` }}
                        />
                      </div>
                    </div>
                    <span className="topic-accuracy">
                      {topic.accuracy.toFixed(1)}%
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {stats.last_activity_date && (
        <div className="last-practice">
          Dernière activité:{" "}
          {new Date(stats.last_activity_date).toLocaleDateString("fr-FR")}
        </div>
      )}
    </div>
  );
};
