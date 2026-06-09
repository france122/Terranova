import * as d3 from 'd3';
import { PALETTE, COURSE_THEME } from './palette';

type G = d3.Selection<SVGGElement, unknown, null, undefined>;

interface GraphNode {
  id: string; name: string; node_type: string; parent_id: string | null;
  description: string; position_x: number; position_y: number;
  state?: string; stars?: number;
}

function getCourse(pid: string | null) { return pid ? pid.split('_')[0] : 'ds'; }

function renderLocked(mk: G) {
  // Ruins: two tilted pillars + rubble
  mk.append('rect')
    .attr('x', -5).attr('y', -10).attr('width', 3).attr('height', 10)
    .attr('fill', '#4a4a44').attr('rx', 0.5).attr('opacity', 0.35)
    .attr('transform', 'rotate(-5)');
  mk.append('rect')
    .attr('x', 2).attr('y', -7).attr('width', 3).attr('height', 7)
    .attr('fill', '#4a4a44').attr('rx', 0.5).attr('opacity', 0.3)
    .attr('transform', 'rotate(3)');
  // Broken arch
  mk.append('path')
    .attr('d', 'M -4 -10 Q -1 -14, 0 -13 M 2 -12 Q 3 -14, 4 -7')
    .attr('fill', 'none').attr('stroke', '#4a4a44')
    .attr('stroke-width', 1.5).attr('opacity', 0.25);
  // Rubble
  for (const [cx, cy] of [[-3, 1], [1, 2], [4, 0], [-1, -1]] as [number, number][]) {
    mk.append('circle').attr('cx', cx).attr('cy', cy).attr('r', 1)
      .attr('fill', '#5a5a52').attr('opacity', 0.25);
  }
}

function renderVisible(mk: G, name: string) {
  // Ghostly building outline
  mk.append('path')
    .attr('d', 'M -8 6 L -8 -4 L 0 -14 L 8 -4 L 8 6 Z')
    .attr('fill', 'none')
    .attr('stroke', 'rgba(180,200,180,0.4)').attr('stroke-width', 1.5)
    .attr('stroke-dasharray', '3,2');
  // Question mark circle
  mk.append('circle')
    .attr('cy', -2).attr('r', 5)
    .attr('fill', 'rgba(150,170,150,0.15)').attr('stroke', 'rgba(180,200,180,0.25)').attr('stroke-width', 0.8);
  mk.append('text')
    .attr('y', 1).attr('text-anchor', 'middle')
    .attr('fill', 'rgba(200,220,200,0.4)').attr('font-size', 9).attr('font-weight', 600)
    .text('?');
  // Name
  mk.append('text').attr('y', 20).attr('text-anchor', 'middle')
    .attr('fill', PALETTE.nodes.visible.text).attr('font-size', 10).attr('font-weight', 500)
    .text(name.length > 6 ? name.slice(0, 5) + '…' : name);
}

function renderUnlocked(mk: G, name: string, th: { primary: string; glow: string }) {
  // Glow aura
  mk.append('circle').attr('r', 28)
    .attr('fill', th.glow).attr('opacity', 0.25).attr('class', 'marker-pulse');

  // Ground shadow
  mk.append('ellipse')
    .attr('cy', 8).attr('rx', 10).attr('ry', 3)
    .attr('fill', 'rgba(0,0,0,0.15)');

  // Building body
  mk.append('rect')
    .attr('x', -7).attr('y', -4).attr('width', 14).attr('height', 12)
    .attr('fill', th.primary).attr('rx', 1).attr('opacity', 0.9);

  // Roof
  mk.append('polygon')
    .attr('points', '-9,-4 0,-14 9,-4')
    .attr('fill', th.primary).attr('filter', 'url(#glow)').attr('opacity', 0.95);

  // Door
  mk.append('rect')
    .attr('x', -2).attr('y', 2).attr('width', 4).attr('height', 6)
    .attr('fill', 'rgba(0,0,0,0.3)').attr('rx', 1);

  // Windows (warm light)
  mk.append('rect')
    .attr('x', -6).attr('y', -1).attr('width', 2.5).attr('height', 2.5)
    .attr('fill', 'rgba(255,255,200,0.85)').attr('rx', 0.3);
  mk.append('rect')
    .attr('x', 3.5).attr('y', -1).attr('width', 2.5).attr('height', 2.5)
    .attr('fill', 'rgba(255,255,200,0.85)').attr('rx', 0.3);

  // Chimney
  mk.append('rect')
    .attr('x', 3).attr('y', -12).attr('width', 3).attr('height', 5)
    .attr('fill', th.primary).attr('opacity', 0.8).attr('rx', 0.5);

  // Smoke particles
  for (let i = 0; i < 3; i++) {
    mk.append('circle')
      .attr('cx', 4.5).attr('cy', -14 - i * 4).attr('r', 1.2 + i * 0.4)
      .attr('fill', 'rgba(200,210,220,0.3)')
      .attr('class', 'chimney-smoke')
      .attr('style', `animation-delay: ${i * 0.8}s`);
  }

  // Name label
  mk.append('text').attr('y', 24).attr('text-anchor', 'middle')
    .attr('fill', '#fff').attr('font-size', 12).attr('font-weight', 600).attr('filter', 'url(#ds)')
    .text(name.length > 6 ? name.slice(0, 5) + '…' : name);
}

