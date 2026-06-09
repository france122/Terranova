import * as d3 from 'd3';
import { PALETTE } from './palette';

type G = d3.Selection<SVGGElement, unknown, null, undefined>;

export const REGIONS: Record<string, {
  path: string;
  label: string;
  labelPos: [number, number];
  biomeType: 'forest' | 'meadow' | 'highland' | 'coastal';
}> = {
  ds_ch1: {
    path: `M 120 310 C 110 240, 160 170, 240 145 C 340 110, 440 90, 530 100
           C 570 100, 580 140, 560 190 C 540 250, 490 310, 430 360
           C 370 400, 280 400, 220 370 C 160 345, 125 330, 120 310 Z`,
    label: '线性表', labelPos: [335, 185],
    biomeType: 'forest',
  },
  ds_ch2: {
    path: `M 100 380 C 140 350, 240 340, 320 360 C 400 340, 450 370, 460 420
           C 475 480, 440 540, 390 575 C 330 610, 250 615, 190 590
           C 130 565, 85 510, 78 450 C 72 410, 82 390, 100 380 Z`,
    label: '栈与队列', labelPos: [275, 395],
    biomeType: 'meadow',
  },
  ds_ch3: {
    path: `M 360 540 C 400 505, 480 490, 560 505 C 640 490, 690 520, 700 570
           C 715 630, 690 690, 640 720 C 580 750, 490 755, 420 730
           C 370 715, 340 670, 335 620 C 330 575, 345 555, 360 540 Z`,
    label: '树与二叉树', labelPos: [520, 515],
    biomeType: 'highland',
  },
  ds_ch4: {
    path: `M 420 730 C 480 700, 580 690, 670 700 C 740 695, 770 730, 760 780
           C 750 830, 710 880, 650 910 C 580 935, 490 940, 420 920
           C 360 905, 320 870, 330 820 C 340 775, 370 750, 420 730 Z`,
    label: '图', labelPos: [585, 740],
    biomeType: 'coastal',
  },
  cn_ch1: {
    path: `M 830 130 C 900 85, 1020 70, 1140 100 C 1250 80, 1350 120, 1400 170
           C 1450 220, 1460 290, 1430 350 C 1400 410, 1320 440, 1230 430
           C 1140 440, 1050 420, 980 390 C 910 360, 850 310, 830 250 C 815 200, 815 160, 830 130 Z`,
    label: '物理层与数据链路层', labelPos: [1130, 175],
    biomeType: 'highland',
  },
  cn_ch2: {
    path: `M 830 400 C 890 370, 1000 355, 1120 375 C 1230 360, 1330 400, 1380 450
           C 1430 500, 1440 570, 1410 630 C 1370 680, 1290 700, 1200 690
           C 1100 700, 1010 690, 940 660 C 870 630, 825 580, 815 520 C 805 470, 815 430, 830 400 Z`,
    label: '网络层', labelPos: [1115, 430],
    biomeType: 'forest',
  },
  cn_ch3: {
    path: `M 860 680 C 920 650, 1030 635, 1150 650 C 1260 640, 1370 680, 1420 740
           C 1470 800, 1450 860, 1390 900 C 1310 935, 1200 950, 1090 940
           C 980 950, 900 935, 860 890 C 820 850, 810 790, 820 740 C 828 710, 840 695, 860 680 Z`,
    label: '传输层与应用层', labelPos: [1140, 680],
    biomeType: 'coastal',
  },
};

export const CONTINENT = `
  M 100 320 C 90 250, 140 170, 220 140 C 310 100, 400 80, 500 95
  C 560 70, 620 60, 700 80 C 760 55, 830 65, 900 90
  C 970 60, 1060 70, 1140 100 C 1220 80, 1300 110, 1370 150
  C 1430 180, 1470 230, 1490 300 C 1510 370, 1520 440, 1510 510
  C 1520 580, 1510 650, 1480 710 C 1460 770, 1420 830, 1360 870
  C 1290 920, 1200 940, 1100 935 C 1020 950, 950 940, 880 920
  C 830 950, 770 955, 710 940 C 640 960, 570 950, 500 930
  C 420 945, 350 930, 290 900 C 220 880, 170 840, 140 780
  C 110 730, 85 670, 75 600 C 65 530, 70 460, 80 400
  C 85 360, 90 340, 100 320 Z`;

export function renderRegions(g: G): void {
  for (const [id, r] of Object.entries(REGIONS)) {
    const biome = PALETTE.biomes[id];
    if (!biome) continue;

    // Base fill with radial gradient
    g.append('path').attr('d', r.path)
      .attr('fill', `url(#rg-${id})`).attr('opacity', 0.88);

    // Noise texture overlay (subtle organic feel)
    g.append('path').attr('d', r.path)
      .attr('fill', biome.main).attr('opacity', 0.08)
      .attr('filter', 'url(#terrain-noise)');

    // Biome-specific pattern overlay
    const patternId = r.biomeType === 'meadow' ? 'grass-hatch'
      : r.biomeType === 'highland' ? 'dot-stipple'
      : 'contours';
    g.append('path').attr('d', r.path)
      .attr('fill', `url(#${patternId})`).attr('opacity', 0.5);

    // Inner shadow border for depth
    g.append('path').attr('d', r.path)
      .attr('fill', 'none')
      .attr('stroke', biome.dark).attr('stroke-width', 5).attr('opacity', 0.25);

    // Edge highlight (rim light)
    g.append('path').attr('d', r.path)
      .attr('fill', 'none')
      .attr('stroke', biome.light).attr('stroke-width', 1.2).attr('opacity', 0.15);
  }
}

export function renderRegionLabels(g: G): void {
  for (const [, r] of Object.entries(REGIONS)) {
    const [x, y] = r.labelPos;
    // Text shadow
    g.append('text').attr('x', x + 1).attr('y', y + 1)
      .attr('text-anchor', 'middle').attr('fill', 'rgba(0,0,0,0.25)')
      .attr('font-size', 14).attr('font-weight', 600).attr('letter-spacing', 3)
      .attr('font-family', "'Cinzel', serif").text(r.label);
    // Main text
    g.append('text').attr('x', x).attr('y', y)
      .attr('text-anchor', 'middle').attr('fill', 'rgba(255,255,255,0.3)')
      .attr('font-size', 14).attr('font-weight', 600).attr('letter-spacing', 3)
      .attr('font-family', "'Cinzel', serif").text(r.label);
    // Decorative line below
    g.append('line')
      .attr('x1', x - 25).attr('y1', y + 8).attr('x2', x + 25).attr('y2', y + 8)
      .attr('stroke', 'rgba(255,255,255,0.1)').attr('stroke-width', 0.5);
  }

  // Course titles
  const titles: [string, number, number][] = [
    ['数据结构', 370, 115],
    ['计算机网络', 1160, 115],
  ];
  for (const [text, x, y] of titles) {
    g.append('text').attr('x', x + 1).attr('y', y + 1)
      .attr('text-anchor', 'middle').attr('fill', 'rgba(0,0,0,0.1)')
      .attr('font-size', 34).attr('font-weight', 700).attr('letter-spacing', 10)
      .attr('font-family', "'Cinzel', serif").text(text);
    g.append('text').attr('x', x).attr('y', y)
      .attr('text-anchor', 'middle').attr('fill', 'rgba(255,255,255,0.12)')
      .attr('font-size', 34).attr('font-weight', 700).attr('letter-spacing', 10)
      .attr('font-family', "'Cinzel', serif").text(text);
  }
}
