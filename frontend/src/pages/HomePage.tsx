import React from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

export const HomePage: React.FC = () => {
  const navigate = useNavigate();
  const { user } = useAuth();

  return (
    <div className="home-page">
      <div className="hero">
        <h1>Test de Culture Civique Française</h1>
        <p className="subtitle">
          Préparez-vous au test de naturalisation française avec notre
          application interactive
        </p>

        {user && (
          <div className="welcome-message">
            <h2>Bienvenue, {user.name || user.email}!</h2>
          </div>
        )}

        <div className="cta-buttons">
          <button
            className="btn btn-primary"
            onClick={() => navigate("/practice")}
          >
            Commencer la pratique
          </button>
          <button
            className="btn btn-secondary"
            onClick={() => navigate("/topics")}
          >
            Explorer les thèmes
          </button>
        </div>
      </div>

      <div className="features">
        <div className="feature-card">
          <h3>📚 15 Thèmes</h3>
          <p>Histoire, politique, géographie et culture française</p>
        </div>
        <div className="feature-card">
          <h3>🎯 Apprentissage Adaptatif</h3>
          <p>Les questions s'adaptent à votre niveau</p>
        </div>
        <div className="feature-card">
          <h3>📊 Suivi des Progrès</h3>
          <p>Visualisez vos statistiques en temps réel</p>
        </div>
        <div className="feature-card">
          <h3>✅ Questions Vérifiées</h3>
          <p>Basées sur le Livret du citoyen officiel</p>
        </div>
      </div>

      <div className="info-section">
        <h2>Comment ça marche?</h2>
        <ol>
          <li>
            <strong>Commencez à pratiquer</strong> - Répondez aux questions sur
            divers thèmes
          </li>
          <li>
            <strong>Recevez des explications détaillées</strong> - Apprenez de
            chaque réponse
          </li>
          <li>
            <strong>Suivez vos progrès</strong> - Consultez vos statistiques par
            thème et catégorie
          </li>
          <li>
            <strong>Améliorez-vous continuellement</strong> - L'algorithme
            adapte les questions à votre niveau
          </li>
        </ol>
      </div>
    </div>
  );
};
