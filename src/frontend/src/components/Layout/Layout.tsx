import { NavLink, Outlet, useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { useState, useRef, type CSSProperties } from 'react';

const navItems = [
  { path: '/map', label: '课程地图' },
  { path: '/quests', label: '学习任务' },
  { path: '/achievements', label: '徽章' },
  { path: '/leaderboard', label: '排行榜' },
  { path: '/profile', label: '个人中心' },
];

const s: Record<string, CSSProperties> = {
  wrapper: {
    display: 'flex',
    height: '100vh',
    width: '100vw',
    overflow: 'hidden',
    background: '#0c0c1d',
  },
  sidebar: {
    width: 220,
    minWidth: 220,
    background: '#10102a',
    borderRight: '1px solid rgba(90,90,138,0.2)',
    display: 'flex',
    flexDirection: 'column',
    zIndex: 10,
  },
  logoArea: {
    padding: '20px 16px 16px',
    borderBottom: '1px solid rgba(90,90,138,0.15)',
    textAlign: 'center' as const,
  },
  logoText: {
    fontFamily: "'Press Start 2P', monospace",
    fontSize: 12,
    color: '#f1c40f',
    letterSpacing: 2,
    textShadow: '0 0 10px rgba(241,196,15,0.3)',
  },
  logoSub: {
    fontFamily: "'Inter', sans-serif",
    fontSize: 11,
    color: '#5a5a7a',
    marginTop: 6,
    letterSpacing: 1,
  },
  nav: {
    flex: 1,
    padding: '12px 8px',
    display: 'flex',
    flexDirection: 'column',
    gap: 2,
  },
  navLink: {
    display: 'flex',
    alignItems: 'center',
    gap: 10,
    padding: '10px 14px',
    borderRadius: 6,
    color: '#6a6a8a',
    fontSize: 14,
    fontFamily: "'Inter', sans-serif",
    fontWeight: 500,
    textDecoration: 'none',
    transition: 'all 0.15s',
  },
  navLinkActive: {
    color: '#c8c8e0',
    background: 'rgba(93,173,226,0.1)',
  },
  navDot: {
    width: 6,
    height: 6,
    borderRadius: '50%',
    flexShrink: 0,
  },
  userSection: {
    margin: '0 8px 8px',
    padding: '14px',
    background: '#0e0e22',
    borderRadius: 8,
    border: '1px solid rgba(90,90,138,0.15)',
  },
  userName: {
    fontSize: 14,
    fontWeight: 600,
    color: '#c8c8e0',
    marginBottom: 2,
  },
  userLevel: {
    fontSize: 12,
    color: '#f1c40f',
    fontFamily: "'Press Start 2P', monospace",
    letterSpacing: 0.5,
  },
  expBarOuter: {
    height: 6,
    background: '#0a0a18',
    borderRadius: 3,
    marginTop: 10,
    overflow: 'hidden',
  },
  expBarInner: {
    height: '100%',
    background: 'linear-gradient(90deg, #5dade2, #f1c40f)',
    borderRadius: 3,
    transition: 'width 0.5s ease',
  },
  expText: {
    fontSize: 11,
    color: '#5a5a7a',
    marginTop: 4,
    textAlign: 'right' as const,
  },
  bottomBar: {
    padding: '8px',
    borderTop: '1px solid rgba(90,90,138,0.15)',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  logoutBtn: {
    padding: '6px 12px',
    background: 'transparent',
    border: '1px solid rgba(231,76,60,0.3)',
    borderRadius: 4,
    color: '#e74c3c',
    fontSize: 12,
    cursor: 'pointer',
  },
  bgmBtn: {
    padding: '6px 12px',
    background: 'transparent',
    border: '1px solid rgba(46,204,113,0.3)',
    borderRadius: 4,
    color: '#2ecc71',
    fontSize: 12,
    cursor: 'pointer',
    minWidth: 60,
    textAlign: 'center' as const,
  },
  content: {
    flex: 1,
    minWidth: 0,
    minHeight: 0,
    overflow: 'auto',
    background: '#0c0c1d',
    position: 'relative',
  },
};

export default function Layout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [bgmPlaying, setBgmPlaying] = useState(false);
  const audioRef = useRef<HTMLAudioElement>(null);

  const handleLogout = () => { logout(); navigate('/login'); };

  const toggleBgm = () => {
    if (audioRef.current) {
      if (bgmPlaying) audioRef.current.pause();
      else { audioRef.current.volume = 0.3; audioRef.current.play().catch(() => {}); }
      setBgmPlaying(!bgmPlaying);
    }
  };

  const isMaxLevel = user ? user.exp >= user.exp_to_next : false;
  const expPercent = user
    ? (isMaxLevel ? 100 : Math.min(100, (user.exp / (user.exp_to_next || 1)) * 100))
    : 0;

  return (
    <div style={s.wrapper}>
      <audio ref={audioRef} src="/bgm.mp3" loop />

      <aside style={s.sidebar}>
        <div style={s.logoArea}>
          <div style={s.logoText}>TERRANOVA</div>
          <div style={s.logoSub}>知识探索平台</div>
        </div>

        <nav style={s.nav}>
          {navItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              style={({ isActive }) => ({
                ...s.navLink,
                ...(isActive ? s.navLinkActive : {}),
              })}
            >
              {({ isActive }) => (
                <>
                  <div style={{
                    ...s.navDot,
                    background: isActive ? '#5dade2' : 'transparent',
                    border: isActive ? 'none' : '1px solid #3a3a5a',
                  }} />
                  {item.label}
                </>
              )}
            </NavLink>
          ))}
        </nav>

        {user && (
          <div style={s.userSection}>
            <div style={s.userName}>{user.nickname || user.username}</div>
            <div style={s.userLevel}>
              Lv.{user.level}
            </div>
            <div style={s.expBarOuter}>
              <div style={{ ...s.expBarInner, width: `${expPercent}%` }} />
            </div>
            <div style={s.expText}>
              {isMaxLevel ? 'MAX' : `${user.exp} / ${user.exp_to_next} EXP`}
            </div>
          </div>
        )}

        <div style={s.bottomBar}>
          <button style={s.bgmBtn} onClick={toggleBgm}>
            {bgmPlaying ? '♪ ON' : '♪ OFF'}
          </button>
          <button style={s.logoutBtn} onClick={handleLogout}>退出</button>
        </div>
      </aside>

      <main style={s.content}>
        <Outlet />
      </main>
    </div>
  );
}