function renderExplored(mk: G, name: string, stars: number, th: { primary: string; glow: string }) {
  // Soft glow
  mk.append('circle').attr('r', 22)
    .attr('fill', th.glow).attr('opacity', 0.15);

  // Ground shadow
  mk.append('ellipse')
    .attr('cy', 10).attr('rx', 14).attr('ry', 4)
    .attr('fill', 'rgba(0,0,0,0.12)');

  // Main building
  mk.append('rect')
    .attr('x', -8).attr('y', -5).attr('width', 16).attr('height', 15)
    .attr('fill', th.primary).attr('rx', 1).attr('opacity', 0.9);

  // Main roof
  mk.append('polygon')
    .attr('points', '-10,-5 0,-16 10,-5')
    .attr('fill', th.primary).attr('filter', 'url(#glow)');

  // Watchtower
  mk.append('rect')
    .attr('x', -2.5).attr('y', -24).attr('width', 5).attr('height', 10)
    .attr('fill', th.primary).attr('opacity', 0.95);
  mk.append('polygon')
    .attr('points', '-3.5,-24 0,-29 3.5,-24')
    .attr('fill', th.primary);

  // Windows
  for (const [wx, wy] of [[-5, -1], [3, -1], [-5, 4], [3, 4]] as [number, number][]) {
    mk.append('rect')
      .attr('x', wx).attr('y', wy).attr('width', 2.5).attr('height', 2.5)
      .attr('fill', 'rgba(255,255,200,0.85)').attr('rx', 0.3);
  }

  // Tower window
  mk.append('rect')
    .attr('x', -1).attr('y', -22).attr('width', 2).attr('height', 2.5)
    .attr('fill', 'rgba(255,255,200,0.9)').attr('rx', 0.3);

  // Flag on tower
  mk.append('polygon')
    .attr('points', '2.5,-29 10,-27 2.5,-25')
    .attr('fill', th.primary).attr('opacity', 0.9)
    .attr('class', 'flag-wave');

  // Door
  mk.append('rect')
    .attr('x', -2.5).attr('y', 3).attr('width', 5).attr('height', 7)
    .attr('fill', 'rgba(0,0,0,0.3)').attr('rx', 1);

  // Stars
  if (stars > 0) {
    mk.append('text').attr('y', -32).attr('text-anchor', 'middle')
      .attr('fill', '#FFD54F').attr('font-size', 9)
      .text('★'.repeat(stars) + '☆'.repeat(3 - stars));
  }

  // Name
  mk.append('text').attr('y', 26).attr('text-anchor', 'middle')
    .attr('fill', '#fff').attr('font-size', 11).attr('font-weight', 600).attr('filter', 'url(#ds)')
    .text(name.length > 6 ? name.slice(0, 5) + '…' : name);
}

