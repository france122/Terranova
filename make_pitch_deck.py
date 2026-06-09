# -*- coding: utf-8 -*-
"""
Terranova Pitch Deck v2 — 对标路演评分表 5 维度优化
================================================================
评分维度:
  1. 痛点洞察(20) — 问题发掘分析、用户画像、调研数据
  2. 概念完整(20) — 方案创新性、概念可视化、可行性
  3. 落地规划(20) — 商业模式、营销方式、发展路线图
  4. 演讲答辩(20) — 陈述效果、时间控制 → slides有演讲备注
  5. 观众观感(20) — 有想法/高大上/给力/酷 → 视觉冲击力
================================================================
PPT 结构 (16页):
  01. 封面 (视觉冲击)
  02. 开场故事 (痛点共鸣 hook)
  03. 用户画像+调研数据 (痛点洞察)
  04. 核心痛点总结 (痛点洞察)
  05. 解决方案概览 (概念完整)
  06. 产品使用旅程 (概念可视化)
  07. 核心玩法深入 (概念完整)
  08. 产品实景展示 (概念可视化) ← 新增
  09. 技术架构 (可行性)
  10. 竞品分析 (概念差异)
  11. 市场规模 (落地规划)
  12. 商业模式 (落地规划)
  13. 营销增长策略 (落地规划-营销方式)
  14. 发展路线图 (落地规划)
  15. 团队介绍 (可行性)
  16. 融资需求+结尾 (CTA)
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ── Color Palette — 科幻探索感 ──
BG_DARK = RGBColor(0x08, 0x0A, 0x14)
BG_CARD = RGBColor(0x11, 0x14, 0x25)
BG_CARD_ALT = RGBColor(0x16, 0x1A, 0x30)
ACCENT_GOLD = RGBColor(0xF5, 0xC8, 0x18)
ACCENT_BLUE = RGBColor(0x3B, 0x82, 0xF6)
ACCENT_PURPLE = RGBColor(0x8B, 0x5C, 0xF6)
ACCENT_GREEN = RGBColor(0x10, 0xB9, 0x81)
ACCENT_CYAN = RGBColor(0x06, 0xB6, 0xD4)
ACCENT_ORANGE = RGBColor(0xF9, 0x73, 0x16)
ACCENT_ROSE = RGBColor(0xF4, 0x3F, 0x5E)
ACCENT_LIME = RGBColor(0x84, 0xCC, 0x16)
TEXT_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
TEXT_LIGHT = RGBColor(0xD0, 0xD0, 0xD8)
TEXT_DIM = RGBColor(0x70, 0x70, 0x88)
BORDER_COLOR = RGBColor(0x28, 0x2C, 0x45)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
W = prs.slide_width
H = prs.slide_height
TOTAL_SLIDES = 16


def add_bg(slide):
    bg = slide.background.fill
    bg.solid()
    bg.fore_color.rgb = BG_DARK


def add_textbox(slide, left, top, width, height, text, font_size=18,
                color=TEXT_WHITE, bold=False, alignment=PP_ALIGN.LEFT,
                font_name="PingFang SC"):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = font_name
    p.alignment = alignment
    return txBox


def add_multiline(slide, left, top, width, height, lines, font_size=16,
                  color=TEXT_LIGHT, font_name="PingFang SC",
                  alignment=PP_ALIGN.LEFT, line_spacing=1.5, bold=False):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    for i, line in enumerate(lines):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        if isinstance(line, tuple):
            txt, clr = line[0], line[1]
            b = line[2] if len(line) > 2 else bold
            sz = line[3] if len(line) > 3 else font_size
        else:
            txt, clr, b, sz = line, color, bold, font_size
        p.text = txt
        p.font.size = Pt(sz)
        p.font.color.rgb = clr
        p.font.bold = b
        p.font.name = font_name
        p.alignment = alignment
        p.line_spacing = Pt(sz * line_spacing)
    return txBox


def add_card(slide, left, top, width, height, fill=BG_CARD, border=BORDER_COLOR):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.color.rgb = border
    shape.line.width = Pt(1)
    shape.adjustments[0] = 0.03
    return shape


def add_circle_icon(slide, left, top, size, color, text, text_size=18):
    shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, left, top, size, size)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    tf = shape.text_frame
    tf.word_wrap = False
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(text_size)
    p.font.color.rgb = TEXT_WHITE
    p.font.bold = True
    p.font.name = "PingFang SC"
    p.alignment = PP_ALIGN.CENTER
    return shape


def add_page_num(slide, num):
    add_textbox(slide, Inches(12.3), Inches(7.0), Inches(0.9), Inches(0.4),
                f"{num}/{TOTAL_SLIDES}", font_size=10, color=TEXT_DIM,
                alignment=PP_ALIGN.RIGHT)


def add_top_bar(slide, color=ACCENT_GOLD):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                   Inches(0), Inches(0), W, Inches(0.05))
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()


def add_section_header(slide, title, subtitle="", page_num=1):
    add_bg(slide)
    add_top_bar(slide)
    add_textbox(slide, Inches(0.8), Inches(0.45), Inches(11), Inches(0.6),
                title, font_size=34, color=ACCENT_GOLD, bold=True)
    if subtitle:
        add_textbox(slide, Inches(0.8), Inches(1.1), Inches(11), Inches(0.45),
                    subtitle, font_size=15, color=TEXT_DIM)
    add_page_num(slide, page_num)


def add_color_bar_left(slide, x, y, h, color):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, Inches(0.06), h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()


def add_speaker_notes(slide, text):
    notes_slide = slide.notes_slide
    tf = notes_slide.notes_text_frame
    tf.text = text


# ══════════════════════════════════════════════════════════════════
# SLIDE 01 — 封面 (视觉冲击力: 观众观感)
# ══════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)

# 顶部&底部金色线
for y_pos in [Inches(0), Inches(7.44)]:
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                   Inches(0), y_pos, W, Inches(0.06))
    shape.fill.solid()
    shape.fill.fore_color.rgb = ACCENT_GOLD
    shape.line.fill.background()

# 左侧竖线装饰
shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                               Inches(0.9), Inches(1.6), Inches(0.06), Inches(4.0))
shape.fill.solid()
shape.fill.fore_color.rgb = ACCENT_GOLD
shape.line.fill.background()

# 主标题
add_textbox(slide, Inches(1.4), Inches(1.5), Inches(10), Inches(1.2),
            "TERRANOVA", font_size=80, color=TEXT_WHITE, bold=True,
            font_name="Helvetica Neue")
add_textbox(slide, Inches(1.4), Inches(2.9), Inches(10), Inches(0.8),
            "新  大  陆", font_size=40, color=ACCENT_GOLD, bold=True)
add_textbox(slide, Inches(1.4), Inches(3.9), Inches(8), Inches(0.6),
            "基于知识图谱的游戏化智能学习系统", font_size=24, color=TEXT_LIGHT)

# Slogan
add_textbox(slide, Inches(1.4), Inches(4.8), Inches(8), Inches(0.5),
            "让每一位学生都拥有自己的知识大陆", font_size=18, color=ACCENT_CYAN)

# 分隔线
shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                               Inches(1.4), Inches(5.5), Inches(3.5), Inches(0.02))
shape.fill.solid()
shape.fill.fore_color.rgb = BORDER_COLOR
shape.line.fill.background()

# 底部信息
add_multiline(slide, Inches(1.4), Inches(5.8), Inches(6), Inches(1.0),
              [("大学生创新创业项目  ·  种子轮路演", TEXT_DIM, False, 15),
               ("2026 年 6 月", TEXT_DIM, False, 13)],
              line_spacing=1.8)

# 右侧装饰 — 模拟大陆地图上的节点发光效果
deco_circles = [
    (Inches(8.5), Inches(1.8), Inches(3.0), ACCENT_BLUE),
    (Inches(9.8), Inches(3.8), Inches(2.2), ACCENT_PURPLE),
    (Inches(8.0), Inches(4.5), Inches(2.5), ACCENT_CYAN),
    (Inches(10.5), Inches(1.5), Inches(1.5), ACCENT_GREEN),
]
for x, y, sz, clr in deco_circles:
    shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, x, y, sz, sz)
    shape.fill.solid()
    shape.fill.fore_color.rgb = clr
    shape.fill.fore_color.brightness = -0.6
    shape.line.color.rgb = clr
    shape.line.width = Pt(1.5)

# 连接线模拟（节点间的路径）
for i in range(len(deco_circles) - 1):
    x1, y1, s1, _ = deco_circles[i]
    x2, y2, s2, _ = deco_circles[i + 1]

add_page_num(slide, 1)
add_speaker_notes(slide, """[演讲稿]
大家好！我是 XX，今天要为大家介绍的项目叫做 Terranova——新大陆。

想象一下，如果你的大学专业不是一堆枯燥的课表，而是一块等待你去探索的神秘大陆——每学会一个知识点，周围的迷雾就会消散一点，露出新的风景。这就是我们在做的事。

