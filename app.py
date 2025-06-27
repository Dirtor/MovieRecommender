import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import time
import numpy as np
from datetime import datetime
import random

# 🎨 页面配置和CSS样式
st.set_page_config(
    page_title="🎬 智能电影推荐系统",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🎨 自定义CSS样式
st.markdown("""
<style>
    /* 主题色彩 */
    .main-header {
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4, #45B7D1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* 美化的功能导航卡片 */
    .nav-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    
    .nav-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        border: 2px solid #4ECDC4;
    }
    
    .nav-card.selected {
        background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(255, 107, 107, 0.3);
        border: 2px solid #FFD700;
    }
    
    .nav-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
        display: block;
    }
    
    .nav-title {
        font-size: 1.1rem;
        font-weight: bold;
        margin-bottom: 0.3rem;
    }
    
    .nav-desc {
        font-size: 0.85rem;
        opacity: 0.9;
    }
    
    /* 卡片样式 */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #FF6B6B;
        margin: 1rem 0;
    }
    
    /* 按钮样式 */
    .stButton > button {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }
    
    /* 侧边栏样式 */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* 信息框样式 */
    .info-box {
        background: linear-gradient(135deg, #74b9ff, #0984e3);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
    }
    
    /* 动画效果 */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.6s ease-in;
    }
    
    /* 电影卡片样式 */
    .movie-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        margin: 0.5rem 0;
        border-left: 3px solid #4ECDC4;
        transition: transform 0.2s ease;
    }
    
    .movie-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    }
    
    /* 进度条样式 */
    .progress-bar {
        width: 100%;
        height: 20px;
        background-color: #e0e0e0;
        border-radius: 10px;
        overflow: hidden;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
        border-radius: 10px;
        transition: width 0.3s ease;
    }
    
    /* 隐藏默认的radio样式 */
    .stRadio > div {
        display: none;
    }
    
    /* 美化侧边栏统计卡片 */
    .sidebar-stat {
        background: rgba(255, 255, 255, 0.1);
        padding: 0.8rem;
        border-radius: 8px;
        margin: 0.3rem 0;
        text-align: center;
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .sidebar-stat h3 {
        margin: 0;
        font-size: 1.5rem;
        color: #4ECDC4;
    }
    
    .sidebar-stat p {
        margin: 0;
        font-size: 0.9rem;
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """📦 数据加载函数 - 使用缓存提高性能"""
    try:
        ratings = pd.read_csv('/Users/dirtortian/Downloads/ml-latest-small/ratings.csv')
        movies = pd.read_csv('/Users/dirtortian/Downloads/ml-latest-small/movies.csv')
        df = pd.merge(ratings, movies, on='movieId')
        
        df_with_genres = df.copy()
        df = df.drop(['genres','timestamp'], axis=1)
        
        ratings_count = pd.DataFrame(df['title'].value_counts())
        ratings_count.rename(columns={'count': 'ratings_count'}, inplace=True)
        movie_matrix = df.pivot_table(index='userId', columns='title', values='rating')
        avg_ratings = df.groupby('title')['rating'].mean().round(2)
        
        return movie_matrix, ratings_count, df_with_genres, avg_ratings
    except Exception as e:
        st.error(f"数据加载错误: {str(e)}")
        return None, None, None, None

def get_movie_recommendations(movie_title, movie_matrix, ratings_count, min_ratings=100):
    """🎯 基于协同过滤的电影推荐算法"""
    try:
        movie_ratings = movie_matrix[movie_title]
        similarity_scores = movie_matrix.corrwith(movie_ratings)
        corr_df = pd.DataFrame(similarity_scores, columns=['correlation'])
        corr_df.dropna(inplace=True)
        corr_df = corr_df.join(ratings_count, how='left')
        filtered_corr_df = corr_df[corr_df['ratings_count'] >= min_ratings]
        result = filtered_corr_df.sort_values(by='correlation', ascending=False)
        result = result[result.index != movie_title]
        return result
    except KeyError:
        st.error(f"电影 '{movie_title}' 在数据库中未找到")
        return pd.DataFrame()

def get_top_movies_by_genre(df_with_genres, genre, min_ratings=50):
    """🏆 按电影类型筛选热门电影"""
    genre_movies = df_with_genres[df_with_genres['genres'].str.contains(genre, na=False)]
    genre_stats = genre_movies.groupby('title').agg({
        'rating': ['mean', 'count']
    }).round(2)
    genre_stats.columns = ['avg_rating', 'rating_count']
    genre_stats = genre_stats[genre_stats['rating_count'] >= min_ratings]
    return genre_stats.sort_values('avg_rating', ascending=False)

def search_movies(movie_matrix, search_term):
    """🔍 模糊搜索电影功能"""
    movie_list = movie_matrix.columns.tolist()
    matches = [movie for movie in movie_list if search_term.lower() in movie.lower()]
    return matches

def get_user_rating_stats(df_with_genres, user_id):
    """👤 用户观影行为分析"""
    user_data = df_with_genres[df_with_genres['userId'] == user_id]
    if user_data.empty:
        return None
    
    stats = {
        'total_movies': len(user_data),
        'avg_rating': user_data['rating'].mean().round(2),
        'favorite_genres': user_data['genres'].str.split('|').explode().value_counts().head(5)
    }
    return stats

# 🆕 新增功能：获取随机推荐
def get_random_recommendations(df_with_genres, count=5):
    """🎲 随机推荐高分电影"""
    high_rated = df_with_genres.groupby('title').agg({
        'rating': ['mean', 'count']
    }).round(2)
    high_rated.columns = ['avg_rating', 'rating_count']
    high_rated = high_rated[(high_rated['avg_rating'] >= 4.0) & (high_rated['rating_count'] >= 50)]
    return high_rated.sample(min(count, len(high_rated)))

# 🆕 新增功能：评分预测
def predict_rating(user_avg, movie_avg, genre_factor=1.0):
    """🔮 简单的评分预测"""
    base_prediction = (user_avg + movie_avg) / 2
    return min(5.0, max(1.0, base_prediction * genre_factor))


# 🎭 欢迎横幅
welcome_container = st.container()
with welcome_container:
    st.markdown("""
    <div class="info-box fade-in">
        <h3>🌟 欢迎来到智能电影推荐系统！</h3>
        <p>发现您的下一部最爱电影 | 基于AI的个性化推荐 | 数据驱动的观影指南</p>
    </div>
    """, unsafe_allow_html=True)

# 数据加载进度
with st.spinner('🔄 正在加载电影数据库...'):
    movie_matrix, ratings_count, df_with_genres, avg_ratings = load_data()
    
if movie_matrix is None:
    st.error("❌ 数据加载失败，请检查数据文件路径")
    st.stop()

# 🎉 加载成功动画
st.success("✅ 数据加载成功！准备为您提供个性化推荐")

# 🎨 美化的侧边栏
# 侧边栏顶部LOGO和标题
st.sidebar.markdown("""
<div style="text-align:center; margin-bottom: 15px;">
    <div style="font-size:1.25rem; font-weight:bold; margin-top:4px; color:#4ECDC4;">
        <span style="font-size:2rem;">🎬</span>智能电影推荐系统
    </div>
</div>
""", unsafe_allow_html=True)

# 🎨 美化的侧边栏
st.sidebar.markdown("### 🎮 功能导航")
st.sidebar.markdown("---")

# 功能选择 - 美化的导航
feature_options = {
    "🎯 个性化推荐": {"desc": "基于AI的智能推荐", "icon": "🎯"},
    "🏆 热门电影": {"desc": "发现高分佳作", "icon": "🏆"},
    "🔍 电影搜索": {"desc": "快速查找电影", "icon": "🔍"},
    "📊 数据分析": {"desc": "深度数据洞察", "icon": "📊"},
    "👤 用户分析": {"desc": "个人观影档案", "icon": "👤"},
    "🎲 随机发现": {"desc": "意外惊喜推荐", "icon": "🎲"}
}

# 初始化session state
if 'selected_feature' not in st.session_state:
    st.session_state.selected_feature = "🎯 个性化推荐"

# 创建美化的导航按钮
for feature_name, feature_info in feature_options.items():
    is_selected = st.session_state.selected_feature == feature_name
    card_class = "nav-card selected" if is_selected else "nav-card"
    
    # 使用columns来创建可点击的卡片效果
    if st.sidebar.button(
        f"{feature_info['icon']} {feature_name.split(' ', 1)[1]}", 
        key=f"nav_{feature_name}",
        help=feature_info['desc'],
        use_container_width=True
    ):
        st.session_state.selected_feature = feature_name
        st.rerun()

selected_feature = st.session_state.selected_feature

# 🎨 侧边栏统计信息（美化升级版）
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="text-align:center; margin-bottom: 10px;">
    <span style="font-size:1.2rem; font-weight:bold; color:#FFD700;">📈 系统统计</span>
</div>
""", unsafe_allow_html=True)

stats_data = [
    {"icon": "🎬", "label": "电影", "value": f"{len(movie_matrix.columns):,}", "color": "#4ECDC4"},
    {"icon": "👥", "label": "用户", "value": f"{len(movie_matrix.index):,}", "color": "#FFD700"},
    {"icon": "⭐", "label": "评分", "value": f"{len(df_with_genres):,}", "color": "#FF6B6B"},
    {"icon": "📊", "label": "平均分", "value": f"{df_with_genres['rating'].mean():.1f}", "color": "#667eea"}
]

for stat in stats_data:
    st.sidebar.markdown(f"""
    <div style="
        background: linear-gradient(90deg, {stat['color']}22 0%, #fff0 100%);
        border-radius: 10px;
        padding: 0.8rem 0.5rem;
        margin-bottom: 10px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border: 1.5px solid {stat['color']}55;
        ">
        <div style="font-size:2rem; margin-bottom:0.2rem;">{stat['icon']}</div>
        <div style="font-size:1.5rem; font-weight:bold; color:{stat['color']};">{stat['value']}</div>
        <div style="font-size:1rem; opacity:0.85;">{stat['label']}</div>
    </div>
    """, unsafe_allow_html=True)

# ===============================
# 🎯 功能1：增强的个性化推荐
# ===============================
if selected_feature == "🎯 个性化推荐":
    st.markdown("## 🎯 个性化电影推荐")
    st.markdown("---")
    
    # 设置区域
    with st.expander("⚙️ 推荐设置", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            top_n = st.slider("推荐数量", 5, 20, 10, help="选择要显示的推荐电影数量")
        with col2:
            min_ratings = st.slider("最小评分数", 50, 500, 100, step=50, help="过滤掉评分数量少的电影")
        with col3:
            similarity_threshold = st.slider("相似度阈值", 0.0, 1.0, 0.1, 0.1, help="设置最低相似度要求")
    
    # 电影选择区域
    st.markdown("### 🎬 选择您喜欢的电影")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        search_term = st.text_input(
            "🔍 搜索电影",
            placeholder="输入电影名称关键词...",
            help="支持模糊搜索，不区分大小写"
        )
    
    with col2:
        search_button = st.button("🔍 搜索", type="secondary")
    
    # 搜索结果或选择列表
    if search_term:
        matches = search_movies(movie_matrix, search_term)
        if matches:
            selected_movie = st.selectbox(
                f'🎯 找到 {len(matches)} 部相关电影',
                matches,
                help="从搜索结果中选择电影"
            )
        else:
            st.warning("😕 未找到匹配的电影，请尝试其他关键词")
            selected_movie = None
    else:
        movie_list = sorted(movie_matrix.columns.tolist())
        selected_movie = st.selectbox(
            '📋 或从完整列表中选择',
            [''] + movie_list,
            help="从所有电影中选择"
        )
        if selected_movie == '':
            selected_movie = None
        # 电影信息展示
    if selected_movie:
        st.markdown("### 📖 电影信息")
        
        info_cols = st.columns(4)
        
        # 获取电影基础数据
        movie_info = ratings_count.loc[selected_movie] if selected_movie in ratings_count.index else None
        avg_rating = avg_ratings.get(selected_movie, 0)
        movie_genres = df_with_genres[df_with_genres['title'] == selected_movie]['genres'].iloc[0] if not df_with_genres[df_with_genres['title'] == selected_movie].empty else "未知"
        
        # 计算流行度
        if movie_info is not None:
            popularity_score = min(100, (movie_info['ratings_count'] / 1000 * 100))
        else:
            popularity_score = 0
        
        # 统一的卡片样式 - 修复文字溢出问题
        card_style_base = """
        <div style="
            background: linear-gradient(135deg, {gradient_colors});
            padding: 15px;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin: 0.5rem 0;
            height: 180px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            overflow: hidden;
            word-wrap: break-word;
            box-sizing: border-box;
        " onmouseover="this.style.transform='translateY(-3px)'; this.style.boxShadow='0 6px 20px rgba(0, 0, 0, 0.15)'" 
           onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 15px rgba(0, 0, 0, 0.1)'">
            <div style="font-size: 1.8rem; margin-bottom: 8px;">{icon}</div>
            <div style="width: 100%; text-align: center;">
                <h4 style="margin: 0 0 6px 0; font-size: 0.9rem; opacity: 0.9; font-weight: 500;">{title}</h4>
                <div style="font-size: 1.4rem; font-weight: bold; margin-bottom: 6px; line-height: 1.2;">{value}</div>
                <div style="font-size: 0.75rem; opacity: 0.8; line-height: 1.1; word-break: break-word; overflow: hidden;">{extra_content}</div>
            </div>
        </div>
        """
        
        # 评分数量卡片
        with info_cols[0]:
            rating_count_value = f"{movie_info['ratings_count']:,}" if movie_info is not None else "0"
            st.markdown(card_style_base.format(
                gradient_colors="#667eea 0%, #764ba2 100%",
                icon="📊",
                title="评分数量",
                value=rating_count_value,
                extra_content="用户评价"
            ), unsafe_allow_html=True)
        
        # 平均评分卡片
        with info_cols[1]:
            stars_count = min(5, max(0, int(avg_rating)))  # 限制星星数量0-5
            stars = "⭐" * stars_count if avg_rating > 0 else "☆☆☆☆☆"
            st.markdown(card_style_base.format(
                gradient_colors="#FF6B6B 0%, #EE5A6F 100%",
                icon="⭐",
                title="平均评分",
                value=f"{avg_rating:.1f}/5.0",
                extra_content=stars
            ), unsafe_allow_html=True)
        
        # 电影类型卡片
        with info_cols[2]:
            # 处理长类型名称，确保不超出框架
            genres_list = movie_genres.split('|')
            if len(genres_list) > 3:
                genres_display = ' • '.join(genres_list[:2]) + f" +{len(genres_list)-2}更多"
            else:
                genres_display = ' • '.join(genres_list)
            
            # 进一步限制长度
            if len(genres_display) > 30:
                genres_display = genres_display[:27] + "..."
            
            st.markdown(card_style_base.format(
                gradient_colors="#4ECDC4 0%, #44A08D 100%",
                icon="🎭",
                title="电影类型",
                value="",
                extra_content=genres_display
            ), unsafe_allow_html=True)
        
        # 流行度卡片
        with info_cols[3]:
            # 流行度等级 - 简化显示
            if popularity_score >= 80:
                popularity_level = "超热门"
            elif popularity_score >= 50:
                popularity_level = "热门"
            elif popularity_score >= 20:
                popularity_level = "一般"
            else:
                popularity_level = "小众精品"
            
            st.markdown(card_style_base.format(
                gradient_colors="#FFD93D 0%, #FF9500 100%",
                icon="🔥",
                title="流行度",
                value=f"{popularity_score:.0f}%",
                extra_content=popularity_level
            ), unsafe_allow_html=True)
        
        # 添加详细信息展示区域
        st.markdown("---")
        detail_col1, detail_col2 = st.columns(2)
        
        with detail_col1:
            st.markdown("#### 🎬 电影详情")
            st.info(f"""
            **电影类型:** {movie_genres.replace('|', ' • ')}
            
            **评分统计:** {avg_rating:.2f}/5.0 (基于 {rating_count_value} 个评分)
            
            **流行度:** {popularity_score:.1f}% ({popularity_level})
            """)
        
        with detail_col2:
            st.markdown("#### 📊 评分分布")
            # 创建简单的评分可视化
            if movie_info is not None and movie_info['ratings_count'] > 0:
                # 显示流行度进度条
                st.write("流行度指标:")
                st.progress(popularity_score / 100)
                
                # 显示评分质量
                quality_score = (avg_rating / 5.0) * 100
                st.write("评分质量:")
                st.progress(quality_score / 100)
                
                st.caption(f"💡 基于 {rating_count_value} 个用户评分的综合分析")
            else:
                st.warning("暂无足够的评分数据")

 
    # 推荐按钮
    if selected_movie:
        if st.button('🚀 获取个性化推荐', type="primary", help="基于您选择的电影生成推荐"):
            with st.spinner('🤖 AI正在分析电影相似性...'):
                # 添加进度条
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(i + 1)
                
                recommendations = get_movie_recommendations(selected_movie, movie_matrix, ratings_count, min_ratings)
                
                if not recommendations.empty:
                    # 过滤相似度
                    recommendations = recommendations[recommendations['correlation'] >= similarity_threshold]
                    
                    if not recommendations.empty:
                        st.markdown(f"### 🎊 为您推荐与《{selected_movie}》相似的电影")
                        
                        # 推荐结果展示
                        display_df = recommendations.head(top_n).copy()
                        display_df['avg_rating'] = display_df.index.map(avg_ratings)
                        display_df['correlation'] = display_df['correlation'].round(4)
                        
                        # 创建可视化的推荐卡片
                        for idx, (movie_title, row) in enumerate(display_df.iterrows()):
                            with st.expander(f"🎬 {idx + 1}. {movie_title}", expanded=idx < 3):
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("相似度", f"{row['correlation']:.1%}")
                                with col2:
                                    st.metric("平均评分", f"{row['avg_rating']:.1f}⭐")
                                with col3:
                                    st.metric("评分数量", f"{row['ratings_count']:,}")
                                
                                # 获取电影类型
                                movie_genre = df_with_genres[df_with_genres['title'] == movie_title]['genres'].iloc[0] if not df_with_genres[df_with_genres['title'] == movie_title].empty else "未知"
                                st.info(f"🎭 类型: {movie_genre.replace('|', ' • ')}")
                    else:
                        st.warning(f"😔 没有找到相似度超过 {similarity_threshold:.1%} 的电影，请降低相似度阈值")
                else:
                    st.warning("😕 暂时没有找到相似的电影推荐")

# ===============================
# 🆕 功能6：随机发现
# ===============================

elif selected_feature == "🎲 随机发现":
    st.markdown("## 🎲 随机发现优质电影")
    st.markdown("---")
    
    # 美化的介绍区域
    st.markdown("""
    <div class="info-box">
        <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 15px;">
            <span style="font-size: 3rem; margin-right: 15px;">🎲</span>
            <div>
                <h3 style="margin: 0; color: white;">🌟 意外惊喜等着您！</h3>
                <p style="margin: 5px 0 0 0; opacity: 0.9;">让AI为您随机推荐一些高质量的电影，也许会发现意想不到的宝藏作品</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 控制面板
    st.markdown("### ⚙️ 随机推荐设置")
    control_col1, control_col2, control_col3 = st.columns([2, 1, 1])
    
    with control_col1:
        random_count = st.slider(
            "随机推荐数量", 
            min_value=3, 
            max_value=15, 
            value=5, 
            help="选择要推荐的电影数量"
        )
    
    with control_col2:
        min_rating = st.slider(
            "最低评分", 
            min_value=3.0, 
            max_value=5.0, 
            value=4.0, 
            step=0.1,
            help="设置推荐电影的最低平均评分"
        )
    
    with control_col3:
        min_review_count = st.slider(
            "最少评价数", 
            min_value=20, 
            max_value=200, 
            value=50, 
            step=10,
            help="确保电影有足够的评价基础"
        )
    
    #    # 按钮区域 - 修复宽度问题
    st.markdown("### 🎯 开始探索")
    
    # 使用更宽的布局，减少左右空白
    btn_col1, btn_col2, btn_col3 = st.columns([0.5, 3, 0.5])  # 改为更宽的中间列
    
    with btn_col2:
        if st.button(
            "🎲 随机发现精彩电影", 
            type="primary", 
            use_container_width=True,
            help="点击获取随机推荐"
        ):
            with st.spinner("🔍 AI正在为您挑选惊喜电影..."):
                # 进度条动画
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i in range(100):
                    progress_bar.progress(i + 1)
                    if i < 30:
                        status_text.text("🔍 搜索高质量电影...")
                    elif i < 60:
                        status_text.text("🎯 筛选符合条件的作品...")
                    elif i < 90:
                        status_text.text("🎲 随机选择推荐...")
                    else:
                        status_text.text("✨ 准备呈现结果...")
                    time.sleep(0.02)
                
                progress_bar.empty()
                status_text.empty()
                
                # 获取随机推荐
                try:
                    high_rated = df_with_genres.groupby('title').agg({
                        'rating': ['mean', 'count']
                    }).round(2)
                    high_rated.columns = ['avg_rating', 'rating_count']
                    
                    # 应用筛选条件
                    filtered_movies = high_rated[
                        (high_rated['avg_rating'] >= min_rating) & 
                        (high_rated['rating_count'] >= min_review_count)
                    ]
                    
                    if len(filtered_movies) < random_count:
                        st.warning(f"⚠️ 符合条件的电影数量不足，仅找到 {len(filtered_movies)} 部电影")
                        random_recs = filtered_movies
                    else:
                        random_recs = filtered_movies.sample(min(random_count, len(filtered_movies)))
                    
                    if not random_recs.empty:
                        st.success(f"🎊 为您精选了 {len(random_recs)} 部优质电影！")
                        
                        # 结果展示区域
                        st.markdown("### 🎬 您的专属电影清单")
                        
                        # 使用简化的方式展示每部电影
                        for idx, (movie_title, row) in enumerate(random_recs.iterrows()):
                            # 获取电影详细信息
                            movie_detail = df_with_genres[df_with_genres['title'] == movie_title].iloc[0] if not df_with_genres[df_with_genres['title'] == movie_title].empty else None
                            movie_genres = movie_detail['genres'].replace('|', ' • ') if movie_detail is not None else "未知类型"
                            
                            # 评分星级显示
                            star_rating = "⭐" * int(row['avg_rating'])
                            
                            # 流行度计算
                            popularity = min(100, (row['rating_count'] / 500 * 100))
                            popularity_emoji = "🔥" if popularity >= 80 else "📈" if popularity >= 50 else "💎"
                            
                            # 推荐理由
                            if row['avg_rating'] >= 4.5:
                                reason = "高分经典之作，值得收藏"
                            elif row['avg_rating'] >= 4.0:
                                reason = "口碑佳作，广受好评"
                            else:
                                reason = "优质作品，不容错过"
                            
                            if popularity >= 70:
                                popularity_desc = "，热门之选"
                            elif popularity < 30:
                                popularity_desc = "，小众精品"
                            else:
                                popularity_desc = ""
                            
                            # 使用expander展示电影信息 - 简化版
                            with st.expander(f"🎬 {idx + 1}. {movie_title} ⭐{row['avg_rating']:.1f}", expanded=idx < 3):
                                # 只保留大号电影名，不要再显示一遍
                                st.markdown(
                                    f"<div style='font-size:1.7rem;font-weight:bold;margin-bottom:0.7em;color:#222;line-height:1.2;'>{movie_title}</div>",
                                    unsafe_allow_html=True
                                )
                                st.markdown(f"**🎭 类型：** {movie_genres}")
                                st.markdown(f"**⭐ 评分：** {row['avg_rating']:.1f}/5.0 {star_rating}")
                                st.markdown(f"**📊 评价数：** {int(row['rating_count']):,}")
                                st.markdown(f"**🔥 流行度：** {popularity:.0f}% {popularity_emoji}")
                                st.info(f"💡 **推荐理由：** {reason}{popularity_desc}")
                                
                                # 使用三列布局展示关键数据
                                metric_col1, metric_col2, metric_col3 = st.columns(3)
                                
                                with metric_col1:
                                    st.metric(
                                        label="⭐ 平均评分",
                                        value=f"{row['avg_rating']:.1f}/5.0",
                                        delta=f"{row['avg_rating'] - df_with_genres['rating'].mean():.1f}" if row['avg_rating'] != df_with_genres['rating'].mean() else None
                                    )
                                
                                with metric_col2:
                                    st.metric(
                                        label="📊 评价数量",
                                        value=f"{int(row['rating_count']):,}",
                                        delta="热门" if row['rating_count'] > 200 else "小众" if row['rating_count'] < 100 else None
                                    )
                                
                                with metric_col3:
                                    st.metric(
                                        label="🎯 推荐指数",
                                        value=f"{(row['avg_rating'] * 20):.0f}%",
                                        delta="强烈推荐" if row['avg_rating'] >= 4.5 else "推荐" if row['avg_rating'] >= 4.0 else None
                                    )
                        
                        # 操作建议 - 简化版
                        st.markdown("---")
                        st.markdown("### 🎯 接下来可以做什么？")
                        
                        suggestion_col1, suggestion_col2, suggestion_col3 = st.columns(3)
                        
                        with suggestion_col1:
                            st.info("🎯 **个性化推荐**\n\n输入感兴趣的电影获取相似推荐")
                        
                        with suggestion_col2:
                            st.info("🔍 **电影搜索**\n\n搜索电影了解更多详细信息")
                        
                        with suggestion_col3:
                            st.info("🎲 **再次随机**\n\n调整筛选条件重新发现电影")
                        
                    else:
                        st.error("😔 抱歉，没有找到符合条件的电影，请尝试调整筛选条件")
                        
                        # 提供建议
                        st.markdown("### 💡 建议")
                        st.markdown("- 降低最低评分要求")
                        st.markdown("- 减少最少评价数要求") 
                        st.markdown("- 或者尝试其他功能模块")
                        
                except Exception as e:
                    st.error(f"❌ 获取推荐时出现错误: {str(e)}")
                    st.markdown("请尝试刷新页面或联系管理员")
    
    # 统计信息展示 - 使用st.metric替代HTML
    st.markdown("---")
    st.markdown("### 📊 数据库概况")
    
    # 计算统计数据
    total_movies = len(df_with_genres['title'].unique())
    high_rated_movies = len(df_with_genres.groupby('title')['rating'].mean()[df_with_genres.groupby('title')['rating'].mean() >= 4.0])
    avg_rating = df_with_genres['rating'].mean()
    
    stats_cols = st.columns(3)
    
    with stats_cols[0]:
        st.metric(
            label="🎬 总电影数量",
            value=f"{total_movies:,}",
            delta="数据库规模"
        )
    
    with stats_cols[1]:
        st.metric(
            label="⭐ 高分电影",
            value=f"{high_rated_movies:,}",
            delta="评分≥4.0"
        )
    
    with stats_cols[2]:
        st.metric(
            label="📊 平均评分",
            value=f"{avg_rating:.1f}",
            delta="总体水平"
        )
    
    # 额外的帮助信息
    with st.expander("ℹ️ 使用提示", expanded=False):
        st.markdown("""
        **如何使用随机发现功能：**
        
        1. **调整设置**: 根据您的喜好调整推荐数量、最低评分和最少评价数
        2. **点击按钮**: 点击"随机发现精彩电影"获取推荐
        3. **浏览结果**: 展开电影卡片查看详细信息
        4. **探索更多**: 使用其他功能深入了解推荐的电影
        
        **参数说明：**
        - **最低评分**: 过滤掉评分较低的电影
        - **最少评价数**: 确保电影有足够的评价基础，提高推荐质量
        - **推荐数量**: 控制一次推荐的电影数量
        """)





# ===============================
# 🏆 功能2：美化的热门电影
# ===============================
elif selected_feature == "🏆 热门电影":
    st.markdown("## 🏆 热门电影排行榜")
    st.markdown("---")
    
    # 类型选择
    all_genres = set()
    for genres in df_with_genres['genres'].dropna():
        all_genres.update(genres.split('|'))
    genre_list = sorted(list(all_genres))
    
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_genre = st.selectbox("🎭 选择电影类型", ["全部"] + genre_list)
    with col2:
        min_ratings_genre = st.slider("最小评分数量", 10, 200, 50)
    with col3:
        sort_by = st.selectbox("排序方式", ["平均评分", "评分数量"])
    
    # 获取数据
    if selected_genre == "全部":
        top_movies = df_with_genres.groupby('title').agg({
            'rating': ['mean', 'count']
        }).round(2)
        top_movies.columns = ['平均评分', '评分数量']
        top_movies = top_movies[top_movies['评分数量'] >= min_ratings_genre]
    else:
        top_movies = get_top_movies_by_genre(df_with_genres, selected_genre, min_ratings_genre)
        top_movies.columns = ['平均评分', '评分数量']
    
    # 排序
    if sort_by == "平均评分":
        top_movies = top_movies.sort_values('平均评分', ascending=False)
    else:
        top_movies = top_movies.sort_values('评分数量', ascending=False)
    
    top_movies = top_movies.head(20)
    
    if not top_movies.empty:
        # 展示热门电影
        st.markdown(f"### 🎬 {selected_genre}类型 - 按{sort_by}排序")
        
        # 前三名特殊展示
        if len(top_movies) >= 3:
            st.markdown("#### 🥇 TOP 3")
            top3_cols = st.columns(3)
            medals = ["🥇", "🥈", "🥉"]
            
            for i, (movie_title, row) in enumerate(top_movies.head(3).iterrows()):
                with top3_cols[i]:
                    st.markdown(f"""
                    <div class="movie-card" style="
                        text-align: center; 
                        border-left: 3px solid #FFD700;
                        min-height: 170px;
                        height: 170px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        align-items: center;
                        overflow: hidden;
                        box-sizing: border-box;
                        padding: 12px 8px 8px 8px;
                    ">
                        <h2 style="margin-bottom:4px; font-size:2rem; line-height:1;">{medals[i]}</h2>
                        <div style="
                            font-size:1.08rem;
                            font-weight:bold;
                            margin-bottom:6px;
                            line-height:1.25;
                            max-width:98%;
                            word-break:break-all;
                            overflow:hidden;
                            text-overflow:ellipsis;
                            white-space:normal;
                            display:-webkit-box;
                            -webkit-line-clamp:2;
                            -webkit-box-orient:vertical;
                        ">{movie_title}</div>
                        <div style="margin:0; font-size:1.05rem;">
                            <strong>⭐ {row['平均评分']:.1f}</strong>
                            <span style="color:#888;">({row['评分数量']:,} 评分)</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        # 完整排行榜
        st.markdown("#### 📊 完整排行榜")
        st.dataframe(
            top_movies,
            use_container_width=True,
            height=400
        )
        
        # 可视化
        fig = px.scatter(
            top_movies,
            x='评分数量',
            y='平均评分',
            title=f'{selected_genre}类型电影评分分布',
            hover_name=top_movies.index,
            color='平均评分',
            size='评分数量',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)
















# ===============================
# 🔍 功能3：美化的电影搜索
# ===============================
elif selected_feature == "🔍 电影搜索":
    st.markdown("## 🔍 智能电影搜索")
    st.markdown("---")
    
    # 搜索界面
    col1, col2 = st.columns([4, 1])
    with col1:
        search_query = st.text_input(
            "输入电影名称",
            placeholder="例如: Toy Story, Star Wars, Avengers...",
            help="支持模糊搜索，不区分大小写"
        )
    with col2:
        search_type = st.selectbox("搜索模式", ["标题搜索", "类型搜索"])
    
    if search_query:
        if search_type == "标题搜索":
            matches = search_movies(movie_matrix, search_query)
        else:
            # 按类型搜索
            matches = df_with_genres[df_with_genres['genres'].str.contains(search_query, case=False, na=False)]['title'].unique().tolist()
        
        if matches:
            st.success(f"🎯 找到 {len(matches)} 部相关电影")
            
            # 分页显示
            page_size = 10
            total_pages = (len(matches) - 1) // page_size + 1
            
            if total_pages > 1:
                page = st.selectbox("选择页面", range(1, total_pages + 1))
                start_idx = (page - 1) * page_size
                end_idx = start_idx + page_size
                current_matches = matches[start_idx:end_idx]
            else:
                current_matches = matches
            
            # 详细搜索结果
            for i, movie in enumerate(current_matches):
                rating_count = ratings_count.loc[movie]['ratings_count'] if movie in ratings_count.index else 0
                avg_rating = avg_ratings.get(movie, 0)
                movie_genres = df_with_genres[df_with_genres['title'] == movie]['genres'].iloc[0] if not df_with_genres[df_with_genres['title'] == movie].empty else "未知"
                
                st.markdown(f"""
                <div class="movie-card">
                    <h4>🎬 {movie}</h4>
                    <div style="display: flex; gap: 20px; align-items: center; flex-wrap: wrap;">
                        <div><strong>⭐ 评分:</strong> {avg_rating:.1f}/5.0</div>
                        <div><strong>📊 评分数:</strong> {rating_count:,}</div>
                        <div><strong>🎭 类型:</strong> {movie_genres.replace('|', ' • ')}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("😕 未找到匹配的电影，请尝试其他关键词")

# ===============================
# 📊 功能4：美化的数据分析
# ===============================
elif selected_feature == "📊 数据分析":
    st.markdown("## 📊 数据分析仪表板")
    st.markdown("---")
    
    # 关键指标
    st.markdown("### 📈 关键指标")
    metrics_cols = st.columns(4)
    
    with metrics_cols[0]:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🎬 电影总数</h3>
            <h2>{len(movie_matrix.columns):,}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with metrics_cols[1]:
        st.markdown(f"""
        <div class="metric-card">
            <h3>👥 用户总数</h3>
            <h2>{len(movie_matrix.index):,}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with metrics_cols[2]:
        st.markdown(f"""
        <div class="metric-card">
            <h3>⭐ 评分总数</h3>
            <h2>{len(df_with_genres):,}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with metrics_cols[3]:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📊 平均评分</h3>
            <h2>{df_with_genres['rating'].mean():.2f}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # 图表区域
    st.markdown("### 📊 数据可视化")
    
    tab1, tab2, tab3 = st.tabs(["📈 评分分布", "🎭 类型分析", "🔥 热门趋势"])
    
    with tab1:
        # 评分分布
        rating_dist = df_with_genres['rating'].value_counts().sort_index()
        fig_rating = px.bar(
            x=rating_dist.index,
            y=rating_dist.values,
            title="评分分布统计",
            labels={'x': '评分', 'y': '数量'},
            color=rating_dist.values,
            color_continuous_scale='Viridis'
        )
        fig_rating.update_layout(showlegend=False)
        st.plotly_chart(fig_rating, use_container_width=True)
    
    with tab2:
        # 类型分析
        genre_counts = Counter()
        for genres in df_with_genres['genres'].dropna():
            genre_counts.update(genres.split('|'))
        
        top_genres = dict(genre_counts.most_common(10))
        fig_genre = px.pie(
            values=list(top_genres.values()),
            names=list(top_genres.keys()),
            title="热门电影类型分布"
        )
        st.plotly_chart(fig_genre, use_container_width=True)
    
    with tab3:
        # 热门电影趋势
        popular_movies = df_with_genres.groupby('title').agg({
            'rating': ['mean', 'count']
        }).round(2)
        popular_movies.columns = ['avg_rating', 'rating_count']
        popular_movies = popular_movies[popular_movies['rating_count'] >= 100].head(20)
        
        fig_popular = px.scatter(
            popular_movies,
            x='rating_count',
            y='avg_rating',
            hover_name=popular_movies.index,
            title="热门电影评分vs数量分布",
            size='rating_count',
            color='avg_rating',
            color_continuous_scale='Plasma'
        )
        st.plotly_chart(fig_popular, use_container_width=True)

# ===============================
# 👤 功能5：美化的用户分析
# ===============================
elif selected_feature == "👤 用户分析":
    st.markdown("## 👤 用户行为分析")
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        user_id = st.number_input(
            "输入用户ID",
            min_value=1,
            max_value=int(df_with_genres['userId'].max()),
            value=1,
            help=f"用户ID范围: 1-{int(df_with_genres['userId'].max())}"
        )
    with col2:
        analyze_button = st.button("🔍 分析用户", type="primary")
    
    if analyze_button:
        user_stats = get_user_rating_stats(df_with_genres, user_id)
        
        if user_stats:
            # 用户画像
            st.markdown(f"### 👤 用户 {user_id} 的观影档案")
            
            # 基础统计
            stats_cols = st.columns(3)
            with stats_cols[0]:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>🎬 观影数量</h3>
                    <h2>{user_stats['total_movies']}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with stats_cols[1]:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>⭐ 平均评分</h3>
                    <h2>{user_stats['avg_rating']}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with stats_cols[2]:
                fav_genre = user_stats['favorite_genres'].index[0] if not user_stats['favorite_genres'].empty else "无"
                st.markdown(f"""
                <div class="metric-card">
                    <h3>🎭 偏好类型</h3>
                    <h2>{fav_genre}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            # 类型偏好可视化
            if not user_stats['favorite_genres'].empty:
                st.markdown("### 🎭 类型偏好分布")
                fig_user_genre = px.bar(
                    x=user_stats['favorite_genres'].values,
                    y=user_stats['favorite_genres'].index,
                    orientation='h',
                    title=f"用户 {user_id} 的类型偏好",
                    color=user_stats['favorite_genres'].values,
                    color_continuous_scale='Blues'
                )
                st.plotly_chart(fig_user_genre, use_container_width=True)
            
            # 高分电影列表
            user_ratings = df_with_genres[df_with_genres['userId'] == user_id].sort_values('rating', ascending=False)
            high_rated = user_ratings[user_ratings['rating'] >= 4.0][['title', 'rating', 'genres']].head(10)
            
            if not high_rated.empty:
                st.markdown("### ⭐ 高分电影列表 (评分 ≥ 4.0)")
                for idx, (_, row) in enumerate(high_rated.iterrows()):
                    st.markdown(f"""
                    <div class="movie-card">
                        <h4>🎬 {idx + 1}. {row['title']}</h4>
                        <div style="display: flex; gap: 20px; align-items: center;">
                            <div><strong>⭐ 评分:</strong> {row['rating']}/5.0</div>
                            <div><strong>🎭 类型:</strong> {row['genres'].replace('|', ' • ')}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("该用户没有评分4.0以上的电影")
        else:
            st.error("❌ 用户不存在或没有评分数据")


# 🎨 页面底部
st.markdown("---")
st.markdown("""
<div style="margin: 30px 0 0 0;">
    <div style="font-size:1.5rem;font-weight:bold;text-align:center;margin-bottom:18px;color:#4ECDC4;">
        💡 使用小贴士
    </div>
    <div style="
        display: flex;
        flex-wrap: wrap;
        gap: 18px;
        justify-content: center;
        align-items: stretch;
    ">
        <div style="
            flex:1 1 260px;
            min-width:260px;
            max-width:340px;
            background: linear-gradient(135deg, #FF6B6B22 0%, #FFD93D22 100%);
            border-radius: 15px;
            padding: 22px 18px;
            box-shadow: 0 2px 10px rgba(255,107,107,0.07);
            display: flex; flex-direction: column; align-items: flex-start;
        ">
            <div style="font-size:2rem;margin-bottom:8px;">🎯</div>
            <div style="font-weight:bold;font-size:1.08rem;margin-bottom:4px;">个性化推荐</div>
            <div style="font-size:0.98rem;opacity:0.85;">基于协同过滤算法，找到与您品味相似的电影</div>
        </div>
        <div style="
            flex:1 1 260px;
            min-width:260px;
            max-width:340px;
            background: linear-gradient(135deg, #4ECDC422 0%, #45B7D122 100%);
            border-radius: 15px;
            padding: 22px 18px;
            box-shadow: 0 2px 10px rgba(78,205,196,0.07);
            display: flex; flex-direction: column; align-items: flex-start;
        ">
            <div style="font-size:2rem;margin-bottom:8px;">🏆</div>
            <div style="font-weight:bold;font-size:1.08rem;margin-bottom:4px;">热门电影</div>
            <div style="font-size:0.98rem;opacity:0.85;">按类型浏览高分电影，发现经典佳作</div>
        </div>
        <div style="
            flex:1 1 260px;
            min-width:260px;
            max-width:340px;
            background: linear-gradient(135deg, #667eea22 0%, #764ba222 100%);
            border-radius: 15px;
            padding: 22px 18px;
            box-shadow: 0 2px 10px rgba(102,126,234,0.07);
            display: flex; flex-direction: column; align-items: flex-start;
        ">
            <div style="font-size:2rem;margin-bottom:8px;">🔍</div>
            <div style="font-weight:bold;font-size:1.08rem;margin-bottom:4px;">电影搜索</div>
            <div style="font-size:0.98rem;opacity:0.85;">快速查找特定电影，支持模糊搜索</div>
        </div>
        <div style="
            flex:1 1 260px;
            min-width:260px;
            max-width:340px;
            background: linear-gradient(135deg, #FFD93D22 0%, #FF6B6B22 100%);
            border-radius: 15px;
            padding: 22px 18px;
            box-shadow: 0 2px 10px rgba(255,217,61,0.07);
            display: flex; flex-direction: column; align-items: flex-start;
        ">
            <div style="font-size:2rem;margin-bottom:8px;">📊</div>
            <div style="font-weight:bold;font-size:1.08rem;margin-bottom:4px;">数据分析</div>
            <div style="font-size:0.98rem;opacity:0.85;">深入了解电影数据趋势和统计信息</div>
        </div>
        <div style="
            flex:1 1 260px;
            min-width:260px;
            max-width:340px;
            background: linear-gradient(135deg, #764ba222 0%, #4ECDC422 100%);
            border-radius: 15px;
            padding: 22px 18px;
            box-shadow: 0 2px 10px rgba(118,75,162,0.07);
            display: flex; flex-direction: column; align-items: flex-start;
        ">
            <div style="font-size:2rem;margin-bottom:8px;">👤</div>
            <div style="font-weight:bold;font-size:1.08rem;margin-bottom:4px;">用户分析</div>
            <div style="font-size:0.98rem;opacity:0.85;">分析个人观影偏好和行为模式</div>
        </div>
        <div style="
            flex:1 1 260px;
            min-width:260px;
            max-width:340px;
            background: linear-gradient(135deg, #45B7D122 0%, #FF6B6B22 100%);
            border-radius: 15px;
            padding: 22px 18px;
            box-shadow: 0 2px 10px rgba(69,183,209,0.07);
            display: flex; flex-direction: column; align-items: flex-start;
        ">
            <div style="font-size:2rem;margin-bottom:8px;">🎲</div>
            <div style="font-weight:bold;font-size:1.08rem;margin-bottom:4px;">随机发现</div>
            <div style="font-size:0.98rem;opacity:0.85;">让AI为您推荐意想不到的优质电影</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 🎨 版权信息
st.markdown("""
<div style="text-align: center; margin-top: 30px; padding: 20px; background: linear-gradient(90deg, #667eea, #764ba2); color: white; border-radius: 10px;">
    <p>🎬 智能电影推荐系统 | 基于机器学习的个性化推荐 | Made with ❤️ using Streamlit</p>
</div>
""", unsafe_allow_html=True)