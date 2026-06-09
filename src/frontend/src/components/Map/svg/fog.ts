import * as d3 from 'd3';

type G = d3.Selection<SVGGElement, unknown, null, undefined>;
type RngFn = () => number;

interface GraphNode {
  id: string; name: string; node_type: string; parent_id: string | null;
  description: string; position_x: number; position_y: number;
  state?: string; stars?: number;
}

// Group nodes by chapter and compute bounding ellipses
function chapterClusters(nodes: GraphNode[]): {
  chId: string; cx: number; cy: number; rx: number; ry: number; fogOp: number;
}[] {
  const chapters = new Map<string, GraphNode[]>();
  for (const n of nodes) {
    const chId = n.parent_id || 'unknown';
    if (!chapters.has(chId)) chapters.set(chId, []);
    chapters.get(chId)!.push(n);
  }

  const clusters: { chId: string; cx: number; cy: number; rx: number; ry: number; fogOp: number }[] = [];
  for (const [chId, chNodes] of chapters) {
    if (!chNodes.length) continue;
    const done = chNodes.filter(n => n.state === 'explored' || n.state === 'mastered').length;
    const fogOp = Math.max(0, 0.85 * (1 - done / chNodes.length));
    if (fogOp < 0.03) continue;

    const xs = chNodes.map(n => n.position_x);
    const ys = chNodes.map(n => n.position_y);
    const minX = Math.min(...xs), maxX = Math.max(...xs);
    const minY = Math.min(...ys), maxY = Math.max(...ys);
    const cx = (minX + maxX) / 2;
    const cy = (minY + maxY) / 2;
    const rx = Math.max((maxX - minX) / 2 + 60, 80);
    const ry = Math.max((maxY - minY) / 2 + 50, 70);

    clusters.push({ chId, cx, cy, rx, ry, fogOp });
  }
  return clusters;
}

export function renderFog(g: G, nodes: GraphNode[], rngFn: (seed: number) => RngFn): void {
  const fogG = g.append('g');
  const clusters = chapterClusters(nodes);

  for (const cluster of clusters) {
    const rand = rngFn(cluster.chId.split('').reduce((a, c) => a + c.charCodeAt(0), 0));

    // Main fog ellipse — soft, heavily blurred
    fogG.append('ellipse')
      .attr('cx', cluster.cx).attr('cy', cluster.cy)
      .attr('rx', cluster.rx * 1.1).attr('ry', cluster.ry * 1.1)
      .attr('fill', 'rgba(180,195,210,0.6)')
      .attr('opacity', cluster.fogOp)
      .attr('filter', 'url(#fblur)');

    // A few additional soft cloud shapes for variation
    const cloudCount = 2 + Math.round(rand() * 2);
    for (let i = 0; i < cloudCount; i++) {
      const ox = (rand() - 0.5) * cluster.rx * 0.8;
      const oy = (rand() - 0.5) * cluster.ry * 0.6;
      const sr = 0.4 + rand() * 0.4;
      fogG.append('ellipse')
        .attr('cx', cluster.cx + ox).attr('cy', cluster.cy + oy)
        .attr('rx', cluster.rx * sr).attr('ry', cluster.ry * sr)
        .attr('fill', 'rgba(200,215,230,0.4)')
        .attr('opacity', cluster.fogOp * 0.6)
        .attr('filter', 'url(#fblur)')
        .attr('class', i % 2 === 0 ? 'fog-drift' : 'fog-drift-alt');
    }
  }
}
