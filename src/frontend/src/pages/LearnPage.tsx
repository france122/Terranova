import { useParams, useNavigate } from 'react-router-dom';
import { useState, useEffect, useRef, type CSSProperties, type FormEvent } from 'react';
import { graph, mapApi, learn } from '../api';
import { useAuth } from '../hooks/useAuth';

/* ── RPG pixel border helper (unified) ── */
const rpgBorder = (bg = '#12122a'): CSSProperties => ({
  background: bg,
  border: '3px solid #5a5a8a',
  boxShadow: 'inset 2px 2px 0 #8888bb, inset -2px -2px 0 #2a2a4a',
});

/* ── Dummy AI responses for the prototype ── */
const AI_RESPONSES = [
  '这是一个很好的问题！让我来为你详细解释一下...',
  '根据这个知识点的核心概念，关键在于理解其底层原理和实际应用场景。',
  '你可以这样理解：首先，我们需要明确基本定义，然后通过具体例子来加深理解。',
  '这个概念和前置知识有密切联系。建议你先回顾一下前面学过的内容，这样理解起来会更顺畅。',
  '在实际编程中，这个概念经常用到。比如在处理大规模数据时，选择合适的数据结构至关重要。',
];

interface ChatMsg { role: 'ai' | 'user'; text: string; }

const s: Record<string, CSSProperties> = {
  page: {
    position: 'absolute', inset: 0,
    overflow: 'auto',
    background: '#0c0c1d',
    padding: '20px 24px',
  },
  headerBar: {
    ...rpgBorder('#0e0e22'),
    display: 'flex', alignItems: 'center', gap: 16, marginBottom: 16,
    padding: '12px 16px',
  },
  backBtn: {
    padding: '8px 14px',
    background: '#0a0a18',
    border: '2px solid',
    borderColor: '#5a5a8a #2a2a4a #2a2a4a #5a5a8a',
    color: '#8a8aaa',
    fontFamily: "'VT323', monospace",
    fontSize: 18,
    cursor: 'pointer',
  },
  exitBtn: {
    padding: '8px 14px',
    background: 'rgba(231,76,60,0.1)',
    border: '2px solid',
    borderColor: '#e74c3c88 #e74c3c44 #e74c3c44 #e74c3c88',
    color: '#e74c3c',
    fontFamily: "'Press Start 2P'", fontSize: 7,
    cursor: 'pointer', letterSpacing: 1,
  },
  panel: {
    ...rpgBorder('#0a0a18'),
    display: 'flex',
    flexDirection: 'column' as const,
  },
  panelHeader: {
    padding: '10px 14px',
    borderBottom: '2px solid #2a2a4a',
    fontFamily: "'Press Start 2P', monospace",
    fontSize: 8, letterSpacing: 1,
  },
  sectionTitle: {
    fontFamily: "'Press Start 2P', monospace",
    fontSize: 8,
    color: '#5a5a8a',
    marginBottom: 10,
    letterSpacing: 1,
  },
};

