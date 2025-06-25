import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime

# 页面配置
st.set_page_config(
    page_title="BI数据分析系统",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# 自定义主题
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background-color: #f8f9fa;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #ffffff;
        border-radius: 4px 4px 0px 0px;
        padding: 10px 16px;
        border: 1px solid #e0e0e0;
    }
    .stTabs [aria-selected="true"] {
        background-color: #5b7cfd;
        color: white;
    }
    .stExpander {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
    }
    .stDataFrame {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
    }
    /* 按钮样式优化 */
    .stButton > button {
        border-radius: 6px;
        border: 1px solid #e0e0e0;
        background-color: #ffffff;
        color: #333333;
        font-size: 12px;
        padding: 4px 8px;
        height: 32px;
        min-width: 60px;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        background-color: #f0f0f0;
        border-color: #5b7cfd;
        color: #5b7cfd;
    }
    .stButton > button:active {
        background-color: #5b7cfd;
        color: white;
    }
    /* 多选框样式优化 */
    .stMultiSelect > div > div {
        border-radius: 6px;
        border: 1px solid #e0e0e0;
    }
    /* 隐藏右上角的 deploy 按钮和菜单 
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
     隐藏 Streamlit 的菜单按钮 
    .stDeployButton {display: none;}
    [data-testid="stToolbar"] {display: none;}
    [data-testid="stDecoration"] {display: none;}
     隐藏结束 */