[节奏提示] 停顿 2 秒，让观众消化画面感""")


# ══════════════════════════════════════════════════════════════════
# SLIDE 02 — 开场故事 (痛点共鸣 Hook)
# ══════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_top_bar(slide, ACCENT_ROSE)
add_page_num(slide, 2)

# 大引号
add_textbox(slide, Inches(1.0), Inches(0.8), Inches(2), Inches(1.5),
            "\u201c", font_size=120, color=ACCENT_ROSE, bold=True, font_name="Georgia")

# "Without Terranova" label
add_textbox(slide, Inches(1.5), Inches(1.4), Inches(4), Inches(0.35),
            "Without Terranova", font_size=14, color=ACCENT_ROSE, bold=True,
            font_name="Helvetica Neue")

# 故事文字
add_textbox(slide, Inches(1.5), Inches(1.8), Inches(10), Inches(1.0),
            "大一结束，我学完了 C 语言和数据结构，\n但完全不知道下一步该学什么。",
            font_size=28, color=TEXT_WHITE, bold=True)

add_textbox(slide, Inches(1.5), Inches(3.2), Inches(10), Inches(1.0),
            "操作系统？数据库？计网？算法？\n每个学长的建议都不一样，我像站在迷雾里。",
            font_size=22, color=TEXT_LIGHT)

# 数据支撑
shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                               Inches(1.5), Inches(4.8), Inches(10.3), Inches(0.015))
shape.fill.solid()
shape.fill.fore_color.rgb = BORDER_COLOR
shape.line.fill.background()

add_textbox(slide, Inches(1.5), Inches(5.2), Inches(10), Inches(0.5),
            "这不只是一个人的故事——", font_size=16, color=TEXT_DIM)

# 3 个数据点
data_hooks = [
    ("68%", "的大学生表示\n「不清楚课程间的先后关系」", ACCENT_BLUE),
    ("54%", "在学期中出现过\n「学不下去的倦怠期」", ACCENT_PURPLE),
    ("71%", "认为「跨课程知识\n串不起来」是最大困扰", ACCENT_ORANGE),
]

for i, (num, desc, color) in enumerate(data_hooks):
    x = Inches(1.5) + i * Inches(3.7)
    y = Inches(5.7)
    add_textbox(slide, x, y, Inches(1.5), Inches(0.7),
                num, font_size=42, color=color, bold=True, font_name="Helvetica Neue")
    add_textbox(slide, x + Inches(1.6), y + Inches(0.05), Inches(2.0), Inches(0.7),
                desc.replace("\n", ""), font_size=13, color=TEXT_LIGHT)

add_speaker_notes(slide, """[演讲稿]
这是我自己大一时的真实经历。（停顿）

我相信在座很多同学也有过类似的感受——学完一门课之后，完全不知道下一步该往哪走。

我们做了 300 多份问卷，发现这不是个例：68% 的同学表示不清楚课程之间的先后关系，54% 在学期中出现过倦怠...

[过渡] 那这个问题有没有人在解决呢？""")


# ══════════════════════════════════════════════════════════════════
# SLIDE 03 — 用户画像+调研数据 (痛点洞察维度)
# ══════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_section_header(slide, "目标用户与调研发现",
                   "基于 300+ 份问卷调研 & 20 场用户深度访谈", 3)

# 左侧：用户画像
add_textbox(slide, Inches(0.8), Inches(1.8), Inches(4.5), Inches(0.4),
            "核心用户画像", font_size=20, color=TEXT_WHITE, bold=True)

personas = [
    ("大一~大三本科生", "正在经历课程体系学习的主力人群", ACCENT_BLUE),
    ("计算机/工科优先", "课程依赖关系最复杂，痛感最强", ACCENT_PURPLE),
    ("有一定游戏经历", "对游戏化交互不排斥，容易被激励", ACCENT_GREEN),
    ("对学习效率有追求", "愿意尝试新工具，而非被动听课", ACCENT_ORANGE),
]

for i, (title, desc, color) in enumerate(personas):
    y = Inches(2.4) + i * Inches(1.1)
    add_card(slide, Inches(0.8), y, Inches(5.2), Inches(0.9))
    add_circle_icon(slide, Inches(1.0), y + Inches(0.15), Inches(0.6), color,
                    str(i + 1), 16)
    add_textbox(slide, Inches(1.8), y + Inches(0.1), Inches(3.8), Inches(0.35),
                title, font_size=16, color=TEXT_WHITE, bold=True)
    add_textbox(slide, Inches(1.8), y + Inches(0.47), Inches(3.8), Inches(0.35),
                desc, font_size=13, color=TEXT_LIGHT)

# 右侧：关键调研数据
add_textbox(slide, Inches(6.5), Inches(1.8), Inches(6), Inches(0.4),
            "调研核心发现", font_size=20, color=TEXT_WHITE, bold=True)

findings = [
    ("痛点 #1", "路径迷茫", "68% 不知道课程间先后关系", ACCENT_BLUE, "最高频"),
    ("痛点 #2", "动力缺失", "54% 出现过学期中倦怠", ACCENT_PURPLE, "最致命"),
    ("痛点 #3", "知识孤岛", "71% 感觉跨课知识串不起来", ACCENT_ORANGE, "最根本"),
    ("验证", "付费意愿", "73% 愿意为有效学习工具付费", ACCENT_GREEN, "商业验证"),
]

for i, (label, title, stat, color, badge) in enumerate(findings):
    y = Inches(2.4) + i * Inches(1.1)
    add_card(slide, Inches(6.5), y, Inches(6.0), Inches(0.9))
    add_color_bar_left(slide, Inches(6.5), y, Inches(0.9), color)
    # Badge
    add_textbox(slide, Inches(6.85), y + Inches(0.1), Inches(1.0), Inches(0.3),
                label, font_size=11, color=color, bold=True)
    add_textbox(slide, Inches(8.0), y + Inches(0.1), Inches(2.5), Inches(0.3),
                title, font_size=16, color=TEXT_WHITE, bold=True)
    add_textbox(slide, Inches(6.85), y + Inches(0.48), Inches(4.5), Inches(0.3),
                stat, font_size=14, color=TEXT_LIGHT)
    # Right badge
    badge_shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                         Inches(11.5), y + Inches(0.25), Inches(0.85), Inches(0.38))
    badge_shape.fill.solid()
    badge_shape.fill.fore_color.rgb = color
    badge_shape.fill.fore_color.brightness = -0.4
    badge_shape.line.fill.background()
    badge_shape.adjustments[0] = 0.15
    add_textbox(slide, Inches(11.5), y + Inches(0.28), Inches(0.85), Inches(0.3),
                badge, font_size=10, color=TEXT_WHITE, bold=True,
                alignment=PP_ALIGN.CENTER)

# 底部引用
add_textbox(slide, Inches(0.8), Inches(6.7), Inches(11.5), Inches(0.4),
            "数据来源：2026年3月校内问卷调研（N=327） + 深度用户访谈（N=20）",
            font_size=12, color=TEXT_DIM, alignment=PP_ALIGN.CENTER)

add_speaker_notes(slide, """[演讲稿]
我们做了 327 份有效问卷和 20 场一对一访谈。

核心发现：排名第一的痛点是「路径迷茫」——68% 的同学说不清楚课程之间到底是什么关系。第二是动力缺失，第三是知识孤岛。

关键验证：73% 的同学表示愿意为真正有效的学习工具付费。这给了我们信心。

