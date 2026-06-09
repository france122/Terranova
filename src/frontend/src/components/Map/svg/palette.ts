export const PALETTE = {
  ocean: {
    deep: '#0d2b45',
    mid: '#1a4a6e',
    surface: '#2d6a94',
    foam: 'rgba(180,220,240,0.3)',
    wave: 'rgba(100,180,220,0.08)',
  },
  beach: {
    sand: '#d4b483',
    wet: '#b89a6a',
    edge: '#c2a572',
  },
  continent: {
    base: '#5a8a4a',
    border: '#3a6a36',
    shadow: 'rgba(20,40,15,0.45)',
  },
  biomes: {
    ds_ch1: { main: '#3d8e3d', light: '#5cb85c', dark: '#1e6e1e', accent: '#78d878' },
    ds_ch2: { main: '#6a9e30', light: '#8ec050', dark: '#4a7e18', accent: '#a8e060' },
    ds_ch3: { main: '#2a7a5a', light: '#48a880', dark: '#0e5e3e', accent: '#60c898' },
    ds_ch4: { main: '#3a6858', light: '#588a78', dark: '#1e4c3e', accent: '#70a898' },
    cn_ch1: { main: '#c8a030', light: '#e8c048', dark: '#a08018', accent: '#f0d860' },
    cn_ch2: { main: '#d49030', light: '#e8a848', dark: '#b07018', accent: '#f0c060' },
    cn_ch3: { main: '#c07840', light: '#d89858', dark: '#a06028', accent: '#e8b068' },
  } as Record<string, { main: string; light: string; dark: string; accent?: string }>,
  nodes: {
    locked:   { fill: '#3a3a3a', stroke: '#2a2a2a', text: 'rgba(150,150,150,0.4)' },
    visible:  { fill: 'rgba(120,140,120,0.25)', stroke: 'rgba(180,200,180,0.5)', text: 'rgba(200,220,200,0.6)' },
    unlocked: { fill: '#4FC3F7', glow: 'rgba(79,195,247,0.45)', stroke: '#fff' },
    explored: { fill: '#81C784', glow: 'rgba(129,199,132,0.35)', stroke: '#e0f0e0' },
    mastered: { fill: '#FFD54F', glow: 'rgba(255,213,79,0.3)', stroke: '#fff5d0', crown: '#FFA000' },
  },
  roads: {
    lit: '#c8b070',
    unlit: '#6a6048',
    shadow: 'rgba(0,0,0,0.25)',
    surface_lit: '#b8a860',
    surface_unlit: '#7a6a48',
    center: 'rgba(230,210,150,0.25)',
  },
  tunnel: {
    line: '#FFD54F',
    particle: 'rgba(255,213,79,0.6)',
    portal: 'rgba(255,213,79,0.2)',
  },
  fog: {
    base: 'rgba(200,215,230,0.75)',
    cloud: 'rgba(220,230,240,0.6)',
    highlight: 'rgba(240,245,250,0.3)',
    shadow: 'rgba(140,155,170,0.2)',
  },
  atmosphere: {
    vignette: 'rgba(10,20,35,0.5)',
    particle: 'rgba(255,255,220,0.15)',
    light: 'rgba(255,250,230,0.04)',
  },
  terrain: {
    mountain: { back: '#4a5a48', front: '#5a6a58', snow: 'rgba(235,245,255,0.7)', shadow: 'rgba(0,0,0,0.15)' },
    tree: {
      trunk: '#5a4a30',
      conifer: { dark: '#2a5a28', mid: '#3a7a38', light: '#4a9a48' },
      deciduous: { dark: '#3a6a2a', mid: '#4a8a3a', light: '#5aaa4a' },
    },
    rock: { fill: '#6a6a60', stroke: '#5a5a52' },
    grass: '#6aaa4a',
    flower: ['#e87070', '#e8c040', '#d080d0', '#70b0e0'],
  },
};

export const COURSE_THEME: Record<string, { primary: string; glow: string }> = {
  ds: { primary: '#4FC3F7', glow: 'rgba(79,195,247,0.5)' },
  cn: { primary: '#81C784', glow: 'rgba(129,199,132,0.5)' },
};
