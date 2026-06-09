import { useState, useEffect, type CSSProperties } from 'react';
import { quest } from '../../api';

/* ── RPG pixel border helper ── */
const rpgBorder = (bg = '#12122a'): CSSProperties => ({
  background: bg,
  border: '3px solid #5a5a8a',
  boxShadow: 'inset 2px 2px 0 #8888bb, inset -2px -2px 0 #2a2a4a',
});

const s: Record<string, CSSProperties> = {
  page: {
    padding: '24px 32px',
    maxWidth: 800,
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
    padding: '10px 24px',
    fontFamily: "'VT323', monospace",
    fontSize: 20,
    cursor: 'pointer',
    border: '2px solid',
    transition: 'all 0.15s',
  },
  card: {
    ...rpgBorder('#0e0e22'),
    padding: '14px 16px',
    marginBottom: 10,
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    transition: 'all 0.15s',
  },
  questTitle: {
    fontFamily: "'Press Start 2P', monospace",
    fontSize: 9,
    color: '#c8c8e0',
    marginBottom: 6,
  },
  questDesc: {
    fontFamily: "'VT323', monospace",
    fontSize: 17,
    color: '#6a6a8a',
  },
  progress: {
    display: 'flex',
    alignItems: 'center',
    gap: 10,
    flexShrink: 0,
  },
  progressBar: {
    width: 80,
    height: 10,
    background: '#0a0a18',
    border: '2px solid',
    borderColor: '#2a2a4a #6a6a8a #6a6a8a #2a2a4a',
    overflow: 'hidden',
  },
  exp: {
    fontFamily: "'Press Start 2P', monospace",
    fontSize: 7,
    color: '#f1c40f',
  },
  done: {
    fontFamily: "'Press Start 2P', monospace",
    fontSize: 7,
    color: '#2ecc71',
    padding: '4px 8px',
    border: '2px solid #2ecc71',
    background: 'rgba(46,204,113,0.1)',
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

export default function QuestPanel() {
  const [tab, setTab] = useState<'daily' | 'challenge'>('daily');
  const [dailyQuests, setDailyQuests] = useState<any[]>([]);
  const [challenges, setChallenges] = useState<any[]>([]);

  useEffect(() => {
    quest.getDailyQuests().then(r => setDailyQuests(r.data)).catch(() => {});
    quest.getChallenges().then(r => setChallenges(r.data)).catch(() => {});
  }, []);

  const quests = tab === 'daily' ? dailyQuests : challenges;

  return (
    <div style={s.page}>
      <div style={s.header}>
        <span style={{ color: '#5dade2' }}>⚔</span>
        冒险任务
      </div>

      <div style={s.tabs}>
        {(['daily', 'challenge'] as const).map(t => (
          <button key={t} style={{
            ...s.tab,
            background: tab === t ? 'rgba(241,196,15,0.12)' : 'transparent',
            color: tab === t ? '#f1c40f' : '#6a6a8a',
            borderColor: tab === t ? '#f1c40f' : '#2a2a4a',
          }} onClick={() => setTab(t)}>
            {tab === t ? '▶ ' : '  '}{t === 'daily' ? '每日任务' : '挑战任务'}
          </button>
        ))}
      </div>

      {quests.length === 0 && (
        <div style={s.empty}>- 暂无任务 -</div>
      )}

      {quests.map((q: any, i: number) => {
        const pct = Math.min(100, (q.progress || 0) / (q.condition_value || 1) * 100);
        return (
          <div key={i} style={s.card}>
            <div style={{ flex: 1, marginRight: 12 }}>
              <div style={s.questTitle}>{q.title}</div>
              <div style={s.questDesc}>{q.description}</div>
            </div>
            <div style={s.progress}>
              <div style={s.progressBar}>
                <div style={{
                  height: '100%',
                  width: `${pct}%`,
                  background: pct >= 100
                    ? 'repeating-linear-gradient(90deg, #2ecc71 0px, #2ecc71 3px, #1a9a50 3px, #1a9a50 5px)'
                    : 'repeating-linear-gradient(90deg, #5dade2 0px, #5dade2 3px, #3a8ab0 3px, #3a8ab0 5px)',
                }} />
              </div>
              <div style={{
                fontFamily: "'VT323', monospace",
                fontSize: 16,
                color: '#6a6a8a',
                minWidth: 36,
                textAlign: 'right' as const,
              }}>
                {q.progress || 0}/{q.condition_value}
              </div>
              {q.status === 'completed'
                ? <div style={s.done}>DONE</div>
                : <div style={s.exp}>+{q.exp_reward}</div>}
            </div>
          </div>
        );
      })}
    </div>
  );
}
