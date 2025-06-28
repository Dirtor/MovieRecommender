# 🎬 智能电影推荐系统

基于机器学习的个性化电影推荐应用，使用协同过滤算法为用户推荐电影。

## 🚀 在线演示

[点击这里体验在线版本](您的Streamlit应用链接)

## 📁 项目结构

```
MovieRecommender/
├── app.py              # 主应用文件
├── requirements.txt    # Python依赖
├── data/              # 数据文件夹
│   ├── ratings.csv    # 用户评分数据
│   └── movies.csv     # 电影信息数据
└── README.md          # 项目说明
```

## 🛠️ 本地运行

1. 克隆仓库：
```bash
git clone [您的仓库地址]
cd MovieRecommender
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 准备数据：
   - 下载 [MovieLens数据集](https://grouplens.org/datasets/movielens/latest/)
   - 将 `ratings.csv` 和 `movies.csv` 放入 `data/` 文件夹

4. 运行应用：
```bash
streamlit run app.py
```

## 🎯 功能特性

- 🎯 **个性化推荐**: 基于协同过滤算法的智能推荐
- 🏆 **热门电影**: 按类型浏览高分电影排行榜
- 🔍 **电影搜索**: 支持模糊搜索的电影查找功能
- 📊 **数据分析**: 电影数据的可视化分析
- 👤 **用户分析**: 个人观影行为分析
- 🎲 **随机发现**: AI推荐的惊喜电影发现

## 📊 数据来源

本项目使用 [MovieLens](https://grouplens.org/datasets/movielens/) 数据集，包含电影评分和电影信息数据。

## 🔧 技术栈

- **Frontend**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Machine Learning**: Scikit-learn
- **Visualization**: Plotly, Matplotlib, Seaborn
- **Deployment**: Streamlit Cloud

## 📝 使用说明

1. **个性化推荐**: 选择您喜欢的电影，系统会推荐相似的电影
2. **热门电影**: 浏览不同类型的高分电影
3. **电影搜索**: 搜索特定电影获取详细信息
4. **数据分析**: 查看电影数据的统计分析
5. **用户分析**: 输入用户ID分析观影偏好
6. **随机发现**: 让AI为您推荐意外的好电影

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 📄 许可证

MIT License
