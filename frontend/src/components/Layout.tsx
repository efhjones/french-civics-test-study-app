import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { ErrorBoundary } from "react-error-boundary";

interface LayoutProps {
  children: React.ReactNode;
}

export const Layout: React.FC<LayoutProps> = ({ children }) => {
  const { user, isAuthenticated, signOut } = useAuth();
  const navigate = useNavigate();

  const handleSignOut = async () => {
    await signOut();
    navigate("/");
  };

  return (
    <div className="app-container">
      <nav className="navbar">
        <div className="nav-brand">
          <Link to="/">🇫🇷 Test Civique</Link>
        </div>
        <div className="nav-links">
          {isAuthenticated ? (
            <>
              <Link to="/">Accueil</Link>
              <Link to="/practice">Pratiquer</Link>
              <Link to="/topics">Thèmes</Link>
              <Link to="/dashboard">Statistiques</Link>
              <div className="nav-user">
                <span>{user?.name || user?.email}</span>
                <button onClick={handleSignOut} className="btn-link">
                  Déconnexion
                </button>
              </div>
            </>
          ) : (
            <>
              <Link to="/">Accueil</Link>
              <Link to="/topics">Thèmes</Link>
            </>
          )}
        </div>
      </nav>
      <ErrorBoundary fallback={<p>⚠️ Something went wrong</p>}>
        <main className="main-content">{children}</main>
      </ErrorBoundary>
      <footer className="footer">
        <p>
          © 2026 French Civics Test - Basé sur le Livret du citoyen officiel
        </p>
      </footer>
    </div>
  );
};
