import { useState, type CSSProperties } from 'react';
import { graph } from '../../api';
import { useEffect } from 'react';

interface Props {
  node: {
    id: string; name: string; description: string; state?: string; stars?: number;
    node_type: string; parent_id: string | null;
  };
  onClose: () => void;
  onComplete: (nodeId: string) => Promise<any>;
  onRate: (nodeId: string, stars: number) => Promise<void>;
}

/* ── RPG pixel border helper ── */
const rpgBorder = (bg = '#12122a'): CSSProperties => ({
  background: bg,
  border: '3px solid #5a5a8a',
  boxShadow: 'inset 2px 2px 0 #8888bb, inset -2px -2px 0 #2a2a4a',
});

const STATE_LABELS: Record<string, { text: string; color: string }> = {
  mastered: { text: '★ 已精通', color: '#f1c40f' },
  explored: { text: '◆ 已探索', color: '#2ecc71' },
  unlocked: { text: '◇ 可学习', color: '#5dade2' },
};

const s: Record<string, CSSProperties> = {
  overlay: {
    position: 'absolute', top: 0, right: 0, width: 360, height: '100%',
    ...rpgBorder('#0e0e22'),
    borderRight: 'none',
    borderTop: 'none',
    borderBottom: 'none',
    padding: '20px 16px', overflowY: 'auto', zIndex: 20,
    animation: 'slideLeft 0.2s ease',
  },
  close: {
    position: 'absolute', top: 10, right: 12, background: 'transparent',
    border: 'none', color: '#6a6a8a', fontFamily: "'Press Start 2P', monospace",
    fontSize: 10, cursor: 'pointer',
  },
  stateBadge: {
    display: 'inline-block',
    padding: '4px 10px',
    border: '2px solid',
    fontFamily: "'Press Start 2P', monospace",
    fontSize: 7,
    letterSpacing: 1,
    marginBottom: 14,
  },
  title: {
    fontFamily: "'Press Start 2P', monospace",
    fontSize: 11,
    color: '#c8c8e0',
    marginBottom: 12,
    lineHeight: 1.6,
  },
  desc: {
    fontFamily: "'VT323', monospace",
    fontSize: 18,
    color: '#6a6a8a',
    lineHeight: 1.5,
    marginBottom: 20,
    borderBottom: '2px solid #2a2a4a',
    paddingBottom: 16,
  },
  section: { marginBottom: 16 },
  sectionTitle: {
    fontFamily: "'Press Start 2P', monospace",
    fontSize: 7,
    color: '#5a5a8a',
    marginBottom: 8,
    letterSpacing: 1,
  },
  prereqItem: {
    fontFamily: "'VT323', monospace",
    fontSize: 18,
    color: '#2ecc71',
    padding: '2px 0',
  },
  btn: {
    width: '100%', padding: '14px 0',
    border: '3px solid',
    fontFamily: "'Press Start 2P', monospace",
    fontSize: 10, cursor: 'pointer',
    transition: 'all 0.15s',
    letterSpacing: 1,
  },
  starRow: {
    display: 'flex', gap: 12, justifyContent: 'center', marginTop: 8,
  },
  star: {
    fontSize: 24, cursor: 'pointer', transition: 'transform 0.15s',
    fontFamily: "'Press Start 2P', monospace",
  },
  result: {
    marginTop: 16, padding: 14,
    ...rpgBorder('#0a0a18'),
  },
  resultItem: {
    fontFamily: "'VT323', monospace",
    fontSize: 18, color: '#c8c8e0', padding: '3px 0',
  },
  tunnel: {
    marginTop: 8, padding: '8px 12px',
    border: '2px solid rgba(241,196,15,0.3)',
    background: 'rgba(241,196,15,0.05)',
    fontFamily: "'VT323', monospace",
    fontSize: 18, color: '#f1c40f',
  },
};

