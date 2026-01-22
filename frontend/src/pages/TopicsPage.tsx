import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';
import type { Topic } from '../types';

export const TopicsPage: React.FC = () => {
  const [topics, setTopics] = useState<Topic[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState<string>('all');

  useEffect(() => {
    loadTopics();
  }, [selectedCategory]);

  const loadTopics = async () => {
    setLoading(true);
    try {
      const category = selectedCategory === 'all' ? undefined : selectedCategory;
      const { topics: loadedTopics } = await apiService.getTopics(category);
      setTopics(loadedTopics);
    } catch (error) {
      console.error('Error loading topics:', error);
    } finally {
      setLoading(false);
    }
  };

  const categories = [
    { value: 'all', label: 'Tous les thèmes' },
    { value: 'French History', label: 'Histoire de France' },
    { value: 'French Politics and Institutions', label: 'Politique et Institutions' },
    { value: 'French Geography', label: 'Géographie' },
    { value: 'French Culture', label: 'Culture' },
  ];

  const groupedTopics = topics.reduce((acc, topic) => {
    if (!acc[topic.category]) {
      acc[topic.category] = [];
    }
    acc[topic.category].push(topic);
    return acc;
  }, {} as Record<string, Topic[]>);

  return (
    <div className="topics-page">
      <h1>Thèmes d'apprentissage</h1>

      <div className="category-filter">
        {categories.map((cat) => (
          <button
            key={cat.value}
            className={`filter-btn ${selectedCategory === cat.value ? 'active' : ''}`}
            onClick={() => setSelectedCategory(cat.value)}
          >
            {cat.label}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="loading">Chargement des thèmes...</div>
      ) : (
        <div className="topics-container">
          {Object.entries(groupedTopics).map(([category, categoryTopics]) => (
            <div key={category} className="category-section">
              <h2 className="category-title">{category}</h2>
              <div className="topics-grid">
                {categoryTopics
                  .sort((a, b) => a.display_order - b.display_order)
                  .map((topic) => (
                    <div key={topic.topic_id} className="topic-card">
                      <h3>{topic.name}</h3>
                      <p className="description">{topic.description}</p>
                      <div className="topic-meta">
                        <span className="topic-id">{topic.topic_id}</span>
                        {topic.source_pages && topic.source_pages.length > 0 && (
                          <span className="pages">
                            Pages: {topic.source_pages.join(', ')}
                          </span>
                        )}
                      </div>
                    </div>
                  ))}
              </div>
            </div>
          ))}
        </div>
      )}

      {!loading && topics.length === 0 && (
        <div className="no-topics">Aucun thème disponible pour cette catégorie</div>
      )}
    </div>
  );
};