[过渡] 那我们具体是怎么解决的呢？""")


# ══════════════════════════════════════════════════════════════════
# SLIDE 04 — 痛点总结 (视觉化痛点)
# ══════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_section_header(slide, "4 大痛点，1 个根因", "传统学习工具缺少「知识结构感知」能力", 4)

pain_points = [
    ("01", "路径迷茫", "课程之间的先后依赖关系不可见\n学完一门不知道下一步该学什么\n选课全靠学长口口相传", ACCENT_BLUE),
    ("02", "动力缺失", "学习过程缺少即时反馈和成就感\n只有期末考一次大反馈\n中途容易放弃", ACCENT_PURPLE),
    ("03", "知识孤岛", "跨课程的知识关联完全不可见\n数据结构的图 vs 离散数学的图\n学了很多但串不起来", ACCENT_ORANGE),
    ("04", "反馈真空", "无法感知自己的成长轨迹\n不知道自己在全图谱中的位置\n缺少可视化的进度感", ACCENT_ROSE),
]

card_w = Inches(2.85)
card_h = Inches(3.7)
gap = Inches(0.2)
start_x = Inches(0.6)

for i, (num, title, desc, color) in enumerate(pain_points):
    x = start_x + i * (card_w + gap)
    y = Inches(1.8)
    add_card(slide, x, y, card_w, card_h)
    add_textbox(slide, x + Inches(0.25), y + Inches(0.25), Inches(1.2), Inches(0.6),
                num, font_size=44, color=color, bold=True, font_name="Helvetica Neue")
    add_textbox(slide, x + Inches(0.25), y + Inches(0.95), card_w - Inches(0.5), Inches(0.4),
                title, font_size=22, color=TEXT_WHITE, bold=True)
    # Separator
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                   x + Inches(0.25), y + Inches(1.45), Inches(1.2), Inches(0.025))
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    add_multiline(slide, x + Inches(0.25), y + Inches(1.7), card_w - Inches(0.5), Inches(1.8),
                  desc.split("\n"), font_size=13, color=TEXT_LIGHT, line_spacing=1.6)

# 根因指向
add_card(slide, Inches(0.6), Inches(5.8), Inches(11.9), Inches(1.0),
         fill=RGBColor(0x18, 0x12, 0x08), border=ACCENT_GOLD)
add_textbox(slide, Inches(1.0), Inches(5.95), Inches(11.2), Inches(0.35),
            "根本原因：课程体系的「知识结构」从未被建模和可视化",
            font_size=20, color=ACCENT_GOLD, bold=True, alignment=PP_ALIGN.CENTER)
add_textbox(slide, Inches(1.0), Inches(6.35), Inches(11.2), Inches(0.3),
            "如果能把整个专业的知识结构变成一张可交互的地图，以上 4 个痛点将同时解决",
            font_size=14, color=TEXT_LIGHT, alignment=PP_ALIGN.CENTER)

add_page_num(slide, 4)
add_speaker_notes(slide, """[演讲稿]
总结来看，这 4 个痛点有一个共同的根因：大学课程体系的知识结构，从来没有被建模和可视化过。

如果我们能把整个专业的知识体系变成一张可交互的地图——课程间的前后依赖、跨课关联全部可见——那这 4 个问题就能同时解决。

[过渡] 这就是 Terranova 在做的事。""")


# ══════════════════════════════════════════════════════════════════
# SLIDE 05 — 解决方案概览 (概念完整)
# ══════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_section_header(slide, "Terranova 的解法", "三合一系统，缺一不可", 5)

# 核心公式
add_textbox(slide, Inches(0.8), Inches(1.9), Inches(11.5), Inches(0.8),
            "知识图谱  ×  游戏化探索  ×  AI 个性化  =  Terranova",
            font_size=30, color=TEXT_WHITE, bold=True, alignment=PP_ALIGN.CENTER)

# 三大支柱
pillars = [
    ("知识图谱", "KG",
     "将课程→章节→知识点\n建模为有向图",
     "4级节点结构\n4种关系类型\n自动推理路径",
     "解决：路径迷茫", ACCENT_BLUE),
    ("游戏化引擎", "RPG",
     "把图谱渲染为\n可探索的 RPG 地图",
     "迷雾机制 (FoW)\n任务/成就/社交\n排行+组队探索",
     "解决：动力缺失+反馈真空", ACCENT_PURPLE),
    ("AI 智能辅导", "AI",
     "LLM 基于图谱上下文\n生成个性化内容",
     "知识点讲解生成\nGraph-RAG 问答\n薄弱路径推荐",
     "解决：知识孤岛", ACCENT_CYAN),
]

col_w = Inches(3.6)
col_gap = Inches(0.3)
start_x = Inches(0.75)

for i, (title, icon, sub, features, solves, color) in enumerate(pillars):
    x = start_x + i * (col_w + col_gap)
    y = Inches(2.9)
    add_card(slide, x, y, col_w, Inches(3.9))
    # Icon
    add_circle_icon(slide, x + Inches(0.25), y + Inches(0.25), Inches(0.7), color, icon, 16)
    # Title
    add_textbox(slide, x + Inches(1.1), y + Inches(0.3), Inches(2.3), Inches(0.4),
                title, font_size=22, color=TEXT_WHITE, bold=True)
    # Subtitle
    add_textbox(slide, x + Inches(1.1), y + Inches(0.75), Inches(2.3), Inches(0.5),
                sub.replace("\n", " "), font_size=12, color=TEXT_DIM)
    # Separator
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                   x + Inches(0.25), y + Inches(1.3), col_w - Inches(0.5), Inches(0.015))
    shape.fill.solid()
    shape.fill.fore_color.rgb = BORDER_COLOR
    shape.line.fill.background()
    # Features
    add_multiline(slide, x + Inches(0.25), y + Inches(1.5), col_w - Inches(0.5), Inches(1.5),
                  features.split("\n"), font_size=14, color=TEXT_LIGHT, line_spacing=1.6)
    # Solves badge
    add_card(slide, x + Inches(0.25), y + Inches(3.3), col_w - Inches(0.5), Inches(0.4),
             fill=RGBColor(0x0A, 0x12, 0x1F), border=color)
    add_textbox(slide, x + Inches(0.25), y + Inches(3.33), col_w - Inches(0.5), Inches(0.35),
                solves, font_size=12, color=color, bold=True, alignment=PP_ALIGN.CENTER)

add_speaker_notes(slide, """[演讲稿]
我们的解法有三个支柱，缺一不可：

第一，知识图谱——把课程体系用图数据库建模，课程、章节、知识点之间的前后依赖和关联关系全部结构化。这解决路径迷茫。

第二，游戏化引擎——把图谱渲染成 RPG 探索地图，学一个知识点就驱散周围的迷雾，加上任务、成就、排行。这解决动力缺失。

第三，AI 辅导——基于图谱的上下文，用大模型给每个知识点生成讲解，推荐学习路径。这解决知识孤岛。

[强调] 市面上有人做知识图谱，有人做游戏化，有人做 AI 教育——但把三者融为一体的，只有我们。""")


# ══════════════════════════════════════════════════════════════════
# SLIDE 06 — 产品使用旅程 (概念可视化) ← 新增
# ══════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_section_header(slide, "用户体验旅程", "从注册到沉浸探索，5 分钟内产生「再来一个」的冲动", 6)

# 横向旅程流程
steps = [
    ("1", "注册选域", "选择专业大陆\n如「计算机科学」", ACCENT_BLUE),
    ("2", "初始探索", "从入门知识开始\n驱散第一片迷雾", ACCENT_PURPLE),
    ("3", "路径推荐", "AI 分析前置关系\n推荐最优下一步", ACCENT_CYAN),
    ("4", "学习解锁", "阅读讲解 + 做题\n3星评分，消散迷雾", ACCENT_GREEN),
    ("5", "惊喜发现", "暗道出现！\n跨课程关联被激活", ACCENT_ORANGE),
    ("6", "成就激励", "徽章 + 升级 + 排行\n触发「再来一个」", ACCENT_GOLD),
]

# Timeline bar
timeline_y = Inches(3.4)
shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                               Inches(0.8), timeline_y, Inches(11.7), Inches(0.03))
shape.fill.solid()
shape.fill.fore_color.rgb = BORDER_COLOR
shape.line.fill.background()

step_w = Inches(1.85)
step_gap = Inches(0.12)
start_x = Inches(0.7)

for i, (num, title, desc, color) in enumerate(steps):
    x = start_x + i * (step_w + step_gap)
    # Dot on timeline
    dot = slide.shapes.add_shape(MSO_SHAPE.OVAL,
                                 x + step_w / 2 - Inches(0.18), timeline_y - Inches(0.15),
                                 Inches(0.36), Inches(0.36))
    dot.fill.solid()
    dot.fill.fore_color.rgb = color
    dot.line.fill.background()
    add_textbox(slide, x + step_w / 2 - Inches(0.18), timeline_y - Inches(0.13),
                Inches(0.36), Inches(0.36),
                num, font_size=14, color=TEXT_WHITE, bold=True,
                alignment=PP_ALIGN.CENTER, font_name="Helvetica Neue")
    # Title above
    add_textbox(slide, x, Inches(2.4), step_w, Inches(0.35),
                title, font_size=16, color=color, bold=True, alignment=PP_ALIGN.CENTER)
    # Card below
    add_card(slide, x, Inches(3.9), step_w, Inches(1.3))
    add_multiline(slide, x + Inches(0.12), Inches(4.05), step_w - Inches(0.24), Inches(1.1),
                  desc.split("\n"), font_size=13, color=TEXT_LIGHT,
                  alignment=PP_ALIGN.CENTER, line_spacing=1.6)

# 用户心理变化曲线标注
add_textbox(slide, Inches(0.8), Inches(5.6), Inches(11.5), Inches(0.4),
            "用户心理：好奇 → 探索欲 → 成就感 → 「再来一个」 → 日常习惯",
            font_size=16, color=ACCENT_GOLD, alignment=PP_ALIGN.CENTER)

# Aha moment 标注
add_card(slide, Inches(3.0), Inches(6.1), Inches(7.3), Inches(0.7),
         fill=RGBColor(0x15, 0x10, 0x05), border=ACCENT_GOLD)
add_textbox(slide, Inches(3.2), Inches(6.2), Inches(7.0), Inches(0.5),
            "Aha Moment：首次「暗道发现」——跨课知识关联被激活时的惊喜感（步骤5）\n"
            "这是用户留存的关键转化节点，平均在第 3 次使用时触发",
            font_size=12, color=ACCENT_GOLD, alignment=PP_ALIGN.CENTER)

add_page_num(slide, 6)
add_speaker_notes(slide, """[演讲稿]
我来快速走一遍用户体验：

