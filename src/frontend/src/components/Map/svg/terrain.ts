import * as d3 from 'd3';
import { PALETTE } from './palette';

type G = d3.Selection<SVGGElement, unknown, null, undefined>;
type RngFn = () => number;

function drawMountain(g: G, cx: number, cy: number, w: number, h: number, r: RngFn) {
  // Irregular silhouette with 5-7 points
  const pts: [number, number][] = [
    [cx - w, cy],
    [cx - w * (0.6 + r() * 0.15), cy - h * (0.35 + r() * 0.1)],
    [cx - w * (0.2 + r() * 0.1), cy - h * (0.8 + r() * 0.15)],
    [cx + w * (r() * 0.05), cy - h],
    [cx + w * (0.2 + r() * 0.1), cy - h * (0.85 + r() * 0.1)],
    [cx + w * (0.55 + r() * 0.15), cy - h * (0.3 + r() * 0.1)],
    [cx + w, cy],
  ];
  const path = pts.map((p, i) => `${i === 0 ? 'M' : 'L'} ${p[0]} ${p[1]}`).join(' ') + ' Z';

  // Back shadow face
  g.append('path').attr('d', path)
    .attr('fill', PALETTE.terrain.mountain.back).attr('opacity', 0.7)
    .attr('transform', `translate(1,1)`);

  // Front face
  g.append('path').attr('d', path)
    .attr('fill', PALETTE.terrain.mountain.front).attr('opacity', 0.75)
    .attr('stroke', '#4a5a46').attr('stroke-width', 0.5);

  // Right shadow (light from upper-left)
  const shadowPts: [number, number][] = [
    pts[3], // peak
    pts[4],
    pts[5],
    pts[6], // right base
  ];
  const shadowPath = shadowPts.map((p, i) => `${i === 0 ? 'M' : 'L'} ${p[0]} ${p[1]}`).join(' ') + ' Z';
  g.append('path').attr('d', shadowPath)
    .attr('fill', PALETTE.terrain.mountain.shadow).attr('opacity', 0.8);

  // Snow cap with wavy snowline
  const snowY = cy - h * 0.65;
  const snowPath = `M ${cx - w * 0.22} ${snowY + r() * 3}
    Q ${cx - w * 0.1} ${snowY + 4 + r() * 2}, ${cx} ${snowY + r() * 3}
    Q ${cx + w * 0.12} ${snowY + 5 + r() * 2}, ${cx + w * 0.2} ${snowY + r() * 3}
    L ${pts[4][0]} ${pts[4][1]}
    L ${pts[3][0]} ${pts[3][1]}
    L ${pts[2][0]} ${pts[2][1]} Z`;
  g.append('path').attr('d', snowPath)
    .attr('fill', PALETTE.terrain.mountain.snow);

  // Ridge line
  g.append('line')
    .attr('x1', pts[2][0]).attr('y1', pts[2][1])
    .attr('x2', cx - w * 0.1).attr('y2', cy - h * 0.2)
    .attr('stroke', 'rgba(0,0,0,0.08)').attr('stroke-width', 0.5);
}

function drawConifer(g: G, x: number, y: number, scale: number, r: RngFn) {
  const h = (10 + r() * 6) * scale;
  const w = (4 + r() * 3) * scale;
  const trunkH = h * 0.25;

  // Shadow
  g.append('ellipse')
    .attr('cx', x).attr('cy', y + 1)
    .attr('rx', w * 0.8).attr('ry', w * 0.2)
    .attr('fill', 'rgba(0,0,0,0.1)');

  // Trunk
  g.append('rect')
    .attr('x', x - scale * 0.8).attr('y', y - trunkH)
    .attr('width', scale * 1.6).attr('height', trunkH)
    .attr('fill', PALETTE.terrain.tree.trunk).attr('rx', 0.5);

  // Three overlapping triangles (bottom to top, decreasing size)
  const layers = [
    { yOff: -trunkH, wMul: 1.0, hMul: 0.45, color: PALETTE.terrain.tree.conifer.dark },
    { yOff: -trunkH - h * 0.2, wMul: 0.8, hMul: 0.4, color: PALETTE.terrain.tree.conifer.mid },
    { yOff: -trunkH - h * 0.4, wMul: 0.55, hMul: 0.35, color: PALETTE.terrain.tree.conifer.light },
  ];
  for (const l of layers) {
    const bw = w * l.wMul;
    const bh = h * l.hMul;
    const by = y + l.yOff;
    g.append('polygon')
      .attr('points', `${x},${by - bh} ${x - bw},${by} ${x + bw},${by}`)
      .attr('fill', l.color).attr('opacity', 0.85);
  }
}

