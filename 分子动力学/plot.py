# 导入所需的模块
import MDAnalysis as mda # 用于读取和分析分子动力学轨迹
import matplotlib.pyplot as plt # 用于绘图
import numpy as np # 用于数值计算

# 读取轨迹文件和拓扑文件
u = mda.Universe("topology.pdb", "trajectory.dcd")

# 选择要绘制的原子
protein = u.select_atoms("protein") # 选择蛋白质原子
water = u.select_atoms("resname SOL") # 选择水分子原子

# 创建一个空的画布
fig = plt.figure(figsize=(10,10))

# 循环遍历轨迹的每一帧
for ts in u.trajectory:
    # 清空画布
    fig.clf()
    # 创建一个3D的子图
    ax = fig.add_subplot(111, projection="3d")
    # 设置标题为当前帧数
    ax.set_title(f"Frame {ts.frame}")
    # 设置坐标轴的范围和标签
    ax.set_xlim(-50, 50)
    ax.set_ylim(-50, 50)
    ax.set_zlim(-50, 50)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    # 绘制蛋白质原子的散点图，颜色为蓝色，大小为5
    ax.scatter(protein.positions[:,0], protein.positions[:,1], protein.positions[:,2], c="b", s=5)
    # 绘制水分子原子的散点图，颜色为红色，大小为2
    ax.scatter(water.positions[:,0], water.positions[:,1], water.positions[:,2], c="r", s=2)
    # 保存当前帧的图片，文件名为frame_帧数.png，分辨率为300 dpi
    plt.savefig(f"frame_{ts.frame}.png", dpi=300)
