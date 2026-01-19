import React, { createContext, useContext, useState, useEffect } from "react";
import { getCurrentUser, signOut as amplifySignOut } from "aws-amplify/auth";
import type { UserProfile } from "../types";
import { apiService } from "../services/api";

interface AuthContextType {
  user: UserProfile | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  signOut: () => Promise<void>;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};

interface AuthProviderProps {
  children: React.ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<UserProfile | null>(null);
  const [isLoading, setLoading] = useState(true);
  console.log({ user });
  const loadUser = async () => {
    try {
      // Check if user is authenticated with Cognito
      await getCurrentUser();

      // Fetch user profile from our API (creates profile if doesn't exist)
      const { user: profile } = await apiService.getUserProfile();
      setUser(profile);
    } catch (error) {
      console.log("Not authenticated");
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!user) {
      loadUser();
    }
  }, [user, isLoading]);

  const signOut = async () => {
    try {
      await amplifySignOut();
      setUser(null);
    } catch (error) {
      console.error("Error signing out:", error);
    }
  };

  const refreshUser = async () => {
    await loadUser();
  };

  const value = {
    user,
    isLoading,
    isAuthenticated: !!user,
    signOut,
    refreshUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
