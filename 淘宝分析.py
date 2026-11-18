# 淘宝用户行为数据分析报告
# 分析目标：使用 pandas 处理数据，分析转化漏斗与星期活跃规律。
# 技术栈：Python, pandas, matplotlib

import pandas as pd
import matplotlib.pyplot as plt

# 解决画图中文显示问题
plt.rcParams['font.sans-serif'] = ['simHei']
plt.rcParams['axes.unicode_minus'] = False

print("开始加载数据...")
# 一、 数据导入与清洗
df = pd.read_csv('D:/玩/淘宝/UserBehavior.csv', nrows=10000, names=['用户id', '商品id', '品类', '行为类型', '时间戳'])
df['行为时间'] = pd.to_datetime(df['时间戳'], unit='s')
df['星期几'] = df['行为时间'].dt.day_name()

print("数据清洗完成，开始分析...")
# 二、 业务发现：按星期几统计浏览人数
pv_data = df[df['行为类型'] == 'pv']
weekday_traffic = pv_data.groupby('星期几')['用户id'].nunique()

# 将英文替换为中文，并固定排序
week_map = {'Monday': '周一', 'Tuesday': '周二', 'Wednesday': '周三',
            'Thursday': '周四', 'Friday': '周五', 'Saturday': '周六', 'Sunday': '周日'}
weekday_traffic.index = weekday_traffic.index.map(week_map)
week_order = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
weekday_traffic = weekday_traffic.reindex(week_order)
print("开始生成图表...")

# 三、 数据可视化
x = weekday_traffic.index.tolist()
y = weekday_traffic.values.tolist()
plt.figure(figsize=(10, 5))
plt.bar(x, y, width=(0.5), color='skyblue')
plt.title('淘宝用户每周浏览活跃人数分布', fontsize=16)
plt.xlabel('星期', fontsize=12)
plt.ylabel('用户活跃数', fontsize=12)
plt.grid(linestyle='--', alpha=0.5)

# 在柱子上显示数字
for a, b in zip(weekday_traffic.index, weekday_traffic.values):
    plt.text(a, b + 1, str(b), ha='center', va='bottom', fontsize=10)



# 保存图片到本地
plt.savefig('D:/玩/淘宝/weekday_traffic_chart.png')
print("图表已保存为图片！")