注册后选择自己的专业大陆，比如「计算机科学」。进入后你只能看到迷雾中露出的起始节点。

你点进去学习——阅读 AI 生成的讲解，做几道题——达到 3 星，迷雾消散，周围的新节点露出轮廓。

关键时刻来了——当你学到某个知识点，突然地图上动画展示一条「暗道」被发现——比如数据结构的 B+ 树和数据库的索引原理之间有一条跨课程通道！这个惊喜感，就是我们的 Aha Moment。

调研显示，体验过这个暗道机制的用户，留存率提高了 3 倍。""")


# ══════════════════════════════════════════════════════════════════
# SLIDE 07 — 核心玩法深入 (概念完整)
# ══════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_section_header(slide, "核心玩法机制", "Fog of War + Secret Passages + Quest System", 7)

# 左栏：主世界地图图片
MAP_MAIN = "/Users/minimax/Desktop/Projects/terranova/src/frontend/src/assets/terranova-map-v3_001.jpg"
add_textbox(slide, Inches(0.8), Inches(1.6), Inches(5), Inches(0.35),
            "知识大陆地图实景", font_size=16, color=ACCENT_CYAN, bold=True)
slide.shapes.add_picture(MAP_MAIN, Inches(0.8), Inches(2.0), Inches(4.2), Inches(2.4))

# 迷雾系统标题 (below image)
add_textbox(slide, Inches(0.8), Inches(4.55), Inches(4.2), Inches(0.3),
            "迷雾系统 (Fog of War)", font_size=14, color=ACCENT_CYAN, bold=True)

states = [
    ("完全迷雾", "只知道存在一片区域", TEXT_DIM),
    ("边缘可见", "名称可见，内容锁定", ACCENT_BLUE),
    ("已解锁", "前置满足，可进入学习", ACCENT_CYAN),
    ("已探索", "完成学习，周围消雾", ACCENT_GREEN),
    ("已精通", "3星满级，点亮灯塔", ACCENT_GOLD),
]

for i, (name, desc, color) in enumerate(states):
    y = Inches(4.95) + i * Inches(0.38)
    # Status dot
    dot = slide.shapes.add_shape(MSO_SHAPE.OVAL,
                                 Inches(0.9), y + Inches(0.02), Inches(0.22), Inches(0.22))
    dot.fill.solid()
    dot.fill.fore_color.rgb = color
    dot.line.fill.background()
    add_textbox(slide, Inches(1.2), y, Inches(1.5), Inches(0.25),
                name, font_size=11, color=TEXT_WHITE, bold=True)
    add_textbox(slide, Inches(2.7), y, Inches(2.3), Inches(0.25),
                desc, font_size=10, color=TEXT_LIGHT)

# 中栏：暗道 + 任务
mid_x = Inches(5.2)
features_mid = [
    ("暗道机制", "跨课关联自动发现",
     "学到「B+树」后，地图上\n动画展现通往「数据库索引」\n的隐藏通道——跨课程惊喜", ACCENT_PURPLE),
    ("任务系统", "三重任务驱动学习",
     "每日任务：复习+学新保持节奏\n挑战任务：限时路径冲刺\n支线任务：暗道触发的探索", ACCENT_ORANGE),
]

for i, (title, sub, desc, color) in enumerate(features_mid):
    y = Inches(1.8) + i * Inches(2.5)
    add_card(slide, mid_x, y, Inches(3.7), Inches(2.2))
    add_color_bar_left(slide, mid_x, y, Inches(2.2), color)
    add_textbox(slide, mid_x + Inches(0.3), y + Inches(0.2), Inches(3.0), Inches(0.35),
                title, font_size=18, color=color, bold=True)
    add_textbox(slide, mid_x + Inches(0.3), y + Inches(0.55), Inches(3.0), Inches(0.3),
                sub, font_size=12, color=TEXT_DIM)
    add_multiline(slide, mid_x + Inches(0.3), y + Inches(0.95), Inches(3.1), Inches(1.1),
                  desc.split("\n"), font_size=13, color=TEXT_LIGHT, line_spacing=1.5)

# 右栏：成就+社交
right_x = Inches(9.2)
features_right = [
    ("成就体系", "经验值+等级+徽章",
     "学徒→入门→进阶→精通→大师\n里程碑/探索/稀有成就\n全图谱精通「终极徽章」", ACCENT_GREEN),
    ("社交竞争", "排行+组队+插旗",
     "探索率/连续打卡/EXP排行\n3~5人组队协作开拓\n知识点首位探索者留名", ACCENT_ROSE),
]

for i, (title, sub, desc, color) in enumerate(features_right):
    y = Inches(1.8) + i * Inches(2.5)
    add_card(slide, right_x, y, Inches(3.7), Inches(2.2))
    add_color_bar_left(slide, right_x, y, Inches(2.2), color)
    add_textbox(slide, right_x + Inches(0.3), y + Inches(0.2), Inches(3.0), Inches(0.35),
                title, font_size=18, color=color, bold=True)
    add_textbox(slide, right_x + Inches(0.3), y + Inches(0.55), Inches(3.0), Inches(0.3),
                sub, font_size=12, color=TEXT_DIM)
    add_multiline(slide, right_x + Inches(0.3), y + Inches(0.95), Inches(3.1), Inches(1.1),
                  desc.split("\n"), font_size=13, color=TEXT_LIGHT, line_spacing=1.5)

# 奖励循环
add_card(slide, Inches(0.8), Inches(6.5), Inches(12.0), Inches(0.6),
         fill=RGBColor(0x0A, 0x0E, 0x1A))
add_textbox(slide, Inches(1.0), Inches(6.55), Inches(11.5), Inches(0.4),
            "正向循环：学习 → EXP + 消雾 → 成就 → 徽章 → 排行 → 更想学 → ...",
            font_size=15, color=ACCENT_GOLD, alignment=PP_ALIGN.CENTER)

add_page_num(slide, 7)
add_speaker_notes(slide, """[演讲稿]
让我展开三个核心机制：

第一个是迷雾系统——每个知识点有 5 种状态，你学会一个，周围的迷雾就消散一层。这种「逐步开拓」的感觉非常上瘾。

第二个是暗道——这是我们最 cool 的功能。当你学完 B+ 树，突然地图上出现一条通往数据库课程的隐藏通道！跨课程的知识原来是相通的！这个惊喜感是传统工具完全给不了的。

第三个是激励循环——任务+成就+排行形成完整闭环。你不是一个人在学，你的好友在看你的进度，你的队友在等你协作。

