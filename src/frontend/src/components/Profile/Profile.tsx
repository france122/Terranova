import { useEffect, type CSSProperties } from 'react';
import { useAuth } from '../../hooks/useAuth';

/* ── RPG pixel border helper ── */
const rpgBorder = (bg = '#12122a'): CSSProperties => ({
  background: bg,
  border: '3px solid #5a5a8a',
  boxShadow: 'inset 2px 2px 0 #8888bb, inset -2px -2px 0 #2a2a4a',
});

const s: Record<string, CSSProperties> = {
  page: {
    padding: '24px 32px',
    maxWidth: 600,
    margin: '0 auto',
    animation: 'fadeIn 0.3s ease',
  },
  header: {
    fontFamily: "'Press Start 2P', monospace",
    fontSize: 14,
    color: '#f1c40f',
    marginBottom: 24,
    textShadow: '2px 2px 0 #8a6a00',
    display: 'flex',
    alignItems: 'center',
    gap: 10,
  },
  charSheet: {
    ...rpgBorder('#0e0e22'),
    padding: '24px 20px',
    marginBottom: 16,
    textAlign: 'center' as const,
  },
  portraitFrame: {
    width: 64,
    height: 64,
    margin: '0 auto 16px',
    background: '#0a0a18',
    border: '3px solid',
    borderColor: '#5a5a8a #2a2a4a #2a2a4a #5a5a8a',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontFamily: "'Press Start 2P', monospace",
    fontSize: 24,
    color: '#5dade2',
  },
  name: {
    fontFamily: "'Press Start 2P', monospace",
    fontSize: 12,
    color: '#c8c8e0',
    marginBottom: 6,
  },
  level: {
    fontFamily: "'Press Start 2P', monospace",
    fontSize: 9,
    color: '#f1c40f',
    marginBottom: 20,
    textShadow: '0 0 8px rgba(241,196,15,0.3)',
  },
  barRow: {
    display: 'flex',
    alignItems: 'center',
    gap: 10,
    margin: '0 auto',
    maxWidth: 320,
    marginBottom: 8,
  },
  barLabel: {
    fontFamily: "'Press Start 2P', monospace",
    fontSize: 8,
    width: 32,
    textAlign: 'right' as const,
    flexShrink: 0,
  },
  barOuter: {
    flex: 1,
    height: 12,
    background: '#0a0a18',
    border: '2px solid',
    borderColor: '#2a2a4a #6a6a8a #6a6a8a #2a2a4a',
    overflow: 'hidden',
  },
  barText: {
    fontFamily: "'VT323', monospace",
    fontSize: 16,
    width: 80,
    textAlign: 'left' as const,
    flexShrink: 0,
  },
  stats: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr 1fr',
    gap: 10,
  },
  stat: {
    ...rpgBorder('#0e0e22'),
    padding: '16px 12px',
    textAlign: 'center' as const,
  },
  statValue: {
    fontFamily: "'Press Start 2P', monospace",
    fontSize: 16,
    marginBottom: 8,
  },
  statLabel: {
    fontFamily: "'VT323', monospace",
    fontSize: 17,
    color: '#6a6a8a',
  },
};

export default function Profile() {
  const { user, refreshUser } = useAuth();

  useEffect(() => {
    refreshUser();
  }, [refreshUser]);

  if (!user) return null;

  const isMaxLevel = user.exp >= user.exp_to_next;
  const expPct = isMaxLevel ? 100 : Math.min(100, user.exp / (user.exp_to_next || 1) * 100);

  return (
    <div style={s.page}>
      <div style={s.header}>
        <span style={{ color: '#5dade2' }}>♦</span>
        冒险者资料
      </div>

      {/* Character Sheet */}
      <div style={s.charSheet}>
        {/* Portrait */}
        <div style={s.portraitFrame}>
          {user.username.charAt(0).toUpperCase()}
        </div>

        <div style={s.name}>{user.nickname || user.username}</div>
        <div style={s.level}>Lv.{user.level}</div>

        {/* EXP Bar */}
        <div style={s.barRow}>
          <div style={{ ...s.barLabel, color: '#f1c40f' }}>EXP</div>
          <div style={s.barOuter}>
            <div style={{
              height: '100%',
              width: `${expPct}%`,
              background: isMaxLevel
                ? 'repeating-linear-gradient(90deg, #f1c40f 0px, #f1c40f 4px, #e67e22 4px, #e67e22 6px)'
                : 'repeating-linear-gradient(90deg, #f1c40f 0px, #f1c40f 4px, #c49f0a 4px, #c49f0a 6px)',
            }} />
          </div>
          <div style={{ ...s.barText, color: isMaxLevel ? '#f1c40f' : '#6a6a8a' }}>
            {isMaxLevel ? 'MAX' : `${user.exp}/${user.exp_to_next}`}
          </div>
        </div>
      </div>

      {/* Stats Grid */}
      <div style={s.stats}>
        <div style={s.stat}>
          <div style={{ ...s.statValue, color: '#5dade2' }}>
            {user.explored_count}
          </div>
          <div style={s.statLabel}>已探索</div>
        </div>
        <div style={s.stat}>
          <div style={{ ...s.statValue, color: '#2ecc71' }}>
            {user.mastered_count}
          </div>
          <div style={s.statLabel}>已精通</div>
        </div>
        <div style={s.stat}>
          <div style={{ ...s.statValue, color: '#f1c40f' }}>
            {user.streak_days}
          </div>
          <div style={s.statLabel}>连续天数</div>
        </div>
      </div>
    </div>
  );
}
