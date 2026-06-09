import { useState, useEffect, type CSSProperties } from 'react';
import { social } from '../../api';

/* ── RPG pixel border helper ── */
const rpgBorder = (bg = '#12122a'): CSSProperties => ({
  background: bg,
  border: '3px solid #5a5a8a',
  boxShadow: 'inset 2px 2px 0 #8888bb, inset -2px -2px 0 #2a2a4a',
});

const TABS = [
  { key: 'exp', label: '经验值' },
  { key: 'streak', label: '连续打卡' },
  { key: 'explore_rate', label: '探索率' },
];

const RANK_SYMBOLS = ['♛', '♕', '♖'];
const RANK_COLORS = ['#f1c40f', '#bdc3c7', '#a0694b'];

const s: Record<string, CSSProperties> = {
  page: {
    padding: '24px 32px',
    maxWidth: 700,
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
  row: {
    display: 'flex',
    alignItems: 'center',
    gap: 12,
    padding: '12px 14px',
    marginBottom: 6,
    transition: 'all 0.15s',
  },
  rank: {
    width: 30,
    textAlign: 'center' as const,
    fontFamily: "'Press Start 2P', monospace",
    fontSize: 10,
    flexShrink: 0,
  },
  avatar: {
    width: 32,
    height: 32,
    background: '#1a1a2e',
    border: '2px solid',
    borderColor: '#5a5a8a #2a2a4a #2a2a4a #5a5a8a',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontFamily: "'Press Start 2P', monospace",
    color: '#5dade2',
    fontSize: 10,
    flexShrink: 0,
  },
  name: {
    flex: 1,
    overflow: 'hidden',
  },
  username: {
    fontFamily: "'Press Start 2P', monospace",
    fontSize: 8,
    color: '#c8c8e0',
  },
  level: {
    fontFamily: "'VT323', monospace",
    fontSize: 16,
    color: '#6a6a8a',
    marginTop: 2,
  },
  value: {
    fontFamily: "'Press Start 2P', monospace",
    fontSize: 10,
    color: '#5dade2',
    flexShrink: 0,
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

export default function Leaderboard() {
  const [tab, setTab] = useState('exp');
  const [data, setData] = useState<any[]>([]);

  useEffect(() => {
    social.getLeaderboard(tab).then(r => setData(r.data)).catch(() => setData([]));
  }, [tab]);

  const unit = tab === 'exp' ? 'EXP' : tab === 'streak' ? '天' : '%';

  return (
    <div style={s.page}>
      <div style={s.header}>
        <span style={{ color: '#5dade2' }}>♛</span>
        英雄榜
      </div>

      <div style={s.tabs}>
        {TABS.map(t => (
          <button key={t.key} style={{
            ...s.tab,
            background: tab === t.key ? 'rgba(241,196,15,0.12)' : 'transparent',
            color: tab === t.key ? '#f1c40f' : '#6a6a8a',
            borderColor: tab === t.key ? '#f1c40f' : '#2a2a4a',
          }} onClick={() => setTab(t.key)}>
            {tab === t.key ? '▶ ' : '  '}{t.label}
          </button>
        ))}
      </div>

      {data.length === 0 && (
        <div style={s.empty}>- 暂无排名数据 -</div>
      )}

      {data.map((item: any) => {
        const isTop3 = item.rank <= 3;
        return (
          <div key={item.rank} style={{
            ...s.row,
            ...rpgBorder(isTop3 ? '#14142e' : '#0e0e22'),
            borderColor: isTop3 ? `${RANK_COLORS[item.rank - 1]}66` : '#2a2a4a',
          }}>
            <div style={{
              ...s.rank,
              color: isTop3 ? RANK_COLORS[item.rank - 1] : '#6a6a8a',
              fontSize: isTop3 ? 14 : 10,
              textShadow: isTop3 ? `0 0 8px ${RANK_COLORS[item.rank - 1]}44` : 'none',
            }}>
              {isTop3 ? RANK_SYMBOLS[item.rank - 1] : item.rank}
            </div>
            <div style={{
              ...s.avatar,
              borderColor: isTop3
                ? `${RANK_COLORS[item.rank - 1]} ${RANK_COLORS[item.rank - 1]}88 ${RANK_COLORS[item.rank - 1]}88 ${RANK_COLORS[item.rank - 1]}`
                : '#5a5a8a #2a2a4a #2a2a4a #5a5a8a',
            }}>
              {(item.nickname || item.username).charAt(0).toUpperCase()}
            </div>
            <div style={s.name}>
              <div style={s.username}>{item.nickname || item.username}</div>
              <div style={s.level}>{item.level}</div>
            </div>
            <div style={{
              ...s.value,
              color: isTop3 ? RANK_COLORS[item.rank - 1] : '#5dade2',
            }}>
              {item.value} {unit}
            </div>
          </div>
        );
      })}
    </div>
  );
}