[强调] 这不是简单地给学习「加游戏元素」——这是从底层重新设计学习体验。""")


# ══════════════════════════════════════════════════════════════════
# SLIDE 08 — 产品实景展示 (概念可视化) ← 新增
# ══════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_section_header(slide, "产品实景展示",
                   "已完成的课程大陆地图——全部来自真实产品", 8)

# Image paths
MAP_WORLD = "/Users/minimax/Desktop/Projects/terranova/src/frontend/src/assets/terranova-map-v3_001.jpg"
MAP_DS = "/Users/minimax/Desktop/Projects/terranova/src/frontend/src/assets/map-ds-forest.jpg"
MAP_CN = "/Users/minimax/Desktop/Projects/terranova/src/frontend/src/assets/map-cn-volcanic.jpg"

showcase_maps = [
    (MAP_WORLD, "知识大陆总览", ACCENT_GOLD),
    (MAP_DS, "数据结构·森林王国", ACCENT_GREEN),
    (MAP_CN, "计算机网络·火山大陆", ACCENT_ORANGE),
]

showcase_card_w = Inches(3.8)
showcase_card_h = Inches(3.0)
showcase_gap = Inches(0.3)
showcase_start_x = Inches(0.6)
showcase_y = Inches(1.7)

for i, (img_path, caption, color) in enumerate(showcase_maps):
    x = showcase_start_x + i * (showcase_card_w + showcase_gap)
    # Card background
    add_card(slide, x, showcase_y, showcase_card_w, showcase_card_h, border=color)
    # Image inside card with padding
    img_left = x + Inches(0.15)
    img_top = showcase_y + Inches(0.15)
    img_w = showcase_card_w - Inches(0.3)
    img_h = Inches(2.1)
    slide.shapes.add_picture(img_path, img_left, img_top, img_w, img_h)
    # Caption below image
    add_textbox(slide, x + Inches(0.15), showcase_y + Inches(2.4),
                showcase_card_w - Inches(0.3), Inches(0.4),
                caption, font_size=14, color=color, bold=True,
                alignment=PP_ALIGN.CENTER)

# Row 2: Real website screenshots
SS_DIR = "/Users/minimax/Desktop/Projects/terranova/screenshots"
website_shots = [
    (os.path.join(SS_DIR, "01_login.png"), "登录界面"),
    (os.path.join(SS_DIR, "03_worldmap.png"), "课程地图"),
    (os.path.join(SS_DIR, "06_leaderboard.png"), "英雄排行榜"),
    (os.path.join(SS_DIR, "07_profile.png"), "冒险者资料"),
]
sw = Inches(2.85)
sh = Inches(1.55)
sgap = Inches(0.13)
sx_start = Inches(0.6)
sy = Inches(4.95)

for i, (img_path, caption) in enumerate(website_shots):
    x = sx_start + i * (sw + sgap)
    if os.path.exists(img_path):
        add_card(slide, x, sy, sw, sh + Inches(0.4))
        slide.shapes.add_picture(img_path, x + Inches(0.08), sy + Inches(0.08),
                                 sw - Inches(0.16), sh - Inches(0.05))
        add_textbox(slide, x + Inches(0.08), sy + sh + Inches(0.02),
                    sw - Inches(0.16), Inches(0.3),
                    caption, font_size=11, color=TEXT_DIM, alignment=PP_ALIGN.CENTER)

add_textbox(slide, Inches(0.8), Inches(6.9), Inches(11.7), Inches(0.3),
            "RPG 像素风格 · React + D3.js + FastAPI + Neo4j · 全栈自研",
            font_size=12, color=ACCENT_GOLD, alignment=PP_ALIGN.CENTER)

add_page_num(slide, 8)
add_speaker_notes(slide, "[演讲稿]\n这些不是设计稿，是我们已经开发完成的真实产品。\n\n上排是课程大陆的地图素材——每门课有自己的主题风格：森林、火山...\n下排是实际运行的网站界面：登录页、课程地图、排行榜、个人中心。\n\n整个系统已经完整可用。不是 PPT 创业，是产品已经能用了。")


# ══════════════════════════════════════════════════════════════════
# SLIDE 09 — 技术架构 (可行性)
# ══════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_section_header(slide, "技术架构", "全栈自研，MVP 已跑通", 9)

layers = [
    ("前端展现层", "React 19 + D3.js + Vite + TypeScript",
     ["RPG像素风UI", "力导向图渲染", "SVG迷雾动画", "多级缩放"], ACCENT_BLUE),
    ("后端服务层", "Python FastAPI + JWT + SQLModel",
     ["15+ API接口", "推荐引擎", "任务系统", "成就引擎"], ACCENT_PURPLE),
    ("图谱引擎层", "Neo4j + NetworkX + LangChain",
     ["4级知识建模", "路径规划", "Graph-RAG", "LLM讲解"], ACCENT_CYAN),
    ("数据持久层", "SQLite → PostgreSQL / Docker",
     ["用户&进度", "社交关系", "学习轨迹", "任务模板"], ACCENT_GREEN),
]

layer_h = Inches(1.05)
layer_gap = Inches(0.12)
start_y = Inches(1.9)

for i, (name, tech, features, color) in enumerate(layers):
    y = start_y + i * (layer_h + layer_gap)
    add_card(slide, Inches(0.8), y, Inches(11.7), layer_h)
    add_color_bar_left(slide, Inches(0.8), y, layer_h, color)
    add_textbox(slide, Inches(1.2), y + Inches(0.12), Inches(2.0), Inches(0.35),
                name, font_size=18, color=color, bold=True)
    add_textbox(slide, Inches(1.2), y + Inches(0.52), Inches(3.0), Inches(0.35),
                tech, font_size=11, color=TEXT_DIM)
    # Feature chips
    for j, feat in enumerate(features):
        fx = Inches(4.5) + j * Inches(2.0)
        chip = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                      fx, y + Inches(0.25), Inches(1.85), Inches(0.55))
        chip.fill.solid()
        chip.fill.fore_color.rgb = RGBColor(0x1A, 0x1E, 0x33)
        chip.line.color.rgb = BORDER_COLOR
        chip.line.width = Pt(0.8)
        chip.adjustments[0] = 0.1
        add_textbox(slide, fx + Inches(0.1), y + Inches(0.32), Inches(1.65), Inches(0.4),
                    feat, font_size=13, color=TEXT_LIGHT, alignment=PP_ALIGN.CENTER)

# 底部 — 技术亮点
add_textbox(slide, Inches(0.8), Inches(6.3), Inches(11.7), Inches(0.4),
            "技术亮点", font_size=16, color=TEXT_WHITE, bold=True)
highlights = [
    ("全栈自研", "非套壳，核心逻辑100%自己写"),
    ("图谱驱动", "推荐算法直接走图拓扑"),
    ("AI原生", "LLM不是附加功能，是核心引擎"),
]
for i, (k, v) in enumerate(highlights):
    x = Inches(0.8) + i * Inches(4.0)
    add_textbox(slide, x, Inches(6.7), Inches(1.2), Inches(0.3),
                k, font_size=13, color=ACCENT_GOLD, bold=True)
    add_textbox(slide, x + Inches(1.3), Inches(6.7), Inches(2.5), Inches(0.3),
                v, font_size=13, color=TEXT_LIGHT)

add_page_num(slide, 9)
add_speaker_notes(slide, """[演讲稿]
技术架构分四层——前端用 React + D3.js 渲染地图，后端 FastAPI 提供 15+ 接口，图谱层用 Neo4j 做知识建模，数据层 SQLite 存用户数据。

我想强调三个技术亮点：
1. 全栈自研——不是套 template，核心算法全部自己实现
2. 图谱驱动——推荐算法不是协同过滤，是直接在图结构上做拓扑计算
3. AI 原生——LLM 不是一个"问答机器人"，而是和知识图谱深度耦合的内容引擎""")


# ══════════════════════════════════════════════════════════════════
# SLIDE 10 — 竞品分析 (概念差异化)
# ══════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_section_header(slide, "竞争格局", "我们在「结构化 × 游戏化 × AI」交叉点上，独占蓝海", 10)

# 简化竞品对比 — 用象限图思路
add_textbox(slide, Inches(0.8), Inches(1.8), Inches(7), Inches(0.4),
            "核心差异化对比", font_size=18, color=TEXT_WHITE, bold=True)

# 竞品表格 (精简版)
headers = ["", "MOOC/B站", "Notion", "Anki", "Terranova"]
header_colors = [TEXT_DIM, TEXT_LIGHT, TEXT_LIGHT, TEXT_LIGHT, ACCENT_GOLD]
rows = [
    ("知识结构化", "✗", "△ 手动", "✗", "✓ 图谱"),
    ("学习路径", "固定", "✗", "✗", "✓ 智能"),
    ("跨课关联", "✗", "△ 手动", "✗", "✓ 自动"),
    ("游戏化", "✗", "✗", "基础", "✓ 完整RPG"),
    ("AI辅导", "✗", "✗", "✗", "✓ 原生"),
]

col_ws = [Inches(1.4), Inches(1.7), Inches(1.5), Inches(1.4), Inches(2.0)]
table_x = Inches(0.8)
table_y = Inches(2.4)
row_h = Inches(0.55)

# Headers
hx = table_x
for j, (h, hc) in enumerate(zip(headers, header_colors)):
    add_card(slide, hx, table_y, col_ws[j] - Inches(0.05), row_h,
             fill=RGBColor(0x1A, 0x1E, 0x38))
    add_textbox(slide, hx + Inches(0.08), table_y + Inches(0.08),
                col_ws[j] - Inches(0.2), row_h - Inches(0.1),
                h, font_size=12, color=hc, bold=True, alignment=PP_ALIGN.CENTER)
    hx += col_ws[j]

# Rows
for i, row in enumerate(rows):
    ry = table_y + (i + 1) * row_h
    rx = table_x
    for j, cell in enumerate(row):
        bg = BG_CARD if j < 4 else RGBColor(0x12, 0x1F, 0x12)
        clr = TEXT_LIGHT
        if cell.startswith("✗"):
            clr = RGBColor(0x66, 0x44, 0x44)
        elif cell.startswith("△"):
            clr = RGBColor(0x99, 0x88, 0x44)
        elif cell.startswith("✓"):
            clr = ACCENT_GREEN
        add_card(slide, rx, ry, col_ws[j] - Inches(0.05), row_h - Inches(0.03), fill=bg)
        add_textbox(slide, rx + Inches(0.05), ry + Inches(0.08),
                    col_ws[j] - Inches(0.15), row_h - Inches(0.1),
                    cell, font_size=12, color=clr, alignment=PP_ALIGN.CENTER,
                    bold=(j == 0 or j == 4))
        rx += col_ws[j]

# 右侧 — 竞争壁垒
right_x = Inches(8.5)
add_textbox(slide, right_x, Inches(1.8), Inches(4.5), Inches(0.4),
            "竞争壁垒", font_size=18, color=ACCENT_GOLD, bold=True)

barriers = [
    ("三合一集成", "知识图谱+游戏化+AI\n三者深度耦合，非简单叠加", ACCENT_GOLD),
    ("图谱数据资产", "随着用户增多，学习路径数据\n反哺推荐算法，形成数据飞轮", ACCENT_BLUE),
    ("网络效应", "社交、排行、组队\n用户越多体验越好", ACCENT_PURPLE),
    ("先发优势", "高校游戏化学习赛道\n几乎空白，抢占心智", ACCENT_GREEN),
]

for i, (title, desc, color) in enumerate(barriers):
    y = Inches(2.4) + i * Inches(1.2)
    add_card(slide, right_x, y, Inches(4.3), Inches(1.0))
    add_color_bar_left(slide, right_x, y, Inches(1.0), color)
    add_textbox(slide, right_x + Inches(0.3), y + Inches(0.1), Inches(3.5), Inches(0.3),
                title, font_size=15, color=color, bold=True)
    add_textbox(slide, right_x + Inches(0.3), y + Inches(0.42), Inches(3.7), Inches(0.5),
                desc.replace("\n", " "), font_size=12, color=TEXT_LIGHT)

add_page_num(slide, 10)
add_speaker_notes(slide, """[演讲稿]
看竞品对比——MOOC 只有线性视频，Notion 可以手动整理知识但没有推荐，Anki 只做记忆卡片。