</style>
""", unsafe_allow_html=True)

# 标题
st.title("📊 BI数据分析系统")

# 侧边栏
with st.sidebar:
    st.header("🎛️ 控制面板")
    data_source = st.selectbox("选择数据源", ["示例数据", "上传文件"])
    
    if data_source == "上传文件":
        uploaded_file = st.file_uploader("上传数据文件", type=['csv', 'xlsx'])
    else:
        uploaded_file = None

# 生成示例数据
def generate_sample_data():
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    
    data = []
    for date in dates:
        for _ in range(np.random.randint(5, 15)):
            data.append({
                '日期': date,
                '产品类别': np.random.choice(['电子产品', '服装', '食品', '家居', '图书']),
                '产品名称': np.random.choice(['iPhone', 'MacBook', 'T恤', '牛仔裤', '面包', '牛奶', '沙发', '台灯', '小说', '教材']),
                '销售额': np.random.randint(100, 5000),
                '数量': np.random.randint(1, 10),
                '地区': np.random.choice(['北京', '上海', '广州', '深圳', '杭州']),
                '客户类型': np.random.choice(['个人', '企业', 'VIP']),
                '支付方式': np.random.choice(['信用卡', '支付宝', '微信', '现金'])
            })
    
    return pd.DataFrame(data)

# 加载数据
@st.cache_data
def load_data():
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            return df
        except Exception as e:
            st.error(f"文件读取错误: {e}")
            return generate_sample_data()
    else:
        return generate_sample_data()

# 加载数据
df = load_data()

# 数据预处理
if not df.empty and '日期' in df.columns:
    df['日期'] = pd.to_datetime(df['日期'])
    df['月份'] = df['日期'].dt.to_period('M')
    df['季度'] = df['日期'].dt.to_period('Q')
    df['年份'] = df['日期'].dt.year

# 主界面
if not df.empty:
    # 顶部指标
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_sales = df['销售额'].sum() if '销售额' in df.columns else 0
        st.metric("总销售额", f"¥{total_sales:,.0f}")
    
    with col2:
        total_orders = len(df)
        st.metric("总订单数", f"{total_orders:,}")
    
    with col3:
        avg_order_value = total_sales / total_orders if total_orders > 0 else 0
        st.metric("平均订单金额", f"¥{avg_order_value:,.0f}")
    
    with col4:
        unique_customers = df['客户类型'].nunique() if '客户类型' in df.columns else 0
        st.metric("客户类型数", f"{unique_customers}")
    
    st.markdown("---")
    
    # 筛选器
    st.subheader("🔍 数据筛选")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if '地区' in df.columns:
            # 获取所有地区选项
            all_regions = df['地区'].unique()
            
            # 初始化session_state
            if 'selected_regions' not in st.session_state:
                st.session_state.selected_regions = list(all_regions)
            
            # 按钮行 - 使用更紧凑的布局
            button_col1, button_col2, button_col3 = st.columns([1, 1, 2])
            with button_col1:
                if st.button("全选", key="select_all_regions", use_container_width=True):
                    st.session_state.selected_regions = list(all_regions)
            with button_col2:
                if st.button("清空", key="clear_all_regions", use_container_width=True):
                    st.session_state.selected_regions = []
            
            # 多选框
            selected_regions = st.multiselect(
                "选择地区", 
                all_regions, 
                default=st.session_state.selected_regions,
                key="regions_multiselect"
            )
            
            # 更新session_state
            st.session_state.selected_regions = selected_regions
        else:
            selected_regions = []
    
    with col2:
        if '产品类别' in df.columns:
            # 获取所有产品类别选项
            all_categories = df['产品类别'].unique()
            
            # 初始化session_state
            if 'selected_categories' not in st.session_state:
                st.session_state.selected_categories = list(all_categories)
            
            # 按钮行 - 使用更紧凑的布局
            button_col1, button_col2, button_col3 = st.columns([1, 1, 2])
            with button_col1:
                if st.button("全选", key="select_all_categories", use_container_width=True):
                    st.session_state.selected_categories = list(all_categories)
            with button_col2:
                if st.button("清空", key="clear_all_categories", use_container_width=True):
                    st.session_state.selected_categories = []
            
            # 多选框
            selected_categories = st.multiselect(
                "选择产品类别", 
                all_categories, 
                default=st.session_state.selected_categories,
                key="categories_multiselect"
            )
            
            # 更新session_state
            st.session_state.selected_categories = selected_categories
        else:
            selected_categories = []
    
    with col3:
        if '日期' in df.columns:
            date_range = st.date_input("选择日期范围", value=(df['日期'].min().date(), df['日期'].max().date()))
        else:
            date_range = None
    
    # 应用筛选
    filtered_df = df.copy()
    if selected_regions:
        filtered_df = filtered_df[filtered_df['地区'].isin(selected_regions)]
    if selected_categories:
        filtered_df = filtered_df[filtered_df['产品类别'].isin(selected_categories)]
    if date_range and len(date_range) == 2:
        filtered_df = filtered_df[
            (filtered_df['日期'].dt.date >= date_range[0]) &
            (filtered_df['日期'].dt.date <= date_range[1])
        ]
    
    # 图表区域
    st.subheader("📈 数据可视化")
    
    tab1, tab2, tab3, tab4 = st.tabs(["销售趋势", "产品分析", "地区分析", "客户分析"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            if '月份' in filtered_df.columns and '销售额' in filtered_df.columns:
                monthly_sales = filtered_df.groupby('月份')['销售额'].sum().reset_index()
                # 将月份格式化为 "2023-06" 的形式
                monthly_sales['月份'] = monthly_sales['月份'].dt.strftime('%Y-%m')
                # 确保月份列被当作字符串处理
                monthly_sales['月份'] = monthly_sales['月份'].astype(str)
                
                fig_monthly = px.line(monthly_sales, x='月份', y='销售额', title="月度销售趋势")
                # 配置X轴，确保使用我们指定的格式
                fig_monthly.update_xaxes(
                    type='category',  # 强制作为分类变量
                    tickangle=45,     # 倾斜标签以防重叠
                    tickmode='array',
                    ticktext=monthly_sales['月份'].tolist(),
                    tickvals=monthly_sales['月份'].tolist()
                )
                st.plotly_chart(fig_monthly, use_container_width=True)
        
        with col2:
            if '季度' in filtered_df.columns and '销售额' in filtered_df.columns:
                quarterly_sales = filtered_df.groupby('季度')['销售额'].sum().reset_index()
                quarterly_sales['季度'] = quarterly_sales['季度'].astype(str)
                
                fig_quarterly = px.bar(quarterly_sales, x='季度', y='销售额', title="季度销售对比")
                st.plotly_chart(fig_quarterly, use_container_width=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            if '产品类别' in filtered_df.columns and '销售额' in filtered_df.columns:
                category_sales = filtered_df.groupby('产品类别')['销售额'].sum().reset_index()
                fig_pie = px.pie(category_sales, values='销售额', names='产品类别', title="产品类别销售占比")
                st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            if '产品名称' in filtered_df.columns and '数量' in filtered_df.columns:
                product_sales = filtered_df.groupby('产品名称')['数量'].sum().sort_values(ascending=True).tail(10)
                fig_bar = px.bar(x=product_sales.values, y=product_sales.index, orientation='h', title="产品销量排行 (Top 10)")
                st.plotly_chart(fig_bar, use_container_width=True)
    
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            if '地区' in filtered_df.columns and '销售额' in filtered_df.columns:
                region_sales = filtered_df.groupby('地区')['销售额'].sum().reset_index()
                fig_region = px.bar(region_sales, x='地区', y='销售额', title="各地区销售情况")
                st.plotly_chart(fig_region, use_container_width=True)
        
        with col2:
            if '地区' in filtered_df.columns:
                region_orders = filtered_df.groupby('地区').size().reset_index(name='订单数')
                fig_orders = px.scatter(region_orders, x='地区', y='订单数', size='订单数', title="各地区订单数量")
                st.plotly_chart(fig_orders, use_container_width=True)
    
    with tab4:
        col1, col2 = st.columns(2)
        
        with col1:
            if '客户类型' in filtered_df.columns and '销售额' in filtered_df.columns:
                customer_sales = filtered_df.groupby('客户类型')['销售额'].sum().reset_index()
                fig_customer = px.pie(customer_sales, values='销售额', names='客户类型', title="客户类型销售占比")
                st.plotly_chart(fig_customer, use_container_width=True)
        
        with col2:
            if '支付方式' in filtered_df.columns:
                payment_methods = filtered_df['支付方式'].value_counts().reset_index()
                payment_methods.columns = ['支付方式', '使用次数']
                fig_payment = px.bar(payment_methods, x='支付方式', y='使用次数', title="支付方式使用情况")
                st.plotly_chart(fig_payment, use_container_width=True)
    
    # 数据表格
    with st.expander("📋 数据详情", expanded=False):
        st.dataframe(filtered_df, use_container_width=True, height=400)
    
    # 数据统计
    st.subheader("📊 数据统计")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**数值型数据统计:**")
        numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            # 格式化数值统计表格
            stats_df = filtered_df[numeric_cols].describe()
            # 格式化数值，保留2位小数
            stats_df = stats_df.round(2)
            # 使用更紧凑的表格样式
            st.dataframe(
                stats_df,
                use_container_width=True,
                height=300,
                column_config={
                    col: st.column_config.NumberColumn(
                        col,
                        format="%.2f",
                        width="medium"
                    ) for col in stats_df.columns
                }
            )
        else:
            st.info("没有数值型数据列")
    
    with col2:
        st.write("**分类数据统计:**")
        categorical_cols = filtered_df.select_dtypes(include=['object']).columns
        if len(categorical_cols) > 0:
            # 为每个分类字段创建单独的统计表格
            for col in categorical_cols:
                with st.expander(f"📊 {col} 统计", expanded=False):
                    value_counts = filtered_df[col].value_counts()
                    total_count = len(filtered_df)
                    
                    # 创建统计表格
                    stats_data = []
                    for value, count in value_counts.head(10).items():  # 显示前10个
                        percentage = (count / total_count) * 100
                        stats_data.append({
                            '值': str(value)[:30] + '...' if len(str(value)) > 30 else str(value),
                            '频次': count,
                            '占比(%)': f"{percentage:.1f}%"
                        })
                    
                    if stats_data:
                        stats_df = pd.DataFrame(stats_data)
                        st.dataframe(
                            stats_df,
                            use_container_width=True,
                            height=min(300, len(stats_data) * 35 + 50),  # 动态调整高度
                            column_config={
                                '值': st.column_config.TextColumn('值', width="medium"),
                                '频次': st.column_config.NumberColumn('频次', format="%d"),
                                '占比(%)': st.column_config.TextColumn('占比(%)', width="small")
                            }
                        )
                        
                        # 显示汇总信息
                        unique_count = value_counts.nunique()
                        st.caption(f"📈 总计: {total_count} 条记录 | 唯一值: {unique_count} 个")
                        
                        # 如果有更多数据，显示提示
                        if len(value_counts) > 10:
                            st.caption(f"💡 显示前10个值，共{len(value_counts)}个唯一值")
                    else:
                        st.info("该字段没有数据")
        else:
            st.info("没有分类数据列")

else:
    st.error("无法加载数据，请检查数据源或文件格式。")

# 页脚
st.markdown("---")
st.markdown("📊 BI数据分析系统 | 基于 Streamlit 构建 | 版本 1.0") 