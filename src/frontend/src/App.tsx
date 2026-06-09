import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './hooks/useAuth';
import Layout from './components/Layout/Layout';
import Login from './components/Auth/Login';
import WorldMapPage from './pages/WorldMapPage';
import ChapterMapPage from './pages/ChapterMapPage';
import LearnPage from './pages/LearnPage';
import QuestPage from './pages/QuestPage';
import AchievementPage from './pages/AchievementPage';
import LeaderboardPage from './pages/LeaderboardPage';
import ProfilePage from './pages/ProfilePage';
import type { ReactNode } from 'react';

function ProtectedRoute({ children }: { children: ReactNode }) {
  const { isAuthenticated, loading } = useAuth();
  if (loading) return <div style={{ color: '#6a6a8a', padding: 40, fontFamily: "'Press Start 2P'" }}>Loading...</div>;
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  return <>{children}</>;
}

function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/" element={<ProtectedRoute><Layout /></ProtectedRoute>}>
        <Route index element={<Navigate to="/map" replace />} />
        <Route path="map" element={<WorldMapPage />} />
        <Route path="map/:courseId" element={<ChapterMapPage />} />
        <Route path="map/:courseId/learn/:nodeId" element={<LearnPage />} />
        <Route path="quests" element={<QuestPage />} />
        <Route path="achievements" element={<AchievementPage />} />
        <Route path="leaderboard" element={<LeaderboardPage />} />
        <Route path="profile" element={<ProfilePage />} />
      </Route>
    </Routes>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </BrowserRouter>
  );
}