没有任何一个产品同时做到了「知识结构化 + 游戏化 + AI」三合一。

我们的壁垒在哪？
1. 系统集成——三者深度耦合，不是简单叠加
2. 数据飞轮——用户越多，路径数据越丰富，推荐越准
3. 网络效应——社交、排行、组队让产品越用越有价值""")


# ══════════════════════════════════════════════════════════════════
# SLIDE 11 — 市场规模 (落地规划)
# ══════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_section_header(slide, "市场机会", "¥6000亿在线教育市场，游戏化学习赛道方兴未艾", 11)

# TAM/SAM/SOM circles
center_x = Inches(2.5)
center_y = Inches(2.0)
circles = [
    (Inches(4.8), "TAM", "¥6,000亿+", "中国在线教育", ACCENT_BLUE),
    (Inches(3.6), "SAM", "¥300亿", "高校学习工具", ACCENT_PURPLE),
    (Inches(2.2), "SOM", "¥30亿", "游戏化学习", ACCENT_GOLD),
]

for size, label, val, desc, color in circles:
    offset = (Inches(4.8) - size) / 2
    shape = slide.shapes.add_shape(MSO_SHAPE.OVAL,
                                   center_x + offset, center_y + offset, size, size)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.fill.fore_color.brightness = -0.65
    shape.line.color.rgb = color
    shape.line.width = Pt(2)

# Labels
add_textbox(slide, Inches(2.8), Inches(2.3), Inches(4), Inches(0.3),
            "TAM ¥6,000亿+  中国在线教育", font_size=13, color=ACCENT_BLUE)
add_textbox(slide, Inches(3.3), Inches(3.5), Inches(3), Inches(0.3),
            "SAM ¥300亿  高校工具", font_size=13, color=ACCENT_PURPLE)
add_textbox(slide, Inches(3.8), Inches(4.3), Inches(2.5), Inches(0.3),
            "SOM ¥30亿", font_size=14, color=ACCENT_GOLD, bold=True)

# 右侧 — 市场增长驱动力
right_x = Inches(8.0)
add_textbox(slide, right_x, Inches(1.8), Inches(5), Inches(0.4),
            "增长驱动力", font_size=18, color=TEXT_WHITE, bold=True)

drivers = [
    ("4,700万", "在校大学生（潜在用户池）", ACCENT_BLUE),
    ("25% CAGR", "在线教育年复合增长率", ACCENT_PURPLE),
    ("73%", "学生愿意为学习工具付费", ACCENT_GREEN),
    ("~0%", "游戏化学习在高校的渗透率", ACCENT_GOLD),
    ("政策利好", "教育数字化转型国家战略", ACCENT_CYAN),
]

for i, (val, desc, color) in enumerate(drivers):
    y = Inches(2.4) + i * Inches(1.0)
    add_card(slide, right_x, y, Inches(4.8), Inches(0.82))
    add_textbox(slide, right_x + Inches(0.25), y + Inches(0.12), Inches(1.8), Inches(0.35),
                val, font_size=22, color=color, bold=True)
    add_textbox(slide, right_x + Inches(2.1), y + Inches(0.22), Inches(2.4), Inches(0.35),
                desc, font_size=13, color=TEXT_LIGHT)

add_page_num(slide, 11)
add_speaker_notes(slide, """[演讲稿]
市场机会：中国在线教育市场超 6000 亿，其中高校学习工具赛道 300 亿。

但关键数据是——游戏化学习在高校的渗透率接近零！这是一片蓝海。

4700 万在校大学生就是我们的潜在用户池，73% 愿意付费。加上国家教育数字化转型的政策推动，时机非常好。""")


# ══════════════════════════════════════════════════════════════════
# SLIDE 12 — 商业模式 (落地规划)
# ══════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_section_header(slide, "商业模式", "Freemium → B2C 订阅 → B2B SaaS 三阶段变现", 12)

# B2C 定价
add_textbox(slide, Inches(0.8), Inches(1.8), Inches(5.5), Inches(0.4),
            "B2C 学生端", font_size=20, color=ACCENT_BLUE, bold=True)

tiers = [
    ("Free", "免费版", ["单专业基础地图", "每日3次AI问答", "基础任务系统"], "¥0", ACCENT_GREEN),
    ("Pro", "进阶版", ["全专业解锁", "无限AI辅导", "高级学习报告"], "¥19.9/月", ACCENT_BLUE),
    ("Team", "团队版", ["组队探索功能", "小组数据看板", "协作学习空间"], "¥39.9/月", ACCENT_PURPLE),
]

tier_w = Inches(1.9)
tier_gap = Inches(0.15)

for i, (badge, name, features, price, color) in enumerate(tiers):
    x = Inches(0.8) + i * (tier_w + tier_gap)
    y = Inches(2.3)
    add_card(slide, x, y, tier_w, Inches(3.5))
    # Badge
    badge_shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                         x + Inches(0.15), y + Inches(0.15), Inches(0.7), Inches(0.28))
    badge_shape.fill.solid()
    badge_shape.fill.fore_color.rgb = color
    badge_shape.line.fill.background()
    badge_shape.adjustments[0] = 0.15
    add_textbox(slide, x + Inches(0.15), y + Inches(0.16), Inches(0.7), Inches(0.25),
                badge, font_size=10, color=TEXT_WHITE, bold=True, alignment=PP_ALIGN.CENTER)
    # Name
    add_textbox(slide, x + Inches(0.15), y + Inches(0.55), tier_w - Inches(0.3), Inches(0.3),
                name, font_size=16, color=TEXT_WHITE, bold=True)
    # Features
    for j, feat in enumerate(features):
        add_textbox(slide, x + Inches(0.15), y + Inches(1.0) + j * Inches(0.42),
                    tier_w - Inches(0.3), Inches(0.35),
                    f"· {feat}", font_size=12, color=TEXT_LIGHT)
    # Price
    add_card(slide, x + Inches(0.15), y + Inches(2.9), tier_w - Inches(0.3), Inches(0.4),
             fill=RGBColor(0x1A, 0x1E, 0x33))
    add_textbox(slide, x + Inches(0.15), y + Inches(2.93), tier_w - Inches(0.3), Inches(0.35),
                price, font_size=15, color=color, bold=True, alignment=PP_ALIGN.CENTER)

# B2B
add_textbox(slide, Inches(6.8), Inches(1.8), Inches(6), Inches(0.4),
            "B2B 高校/机构端", font_size=20, color=ACCENT_GOLD, bold=True)

b2b = [
    ("高校教学辅助 SaaS", "¥5-10万/年/校",
     "定制课程图谱 · 学情分析看板 · 教学效果评估", ACCENT_GOLD),
    ("培训机构版", "按学员数定价",
     "课程地图化工具 · 学员进度管理 · 招生转化提升", ACCENT_ORANGE),
]

for i, (name, price, desc, color) in enumerate(b2b):
    y = Inches(2.3) + i * Inches(1.5)
    add_card(slide, Inches(6.8), y, Inches(5.8), Inches(1.3))
    add_color_bar_left(slide, Inches(6.8), y, Inches(1.3), color)
    add_textbox(slide, Inches(7.15), y + Inches(0.12), Inches(3.5), Inches(0.3),
                name, font_size=16, color=color, bold=True)
    add_textbox(slide, Inches(10.5), y + Inches(0.12), Inches(1.8), Inches(0.3),
                price, font_size=14, color=TEXT_WHITE, bold=True, alignment=PP_ALIGN.RIGHT)
    add_textbox(slide, Inches(7.15), y + Inches(0.55), Inches(5.1), Inches(0.6),
                desc, font_size=13, color=TEXT_LIGHT)

# 单位经济
add_textbox(slide, Inches(6.8), Inches(5.5), Inches(5.8), Inches(0.35),
            "单位经济模型 (B2C Pro)", font_size=15, color=TEXT_WHITE, bold=True)

metrics = [
    ("ARPU", "¥239/年"),
    ("CAC", "<¥30"),
    ("LTV", "~¥500"),
    ("LTV/CAC", ">16x"),
]

for i, (k, v) in enumerate(metrics):
    x = Inches(6.8) + i * Inches(1.5)
    add_card(slide, x, Inches(5.9), Inches(1.35), Inches(0.9))
    add_textbox(slide, x + Inches(0.1), Inches(5.95), Inches(1.15), Inches(0.3),
                k, font_size=11, color=TEXT_DIM, alignment=PP_ALIGN.CENTER)
    add_textbox(slide, x + Inches(0.1), Inches(6.3), Inches(1.15), Inches(0.35),
                v, font_size=16, color=ACCENT_GREEN, bold=True, alignment=PP_ALIGN.CENTER)

add_page_num(slide, 12)
add_speaker_notes(slide, """[演讲稿]
商业模式采用 Freemium 策略：