function drawDeciduous(g: G, x: number, y: number, scale: number, r: RngFn) {
  const trunkH = (5 + r() * 3) * scale;
  const crownR = (4 + r() * 3) * scale;

  // Shadow
  g.append('ellipse')
    .attr('cx', x).attr('cy', y + 1)
    .attr('rx', crownR * 0.9).attr('ry', crownR * 0.25)
    .attr('fill', 'rgba(0,0,0,0.1)');

  // Trunk
  g.append('rect')
    .attr('x', x - scale * 0.7).attr('y', y - trunkH)
    .attr('width', scale * 1.4).attr('height', trunkH)
    .attr('fill', PALETTE.terrain.tree.trunk).attr('rx', 0.5);

  // Canopy - two overlapping ellipses
  const crownY = y - trunkH - crownR * 0.5;
  g.append('ellipse')
    .attr('cx', x - crownR * 0.2).attr('cy', crownY + crownR * 0.15)
    .attr('rx', crownR * 0.85).attr('ry', crownR * 0.75)
    .attr('fill', PALETTE.terrain.tree.deciduous.dark).attr('opacity', 0.8);
  g.append('ellipse')
    .attr('cx', x + crownR * 0.15).attr('cy', crownY - crownR * 0.1)
    .attr('rx', crownR * 0.75).attr('ry', crownR * 0.65)
    .attr('fill', PALETTE.terrain.tree.deciduous.mid).attr('opacity', 0.85);
  // Highlight spot
  g.append('ellipse')
    .attr('cx', x - crownR * 0.15).attr('cy', crownY - crownR * 0.25)
    .attr('rx', crownR * 0.35).attr('ry', crownR * 0.3)
    .attr('fill', PALETTE.terrain.tree.deciduous.light).attr('opacity', 0.5);
}

function drawRock(g: G, x: number, y: number, size: number, r: RngFn) {
  const pts: string[] = [];
  const n = 5 + Math.floor(r() * 2);
  for (let i = 0; i < n; i++) {
    const a = (i / n) * Math.PI * 2 - Math.PI / 2;
    const rad = size * (0.6 + r() * 0.4);
    pts.push(`${x + Math.cos(a) * rad},${y + Math.sin(a) * rad * 0.6}`);
  }
  // Shadow
  g.append('ellipse')
    .attr('cx', x).attr('cy', y + size * 0.3)
    .attr('rx', size * 0.8).attr('ry', size * 0.2)
    .attr('fill', 'rgba(0,0,0,0.1)');
  // Rock body
  g.append('polygon').attr('points', pts.join(' '))
    .attr('fill', PALETTE.terrain.rock.fill).attr('stroke', PALETTE.terrain.rock.stroke)
    .attr('stroke-width', 0.5).attr('opacity', 0.7)
    .attr('stroke-linejoin', 'round');
  // Highlight
  g.append('ellipse')
    .attr('cx', x - size * 0.15).attr('cy', y - size * 0.15)
    .attr('rx', size * 0.3).attr('ry', size * 0.2)
    .attr('fill', 'rgba(255,255,255,0.08)');
}

function drawGrassTuft(g: G, x: number, y: number, r: RngFn) {
  const blades = 3 + Math.floor(r() * 2);
  for (let i = 0; i < blades; i++) {
    const angle = -0.3 + r() * 0.6;
    const h = 5 + r() * 4;
    const cx = x + (r() - 0.5) * 3;
    g.append('path')
      .attr('d', `M ${cx} ${y} Q ${cx + angle * 4} ${y - h * 0.6}, ${cx + angle * 6} ${y - h}`)
      .attr('fill', 'none').attr('stroke', PALETTE.terrain.grass).attr('stroke-width', 0.7)
      .attr('opacity', 0.4 + r() * 0.2);
  }
}

