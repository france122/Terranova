import { useState, useEffect, type CSSProperties } from 'react';
import { achievement } from '../../api';

/* ── RPG pixel border helper (unified) ── */
const rpgBorder = (bg = '#12122a'): CSSProperties => ({
  background: bg,
  border: '3px solid #5a5a8a',
  boxShadow: 'inset 2px 2px 0 #8888bb, inset -2px -2px 0 #2a2a4a',
});

const CATEGORY_LABELS: Record<string, string> = {
  milestone: '里程碑',
  mastery: '精通',
  streak: '坚持',
  exploration: '探索',
};

const CATEGORY_COLORS: Record<string, string> = {
  milestone: '#f1c40f',
  mastery: '#e74c3c',
  streak: '#e67e22',
  exploration: '#5dade2',
};

const ICONS: Record<string, string> = {
  foot: '🚀', compass: '🧭', map: '🗺️', star: '⭐', crown: '👑',
  fire: '🔥', flame: '🔥', trophy: '🏆', book: '📖', shield: '🛡️',
};

const s: Record<string, CSSProperties> = {
  page: {
    padding: '24px 32px',
    maxWidth: 960,
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
    justifyContent: 'space-between',
    gap: 10,
  },
  tabs: {
    display: 'flex',
    gap: 0,
    marginBottom: 20,
  },
  tab: {
    padding: '10px 20px',
    fontFamily: "'VT323', monospace",
    fontSize: 20,
    cursor: 'pointer',
    border: '2px solid',
    transition: 'all 0.15s',
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))',
    gap: 12,
  },
  badge: {
    ...rpgBorder('#0e0e22'),
    padding: '20px 16px',
    textAlign: 'center' as const,
    transition: 'all 0.15s',
    position: 'relative' as const,
  },
  badgeIcon: {
    width: 52,
    height: 52,
    margin: '0 auto 12px',
    background: '#0a0a18',
    border: '3px solid',
    borderColor: '#5a5a8a #2a2a4a #2a2a4a #5a5a8a',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: 24,
  },
  badgeName: {
    fontFamily: "'Press Start 2P', monospace",
    fontSize: 8,
    marginBottom: 6,
    lineHeight: 1.6,
  },
  badgeDesc: {
    fontFamily: "'VT323', monospace",
    fontSize: 16,
    lineHeight: 1.4,
    marginBottom: 10,
  },
  badgeTag: {
    display: 'inline-block',
    padding: '3px 8px',
    border: '2px solid',
    fontFamily: "'Press Start 2P', monospace",
    fontSize: 7,
    letterSpacing: 1,
  },
  empty: {
    fontFamily: "'VT323', monospace",
    fontSize: 20,
    color: '#6a6a8a',
    textAlign: 'center' as const,
    padding: 40,
    ...rpgBorder('#0e0e22'),
  },
};

export default function AchievementWall() {
  const [achievements, setAchievements] = useState<any[]>([]);
  const [filter, setFilter] = useState<string>('all');

  useEffect(() => {
    achievement.getAchievements().then(r => setAchievements(r.data)).catch(() => {});
  }, []);

  const earnedCount = achievements.filter(a => a.earned).length;
  const totalCount = achievements.length;
  const categories = ['all', ...Object.keys(CATEGORY_LABELS)];

  const filtered = filter === 'all'
    ? achievements
    : achievements.filter(a => a.category === filter);

  return (
    <div style={s.page}>
      {/* Header */}
      <div style={s.header}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <span style={{ color: '#5dade2' }}>♛</span>
          徽章墙
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <span style={{
            fontFamily: "'Press Start 2P'", fontSize: 14, color: '#f1c40f',
          }}>{earnedCount}</span>
          <span style={{
            fontFamily: "'VT323'", fontSize: 18, color: '#6a6a8a',
          }}>/ {totalCount}</span>
        </div>
      </div>

      {/* Category tabs */}
      <div style={s.tabs}>
        {categories.map(cat => {
          const isActive = filter === cat;
          const label = cat === 'all' ? '全部' : CATEGORY_LABELS[cat] || cat;
          return (
            <button key={cat} onClick={() => setFilter(cat)} style={{
              ...s.tab,
              background: isActive ? 'rgba(241,196,15,0.12)' : 'transparent',
              color: isActive ? '#f1c40f' : '#6a6a8a',
              borderColor: isActive ? '#f1c40f' : '#2a2a4a',
            }}>
              {isActive ? '▶ ' : '  '}{label}
            </button>
          );
        })}
      </div>

      {filtered.length === 0 && (
        <div style={s.empty}>- 暂无徽章 -</div>
      )}

      {/* Badge grid */}
      <div style={s.grid}>
        {filtered.map((a: any) => {
          const earned = a.earned;
          const catColor = CATEGORY_COLORS[a.category] || '#5a5a7a';
          return (
            <div key={a.id} style={{
              ...s.badge,
              opacity: earned ? 1 : 0.45,
            }}>
              {/* Icon */}
              <div style={{
                ...s.badgeIcon,
                borderColor: earned
                  ? `${catColor} ${catColor}88 ${catColor}88 ${catColor}`
                  : '#3a3a5a #1a1a2e #1a1a2e #3a3a5a',
                background: earned ? `${catColor}10` : '#0a0a18',
                filter: earned ? 'none' : 'grayscale(1) brightness(0.6)',
              }}>
                {ICONS[a.icon] || '🏆'}
              </div>

              {/* Name */}
              <div style={{
                ...s.badgeName,
                color: earned ? '#c8c8e0' : '#6a6a7a',
              }}>
                {a.name}
              </div>

              {/* Description */}
              <div style={{
                ...s.badgeDesc,
                color: earned ? '#6a6a8a' : '#2a2a4a',
              }}>
                {a.description}
              </div>

              {/* Status tag */}
              <div style={{
                ...s.badgeTag,
                color: earned ? catColor : '#3a3a5a',
                borderColor: earned ? catColor : '#2a2a4a',
                background: earned ? `${catColor}15` : 'transparent',
              }}>
                {earned ? 'EARNED' : (CATEGORY_LABELS[a.category] || a.category)}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