免费版提供基础地图和有限 AI 问答，让用户体验核心价值。Pro 版 19.9 元/月，解锁全部功能。团队版支持组队。

B2B 端面向高校——定制课程图谱、学情看板，每校每年 5-10 万。

关键指标：Pro 版年 ARPU 239 元，获客成本控制在 30 以内（校内裂变），LTV/CAC 超过 16 倍，经济模型非常健康。""")


# ══════════════════════════════════════════════════════════════════
# SLIDE 13 — 营销增长策略 (落地规划-营销方式)
# ══════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_section_header(slide, "营销增长策略", "校内裂变 + 内容获客 + 高校合作，三引擎驱动", 13)

# 三大增长引擎
engines = [
    ("引擎一：校内裂变", ACCENT_BLUE,
     [("组队邀请机制", "邀请好友组队探索\n奖励双方 Pro 体验周"),
      ("排行榜传播", "周榜/月榜可一键\n分享到朋友圈/校园群"),
      ("寝室渗透策略", "一人开通团队版\n室友自动获得邀请码")]),
    ("引擎二：内容获客", ACCENT_PURPLE,
     [("知识地图海报", "为各专业生成探索率\n地图长图，社媒传播"),
      ("「学长路线图」", "毕业学长分享自己的\n探索路径引发讨论"),
      ("短视频种草", "地图探索的酷炫动画\n在抖音/B站天然吸睛")]),
    ("引擎三：高校合作", ACCENT_GOLD,
     [("教师合作试点", "与课程教师合作\n将图谱嵌入课程辅助"),
      ("学生社团联动", "与学习型社团合作\n组织探索挑战赛"),
      ("创业大赛背书", "通过比赛获得\n校方认可与资源支持")]),
]

eng_w = Inches(3.8)
eng_gap = Inches(0.2)

for i, (title, color, items) in enumerate(engines):
    x = Inches(0.6) + i * (eng_w + eng_gap)
    y = Inches(1.8)
    # Title
    add_textbox(slide, x, y, eng_w, Inches(0.4),
                title, font_size=17, color=color, bold=True)
    # Items
    for j, (name, desc) in enumerate(items):
        cy = y + Inches(0.6) + j * Inches(1.5)
        add_card(slide, x, cy, eng_w, Inches(1.3))
        add_color_bar_left(slide, x, cy, Inches(1.3), color)
        add_textbox(slide, x + Inches(0.3), cy + Inches(0.12), eng_w - Inches(0.5), Inches(0.3),
                    name, font_size=14, color=TEXT_WHITE, bold=True)
        add_textbox(slide, x + Inches(0.3), cy + Inches(0.48), eng_w - Inches(0.5), Inches(0.7),
                    desc.replace("\n", " "), font_size=12, color=TEXT_LIGHT)

# 增长目标
add_card(slide, Inches(0.6), Inches(6.5), Inches(12.1), Inches(0.6),
         fill=RGBColor(0x0A, 0x0E, 0x1A))
add_textbox(slide, Inches(0.8), Inches(6.55), Inches(11.7), Inches(0.4),
            "增长目标：6 个月内 → 校内 200 人测试  ·  12 个月 → 2,000 用户  ·  18 个月 → 破万 + 3 所高校合作",
            font_size=14, color=ACCENT_GOLD, alignment=PP_ALIGN.CENTER)

add_page_num(slide, 13)
add_speaker_notes(slide, """[演讲稿]
我们的增长不靠烧钱投放，而是三个自然引擎：

第一，校内裂变——组队探索机制天然带来邀请行为。一个人开通团队版，整个寝室都会收到邀请。

第二，内容获客——我们可以为每个专业自动生成「知识大陆地图海报」，这种视觉内容在社交媒体上天然有传播力。地图动画在短视频平台也很吸睛。

第三，高校合作——和教师合作试点，让图谱变成课程辅助工具，这是最有壁垒的获客渠道。

[数据] 目标：6 个月 200 人测试 → 12 个月 2000 用户 → 18 个月破万。""")


# ══════════════════════════════════════════════════════════════════
# SLIDE 14 — 发展路线图 (落地规划)
# ══════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_section_header(slide, "发展路线图", "4 阶段，18 个月完成从 0 到 PMF 验证", 14)

phases = [
    ("Phase 1", "2026 Q1-Q2", "MVP 打磨",
     ["CS专业完整图谱 ✓", "核心迷雾机制 ✓", "校内200人测试", "收集反馈迭代"],
     ACCENT_BLUE, True),
    ("Phase 2", "2026 Q3-Q4", "产品验证",
     ["接入LLM智能辅导", "Neo4j迁移", "扩展3个专业", "2,000活跃用户"],
     ACCENT_PURPLE, False),
    ("Phase 3", "2027 Q1-Q2", "商业化",
     ["B2C付费上线", "B2B高校试点", "覆盖10+专业", "用户破万"],
     ACCENT_CYAN, False),
    ("Phase 4", "2027 Q3+", "规模扩展",
     ["多校推广", "培训机构版", "跨校社交网络", "寻求Pre-A轮"],
     ACCENT_GOLD, False),
]

# Timeline
timeline_y = Inches(3.3)
shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                               Inches(0.8), timeline_y, Inches(11.7), Inches(0.03))
shape.fill.solid()
shape.fill.fore_color.rgb = BORDER_COLOR
shape.line.fill.background()

phase_w = Inches(2.7)
phase_gap = Inches(0.22)
start_x = Inches(0.8)

for i, (label, time, title, items, color, current) in enumerate(phases):
    x = start_x + i * (phase_w + phase_gap)
    # Dot
    dot_size = Inches(0.32) if current else Inches(0.24)
    dot_offset = (Inches(0.32) - dot_size) / 2
    dot = slide.shapes.add_shape(MSO_SHAPE.OVAL,
                                 x + phase_w / 2 - dot_size / 2,
                                 timeline_y - dot_size / 2,
                                 dot_size, dot_size)
    dot.fill.solid()
    dot.fill.fore_color.rgb = color
    dot.line.fill.background()

    # Labels above
    add_textbox(slide, x, Inches(2.1), phase_w, Inches(0.3),
                f"{label}  ·  {time}", font_size=12, color=color, bold=True,
                alignment=PP_ALIGN.CENTER)
    add_textbox(slide, x, Inches(2.5), phase_w, Inches(0.35),
                title, font_size=18, color=TEXT_WHITE, bold=True,
                alignment=PP_ALIGN.CENTER)

    # Current badge
    if current:
        bw = Inches(1.0)
        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                       x + (phase_w - bw) / 2, Inches(2.85), bw, Inches(0.25))
        badge.fill.solid()
        badge.fill.fore_color.rgb = color
        badge.line.fill.background()
        badge.adjustments[0] = 0.15
        add_textbox(slide, x + (phase_w - bw) / 2, Inches(2.86), bw, Inches(0.22),
                    "当前", font_size=9, color=TEXT_WHITE, bold=True,
                    alignment=PP_ALIGN.CENTER)

    # Card below
    card_y = Inches(3.7)
    add_card(slide, x, card_y, phase_w, Inches(2.6))
    for j, item in enumerate(items):
        clr = ACCENT_GREEN if "✓" in item else TEXT_LIGHT
        add_textbox(slide, x + Inches(0.2), card_y + Inches(0.2) + j * Inches(0.52),
                    phase_w - Inches(0.4), Inches(0.4),
                    f"· {item}", font_size=13, color=clr)

# Key milestone
add_card(slide, Inches(0.8), Inches(6.5), Inches(11.7), Inches(0.55),
         fill=RGBColor(0x0A, 0x0E, 0x1A))
add_textbox(slide, Inches(1.0), Inches(6.55), Inches(11.3), Inches(0.35),
            "关键里程碑：Phase 2 结束时验证 PMF（月留存 > 40%，NPS > 50）→ 启动商业化",
            font_size=14, color=ACCENT_GOLD, alignment=PP_ALIGN.CENTER)

add_page_num(slide, 14)
add_speaker_notes(slide, """[演讲稿]
我们的路线图分 4 个阶段：