function renderMastered(mk: G, name: string) {
  // Golden aura
  mk.append('circle').attr('r', 32)
    .attr('fill', 'rgba(255,213,79,0.1)').attr('class', 'marker-pulse');

  // Ground shadow
  mk.append('ellipse')
    .attr('cy', 12).attr('rx', 16).attr('ry', 4)
    .attr('fill', 'rgba(0,0,0,0.15)');

  // Platform
  mk.append('rect')
    .attr('x', -14).attr('y', 5).attr('width', 28).attr('height', 6)
    .attr('fill', '#8a7020').attr('rx', 2).attr('opacity', 0.8);

  // Castle tower
  mk.append('rect')
    .attr('x', -5).attr('y', -22).attr('width', 10).attr('height', 28)
    .attr('fill', '#FFD54F').attr('rx', 1).attr('filter', 'url(#goldf)');

  // Battlements (crenellations)
  for (let i = -4; i <= 4; i += 4) {
    mk.append('rect')
      .attr('x', i - 1.5).attr('y', -26).attr('width', 3).attr('height', 4)
      .attr('fill', '#FFD54F').attr('rx', 0.5);
  }

  // Side walls
  mk.append('rect')
    .attr('x', -12).attr('y', -8).attr('width', 7).attr('height', 14)
    .attr('fill', '#E6C030').attr('rx', 1);
  mk.append('rect')
    .attr('x', 5).attr('y', -8).attr('width', 7).attr('height', 14)
    .attr('fill', '#E6C030').attr('rx', 1);

  // Beacon light
  mk.append('circle')
    .attr('cy', -30).attr('r', 4)
    .attr('fill', '#FFFDE0').attr('filter', 'url(#goldf)');

  // Light beams
  mk.append('polygon')
    .attr('points', '-3,-30 -18,-38 -15,-25')
    .attr('fill', 'rgba(255,253,224,0.15)');
  mk.append('polygon')
    .attr('points', '3,-30 18,-38 15,-25')
    .attr('fill', 'rgba(255,253,224,0.15)');

  // Banner
  mk.append('polygon')
    .attr('points', '-12,-8 -18,-5 -12,-2')
    .attr('fill', '#FFA000').attr('opacity', 0.9).attr('class', 'flag-wave');

  // Windows
  for (const [wx, wy] of [[-2, -18], [0, -12], [-2, -6], [-10, -4], [7, -4]] as [number, number][]) {
    mk.append('rect')
      .attr('x', wx).attr('y', wy).attr('width', 2).attr('height', 3)
      .attr('fill', 'rgba(255,255,200,0.9)').attr('rx', 0.3);
  }

  // Three stars above
  mk.append('text').attr('y', -38).attr('text-anchor', 'middle')
    .attr('fill', '#FFD54F').attr('font-size', 10).text('★★★');

  // Sparkle particles
  const sparklePositions = [[-15, -20], [16, -15], [-10, -30], [12, -28]];
  sparklePositions.forEach(([sx, sy], i) => {
    mk.append('polygon')
      .attr('points', `${sx},${sy! - 2} ${sx! + 1},${sy} ${sx},${sy! + 2} ${sx! - 1},${sy}`)
      .attr('fill', '#FFD54F').attr('opacity', 0.6)
      .attr('class', 'sparkle')
      .attr('style', `animation-delay: ${i * 0.5}s`);
  });

  // Name
  mk.append('text').attr('y', 28).attr('text-anchor', 'middle')
    .attr('fill', '#FFD54F').attr('font-size', 11).attr('font-weight', 700).attr('filter', 'url(#ds)')
    .text(name.length > 6 ? name.slice(0, 5) + '…' : name);
}

export function renderNodeMarkers(
  g: G,
  nodes: GraphNode[],
  onSelect: (n: GraphNode) => void,
): void {
  const mG = g.append('g');

  for (const n of nodes) {
    const x = n.position_x, y = n.position_y;
    const st = n.state || 'locked';
    const cs = getCourse(n.parent_id);
    const th = COURSE_THEME[cs] || COURSE_THEME.ds;
    const interactive = ['unlocked', 'explored', 'mastered'].includes(st);

    const mk = mG.append('g')
      .attr('transform', `translate(${x},${y})`)
      .attr('cursor', interactive ? 'pointer' : 'default');

    if (interactive) {
      mk.on('click', () => onSelect(n));
    }

    switch (st) {
      case 'locked':
        renderLocked(mk as any);
        break;
      case 'visible':
        renderVisible(mk as any, n.name);
        break;
      case 'unlocked':
        renderUnlocked(mk as any, n.name, th);
        break;
      case 'explored':
        renderExplored(mk as any, n.name, n.stars || 0, th);
        break;
      case 'mastered':
        renderMastered(mk as any, n.name);
        break;
    }
  }
}