export default function NodeDetail({ node, onClose, onComplete, onRate }: Props) {
  const [prereqs, setPrereqs] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  useEffect(() => {
    graph.getNode(node.id).then(res => {
      setPrereqs(res.data.prerequisites || []);
    }).catch(() => {});
  }, [node.id]);

  const handleComplete = async () => {
    setLoading(true);
    const res = await onComplete(node.id);
    if (res) setResult(res);
    setLoading(false);
  };

  const isExplored = node.state === 'explored' || node.state === 'mastered';
  const stateInfo = STATE_LABELS[node.state || ''] || STATE_LABELS.unlocked;

  return (
    <div style={s.overlay}>
      <button style={s.close} onClick={onClose}>X</button>

      {/* State Badge */}
      <div style={{
        ...s.stateBadge,
        color: stateInfo.color,
        borderColor: stateInfo.color,
        background: `${stateInfo.color}15`,
      }}>
        {stateInfo.text}
      </div>

      <div style={s.title}>{node.name}</div>
      <div style={s.desc}>{node.description}</div>

      {/* Stars */}
      {isExplored && (
        <div style={s.section}>
          <div style={s.sectionTitle}>MASTERY</div>
          <div style={s.starRow}>
            {[1, 2, 3].map(i => (
              <span key={i} style={{
                ...s.star,
                color: i <= (node.stars || 0) ? '#f1c40f' : '#2a2a4a',
                textShadow: i <= (node.stars || 0) ? '0 0 8px rgba(241,196,15,0.5)' : 'none',
              }}
                onClick={() => onRate(node.id, i)}
              >★</span>
            ))}
          </div>
        </div>
      )}

      {/* Prerequisites */}
      {prereqs.length > 0 && (
        <div style={s.section}>
          <div style={s.sectionTitle}>PREREQUISITES</div>
          {prereqs.map((p: any) => (
            <div key={p.id || p} style={s.prereqItem}>
              ✓ {p.name || p}
            </div>
          ))}
        </div>
      )}

      {/* Action */}
      {node.state === 'unlocked' && !result && (
        <button
          style={{
            ...s.btn,
            background: loading ? '#1a1a2e' : '#5dade2',
            borderColor: loading ? '#2a2a4a' : '#8adcff #2a7aa0 #2a7aa0 #8adcff',
            color: loading ? '#6a6a8a' : '#0a0a18',
          }}
          onClick={handleComplete}
          disabled={loading}
        >
          {loading ? 'LOADING...' : '▶ 开始探索'}
        </button>
      )}

      {/* Result */}
      {result && (
        <div style={s.result}>
          <div style={{
            fontFamily: "'Press Start 2P', monospace",
            fontSize: 9, color: '#f1c40f', marginBottom: 10,
            textShadow: '0 0 8px rgba(241,196,15,0.4)',
          }}>
            COMPLETE!
          </div>
          <div style={s.resultItem}>▸ +{result.exp_gained} EXP</div>
          {result.new_level && (
            <div style={{ ...s.resultItem, color: '#f1c40f', fontWeight: 600 }}>
              ▸ LEVEL UP! → {result.new_level}
            </div>
          )}
          {result.unlocked_nodes?.length > 0 && (
            <div style={s.resultItem}>
              ▸ 解锁 {result.unlocked_nodes.length} 个新地点：
              {result.unlocked_nodes.map((n: any) => n.name).join('、')}
            </div>
          )}
          {result.discovered_tunnels?.length > 0 && result.discovered_tunnels.map((t: any) => (
            <div key={t.id} style={s.tunnel}>
              ★ 发现暗道！与「{t.name}」相通
            </div>
          ))}
          {result.achievements_earned?.length > 0 && result.achievements_earned.map((a: any) => (
            <div key={a.key} style={{
              ...s.tunnel,
              background: 'rgba(46,204,113,0.05)',
              borderColor: 'rgba(46,204,113,0.3)',
              color: '#2ecc71',
            }}>
              ★ 获得成就：{a.name}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
