import * as d3 from 'd3';
import { PALETTE } from './palette';

type G = d3.Selection<SVGGElement, unknown, null, undefined>;

interface GraphNode {
  id: string; name: string; node_type: string; parent_id: string | null;
  description: string; position_x: number; position_y: number;
  state?: string; stars?: number;
}

interface GraphEdge { source: string; target: string; edge_type: string; }

function roadPath(x1: number, y1: number, x2: number, y2: number) {
  const mx = (x1 + x2) / 2, my = (y1 + y2) / 2;
  const dx = x2 - x1, dy = y2 - y1, d = Math.sqrt(dx * dx + dy * dy);
  const off = Math.min(d * 0.18, 40);
  return `M ${x1} ${y1} Q ${mx + (-dy / d) * off} ${my + (dx / d) * off} ${x2} ${y2}`;
}

export function renderRoads(
  g: G,
  edges: GraphEdge[],
  nodeMap: Map<string, GraphNode>,
): void {
  const roadG = g.append('g');

  // ═══ PREREQUISITE ROADS ═══
  for (const e of edges) {
    if (e.edge_type !== 'PREREQUISITE') continue;
    const s = nodeMap.get(e.source), t = nodeMap.get(e.target);
    if (!s || !t) continue;
    const lit = (s.state === 'explored' || s.state === 'mastered') &&
                (t.state === 'explored' || t.state === 'mastered');
    const d = roadPath(s.position_x, s.position_y, t.position_x, t.position_y);

    // 1. Wide shadow
    roadG.append('path').attr('d', d).attr('fill', 'none')
      .attr('stroke', PALETTE.roads.shadow).attr('stroke-width', 6.5)
      .attr('stroke-linecap', 'round').attr('filter', 'url(#soften)');

    // 2. Road bed
    roadG.append('path').attr('d', d).attr('fill', 'none')
      .attr('stroke', lit ? PALETTE.roads.lit : PALETTE.roads.unlit)
      .attr('stroke-width', 5).attr('stroke-linecap', 'round')
      .attr('opacity', lit ? 0.85 : 0.4);

    // 3. Road surface
    roadG.append('path').attr('d', d).attr('fill', 'none')
      .attr('stroke', lit ? PALETTE.roads.surface_lit : PALETTE.roads.surface_unlit)
      .attr('stroke-width', 3.5).attr('stroke-linecap', 'round')
      .attr('opacity', lit ? 0.9 : 0.45);

    // 4. Stone texture (lit only)
    if (lit) {
      roadG.append('path').attr('d', d).attr('fill', 'none')
        .attr('stroke', 'rgba(230,210,150,0.3)')
        .attr('stroke-width', 1.5).attr('stroke-dasharray', '2,3')
        .attr('stroke-linecap', 'round');
    }

    // 5. Center highlight
    roadG.append('path').attr('d', d).attr('fill', 'none')
      .attr('stroke', lit ? PALETTE.roads.center : 'rgba(160,140,100,0.08)')
      .attr('stroke-width', 0.8).attr('stroke-dasharray', '5,10')
      .attr('stroke-linecap', 'round');
  }

  // ═══ RELATED_TO TUNNELS ═══
  for (const e of edges) {
    if (e.edge_type !== 'RELATED_TO') continue;
    const s = nodeMap.get(e.source), t = nodeMap.get(e.target);
    if (!s || !t) continue;
    const show = (s.state === 'explored' || s.state === 'mastered') &&
                 (t.state === 'explored' || t.state === 'mastered');
    if (!show) continue;
    const d = roadPath(s.position_x, s.position_y, t.position_x, t.position_y);

    // Tunnel glow underlay
    roadG.append('path').attr('d', d).attr('fill', 'none')
      .attr('stroke', 'rgba(255,213,79,0.12)').attr('stroke-width', 8)
      .attr('stroke-linecap', 'round');

    // Main dashed line
    roadG.append('path').attr('d', d).attr('fill', 'none')
      .attr('stroke', PALETTE.tunnel.line).attr('stroke-width', 2.5)
      .attr('stroke-dasharray', '10,8').attr('stroke-linecap', 'round')
      .attr('opacity', 0.7).attr('class', 'tunnel-dash');

    // Particle flow
    roadG.append('path').attr('d', d).attr('fill', 'none')
      .attr('stroke', PALETTE.tunnel.particle).attr('stroke-width', 1.5)
      .attr('stroke-dasharray', '2,25').attr('stroke-linecap', 'round')
      .attr('class', 'tunnel-particle');

    // Portal circles at both endpoints
    for (const p of [s, t]) {
      // Outer ring
      roadG.append('circle')
        .attr('cx', p.position_x).attr('cy', p.position_y).attr('r', 18)
        .attr('fill', 'none').attr('stroke', 'rgba(255,213,79,0.15)')
        .attr('stroke-width', 2.5);
      // Middle ring
      roadG.append('circle')
        .attr('cx', p.position_x).attr('cy', p.position_y).attr('r', 12)
        .attr('fill', 'none').attr('stroke', 'rgba(255,213,79,0.25)')
        .attr('stroke-width', 1.5);
      // Inner glow
      roadG.append('circle')
        .attr('cx', p.position_x).attr('cy', p.position_y).attr('r', 7)
        .attr('fill', PALETTE.tunnel.portal);
      // Center sparkle (4-pointed star)
      const sx = p.position_x, sy = p.position_y;
      roadG.append('polygon')
        .attr('points', `${sx},${sy - 3} ${sx + 1},${sy} ${sx},${sy + 3} ${sx - 1},${sy}`)
        .attr('fill', '#FFD54F').attr('opacity', 0.7)
        .attr('class', 'portal-sparkle');
    }
  }
}
