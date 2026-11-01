"""生成五套试卷需要的所有插图（300 dpi，纯黑线条，宋体中文）。"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Rectangle, FancyArrowPatch
import calendar, datetime

fp = '/usr/share/fonts/opentype/noto-cjk-otf/NotoSerifCJKsc-Regular.otf'
font_manager.fontManager.addfont(fp)
plt.rcParams['font.family'] = 'Noto Serif CJK SC'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['mathtext.fontset'] = 'cm'

OUT = 'figs/'


def save(fig, name):
    fig.savefig(OUT + name, bbox_inches='tight', facecolor='w', dpi=300)
    plt.close(fig)
    print('saved', name)


def numline(name, xmin, xmax, points, figw=7.4, ylim=(-1.0, 1.0), tick_step=1):
    """points: dict label -> x"""
    fig, ax = plt.subplots(figsize=(figw, 1.35))
    ax.set_xlim(xmin - 0.35, xmax + 0.55)
    ax.set_ylim(*ylim)
    ax.annotate('', xy=(xmax + 0.45, 0), xytext=(xmin - 0.3, 0),
                arrowprops=dict(arrowstyle='->', color='k', lw=1.1, shrinkA=0, shrinkB=0))
    for i in range(int(xmin), int(xmax) + 1, tick_step):
        ax.plot([i, i], [-0.13, 0.13], color='k', lw=1.0)
        ax.text(i, -0.36, str(i), ha='center', va='top', fontsize=9)
    for lab, x in points.items():
        ax.plot([x], [0], 'ko', ms=4.5)
        ax.text(x, 0.3, lab, ha='center', va='bottom', fontsize=10.5)
    ax.set_axis_off()
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    save(fig, name)


def squares_row(name, stages, rows=1, cell=0.55, name_labels=None, figw=None):
    """把若干个小正方形按每 stage 的布局画出来。stages: list of (cols,rows) or list of list of (c,r)"""
    # stages: list of dict {(col,row)} sets
    figw = figw or (0.9 + 0.85 * len(stages) * 4)
    fig, ax = plt.subplots(figsize=(figw, 2.1))
    xoff = 0
    for k, cells in enumerate(stages):
        for (c, r) in cells:
            ax.add_patch(Rectangle((xoff + c, r), 1, 1, fill=False, lw=1.0, ec='k'))
        ax.text(xoff + max(c for c, r in cells) / 2 + 0.5, -0.28, name_labels[k] if name_labels else f'第{k+1}个',
                ha='center', va='top', fontsize=9)
        xoff += max(c for c, r in cells) + 2.4
    ax.set_xlim(-0.3, xoff - 0.8)
    ax.set_ylim(-0.9, max(r for cells in stages for c, r in cells) + 1.2)
    ax.set_aspect('equal')
    ax.set_axis_off()
    save(fig, name)


def step_squares(name):
    """第n个图形 = 3行×n个 + 右下1个 => 3n+1"""
    stages = []
    for n in (1, 2, 3):
        cells = [(c, r) for r in range(3) for c in range(n)]
        cells.append((n, 0))
        stages.append(set(cells))
    squares_row(name, stages, figw=4.45)


def match_triangles(name):
    """火柴棒搭三角形连排（相邻共用一条边）：3,5,7 根"""
    import numpy as np
    h = np.sqrt(3) / 2
    fig, ax = plt.subplots(figsize=(4.75, 1.35))
    xoff = 0
    for k, n in enumerate((1, 2, 3)):
        for i in range(n):
            if i % 2 == 0:
                j = i // 2
                pts = [(xoff + j, 0), (xoff + j + 1, 0), (xoff + j + 0.5, h)]
            else:
                j = (i - 1) // 2
                pts = [(xoff + j + 0.5, h), (xoff + j + 1.5, h), (xoff + j + 1, 0)]
            ax.add_patch(plt.Polygon(pts, closed=True, fill=False, lw=1.5, ec='k'))
        ax.text(xoff + n / 2, -0.14, f'第{k+1}个', ha='center', va='top', fontsize=9)
        xoff += n + 1.6
    ax.set_xlim(-0.3, xoff - 0.9)
    ax.set_ylim(-0.55, 1.05)
    ax.set_aspect('equal')
    ax.set_axis_off()
    save(fig, name)


def match_hexagons(name):
    """火柴棒搭正六边形连排（相邻共用一条边）：6,11,16 根"""
    import numpy as np
    dx = 2 * 0.5 * np.cos(np.pi / 6)  # 相邻六边形中心距（共用竖边）
    fig, ax = plt.subplots(figsize=(4.75, 1.35))
    xoff = 0
    for k, n in enumerate((1, 2, 3)):
        for i in range(n):
            cx = xoff + i * dx
            pts = [(cx + 0.5 * np.cos(np.pi / 2 + j * np.pi / 3),
                    0.5 * np.sin(np.pi / 2 + j * np.pi / 3) + 0.5) for j in range(6)]
            pts.append(pts[0])
            xs, ys = zip(*pts)
            ax.plot(xs, ys, color='k', lw=1.6)
        ax.text(xoff + (n - 1) * dx / 2, -0.18, f'第{k+1}个', ha='center', va='top', fontsize=9)
        xoff += (n - 1) * dx + 2.0
    ax.set_xlim(-0.6, xoff - 0.7)
    ax.set_ylim(-0.6, 1.35)
    ax.set_aspect('equal')
    ax.set_axis_off()
    save(fig, name)


def calendar_img(name, year, month):
    cal = calendar.Calendar(firstweekday=6)  # 周日开头
    weeks = cal.monthdayscalendar(year, month)
    fig, ax = plt.subplots(figsize=(2.85, 0.34 * (len(weeks) + 1) + 0.22))
    ncol = 7
    head = ['日', '一', '二', '三', '四', '五', '六']
    for j, h in enumerate(head):
        ax.text(j + 0.5, -0.5, h, ha='center', va='center', fontsize=10)
    for i, wk in enumerate(weeks):
        for j, d in enumerate(wk):
            if d == 0:
                continue
            ax.text(j + 0.5, i + 0.5, str(d), ha='center', va='center', fontsize=9.5)
    ax.set_xlim(0, ncol)
    ax.set_ylim(len(weeks), -1)
    ax.set_aspect('equal')
    ax.set_xticks(range(ncol + 1))
    ax.set_yticks(list(range(len(weeks) + 1)) + [-1])
    ax.grid(True, color='k', lw=0.8)
    ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
    for s in ax.spines.values():
        s.set_visible(False)
    save(fig, name)


def rect_cut_square(name):
    """长方形 a×b，左上角剪去边长 c 的正方形"""
    fig, ax = plt.subplots(figsize=(2.75, 1.85))
    a, b, c = 5.0, 3.0, 1.2
    # 剩余部分（左上角剪去边长 c 的正方形）
    pts = [(0, 0), (a, 0), (a, b), (c, b), (c, b - c), (0, b - c)]
    ax.add_patch(plt.Polygon(pts, closed=True, fill=False, lw=1.2, ec='k'))
    # 被剪去的正方形（虚线示意）
    ax.add_patch(Rectangle((0, b - c), c, c, fill=True, fc='#f4f4f4', ec='k', lw=0.9, ls='--'))
    ax.text(a / 2, -0.25, '$a$', ha='center', va='top', fontsize=11)
    ax.text(-0.28, b / 2, '$b$', ha='right', va='center', fontsize=11, rotation=90)
    ax.annotate('$c$', xy=(c / 2, b - c / 2), ha='center', va='center', fontsize=10)
    ax.set_xlim(-0.6, a + 0.35)
    ax.set_ylim(-0.6, b + 0.35)
    ax.set_aspect('equal')
    ax.set_axis_off()
    save(fig, name)


def triangle_dots(name):
    """三角形点阵：第n个有 n(n+1)/2 个点"""
    fig, ax = plt.subplots(figsize=(4.35, 1.55))
    xoff = 0
    for k, n in enumerate((1, 2, 3)):
        for r in range(n):
            for c in range(r + 1):
                ax.plot([xoff + (c - r / 2) * 0.55], [-r * 0.48], 'ko', ms=5.5)
        ax.text(xoff, -1.45, f'第{k+1}个', ha='center', va='top', fontsize=10.5)
        xoff += 3.0
    ax.set_xlim(-1.0, xoff - 1.2)
    ax.set_ylim(-2.0, 0.5)
    ax.set_aspect('equal')
    ax.set_axis_off()
    save(fig, name)


def ring_dots(name):
    """正方形边框点阵：第n个有 4n 个点"""
    fig, ax = plt.subplots(figsize=(4.35, 1.35))
    xoff = 0
    for k, n in enumerate((1, 2, 3)):
        m = n + 1  # 每边 m 个点，共 4m-4 = 4n 个
        for i in range(m):
            for j in range(m):
                if i in (0, m - 1) or j in (0, m - 1):
                    ax.plot([xoff + i * 0.48], [j * 0.48], 'ko', ms=5.0)
        ax.text(xoff + (m - 1) * 0.24, -0.35, f'第{k+1}个', ha='center', va='top', fontsize=10.5)
        xoff += 4.6
    ax.set_xlim(-0.4, xoff - 0.6)
    ax.set_ylim(-0.8, 1.9)
    ax.set_aspect('equal')
    ax.set_axis_off()
    save(fig, name)


def two_squares(name):
    """两个正方形（边长 a、b）拼合，求组合图形周长"""
    fig, ax = plt.subplots(figsize=(2.75, 1.75))
    a, b = 3.2, 1.6
    ax.add_patch(Rectangle((0, 0), a, a, fill=False, lw=1.1, ec='k'))
    ax.add_patch(Rectangle((a, 0), b, b, fill=False, lw=1.1, ec='k'))
    ax.text(a / 2, a + 0.2, '$a$', ha='center', va='bottom', fontsize=11)
    ax.text(a + b / 2, -0.22, '$b$', ha='center', va='top', fontsize=11)
    ax.set_xlim(-0.45, a + b + 0.6)
    ax.set_ylim(-0.6, a + 0.7)
    ax.set_aspect('equal')
    ax.set_axis_off()
    save(fig, name)


def row_squares(name):
    """一排小正方形：1、2、3 个，用于周长规律"""
    fig, ax = plt.subplots(figsize=(3.95, 1.1))
    xoff = 0
    for k, n in enumerate((1, 2, 3)):
        for i in range(n):
            ax.add_patch(Rectangle((xoff + i * 0.6, 0), 0.6, 0.6, fill=False, lw=1.0, ec='k'))
        ax.text(xoff + (n - 1) * 0.3 + 0.3, -0.16, f'第{k+1}个', ha='center', va='top', fontsize=9)
        xoff += n * 0.6 + 1.9
    ax.set_xlim(-0.2, xoff - 1.1)
    ax.set_ylim(-0.6, 0.85)
    ax.set_aspect('equal')
    ax.set_axis_off()
    save(fig, name)


def plain_rect(name):
    """长 a、宽 b 的长方形（用于周长、面积代数式）"""
    fig, ax = plt.subplots(figsize=(2.35, 1.4))
    a, b = 4.6, 2.6
    ax.add_patch(Rectangle((0, 0), a, b, fill=False, lw=1.1, ec='k'))
    ax.text(a / 2, -0.24, '$a$', ha='center', va='top', fontsize=11)
    ax.text(-0.26, b / 2, '$b$', ha='right', va='center', fontsize=11, rotation=90)
    ax.set_xlim(-0.6, a + 0.3)
    ax.set_ylim(-0.65, b + 0.35)
    ax.set_aspect('equal')
    ax.set_axis_off()
    save(fig, name)


def quad_sides(name):
    """四边形，四边标注代数式"""
    fig, ax = plt.subplots(figsize=(2.55, 1.9))
    pts = [(0, 0), (4.6, 0), (3.5, 2.3), (0.6, 2.0)]
    poly = plt.Polygon(pts, closed=True, fill=False, lw=1.1, ec='k')
    ax.add_patch(poly)
    ax.text(2.3, -0.28, '$2a+b$', ha='center', va='top', fontsize=10)
    ax.text(3.52, 2.55, '$3a-b$', ha='center', va='bottom', fontsize=10)
    ax.text(2.05, 2.32, '$a+2b$', ha='center', va='bottom', fontsize=10)
    ax.text(-0.22, 1.0, '$a-b$', ha='right', va='center', fontsize=10, rotation=90)
    ax.set_xlim(-0.9, 4.9)
    ax.set_ylim(-0.75, 2.95)
    ax.set_aspect('equal')
    ax.set_axis_off()
    save(fig, name)


def number_array(name):
    """自然数数阵：1 / 2 3 / 4 5 6 / 7 8 9 10"""
    fig, ax = plt.subplots(figsize=(1.95, 1.35))
    rows = [[1], [2, 3], [4, 5, 6], [7, 8, 9, 10]]
    for i, r in enumerate(rows):
        for j, v in enumerate(r):
            ax.text(j + (4 - len(r)) / 2, -i * 0.42, str(v), ha='center', va='center', fontsize=10)
    ax.set_xlim(-0.55, 3.55)
    ax.set_ylim(-1.6, 0.5)
    ax.set_aspect('equal')
    ax.set_axis_off()
    save(fig, name)


if __name__ == '__main__':
    # 卷1
    numline('j1_axis.png', -6, 4, {'A': -2.5, 'B': -1, 'C': 2}, figw=4.35)
    step_squares('j1_step.png')
    calendar_img('j1_cal.png', 2026, 11)
    # 卷2
    match_triangles('j2_tri.png')
    numline('j2_axis.png', -3, 5, {'A': -3, 'B': 5}, figw=4.3)
    plain_rect('j2_rect.png')
    number_array('j2_array.png')
    # 卷3
    numline('j3_axis.png', -3, 4, {'A': -3, 'B': 1, 'C': 4}, figw=4.3)
    rect_cut_square('j3_rect.png')
    triangle_dots('j3_dots.png')
    # 卷4
    numline('j4_axis1.png', -2, 3, {'$a$': -2, '$b$': 3}, figw=4.0)
    numline('j4_axis2.png', -1, 5, {'$a$': -1, '$b$': 2, '$c$': 5}, figw=4.25)
    ring_dots('j4_ring.png')
    row_squares('j4_row.png')
    two_squares('j4_two.png')
    # 卷5
    numline('j5_axis1.png', -2, 5, {'$a$': -2, '$b$': 5}, figw=4.0)
    numline('j5_axis2.png', -4, 1, {'$a$': -4, '$b$': 1}, figw=3.9)
    match_hexagons('j5_hex.png')
    quad_sides('j5_quad.png')
