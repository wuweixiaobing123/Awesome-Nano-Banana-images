import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager

# 中文字体
fp = '/usr/share/fonts/opentype/noto-cjk-otf/NotoSerifCJKsc-Regular.otf'
font_manager.fontManager.addfont(fp)
plt.rcParams['font.family'] = 'Noto Serif CJK SC'
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(6, 1.1), dpi=300)
ax.set_xlim(-5.5, 5.5)
ax.set_ylim(-1, 1)
ax.axhline(0, color='k', lw=1.2)
ax.annotate('', xy=(5.3, 0), xytext=(-5.3, 0),
            arrowprops=dict(arrowstyle='->', color='k', lw=1.2))
for i in range(-5, 6):
    ax.plot([i, i], [-0.12, 0.12], color='k', lw=1)
    ax.text(i, -0.42, str(i), ha='center', va='top', fontsize=9)
ax.set_axis_off()
plt.tight_layout(pad=0.1)
plt.savefig('figs/test.png', bbox_inches='tight', facecolor='w')
print('saved')