export default function LearnPage() {
  const { courseId, nodeId } = useParams<{ courseId: string; nodeId: string }>();
  const navigate = useNavigate();
  const { refreshUser } = useAuth();

  const [node, setNode] = useState<any>(null);
  const [nodeState, setNodeState] = useState<string>('locked');
  const [nodeStars, setNodeStars] = useState(0);
  const [prereqs, setPrereqs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [completing, setCompleting] = useState(false);
  const [result, setResult] = useState<any>(null);

  // Video prototype state
  const [videoPlaying, setVideoPlaying] = useState(false);
  const [videoProgress, setVideoProgress] = useState(0);
  const videoTimer = useRef<ReturnType<typeof setInterval> | undefined>(undefined);
  const autoCompleted = useRef(false);

  // AI Chat prototype state
  const [messages, setMessages] = useState<ChatMsg[]>([
    { role: 'ai', text: '你好！我是你的 AI 助教。关于这个知识点，你有什么问题吗？' },
  ]);
  const [chatInput, setChatInput] = useState('');
  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!nodeId) return;
    const load = async () => {
      setLoading(true);
      try {
        const [nodeRes, stateRes] = await Promise.all([
          graph.getNode(nodeId),
          mapApi.getMapState('cs'),
        ]);
        setNode(nodeRes.data);
        setPrereqs(nodeRes.data.prerequisites || []);
        const ns = stateRes.data.nodes.find((n: any) => n.node_id === nodeId);
        if (ns) { setNodeState(ns.state); setNodeStars(ns.stars); }
      } catch (e) { console.error(e); }
      setLoading(false);
    };
    load();
  }, [nodeId]);

  // Video timer simulation
  useEffect(() => {
    if (videoPlaying) {
      videoTimer.current = setInterval(() => {
        setVideoProgress(p => {
          if (p >= 100) { setVideoPlaying(false); return 100; }
          return p + 0.5;
        });
      }, 100);
    } else {
      clearInterval(videoTimer.current);
    }
    return () => clearInterval(videoTimer.current);
  }, [videoPlaying]);

  // Auto-complete when video finishes
  useEffect(() => {
    if (
      videoProgress >= 100 &&
      !autoCompleted.current &&
      nodeState === 'unlocked' &&
      !result &&
      !completing &&
      nodeId
    ) {
      autoCompleted.current = true;
      handleAutoComplete();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [videoProgress, nodeState, result, completing, nodeId]);

  // Chat auto-scroll
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleAutoComplete = async () => {
    if (!nodeId) return;
    setCompleting(true);
    try {
      const r = await learn.completeNode(nodeId);
      setResult(r.data);
      setNodeState('explored');
      await refreshUser();
    } catch {}
    setCompleting(false);
  };

  const handleRate = async (stars: number) => {
    if (!nodeId || stars <= nodeStars) return;
    try {
      await learn.rateNode(nodeId, stars);
      setNodeStars(stars);
      await refreshUser();
    } catch {}
  };

  const handleChatSend = (e?: FormEvent) => {
    e?.preventDefault();
    if (!chatInput.trim()) return;
    const userMsg = chatInput.trim();
    setMessages(prev => [...prev, { role: 'user', text: userMsg }]);
    setChatInput('');
    setTimeout(() => {
      const resp = AI_RESPONSES[Math.floor(Math.random() * AI_RESPONSES.length)];
      setMessages(prev => [...prev, { role: 'ai', text: resp }]);
    }, 800 + Math.random() * 1200);
  };

  if (loading) {
    return (
      <div style={{ padding: 40, fontFamily: "'Press Start 2P'", fontSize: 10, color: '#6a6a8a' }}>
        LOADING...
      </div>
    );
  }

  if (!node) {
    return (
      <div style={{ padding: 40, fontFamily: "'Press Start 2P'", fontSize: 10, color: '#e74c3c' }}>
        NODE NOT FOUND
      </div>
    );
  }

  const isExplored = nodeState === 'explored' || nodeState === 'mastered';

  return (
    <div style={s.page}>
      {/* ── Header ── */}
      <div style={s.headerBar}>
        <button onClick={() => navigate(`/map/${courseId}`)} style={s.backBtn}>
          ← 返回
        </button>
        <div style={{ flex: 1 }}>
          <div style={{
            fontFamily: "'Press Start 2P', monospace", fontSize: 11,
            color: '#c8c8e0', lineHeight: 1.6,
          }}>
            {node.name}
          </div>
          <div style={{
            fontFamily: "'VT323', monospace", fontSize: 17, color: '#6a6a8a', marginTop: 2,
          }}>
            {node.description}
          </div>
        </div>
        <button onClick={() => navigate(`/map/${courseId}`)} style={s.exitBtn}>
          EXIT
        </button>
        {/* Stars */}
        {isExplored && (
          <div style={{ display: 'flex', gap: 4 }}>
            {[1, 2, 3].map(i => (
              <span key={i}
                onClick={() => handleRate(i)}
                style={{
                  fontFamily: "'Press Start 2P'", fontSize: 14,
                  cursor: i > nodeStars ? 'pointer' : 'default',
                  color: i <= nodeStars ? '#f1c40f' : '#2a2a4a',
                  textShadow: i <= nodeStars ? '0 0 8px rgba(241,196,15,0.5)' : 'none',
                  opacity: i <= nodeStars ? 1 : 0.6,
                }}
              >★</span>
            ))}
          </div>
        )}
      </div>

      {/* ── Main Content: 2 columns ── */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: '1fr 1fr',
        gap: 12,
        marginBottom: 12,
        minHeight: 400,
      }}>
        {/* ── Left: Video Player ── */}
        <div style={s.panel}>
          <div style={{ ...s.panelHeader, color: '#5dade2' }}>STUDY VIDEO</div>
          {/* Video Area */}
          <div style={{
            flex: 1, minHeight: 260,
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            background: '#050510',
            position: 'relative',
            cursor: 'pointer',
          }}
            onClick={() => { if (videoProgress < 100) setVideoPlaying(!videoPlaying); }}
          >
            {!videoPlaying && videoProgress === 0 && (
              <div style={{ textAlign: 'center' }}>
                <div style={{
                  width: 56, height: 56,
                  border: '3px solid #5dade2',
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  margin: '0 auto 10px',
                }}>
                  <span style={{
                    fontFamily: "'Press Start 2P'", fontSize: 14, color: '#5dade2',
                    marginLeft: 3,
                  }}>▶</span>
                </div>
                <div style={{ fontFamily: "'VT323'", fontSize: 18, color: '#6a6a8a' }}>
                  点击播放
                </div>
              </div>
            )}
            {videoPlaying && (
              <div style={{
                fontFamily: "'Press Start 2P'", fontSize: 8, color: '#5dade2',
                animation: 'pulse 2s infinite',
              }}>
                ▶ PLAYING...
              </div>
            )}
            {!videoPlaying && videoProgress > 0 && videoProgress < 100 && (
              <div style={{
                fontFamily: "'Press Start 2P'", fontSize: 8, color: '#6a6a8a',
              }}>
                ⏸ PAUSED
              </div>
            )}
            {videoProgress >= 100 && (
              <div style={{
                fontFamily: "'Press Start 2P'", fontSize: 8, color: '#2ecc71',
              }}>
                ✓ COMPLETED
              </div>
            )}
            {videoPlaying && (
              <div style={{
                position: 'absolute', bottom: 14, left: 14, right: 14,
                background: 'rgba(0,0,0,0.7)', padding: '6px 10px',
                fontFamily: "'VT323'", fontSize: 16, color: '#e0e0e0',
                textAlign: 'center',
              }}>
                {node.description}
              </div>
            )}
          </div>
          {/* Progress Bar */}
          <div style={{
            padding: '10px 14px',
            borderTop: '2px solid #2a2a4a',
            display: 'flex', alignItems: 'center', gap: 10,
          }}>
            <button
              onClick={(e) => { e.stopPropagation(); if (videoProgress < 100) setVideoPlaying(!videoPlaying); }}
              style={{
                background: 'transparent', border: 'none',
                fontFamily: "'Press Start 2P'", fontSize: 8,
                color: videoPlaying ? '#f1c40f' : '#5dade2',
                cursor: videoProgress >= 100 ? 'default' : 'pointer',
              }}
            >
              {videoProgress >= 100 ? '✓' : videoPlaying ? '⏸' : '▶'}
            </button>
            <div style={{
              flex: 1, height: 8, background: '#0a0a18',
              border: '2px solid', borderColor: '#2a2a4a #5a5a8a #5a5a8a #2a2a4a',
              overflow: 'hidden',
            }}>
              <div style={{
                height: '100%', width: `${videoProgress}%`,
                background: videoProgress >= 100
                  ? 'repeating-linear-gradient(90deg, #2ecc71 0px, #2ecc71 3px, #1a9a50 3px, #1a9a50 5px)'
                  : 'repeating-linear-gradient(90deg, #5dade2 0px, #5dade2 3px, #3a8ab0 3px, #3a8ab0 5px)',
                transition: 'width 0.1s linear',
              }} />
            </div>
            <div style={{
              fontFamily: "'VT323'", fontSize: 16, color: '#6a6a8a', minWidth: 80,
            }}>
              {Math.floor(videoProgress * 0.12)}:{(Math.floor(videoProgress * 0.72) % 60).toString().padStart(2, '0')} / 12:00
            </div>
          </div>
        </div>

        {/* ── Right: AI Chat ── */}
        <div style={s.panel}>
          <div style={{ ...s.panelHeader, color: '#2ecc71' }}>AI TUTOR</div>
          {/* Messages */}
          <div style={{
            flex: 1, overflow: 'auto', padding: '12px 14px',
            display: 'flex', flexDirection: 'column', gap: 10,
            minHeight: 260,
          }}>
            {messages.map((msg, i) => (
              <div key={i} style={{
                display: 'flex',
                justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start',
              }}>
                <div style={{
                  maxWidth: '80%',
                  padding: '8px 12px',
                  background: msg.role === 'ai' ? '#12122a' : 'rgba(93,173,226,0.15)',
                  border: `2px solid ${msg.role === 'ai' ? '#2a2a4a' : 'rgba(93,173,226,0.3)'}`,
                  fontFamily: "'VT323'", fontSize: 18, lineHeight: 1.4,
                  color: msg.role === 'ai' ? '#c8c8e0' : '#5dade2',
                }}>
                  {msg.role === 'ai' && (
                    <div style={{
                      fontFamily: "'Press Start 2P'", fontSize: 6,
                      color: '#2ecc71', marginBottom: 4, letterSpacing: 1,
                    }}>AI</div>
                  )}
                  {msg.text}
                </div>
              </div>
            ))}
            <div ref={chatEndRef} />
          </div>
          {/* Input */}
          <form
            onSubmit={handleChatSend}
            style={{
              padding: '10px 14px',
              borderTop: '2px solid #2a2a4a',
              display: 'flex', gap: 8,
            }}
          >
            <input
              value={chatInput}
              onChange={e => setChatInput(e.target.value)}
              placeholder="输入你的问题..."
              style={{
                flex: 1, padding: '8px 10px',
                background: '#0a0a18',
                border: '2px solid', borderColor: '#2a2a4a #5a5a8a #5a5a8a #2a2a4a',
                fontFamily: "'VT323'", fontSize: 18,
                color: '#c8c8e0', outline: 'none', caretColor: '#f1c40f',
              }}
            />
            <button
              type="submit"
              style={{
                padding: '8px 16px',
                background: '#2ecc71',
                border: '2px solid', borderColor: '#5aea95 #1a9a50 #1a9a50 #5aea95',
                fontFamily: "'Press Start 2P'", fontSize: 7,
                color: '#0a0a18', cursor: 'pointer',
              }}
            >
              SEND
            </button>
          </form>
        </div>
      </div>

      {/* ── Bottom: Node Info + Status ── */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: '1fr 1fr',
        gap: 12,
      }}>
        {/* Prerequisites */}
        <div style={{ ...rpgBorder('#0a0a18'), padding: '14px 16px' }}>
          <div style={s.sectionTitle}>PREREQUISITES</div>
          {prereqs.length === 0 ? (
            <div style={{ fontFamily: "'VT323'", fontSize: 18, color: '#2ecc71' }}>
              无前置要求 - 可直接学习
            </div>
          ) : (
            prereqs.map((p: any) => (
              <div key={p.id || p} style={{
                fontFamily: "'VT323'", fontSize: 18, color: '#2ecc71', padding: '2px 0',
              }}>
                ✓ {p.name || p}
              </div>
            ))
          )}
        </div>

        {/* Status Panel */}
        <div style={{ ...rpgBorder('#0a0a18'), padding: '14px 16px' }}>
          <div style={s.sectionTitle}>STATUS</div>

          {/* Unlocked: show video progress hint */}
          {nodeState === 'unlocked' && !result && !completing && videoProgress < 100 && (
            <div>
              <div style={{ fontFamily: "'VT323'", fontSize: 18, color: '#5dade2' }}>
                ▸ 观看视频后自动完成学习
              </div>
              {videoProgress > 0 && (
                <div style={{
                  fontFamily: "'Press Start 2P'", fontSize: 8,
                  color: '#6a6a8a', marginTop: 8,
                }}>
                  VIDEO {Math.round(videoProgress)}%
                </div>
              )}
            </div>
          )}

          {/* Completing */}
          {completing && (
            <div style={{
              fontFamily: "'Press Start 2P'", fontSize: 9,
              color: '#5dade2', animation: 'pulse 1.5s infinite',
            }}>
              COMPLETING...
            </div>
          )}

          {/* Result */}
          {result && (
            <div>
              <div style={{
                fontFamily: "'Press Start 2P'", fontSize: 9,
                color: '#f1c40f', marginBottom: 8,
                textShadow: '0 0 8px rgba(241,196,15,0.4)',
              }}>
                COMPLETE!
              </div>
              <div style={{ fontFamily: "'VT323'", fontSize: 18, color: '#c8c8e0' }}>
                ▸ +{result.exp_gained} EXP
              </div>
              {result.new_level && (
                <div style={{ fontFamily: "'VT323'", fontSize: 18, color: '#f1c40f' }}>
                  ▸ LEVEL UP! → {result.new_level}
                </div>
              )}
              {result.unlocked_nodes?.length > 0 && (
                <div style={{ fontFamily: "'VT323'", fontSize: 18, color: '#c8c8e0' }}>
                  ▸ 解锁 {result.unlocked_nodes.length} 个新节点
                </div>
              )}
            </div>
          )}

          {/* Already explored */}
          {isExplored && !result && (
            <div style={{
              fontFamily: "'Press Start 2P'", fontSize: 9,
              color: '#2ecc71',
            }}>
              ✓ EXPLORED
            </div>
          )}

          {/* Locked */}
          {(nodeState === 'locked' || nodeState === 'visible') && (
            <div style={{
              fontFamily: "'VT323'", fontSize: 18, color: '#e74c3c',
            }}>
              需要先完成前置知识点才能学习
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
