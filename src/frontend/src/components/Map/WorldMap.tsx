import { useEffect, useState, useCallback, type CSSProperties } from 'react';
import { useNavigate } from 'react-router-dom';
import { graph, mapApi } from '../../api';

/* ── RPG pixel border helper (unified) ── */
const rpgBorder = (bg = '#12122a'): CSSProperties => ({
  background: bg,
  border: '3px solid #5a5a8a',
  boxShadow: 'inset 2px 2px 0 #8888bb, inset -2px -2px 0 #2a2a4a',
});

/* ── All courses ── */
const ALL_COURSES = [
  { id: 'ds', name: '数据结构', desc: '研究数据的逻辑结构、存储结构及其运算', icon: '🌲', theme: '#2ecc71', requires: [] as string[], requiredRate: 0 },
  { id: 'cn', name: '计算机网络', desc: '研究计算机之间数据通信与网络协议', icon: '🌋', theme: '#e74c3c', requires: [] as string[], requiredRate: 0 },
  { id: 'dm', name: '离散数学', desc: '集合论、图论、组合数学与数理逻辑', icon: '🔮', theme: '#f39c12', requires: [] as string[], requiredRate: 0 },
  { id: 'os', name: '操作系统', desc: '进程管理、内存管理、文件系统与设备管理', icon: '⚙️', theme: '#9b59b6', requires: ['ds'], requiredRate: 50 },
  { id: 'db', name: '数据库原理', desc: '关系模型、SQL、事务处理与数据库设计', icon: '💎', theme: '#3498db', requires: ['ds'], requiredRate: 50 },
  { id: 'algo', name: '算法设计与分析', desc: '分治、动态规划、贪心、回溯等算法设计范式', icon: '🧩', theme: '#e67e22', requires: ['ds', 'dm'], requiredRate: 40 },
  { id: 'compiler', name: '编译原理', desc: '词法分析、语法分析、语义分析与代码生成', icon: '🏔️', theme: '#1abc9c', requires: ['ds', 'dm'], requiredRate: 60 },
  { id: 'se', name: '软件工程', desc: '需求分析、系统设计、测试与项目管理', icon: '🏗️', theme: '#2c3e50', requires: ['ds', 'db'], requiredRate: 60 },
];

const COURSE_NAMES: Record<string, string> = {};
ALL_COURSES.forEach(c => { COURSE_NAMES[c.id] = c.name; });

interface CourseCardData {
  id: string; name: string; desc: string; icon: string; theme: string;
  status: 'active' | 'unlockable' | 'locked';
  chapters: number; totalKP: number; exploredKP: number;
  requires: string[]; requiredRate: number;
  unlockMsg?: string;
}

const s: Record<string, CSSProperties> = {
  page: {
    position: 'absolute', inset: 0, overflow: 'auto',
    background: '#0c0c1d', padding: '24px 32px',
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
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
    gap: 12,
  },
  card: {
    ...rpgBorder('#0e0e22'),
    padding: '16px',
    cursor: 'default',
    transition: 'all 0.15s',
    position: 'relative' as const,
    overflow: 'hidden' as const,
  },
  cardTitle: {
    fontFamily: "'Press Start 2P', monospace",
    fontSize: 10,
    color: '#c8c8e0',
    marginBottom: 4,
  },
  cardDesc: {
    fontFamily: "'VT323', monospace",
    fontSize: 17,
    color: '#6a6a8a',
    lineHeight: 1.4,
    marginBottom: 12,
  },
  barOuter: {
    height: 10,
    background: '#0a0a18',
    border: '2px solid',
    borderColor: '#2a2a4a #6a6a8a #6a6a8a #2a2a4a',
    overflow: 'hidden',
  },
  btn: {
    padding: '10px 0',
    width: '100%',
    border: '3px solid',
    fontFamily: "'Press Start 2P', monospace",
    fontSize: 9,
    cursor: 'pointer',
    letterSpacing: 1,
    transition: 'all 0.15s',
  },
  statBadge: {
    display: 'inline-block',
    padding: '3px 8px',
    border: '2px solid',
    fontFamily: "'Press Start 2P', monospace",
    fontSize: 7,
    letterSpacing: 1,
    position: 'absolute' as const,
    top: 10,
    right: 10,
  },
  statsRow: {
    display: 'flex',
    gap: 20,
  },
  statBox: {
    textAlign: 'center' as const,
  },
  statVal: {
    fontFamily: "'Press Start 2P', monospace",
    fontSize: 14,
  },
  statLabel: {
    fontFamily: "'VT323', monospace",
    fontSize: 16,
    color: '#6a6a8a',
    marginTop: 2,
  },
};