export function renderTerrain(g: G, rngFn: (seed: number) => RngFn): void {
  const tg = g.append('g').attr('clip-path', 'url(#continent-clip)');

  // ── Mountains ──
  const mountainClusters = [
    { cx: 490, cy: 130, count: 5, seed: 42, sizeRange: [12, 20] as [number, number], hRange: [22, 35] as [number, number] },
    { cx: 760, cy: 190, count: 3, seed: 17, sizeRange: [8, 14] as [number, number], hRange: [16, 24] as [number, number] },
    { cx: 155, cy: 460, count: 3, seed: 73, sizeRange: [10, 16] as [number, number], hRange: [18, 28] as [number, number] },
    { cx: 680, cy: 660, count: 4, seed: 55, sizeRange: [10, 18] as [number, number], hRange: [18, 30] as [number, number] },
    { cx: 870, cy: 280, count: 4, seed: 91, sizeRange: [10, 16] as [number, number], hRange: [20, 32] as [number, number] },
    { cx: 1380, cy: 340, count: 4, seed: 33, sizeRange: [10, 16] as [number, number], hRange: [18, 28] as [number, number] },
    { cx: 1350, cy: 750, count: 3, seed: 66, sizeRange: [8, 14] as [number, number], hRange: [16, 24] as [number, number] },
    { cx: 440, cy: 850, count: 3, seed: 88, sizeRange: [8, 14] as [number, number], hRange: [16, 24] as [number, number] },
  ];

  for (const cluster of mountainClusters) {
    const r = rngFn(cluster.seed);
    for (let i = 0; i < cluster.count; i++) {
      const mx = cluster.cx + (r() - 0.5) * 100;
      const my = cluster.cy + (r() - 0.5) * 40;
      const w = cluster.sizeRange[0] + r() * (cluster.sizeRange[1] - cluster.sizeRange[0]);
      const h = cluster.hRange[0] + r() * (cluster.hRange[1] - cluster.hRange[0]);
      drawMountain(tg, mx, my, w, h, r);
    }
  }

  // ── Trees ──
  const treeClusters = [
    { cx: 290, cy: 260, count: 12, spread: 60, seed: 101, type: 'conifer' as const },
    { cx: 250, cy: 490, count: 10, spread: 50, seed: 202, type: 'deciduous' as const },
    { cx: 500, cy: 595, count: 10, spread: 60, seed: 303, type: 'conifer' as const },
    { cx: 600, cy: 800, count: 8, spread: 50, seed: 404, type: 'deciduous' as const },
    { cx: 1010, cy: 310, count: 10, spread: 60, seed: 505, type: 'conifer' as const },
    { cx: 1110, cy: 540, count: 12, spread: 65, seed: 606, type: 'conifer' as const },
    { cx: 1060, cy: 750, count: 8, spread: 50, seed: 707, type: 'deciduous' as const },
    { cx: 200, cy: 710, count: 6, spread: 40, seed: 808, type: 'deciduous' as const },
    { cx: 1310, cy: 500, count: 8, spread: 50, seed: 909, type: 'conifer' as const },
    { cx: 370, cy: 420, count: 6, spread: 35, seed: 111, type: 'deciduous' as const },
    { cx: 1200, cy: 800, count: 6, spread: 45, seed: 222, type: 'deciduous' as const },
  ];

  for (const cluster of treeClusters) {
    const r = rngFn(cluster.seed);
    for (let i = 0; i < cluster.count; i++) {
      const tx = cluster.cx + (r() - 0.5) * cluster.spread * 2;
      const ty = cluster.cy + (r() - 0.5) * cluster.spread * 1.1;
      const scale = 0.7 + r() * 0.6;
      if (cluster.type === 'conifer') {
        drawConifer(tg, tx, ty, scale, r);
      } else {
        drawDeciduous(tg, tx, ty, scale, r);
      }
    }
  }

  // ── Rocks (highland & coastal regions) ──
  const rockClusters = [
    { cx: 870, cy: 280, count: 6, spread: 70, seed: 151 },
    { cx: 1130, cy: 175, count: 5, spread: 80, seed: 152 },
    { cx: 520, cy: 560, count: 4, spread: 50, seed: 153 },
    { cx: 585, cy: 740, count: 4, spread: 50, seed: 154 },
    { cx: 1140, cy: 680, count: 5, spread: 70, seed: 155 },
  ];

  for (const cluster of rockClusters) {
    const r = rngFn(cluster.seed);
    for (let i = 0; i < cluster.count; i++) {
      const rx = cluster.cx + (r() - 0.5) * cluster.spread * 2;
      const ry = cluster.cy + (r() - 0.5) * cluster.spread;
      const size = 3 + r() * 5;
      drawRock(tg, rx, ry, size, r);
    }
  }

  // ── Grass tufts (meadow regions) ──
  const grassClusters = [
    { cx: 275, cy: 395, count: 20, spread: 60, seed: 261 },
    { cx: 370, cy: 420, count: 12, spread: 40, seed: 262 },
  ];

  for (const cluster of grassClusters) {
    const r = rngFn(cluster.seed);
    for (let i = 0; i < cluster.count; i++) {
      const gx = cluster.cx + (r() - 0.5) * cluster.spread * 2;
      const gy = cluster.cy + (r() - 0.5) * cluster.spread;
      drawGrassTuft(tg, gx, gy, r);
    }
  }

  // ── Flowers (sparse) ──
  const flowerSeeds = [
    { cx: 290, cy: 250, count: 5, spread: 50, seed: 371 },
    { cx: 260, cy: 480, count: 4, spread: 40, seed: 372 },
    { cx: 1100, cy: 530, count: 4, spread: 50, seed: 373 },
  ];

  for (const cluster of flowerSeeds) {
    const r = rngFn(cluster.seed);
    for (let i = 0; i < cluster.count; i++) {
      const fx = cluster.cx + (r() - 0.5) * cluster.spread * 2;
      const fy = cluster.cy + (r() - 0.5) * cluster.spread;
      const color = PALETTE.terrain.flower[Math.floor(r() * PALETTE.terrain.flower.length)];
      tg.append('circle')
        .attr('cx', fx).attr('cy', fy).attr('r', 1.5)
        .attr('fill', color).attr('opacity', 0.55);
    }
  }
}
