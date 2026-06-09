import * as d3 from 'd3';

type G = d3.Selection<SVGGElement, unknown, null, undefined>;

const RIVER = `M 790 55 C 800 120, 775 200, 795 280 C 815 360, 775 440, 790 520
  C 805 600, 780 680, 795 760 C 805 840, 790 920, 795 965`;
const LAKE1 = `M 340 580 C 365 555, 410 550, 430 570 C 450 590, 440 620, 415 635 C 385 645, 345 635, 330 615 C 318 595, 320 570, 340 580 Z`;
const LAKE2 = `M 1155 415 C 1185 398, 1225 405, 1240 428 C 1255 452, 1240 480, 1210 492 C 1178 498, 1148 485, 1138 462 C 1128 438, 1138 418, 1155 415 Z`;

export function renderWater(g: G): void {
  // ═══ RIVER (5 layers) ═══

  // 1. River bed shadow
  g.append('path').attr('d', RIVER).attr('fill', 'none')
    .attr('stroke', 'rgba(0,0,0,0.3)').attr('stroke-width', 18)
    .attr('stroke-linecap', 'round')
    .attr('transform', 'translate(1,2)').attr('filter', 'url(#soften)');

  // 2. River bank (earth tone)
  g.append('path').attr('d', RIVER).attr('fill', 'none')
    .attr('stroke', '#3a5a38').attr('stroke-width', 14)
    .attr('stroke-linecap', 'round').attr('opacity', 0.5);

  // 3. Water body
  g.append('path').attr('d', RIVER).attr('fill', 'none')
    .attr('stroke', '#2a6a98').attr('stroke-width', 8)
    .attr('stroke-linecap', 'round').attr('opacity', 0.7);

  // 4. Surface highlight
  g.append('path').attr('d', RIVER).attr('fill', 'none')
    .attr('stroke', 'rgba(140,210,240,0.3)').attr('stroke-width', 2)
    .attr('stroke-linecap', 'round')
    .attr('stroke-dasharray', '12,20');

  // 5. Flowing shimmer
  g.append('path').attr('d', RIVER).attr('fill', 'none')
    .attr('stroke', 'rgba(180,230,255,0.25)').attr('stroke-width', 1)
    .attr('stroke-dasharray', '4,30').attr('stroke-linecap', 'round')
    .attr('class', 'river-shimmer');

  // ═══ LAKES (4 layers each) ═══
  for (const lk of [LAKE1, LAKE2]) {
    // 1. Shadow
    g.append('path').attr('d', lk)
      .attr('fill', 'rgba(0,0,0,0.2)')
      .attr('transform', 'translate(2,3)')
      .attr('filter', 'url(#soften)');

    // 2. Water body
    g.append('path').attr('d', lk)
      .attr('fill', '#1a5878').attr('opacity', 0.75);

    // 3. Depth highlight (lighter center)
    g.append('path').attr('d', lk)
      .attr('fill', 'rgba(60,150,200,0.15)');

    // 4. Surface shimmer
    g.append('path').attr('d', lk)
      .attr('fill', 'rgba(120,200,240,0.1)')
      .attr('class', 'water-surface');
  }
}