export default function WorldMap() {
  const navigate = useNavigate();
  const [courses, setCourses] = useState<CourseCardData[]>([]);
  const [loading, setLoading] = useState(true);

  const loadData = useCallback(async () => {
    try {
      const [gr, mr] = await Promise.all([
        graph.getDomainMap('cs'),
        mapApi.getMapState('cs'),
      ]);

      const nodes = gr.data.nodes as any[];
      const stateMap: Record<string, string> = {};
      for (const n of mr.data.nodes) stateMap[n.node_id] = n.state;

      const courseProgress: Record<string, { total: number; explored: number; chapters: number }> = {};
      const chapterNodes = nodes.filter((n: any) => n.node_type === 'chapter');
      const kpNodes = nodes.filter((n: any) => n.node_type === 'knowledge_point');
      const courseNodes = nodes.filter((n: any) => n.node_type === 'course');
      const activeCourseIds = new Set(courseNodes.map((c: any) => c.id));

      for (const c of ALL_COURSES) {
        if (activeCourseIds.has(c.id)) {
          const chapters = chapterNodes.filter((ch: any) => ch.parent_id === c.id);
          const chapterIds = new Set(chapters.map((ch: any) => ch.id));
          const kps = kpNodes.filter((kp: any) => chapterIds.has(kp.parent_id));
          const explored = kps.filter((kp: any) => {
            const st = stateMap[kp.id];
            return st === 'explored' || st === 'mastered';
          });
          courseProgress[c.id] = { total: kps.length, explored: explored.length, chapters: chapters.length };
        }
      }

      const cardData: CourseCardData[] = ALL_COURSES.map(c => {
        const progress = courseProgress[c.id] || { total: 0, explored: 0, chapters: 0 };
        const isActive = activeCourseIds.has(c.id);

        let status: CourseCardData['status'] = 'locked';
        let unlockMsg: string | undefined;

        if (isActive) {
          status = 'active';
        } else if (c.requires.length > 0) {
          const allMet = c.requires.every(reqId => {
            const p = courseProgress[reqId];
            if (!p || p.total === 0) return false;
            return (p.explored / p.total * 100) >= c.requiredRate;
          });
          if (allMet) {
            status = 'unlockable';
            unlockMsg = '前置课程已满足，即将开放';
          } else {
            status = 'locked';
            const msgs = c.requires.map(reqId => {
              const p = courseProgress[reqId];
              const name = COURSE_NAMES[reqId] || reqId;
              if (!p || p.total === 0) return `${name} (未开始)`;
              const rate = Math.round(p.explored / p.total * 100);
              return `${name} ${rate}%/${c.requiredRate}%`;
            });
            unlockMsg = `需要: ${msgs.join('、')}`;
          }
        }

        return {
          ...c,
          status,
          chapters: progress.chapters || 0,
          totalKP: progress.total,
          exploredKP: progress.explored,
          unlockMsg,
        };
      });

      setCourses(cardData);
    } catch (e) { console.error(e); }
    setLoading(false);
  }, []);

  useEffect(() => { loadData(); }, [loadData]);

  const handleEnter = (courseId: string) => navigate(`/map/${courseId}`);

  const activeCourses = courses.filter(c => c.status === 'active').length;
  const totalExplored = courses.reduce((sum, c) => sum + c.exploredKP, 0);
  const totalKP = courses.reduce((sum, c) => sum + c.totalKP, 0);

  return (
    <div style={s.page}>
      {/* ── Header ── */}
      <div style={s.header}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <span style={{ color: '#5dade2' }}>⚑</span>
          课程地图
        </div>
        <div style={s.statsRow}>
          {[
            { label: '已开放', value: activeCourses, color: '#2ecc71' },
            { label: '已探索', value: totalExplored, color: '#5dade2' },
            { label: '知识点', value: totalKP, color: '#f1c40f' },
          ].map(st => (
            <div key={st.label} style={s.statBox}>
              <div style={{ ...s.statVal, color: st.color }}>{st.value}</div>
              <div style={s.statLabel}>{st.label}</div>
            </div>
          ))}
        </div>
      </div>

      {loading && (
        <div style={{
          textAlign: 'center', padding: 60,
          fontFamily: "'Press Start 2P'", fontSize: 10, color: '#6a6a8a',
        }}>LOADING...</div>
      )}

      {!loading && (
        <div style={s.grid}>
          {courses.map(c => {
            const pct = c.totalKP > 0 ? Math.round((c.exploredKP / c.totalKP) * 100) : 0;
            const isClickable = c.status === 'active';
            const isLocked = c.status === 'locked';

            return (
              <div
                key={c.id}
                onClick={() => isClickable && handleEnter(c.id)}
                style={{
                  ...s.card,
                  opacity: isLocked ? 0.5 : 1,
                  cursor: isClickable ? 'pointer' : 'default',
                }}
              >
                {/* Status badge */}
                {c.status !== 'active' && (
                  <div style={{
                    ...s.statBadge,
                    color: c.status === 'unlockable' ? '#f1c40f' : '#5a5a7a',
                    borderColor: c.status === 'unlockable' ? '#f1c40f' : '#3a3a5a',
                    background: c.status === 'unlockable' ? 'rgba(241,196,15,0.1)' : 'rgba(90,90,138,0.1)',
                  }}>
                    {c.status === 'unlockable' ? 'READY' : 'LOCKED'}
                  </div>
                )}

                {/* Icon + Name */}
                <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 8 }}>
                  <div style={{
                    width: 40, height: 40,
                    background: '#0a0a18',
                    border: '3px solid',
                    borderColor: `${c.theme}88 ${c.theme}44 ${c.theme}44 ${c.theme}88`,
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    fontSize: 20,
                  }}>
                    {c.icon}
                  </div>
                  <div>
                    <div style={s.cardTitle}>{c.name}</div>
                    {c.chapters > 0 && (
                      <div style={{
                        fontFamily: "'VT323', monospace", fontSize: 16, color: '#5a5a7a',
                      }}>
                        {c.chapters} 章节 · {c.totalKP} 知识点
                      </div>
                    )}
                  </div>
                </div>

                <div style={s.cardDesc}>{c.desc}</div>

                {/* Progress bar */}
                {c.status === 'active' && c.totalKP > 0 && (
                  <div style={{ marginBottom: 12 }}>
                    <div style={{
                      display: 'flex', justifyContent: 'space-between', marginBottom: 4,
                    }}>
                      <span style={{
                        fontFamily: "'Press Start 2P'", fontSize: 7, color: '#5a5a7a', letterSpacing: 1,
                      }}>PROGRESS</span>
                      <span style={{
                        fontFamily: "'Press Start 2P'", fontSize: 7,
                        color: pct >= 80 ? '#2ecc71' : pct >= 40 ? '#f1c40f' : '#5dade2',
                      }}>{pct}%</span>
                    </div>
                    <div style={s.barOuter}>
                      <div style={{
                        height: '100%', width: `${pct}%`,
                        background: `repeating-linear-gradient(90deg, ${c.theme} 0px, ${c.theme} 4px, ${c.theme}aa 4px, ${c.theme}aa 6px)`,
                      }} />
                    </div>
                  </div>
                )}

                {/* Unlock message */}
                {c.unlockMsg && (
                  <div style={{
                    fontFamily: "'VT323', monospace", fontSize: 16,
                    color: c.status === 'unlockable' ? '#f1c40f' : '#5a5a7a',
                    padding: '6px 10px',
                    border: `2px solid ${c.status === 'unlockable' ? 'rgba(241,196,15,0.3)' : '#2a2a4a'}`,
                    background: c.status === 'unlockable' ? 'rgba(241,196,15,0.05)' : 'transparent',
                    marginBottom: 12,
                  }}>
                    {c.status === 'unlockable' ? '★ ' : '▸ '}{c.unlockMsg}
                  </div>
                )}

                {/* Action button */}
                {isClickable && (
                  <button style={{
                    ...s.btn,
                    background: c.theme,
                    borderColor: `${c.theme} ${c.theme}88 ${c.theme}88 ${c.theme}`,
                    color: '#0a0a18',
                  }}>
                    ▶ 进入探索
                  </button>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
