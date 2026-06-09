import * as d3 from 'd3';
import { PALETTE } from './palette';

type G = d3.Selection<SVGGElement, unknown, null, undefined>;
type RngFn = () => number;

export function renderOcean(g: G, vw: number, vh: number, rngFn: (seed: number) => RngFn): void {
  // Ocean background
  g.append('rect')
    .attr('x', -400).attr('y', -400)
    .attr('width', vw + 800).attr('height', vh + 800)
    .attr('fill', 'url(#ocean)');

  // Wave pattern overlay
  g.append('rect')
    .attr('x', -400).attr('y', -400)
    .attr('width', vw + 800).attr('height', vh + 800)
    .attr('fill', 'url(#wave-pattern)').attr('opacity', 0.5);

  // Wave lines (varied)
  const wv = g.append('g').attr('opacity', 0.05).attr('class', 'ocean-wave');
  const r = rngFn(999);
  for (let i = 0; i < 16; i++) {
    const y = -80 + i * 75;
    const amp = 8 + r() * 8;
    wv.append('path')
      .attr('d', `M -200 ${y} Q 100 ${y - amp},400 ${y} T 1000 ${y} T 1600 ${y} T 2200 ${y}`)
      .attr('fill', 'none').attr('stroke', '#8ac8e8').attr('stroke-width', 0.8);
  }

  // Small decorative islands
  const islands: [number, number, number][] = [
    [-150, 400, 12], [1650, 300, 10], [-100, 800, 8], [1700, 700, 9],
  ];
  for (const [ix, iy, isize] of islands) {
    g.append('ellipse')
      .attr('cx', ix).attr('cy', iy)
      .attr('rx', isize).attr('ry', isize * 0.5)
      .attr('fill', PALETTE.beach.sand).attr('opacity', 0.2);
    g.append('ellipse')
      .attr('cx', ix).attr('cy', iy - isize * 0.2)
      .attr('rx', isize * 0.5).attr('ry', isize * 0.25)
      .attr('fill', '#4a7a4a').attr('opacity', 0.15);
  }
}

export function renderContinentBase(g: G, continent: string): void {
  // Shadow
  g.append('path').attr('d', continent)
    .attr('fill', PALETTE.continent.shadow)
    .attr('transform', 'translate(6,10)').attr('filter', 'url(#soften)');

  // Beach ring (outer)
  g.append('path').attr('d', continent)
    .attr('fill', 'none').attr('stroke', PALETTE.beach.sand)
    .attr('stroke-width', 14).attr('opacity', 0.4);

  // Beach ring (inner)
  g.append('path').attr('d', continent)
    .attr('fill', 'none').attr('stroke', PALETTE.beach.edge)
    .attr('stroke-width', 6).attr('opacity', 0.25);

  // Continent fill
  g.append('path').attr('d', continent)
    .attr('fill', PALETTE.continent.base)
    .attr('stroke', PALETTE.continent.border).attr('stroke-width', 2);
}

export function renderVignette(g: G, vw: number, vh: number, defs: d3.Selection<SVGDefsElement, unknown, null, undefined>): void {
  // Vignette gradient — covers the viewport area only
  const vg = defs.append('radialGradient').attr('id', 'vignette')
    .attr('cx', '50%').attr('cy', '50%').attr('r', '55%');
  vg.append('stop').attr('offset', '0%').attr('stop-color', 'rgba(0,0,0,0)');
  vg.append('stop').attr('offset', '70%').attr('stop-color', 'rgba(0,0,0,0)');
  vg.append('stop').attr('offset', '100%').attr('stop-color', 'rgba(5,15,30,0.45)');

  g.append('rect')
    .attr('x', 0).attr('y', 0)
    .attr('width', vw).attr('height', vh)
    .attr('fill', 'url(#vignette)');
}

export function renderAmbientLight(g: G): void {
  // Warm light source from upper-left
  g.append('circle')
    .attr('cx', 300).attr('cy', 200).attr('r', 400)
    .attr('fill', PALETTE.atmosphere.light);
}

export function renderParticles(g: G, vw: number, vh: number, rngFn: (seed: number) => RngFn): void {
  const r = rngFn(555);
  const particleG = g.append('g').attr('clip-path', 'url(#continent-clip)');

  for (let i = 0; i < 12; i++) {
    const px = 100 + r() * (vw - 200);
    const py = 100 + r() * (vh - 200);
    const size = 1 + r() * 1.5;
    particleG.append('circle')
      .attr('cx', px).attr('cy', py).attr('r', size)
      .attr('fill', PALETTE.atmosphere.particle)
      .attr('class', 'ambient-particle')
      .attr('style', `animation-delay: ${r() * 6}s`);
  }
}