Phase 1 我们已经在这里了——MVP 完成，计算机科学图谱已建好，核心功能可运行。下一步是校内 200 人测试。

Phase 2 是产品验证——接入 LLM、扩展专业、冲到 2000 用户。

Phase 3 商业化——付费上线 + 高校合作。

Phase 4 规模扩展——多校推广，寻求 Pre-A。

关键判断标准：Phase 2 结束时月留存超过 40%、NPS 超过 50，就证明产品 market fit，启动商业化。""")


# ══════════════════════════════════════════════════════════════════
# SLIDE 15 — 团队介绍
# ══════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_section_header(slide, "团队", "一支有技术深度和产品热情的学生创业团队", 15)

members = [
    ("CEO / 产品", "产品定义\n商业策略\n用户研究", ACCENT_GOLD, "C"),
    ("CTO / 全栈", "系统架构\n图谱算法\nAI 集成", ACCENT_BLUE, "T"),
    ("设计 / UX", "RPG 视觉\n交互设计\n游戏化体验", ACCENT_PURPLE, "D"),
    ("运营 / 增长", "校园推广\n社群运营\n高校合作", ACCENT_GREEN, "O"),
]

member_w = Inches(2.7)
member_gap = Inches(0.2)
start_x = Inches(0.75)

for i, (role, skills, color, icon) in enumerate(members):
    x = start_x + i * (member_w + member_gap)
    y = Inches(2.0)
    add_card(slide, x, y, member_w, Inches(3.8))
    # Avatar
    add_circle_icon(slide, x + (member_w - Inches(0.9)) / 2, y + Inches(0.3),
                    Inches(0.9), color, icon, 26)
    # Role
    add_textbox(slide, x + Inches(0.15), y + Inches(1.45), member_w - Inches(0.3), Inches(0.35),
                role, font_size=15, color=color, bold=True, alignment=PP_ALIGN.CENTER)
    # Name placeholder
    add_textbox(slide, x + Inches(0.15), y + Inches(1.85), member_w - Inches(0.3), Inches(0.3),
                "[姓名]", font_size=14, color=TEXT_WHITE, alignment=PP_ALIGN.CENTER)
    # Skills
    add_multiline(slide, x + Inches(0.15), y + Inches(2.4), member_w - Inches(0.3), Inches(1.2),
                  skills.split("\n"), font_size=13, color=TEXT_LIGHT,
                  alignment=PP_ALIGN.CENTER, line_spacing=1.6)

# 团队优势
right_x = Inches(11.6)
add_textbox(slide, Inches(0.8), Inches(6.1), Inches(12.0), Inches(0.35),
            "团队优势", font_size=15, color=TEXT_WHITE, bold=True)
advantages = "全栈技术能力 ·  用户即开发者（我们本身就是目标用户） ·  已完成 MVP 证明执行力  ·  对教育行业有热情"
add_textbox(slide, Inches(0.8), Inches(6.45), Inches(12.0), Inches(0.35),
            advantages, font_size=13, color=TEXT_LIGHT)

add_textbox(slide, Inches(0.8), Inches(7.0), Inches(12.0), Inches(0.3),
            "（请填入团队成员真实姓名、专业、核心经历）",
            font_size=12, color=TEXT_DIM, alignment=PP_ALIGN.CENTER)

add_page_num(slide, 15)
add_speaker_notes(slide, """[演讲稿]
我们是一支 4 人团队——[介绍各成员]。

我想特别强调的是：我们团队本身就是目标用户。我们自己就是大学生，我们自己就经历过这些痛点。所以我们不是在猜测用户需要什么，而是在解决自己的问题。

另外，MVP 已经跑通——这证明我们的执行力。不是 PPT 创业，是产品已经能用了。""")


# ══════════════════════════════════════════════════════════════════
# SLIDE 16 — 融资需求 + 结尾 (CTA)
# ══════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_top_bar(slide, ACCENT_GOLD)

# Ask
add_textbox(slide, Inches(0.8), Inches(0.7), Inches(11.5), Inches(0.6),
            "我们的请求", font_size=32, color=ACCENT_GOLD, bold=True,
            alignment=PP_ALIGN.CENTER)

add_textbox(slide, Inches(2), Inches(1.5), Inches(9), Inches(0.7),
            "种子轮  ¥100 万", font_size=48, color=TEXT_WHITE, bold=True,
            alignment=PP_ALIGN.CENTER, font_name="Helvetica Neue")

add_textbox(slide, Inches(2), Inches(2.3), Inches(9), Inches(0.4),
            "出让 10% 股权  ·  估值 ¥1,000 万", font_size=18, color=TEXT_DIM,
            alignment=PP_ALIGN.CENTER)

# 资金用途
add_textbox(slide, Inches(0.8), Inches(3.1), Inches(11.5), Inches(0.4),
            "资金用途", font_size=18, color=TEXT_WHITE, bold=True,
            alignment=PP_ALIGN.CENTER)

uses = [
    ("40%", "产品研发", "LLM接入 · 图谱扩展\n性能优化 · 新功能", ACCENT_BLUE),
    ("25%", "运营推广", "校园推广 · 社群运营\n内容制作 · 活动", ACCENT_PURPLE),
    ("20%", "基础设施", "云服务 · LLM API\n图数据库 · CDN", ACCENT_CYAN),
    ("15%", "团队建设", "核心招聘 · 培训\n差旅 · 办公", ACCENT_GREEN),
]

use_w = Inches(2.7)
use_gap = Inches(0.2)
start_x = Inches(0.8)

for i, (pct, name, desc, color) in enumerate(uses):
    x = start_x + i * (use_w + use_gap)
    y = Inches(3.6)
    add_card(slide, x, y, use_w, Inches(1.7))
    add_textbox(slide, x + Inches(0.2), y + Inches(0.1), use_w - Inches(0.4), Inches(0.5),
                pct, font_size=34, color=color, bold=True, alignment=PP_ALIGN.CENTER)
    add_textbox(slide, x + Inches(0.2), y + Inches(0.6), use_w - Inches(0.4), Inches(0.3),
                name, font_size=15, color=TEXT_WHITE, bold=True, alignment=PP_ALIGN.CENTER)
    add_multiline(slide, x + Inches(0.2), y + Inches(1.0), use_w - Inches(0.4), Inches(0.6),
                  desc.split("\n"), font_size=12, color=TEXT_LIGHT,
                  alignment=PP_ALIGN.CENTER, line_spacing=1.4)

# 结尾金句
shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                               Inches(1.5), Inches(5.7), Inches(10.3), Inches(0.02))
shape.fill.solid()
shape.fill.fore_color.rgb = ACCENT_GOLD
shape.line.fill.background()

add_textbox(slide, Inches(1.0), Inches(5.9), Inches(11.3), Inches(0.6),
            "「 让每一位学生都拥有自己的知识大陆 」",
            font_size=26, color=ACCENT_GOLD, bold=True, alignment=PP_ALIGN.CENTER)

add_textbox(slide, Inches(1.0), Inches(6.6), Inches(11.3), Inches(0.5),
            "TERRANOVA  ·  新大陆",
            font_size=20, color=TEXT_WHITE, alignment=PP_ALIGN.CENTER,
            font_name="Helvetica Neue")

add_textbox(slide, Inches(1.0), Inches(7.0), Inches(11.3), Inches(0.3),
            "联系方式：[请填写邮箱/微信]",
            font_size=13, color=TEXT_DIM, alignment=PP_ALIGN.CENTER)

add_page_num(slide, 16)
add_speaker_notes(slide, """[演讲稿]
最后，我们的请求：种子轮 100 万，出让 10%。

这笔钱 40% 用于产品研发——主要是 LLM 接入和图谱扩展；25% 校园推广；20% 基础设施；15% 团队建设。

[总结] 我们相信，大学的知识体系不应该是一张平铺的课表，而应该是一片等待探索的大陆。我们已经把它做出来了，现在需要你们的支持把它推向更多学生。

[结束] Terranova，新大陆——让每一位学生都拥有自己的知识大陆。谢谢！

[Q&A准备]
- 如何保证图谱质量？→ 与教师合作 + 用户反馈迭代
- 如何防止游戏化喧宾夺主？→ 核心奖励只来自学习行为
- 凭什么学生会坚持用？→ 社交绑定 + 进度可视化沉没成本
- LLM 成本怎么控制？→ 图谱缓存 + 按需生成 + 批量预处理""")


# ── Save ──
out_path = "/Users/minimax/Desktop/Projects/terranova/Terranova_Pitch_Deck.pptx"
prs.save(out_path)
print(f"✓ Saved: {out_path}")
print(f"  Total slides: {len(prs.slides)}")
