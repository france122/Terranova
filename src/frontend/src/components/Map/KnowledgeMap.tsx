import { useEffect, useRef, useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import * as d3 from 'd3';
import { graph, mapApi } from '../../api';
import { useAuth } from '../../hooks/useAuth';

import { renderDefs } from './svg/defs';
import { renderNodeMarkers } from './svg/nodeMarkers';
import { renderRoads } from './svg/roads';
import { renderFog } from './svg/fog';

import mapBgDefault from '../../assets/terranova-map-v3_001.jpg';
import mapBgDS from '../../assets/map-ds-forest.jpg';
import mapBgCN from '../../assets/map-cn-volcanic.jpg';
import type { CSSProperties } from 'react';

const COURSE_MAPS: Record<string, string> = {
  ds: mapBgDS,
  cn: mapBgCN,
};

interface GraphNode {
  id: string; name: string; node_type: string; parent_id: string | null;
  description: string; position_x: number; position_y: number;
  state?: string; stars?: number;
}
interface GraphEdge { source: string; target: string; edge_type: string; }

const VW = 1600, VH = 1000;

function rng(seed: number) {
  let s = seed;
  return () => { s = (s * 16807) % 2147483647; return s / 2147483647; };
}

/* ── RPG pixel border helper ── */
const rpgBorder = (bg = '#12122a'): CSSProperties => ({
  background: bg,
  border: '3px solid #5a5a8a',
  boxShadow: 'inset 2px 2px 0 #8888bb, inset -2px -2px 0 #2a2a4a',
});

/* ── Course display names ── */
const COURSE_NAMES: Record<string, string> = {
  ds: '数据结构',
  cn: '计算机网络',
  os: '操作系统',
  db: '数据库原理',
  dm: '离散数学',
  algo: '算法设计与分析',
  compiler: '编译原理',
  se: '软件工程',
};

interface Props {
  courseId: string;
}

export default function KnowledgeMap({ courseId }: Props) {
  const containerRef = useRef<HTMLDivElement>(null);
  const svgRef = useRef<SVGSVGElement>(null);
  const zoomRef = useRef<d3.ZoomBehavior<SVGSVGElement, unknown> | null>(null);
  const [nodes, setNodes] = useState<GraphNode[]>([]);
  const [edges, setEdges] = useState<GraphEdge[]>([]);
  const [exploreRate, setExploreRate] = useState(0);
  useAuth(); // keep auth context active
  const navigate = useNavigate();

  const loadData = useCallback(async () => {
    try {
      const [gr, mr] = await Promise.all([graph.getDomainMap('cs'), mapApi.getMapState('cs')]);
      const allNodes = gr.data.nodes as GraphNode[];
      const allEdges = gr.data.edges as GraphEdge[];
      const sm: Record<string, { state: string; stars: number }> = {};
      for (const n of mr.data.nodes) sm[n.node_id] = { state: n.state, stars: n.stars };

      // Find chapters belonging to this course
      const chapterIds = new Set(
        allNodes
          .filter(n => n.node_type === 'chapter' && n.parent_id === courseId)
          .map(n => n.id)
      );

      // Filter knowledge points by chapter
      const merged = allNodes
        .filter(n => n.node_type === 'knowledge_point' && chapterIds.has(n.parent_id || ''))
        .map(n => ({ ...n, state: sm[n.id]?.state || 'locked', stars: sm[n.id]?.stars || 0 }));

      const ids = new Set(merged.map(n => n.id));
      setNodes(merged);
      setEdges(allEdges.filter(e => ids.has(e.source) && ids.has(e.target)));

      // Calculate course-specific explore rate
      const explored = merged.filter(n => n.state === 'explored' || n.state === 'mastered').length;
      setExploreRate(merged.length > 0 ? Math.round((explored / merged.length) * 100) : 0);
    } catch (e) { console.error(e); }
  }, [courseId]);

  useEffect(() => { loadData(); }, [loadData]);

  /* ── Calculate the minimum scale that covers the viewport ── */
  const getCoverScale = useCallback(() => {
    if (!svgRef.current) return 1;
    const w = svgRef.current.clientWidth, h = svgRef.current.clientHeight;
    if (w === 0 || h === 0) return 1;
    return Math.max(w / VW, h / VH);
  }, []);

  /* ── Fit map to fill the container (cover mode) ── */
  const fitToScreen = useCallback(() => {
    if (!svgRef.current || !zoomRef.current) return;
    const svg = d3.select(svgRef.current);
    const el = svgRef.current;
    const w = el.clientWidth, h = el.clientHeight;
    if (w === 0 || h === 0) return;
    const sc = getCoverScale();
    zoomRef.current.scaleExtent([sc, Math.max(sc * 4, 3)]);
    svg.call(
      zoomRef.current.transform,
      d3.zoomIdentity.translate((w - VW * sc) / 2, (h - VH * sc) / 2).scale(sc)
    );
  }, [getCoverScale]);

  /* ── Handle node click → navigate to learn page ── */
  const handleNodeClick = useCallback((n: GraphNode) => {
    const st = n.state || 'locked';
    if (['unlocked', 'explored', 'mastered'].includes(st)) {
      navigate(`/map/${courseId}/learn/${n.id}`);
    }
  }, [navigate, courseId]);

  /* ── Render map SVG ── */
  useEffect(() => {
    if (!svgRef.current || !nodes.length) return;
    const svg = d3.select(svgRef.current);
    svg.selectAll('*').remove();
    const nm = new Map(nodes.map(n => [n.id, n]));

    const defs = svg.append('defs');
    renderDefs(defs as any);

    const g = svg.append('g');
    const minScale = getCoverScale();

    const zoom = d3.zoom<SVGSVGElement, unknown>()
      .scaleExtent([minScale, Math.max(minScale * 4, 3)])
      .on('zoom', (e) => {
        const t = e.transform;
        const el = svgRef.current!;
        const w = el.clientWidth, h = el.clientHeight;
        const maxTx = 0, maxTy = 0;
        const minTx = w - VW * t.k, minTy = h - VH * t.k;
        const cx = Math.min(maxTx, Math.max(minTx, t.x));
        const cy = Math.min(maxTy, Math.max(minTy, t.y));
        const constrained = d3.zoomIdentity.translate(cx, cy).scale(t.k);
        g.attr('transform', constrained.toString());
        if (cx !== t.x || cy !== t.y) svg.property('__zoom', constrained);
      });
    zoomRef.current = zoom;
    svg.call(zoom);

    const mapBg = COURSE_MAPS[courseId] || mapBgDefault;

    g.append('image')
      .attr('href', mapBg)
      .attr('x', 0).attr('y', 0)
      .attr('width', VW).attr('height', VH)
      .attr('preserveAspectRatio', 'xMidYMid slice');

    renderRoads(g as any, edges, nm as any);
    renderFog(g as any, nodes, rng);
    renderNodeMarkers(g as any, nodes, handleNodeClick);

    fitToScreen();
  }, [nodes, edges, fitToScreen, getCoverScale, handleNodeClick]);

  /* ── Handle resize ── */
  useEffect(() => {
    const onResize = () => fitToScreen();
    window.addEventListener('resize', onResize);
    let ro: ResizeObserver | null = null;
    if (containerRef.current) {
      ro = new ResizeObserver(() => fitToScreen());
      ro.observe(containerRef.current);
    }
    return () => { window.removeEventListener('resize', onResize); ro?.disconnect(); };
  }, [fitToScreen]);

  /* ── Pixel-style bar ── */
  const barSegments = 20;
  const filledSegments = Math.round((exploreRate / 100) * barSegments);

  return (
    <div
      ref={containerRef}
      style={{ position: 'absolute', inset: 0, overflow: 'hidden', background: '#0a1520' }}
    >
      {/* ── Back Button ── */}
      <button
        onClick={() => navigate('/map')}
        style={{
          position: 'absolute', top: 16, left: 16, zIndex: 10,
          padding: '8px 16px',
          borderRadius: 6,
          background: 'rgba(12,12,29,0.9)',
          border: '1px solid rgba(90,90,138,0.3)',
          backdropFilter: 'blur(8px)',
          color: '#c8c8e0',
          fontSize: 14,
          fontWeight: 500,
          cursor: 'pointer',
        }}
      >
        ← 课程地图
      </button>

      {/* ── Course Title ── */}
      <div style={{
        position: 'absolute', top: 16, left: '50%', transform: 'translateX(-50%)',
        zIndex: 10,
        ...rpgBorder('rgba(12,12,29,0.92)'),
        padding: '8px 20px',
      }}>
        <span style={{
          fontFamily: "'Press Start 2P', monospace",
          fontSize: 10, color: '#f1c40f',
          textShadow: '2px 2px 0 #8a6a00',
        }}>
          {COURSE_NAMES[courseId] || courseId}
        </span>
      </div>

      {/* ── HUD ── */}
      <div style={{
        position: 'absolute', bottom: 16, right: 16, zIndex: 10,
        ...rpgBorder('rgba(12,12,29,0.92)'),
        padding: '10px 14px',
        display: 'flex', alignItems: 'center', gap: 12, minWidth: 240,
      }}>
        <div style={{
          fontFamily: "'Press Start 2P', monospace", fontSize: 7,
          color: '#6a6a8a', letterSpacing: 1,
        }}>EXPLORE</div>
        <div style={{ display: 'flex', gap: 1, flex: 1 }}>
          {Array.from({ length: barSegments }, (_, i) => (
            <div key={i} style={{
              width: 4, height: 10,
              background: i < filledSegments
                ? (i < barSegments * 0.3 ? '#e74c3c' : i < barSegments * 0.7 ? '#f1c40f' : '#2ecc71')
                : '#1a1a2e',
              border: '1px solid #2a2a4a',
            }} />
          ))}
        </div>
        <div style={{
          fontFamily: "'Press Start 2P', monospace", fontSize: 9,
          color: exploreRate >= 50 ? '#2ecc71' : '#f1c40f',
        }}>{exploreRate}%</div>
      </div>

      {/* ── Legend ── */}
      <div style={{
        position: 'absolute', bottom: 16, left: 16, zIndex: 10,
        ...rpgBorder('rgba(12,12,29,0.92)'),
        padding: '8px 12px', display: 'flex', gap: 14,
      }}>
        {[
          { c: '#3a3a3a', l: '未知', shape: '■' },
          { c: '#6a8a6a', l: '可见', shape: '◇' },
          { c: '#5dade2', l: '可探索', shape: '◆' },
          { c: '#2ecc71', l: '已探索', shape: '◆' },
          { c: '#f1c40f', l: '已精通', shape: '★' },
        ].map(i => (
          <div key={i.l} style={{
            display: 'flex', alignItems: 'center', gap: 4,
            fontFamily: "'VT323', monospace", fontSize: 15, color: '#6a6a8a',
          }}>
            <span style={{ color: i.c, fontSize: 12 }}>{i.shape}</span>
            <span>{i.l}</span>
          </div>
        ))}
      </div>

      <svg
        ref={svgRef}
        style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', display: 'block' }}
      />
    </div>
  );
}