export function renderCompass(g: G, vw: number): void {
  const comp = g.append('g').attr('transform', `translate(${vw - 75},75)`).attr('opacity', 0.4);

  // Outer ring
  comp.append('circle').attr('r', 30)
    .attr('fill', 'rgba(0,0,0,0.25)')
    .attr('stroke', 'rgba(210,190,140,0.4)').attr('stroke-width', 1.5);

  // Inner ring
  comp.append('circle').attr('r', 22)
    .attr('fill', 'none')
    .attr('stroke', 'rgba(210,190,140,0.2)').attr('stroke-width', 0.5);

  // Tick marks (16)
  for (let i = 0; i < 16; i++) {
    const a = (i / 16) * Math.PI * 2 - Math.PI / 2;
    const inner = i % 4 === 0 ? 22 : i % 2 === 0 ? 24 : 26;
    const outer = 28;
    comp.append('line')
      .attr('x1', Math.cos(a) * inner).attr('y1', Math.sin(a) * inner)
      .attr('x2', Math.cos(a) * outer).attr('y2', Math.sin(a) * outer)
      .attr('stroke', 'rgba(210,190,140,0.3)').attr('stroke-width', i % 4 === 0 ? 1.2 : 0.5);
  }

  // Cardinal triangles
  // N (red)
  comp.append('polygon').attr('points', '0,-22 3,-6 -3,-6').attr('fill', '#c44');
  // S (white)
  comp.append('polygon').attr('points', '0,22 3,6 -3,6').attr('fill', 'rgba(200,200,200,0.5)');
  // E
  comp.append('polygon').attr('points', '22,0 6,3 6,-3').attr('fill', 'rgba(210,190,140,0.4)');
  // W
  comp.append('polygon').attr('points', '-22,0 -6,3 -6,-3').attr('fill', 'rgba(210,190,140,0.4)');

  // Ordinal triangles (smaller)
  const ordinals = [
    [Math.PI / 4 - Math.PI / 2, 16],
    [3 * Math.PI / 4 - Math.PI / 2, 16],
    [5 * Math.PI / 4 - Math.PI / 2, 16],
    [7 * Math.PI / 4 - Math.PI / 2, 16],
  ];
  for (const [a, dist] of ordinals) {
    const cx = Math.cos(a as number) * (dist as number);
    const cy = Math.sin(a as number) * (dist as number);
    const dx = Math.cos(a as number) * 4;
    const dy = Math.sin(a as number) * 4;
    const px = -dy * 0.4, py = dx * 0.4;
    comp.append('polygon')
      .attr('points', `${cx + dx},${cy + dy} ${cx + px},${cy + py} ${cx - px},${cy - py}`)
      .attr('fill', 'rgba(210,190,140,0.25)');
  }

  // Center dot
  comp.append('circle').attr('r', 2).attr('fill', 'rgba(210,190,140,0.5)');

  // Direction letters
  const dirs: [string, number, number][] = [['N', 0, -32], ['S', 0, 36], ['E', 34, 4], ['W', -34, 4]];
  for (const [label, dx, dy] of dirs) {
    comp.append('text').attr('x', dx).attr('y', dy)
      .attr('text-anchor', 'middle').attr('fill', 'rgba(210,190,140,0.5)')
      .attr('font-size', 8).attr('font-weight', 700).text(label);
  }
}

export function renderBorderDecoration(g: G, vw: number, vh: number): void {
  const inset = 35;
  const lineColor = 'rgba(210,190,140,0.06)';

  // Double border lines
  g.append('rect')
    .attr('x', -400 + inset).attr('y', -400 + inset)
    .attr('width', vw + 800 - inset * 2).attr('height', vh + 800 - inset * 2)
    .attr('fill', 'none').attr('stroke', lineColor).attr('stroke-width', 0.5).attr('rx', 4);
  g.append('rect')
    .attr('x', -400 + inset + 4).attr('y', -400 + inset + 4)
    .attr('width', vw + 800 - inset * 2 - 8).attr('height', vh + 800 - inset * 2 - 8)
    .attr('fill', 'none').attr('stroke', lineColor).attr('stroke-width', 0.3).attr('rx', 3);

  // Corner flourishes (simple scrollwork)
  const cornerSize = 20;
  const corners: [number, number, string][] = [
    [-400 + inset + 8, -400 + inset + 8, ''],
    [vw + 400 - inset - 8, -400 + inset + 8, 'scale(-1,1)'],
    [-400 + inset + 8, vh + 400 - inset - 8, 'scale(1,-1)'],
    [vw + 400 - inset - 8, vh + 400 - inset - 8, 'scale(-1,-1)'],
  ];

  for (const [cx, cy, flip] of corners) {
    const cg = g.append('g')
      .attr('transform', `translate(${cx},${cy}) ${flip}`)
      .attr('opacity', 0.12);
    cg.append('path')
      .attr('d', `M 0 0 Q ${cornerSize * 0.5} 0, ${cornerSize} ${cornerSize * 0.3}`)
      .attr('fill', 'none').attr('stroke', '#d4c090').attr('stroke-width', 1);
    cg.append('path')
      .attr('d', `M 0 0 Q 0 ${cornerSize * 0.5}, ${cornerSize * 0.3} ${cornerSize}`)
      .attr('fill', 'none').attr('stroke', '#d4c090').attr('stroke-width', 1);
    cg.append('circle').attr('r', 1.5).attr('fill', '#d4c090');
  }
}
