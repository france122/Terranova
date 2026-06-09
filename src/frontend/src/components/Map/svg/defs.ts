import * as d3 from 'd3';
import { PALETTE } from './palette';
import { REGIONS, CONTINENT } from './regions';

type Sel = d3.Selection<SVGDefsElement, unknown, null, undefined>;

function rng(seed: number) {
  let s = seed;
  return () => { s = (s * 16807) % 2147483647; return s / 2147483647; };
}

export function renderDefs(defs: Sel): void {
  // ── Ocean gradient ──
  const og = defs.append('radialGradient').attr('id', 'ocean')
    .attr('cx', '50%').attr('cy', '50%').attr('r', '65%');
  og.append('stop').attr('offset', '0%').attr('stop-color', PALETTE.ocean.mid);
  og.append('stop').attr('offset', '60%').attr('stop-color', PALETTE.ocean.deep);
  og.append('stop').attr('offset', '100%').attr('stop-color', '#081828');

  // ── Sand gradient ──
  const sg = defs.append('linearGradient').attr('id', 'sand-grad')
    .attr('x1', '0%').attr('y1', '0%').attr('x2', '0%').attr('y2', '100%');
  sg.append('stop').attr('offset', '0%').attr('stop-color', PALETTE.beach.sand);
  sg.append('stop').attr('offset', '100%').attr('stop-color', PALETTE.beach.wet);

  // ── Per-region gradients ──
  Object.entries(REGIONS).forEach(([id, _r]) => {
    const biome = PALETTE.biomes[id];
    if (!biome) return;
    const g = defs.append('radialGradient').attr('id', `rg-${id}`)
      .attr('cx', '45%').attr('cy', '40%').attr('r', '65%');
    g.append('stop').attr('offset', '0%').attr('stop-color', biome.light);
    g.append('stop').attr('offset', '55%').attr('stop-color', biome.main);
    g.append('stop').attr('offset', '100%').attr('stop-color', biome.dark);
  });

  // ── Gold gradient (mastered nodes) ──
  const gg = defs.append('linearGradient').attr('id', 'gold-grad')
    .attr('x1', '0%').attr('y1', '0%').attr('x2', '100%').attr('y2', '100%');
  gg.append('stop').attr('offset', '0%').attr('stop-color', '#FFA000');
  gg.append('stop').attr('offset', '50%').attr('stop-color', '#FFD54F');
  gg.append('stop').attr('offset', '100%').attr('stop-color', '#FFECB3');

  // ── Cloud pattern (improved) ──
  const cp = defs.append('pattern').attr('id', 'clouds')
    .attr('width', 200).attr('height', 150)
    .attr('patternUnits', 'userSpaceOnUse');
  const cr = rng(777);
  for (let i = 0; i < 15; i++) {
    const cx = cr() * 200, cy = cr() * 150;
    const rx = 20 + cr() * 40, ry = 15 + cr() * 25;
    const op = 0.08 + cr() * 0.18;
    cp.append('ellipse').attr('cx', cx).attr('cy', cy)
      .attr('rx', rx).attr('ry', ry)
      .attr('fill', `rgba(220,230,240,${op})`);
  }

  // ── Contour pattern (curved) ──
  const contour = defs.append('pattern').attr('id', 'contours')
    .attr('width', 80).attr('height', 80)
    .attr('patternUnits', 'userSpaceOnUse').attr('patternTransform', 'rotate(15)');
  for (let i = 0; i < 4; i++) {
    const y = i * 20;
    contour.append('path')
      .attr('d', `M 0 ${y} Q 20 ${y - 3}, 40 ${y} T 80 ${y}`)
      .attr('fill', 'none').attr('stroke', 'rgba(255,255,255,0.03)').attr('stroke-width', 0.8);
  }

  // ── Grass hatch pattern ──
  const grass = defs.append('pattern').attr('id', 'grass-hatch')
    .attr('width', 20).attr('height', 20)
    .attr('patternUnits', 'userSpaceOnUse').attr('patternTransform', 'rotate(45)');
  for (let i = 0; i < 4; i++) {
    grass.append('line')
      .attr('x1', i * 5 + 2).attr('y1', 0).attr('x2', i * 5 + 2).attr('y2', 3)
      .attr('stroke', 'rgba(100,180,60,0.06)').attr('stroke-width', 0.8);
  }

  // ── Dot stipple pattern ──
  const stipple = defs.append('pattern').attr('id', 'dot-stipple')
    .attr('width', 16).attr('height', 16)
    .attr('patternUnits', 'userSpaceOnUse');
  const sr = rng(333);
  for (let i = 0; i < 6; i++) {
    stipple.append('circle')
      .attr('cx', sr() * 16).attr('cy', sr() * 16)
      .attr('r', 0.5 + sr() * 0.5)
      .attr('fill', `rgba(200,200,180,${0.04 + sr() * 0.04})`);
  }

  // ── Wave pattern (ocean) ──
  const wave = defs.append('pattern').attr('id', 'wave-pattern')
    .attr('width', 120).attr('height', 40)
    .attr('patternUnits', 'userSpaceOnUse');
  for (let i = 0; i < 3; i++) {
    const y = 8 + i * 14;
    wave.append('path')
      .attr('d', `M 0 ${y} Q 15 ${y - 4}, 30 ${y} T 60 ${y} T 90 ${y} T 120 ${y}`)
      .attr('fill', 'none').attr('stroke', 'rgba(100,180,220,0.06)').attr('stroke-width', 0.6);
  }

  // ── Filters ──

  // Fog blur
  const fb = defs.append('filter').attr('id', 'fblur')
    .attr('x', '-40%').attr('y', '-40%').attr('width', '180%').attr('height', '180%');
  fb.append('feGaussianBlur').attr('stdDeviation', 22);

  // Glow
  const gf = defs.append('filter').attr('id', 'glow')
    .attr('x', '-60%').attr('y', '-60%').attr('width', '220%').attr('height', '220%');
  gf.append('feGaussianBlur').attr('stdDeviation', 3).attr('result', 'b');
  const gm = gf.append('feMerge');
  gm.append('feMergeNode').attr('in', 'b');
  gm.append('feMergeNode').attr('in', 'SourceGraphic');

  // Gold glow
  const goldf = defs.append('filter').attr('id', 'goldf')
    .attr('x', '-60%').attr('y', '-60%').attr('width', '220%').attr('height', '220%');
  goldf.append('feGaussianBlur').attr('stdDeviation', 4).attr('result', 'b');
  const gm2 = goldf.append('feMerge');
  gm2.append('feMergeNode').attr('in', 'b');
  gm2.append('feMergeNode').attr('in', 'SourceGraphic');

  // Soften
  defs.append('filter').attr('id', 'soften')
    .append('feGaussianBlur').attr('stdDeviation', 5);

  // Drop shadow
  const ds = defs.append('filter').attr('id', 'ds');
  ds.append('feGaussianBlur').attr('stdDeviation', 1.5).attr('in', 'SourceAlpha').attr('result', 's');
  ds.append('feOffset').attr('dx', 1).attr('dy', 2).attr('in', 's').attr('result', 'o');
  const dsm = ds.append('feMerge');
  dsm.append('feMergeNode').attr('in', 'o');
  dsm.append('feMergeNode').attr('in', 'SourceGraphic');

  // Inner shadow
  const isf = defs.append('filter').attr('id', 'inner-shadow')
    .attr('x', '-10%').attr('y', '-10%').attr('width', '120%').attr('height', '120%');
  isf.append('feGaussianBlur').attr('stdDeviation', 4).attr('in', 'SourceAlpha').attr('result', 'blur');
  isf.append('feOffset').attr('dx', 2).attr('dy', 3).attr('in', 'blur').attr('result', 'offset');
  isf.append('feComposite').attr('operator', 'out').attr('in', 'offset').attr('in2', 'SourceAlpha').attr('result', 'inverse');
  isf.append('feFlood').attr('flood-color', 'rgba(0,0,0,0.3)').attr('result', 'color');
  isf.append('feComposite').attr('operator', 'in').attr('in', 'color').attr('in2', 'inverse').attr('result', 'shadow');
  const ism = isf.append('feMerge');
  ism.append('feMergeNode').attr('in', 'shadow');
  ism.append('feMergeNode').attr('in', 'SourceGraphic');

  // Terrain noise texture
  const tnf = defs.append('filter').attr('id', 'terrain-noise')
    .attr('x', '0%').attr('y', '0%').attr('width', '100%').attr('height', '100%');
  tnf.append('feTurbulence').attr('type', 'fractalNoise')
    .attr('baseFrequency', '0.65').attr('numOctaves', 4).attr('result', 'noise');
  tnf.append('feColorMatrix').attr('type', 'saturate').attr('values', '0').attr('in', 'noise').attr('result', 'gray');
  tnf.append('feBlend').attr('mode', 'overlay').attr('in', 'SourceGraphic').attr('in2', 'gray');

  // ── Clip paths ──
  defs.append('clipPath').attr('id', 'continent-clip')
    .append('path').attr('d', CONTINENT);

  Object.entries(REGIONS).forEach(([id, r]) => {
    defs.append('clipPath').attr('id', `region-clip-${id}`)
      .append('path').attr('d', r.path);
  });
}
