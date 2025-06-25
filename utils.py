"""
BI系统工具函数模块
包含数据处理、分析和可视化的辅助函数
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io

def validate_data(df):
    """
    验证数据格式是否符合要求
    
    Args:
        df (pd.DataFrame): 待验证的数据框
        
    Returns:
        tuple: (是否有效, 错误信息列表)
    """
    errors = []
    
    # 检查必需字段
    required_fields = ['日期', '销售额']
    for field in required_fields:
        if field not in df.columns:
            errors.append(f"缺少必需字段: {field}")
    
    # 检查数据类型
    if '日期' in df.columns:
        try:
            pd.to_datetime(df['日期'])
        except:
            errors.append("日期字段格式不正确")
    
    if '销售额' in df.columns:
        if not pd.api.types.is_numeric_dtype(df['销售额']):
            errors.append("销售额字段必须是数值类型")
    
    return len(errors) == 0, errors

def preprocess_data(df):
    """
    数据预处理
    
    Args:
        df (pd.DataFrame): 原始数据框
        
    Returns:
        pd.DataFrame: 预处理后的数据框
    """
    df_processed = df.copy()
    
    # 处理日期字段
    if '日期' in df_processed.columns:
        df_processed['日期'] = pd.to_datetime(df_processed['日期'])
        df_processed['月份'] = df_processed['日期'].dt.to_period('M')
        df_processed['季度'] = df_processed['日期'].dt.to_period('Q')
        df_processed['年份'] = df_processed['日期'].dt.year
        df_processed['星期'] = df_processed['日期'].dt.day_name()
    
    # 处理数值字段
    numeric_fields = ['销售额', '数量']
    for field in numeric_fields:
        if field in df_processed.columns:
            df_processed[field] = pd.to_numeric(df_processed[field], errors='coerce')
    
    return df_processed

def calculate_kpis(df):
    """
    计算关键绩效指标
    
    Args:
        df (pd.DataFrame): 数据框
        
    Returns:
        dict: KPI字典
    """
    kpis = {}
    
    if '销售额' in df.columns:
        kpis['总销售额'] = df['销售额'].sum()
        kpis['平均销售额'] = df['销售额'].mean()
        kpis['最大销售额'] = df['销售额'].max()
        kpis['最小销售额'] = df['销售额'].min()
    
    kpis['总订单数'] = len(df)
    
    if '销售额' in df.columns and len(df) > 0:
        kpis['平均订单金额'] = df['销售额'].sum() / len(df)
    
    if '客户类型' in df.columns:
        kpis['客户类型数'] = df['客户类型'].nunique()
    
    if '地区' in df.columns:
        kpis['地区数'] = df['地区'].nunique()
    
    if '产品类别' in df.columns:
        kpis['产品类别数'] = df['产品类别'].nunique()
    
    return kpis

def create_sales_trend_chart(df, period='month'):
    """
    创建销售趋势图表
    
    Args:
        df (pd.DataFrame): 数据框
        period (str): 时间周期 ('month', 'quarter', 'week')
        
    Returns:
        plotly.graph_objects.Figure: 图表对象
    """
    if '销售额' not in df.columns:
        return None
    
    if period == 'month' and '月份' in df.columns:
        group_col = '月份'
    elif period == 'quarter' and '季度' in df.columns:
        group_col = '季度'
    elif period == 'week' and '星期' in df.columns:
        group_col = '星期'
    else:
        return None
    
    sales_data = df.groupby(group_col)['销售额'].sum().reset_index()
    sales_data[group_col] = sales_data[group_col].astype(str)
    
    fig = px.line(
        sales_data,
        x=group_col,
        y='销售额',
        title=f"{period.title()}销售趋势",
        markers=True
    )
    
    fig.update_layout(
        xaxis_title=period.title(),
        yaxis_title="销售额 (¥)",
        height=400
    )
    
    return fig

def create_category_analysis_chart(df, chart_type='pie'):
    """
    创建产品类别分析图表
    
    Args:
        df (pd.DataFrame): 数据框
        chart_type (str): 图表类型 ('pie', 'bar')
        
    Returns:
        plotly.graph_objects.Figure: 图表对象
    """
    if '产品类别' not in df.columns or '销售额' not in df.columns:
        return None
    
    category_data = df.groupby('产品类别')['销售额'].sum().reset_index()
    
    if chart_type == 'pie':
        fig = px.pie(
            category_data,
            values='销售额',
            names='产品类别',
            title="产品类别销售占比"
        )
    elif chart_type == 'bar':
        fig = px.bar(
            category_data,
            x='产品类别',
            y='销售额',
            title="产品类别销售情况",
            color='销售额',
            color_continuous_scale='Blues'
        )
    
    fig.update_layout(height=400)
    return fig

def create_region_analysis_chart(df):
    """
    创建地区分析图表
    
    Args:
        df (pd.DataFrame): 数据框
        
    Returns:
        plotly.graph_objects.Figure: 图表对象
    """
    if '地区' not in df.columns:
        return None
    
    # 地区销售情况
    region_sales = df.groupby('地区')['销售额'].sum().reset_index() if '销售额' in df.columns else None
    region_orders = df.groupby('地区').size().reset_index(name='订单数')
    
    if region_sales is not None:
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('各地区销售情况', '各地区订单数量'),
            specs=[[{"type": "bar"}, {"type": "scatter"}]]
        )
        
        # 销售柱状图
        fig.add_trace(
            go.Bar(x=region_sales['地区'], y=region_sales['销售额'], name='销售额'),
            row=1, col=1
        )
        
        # 订单散点图
        fig.add_trace(
            go.Scatter(x=region_orders['地区'], y=region_orders['订单数'], 
                      mode='markers', name='订单数', marker=dict(size=region_orders['订单数'])),
            row=1, col=2
        )
    else:
        fig = px.bar(
            region_orders,
            x='地区',
            y='订单数',
            title="各地区订单数量"
        )
    
    fig.update_layout(height=400, showlegend=False)
    return fig

def create_customer_analysis_chart(df):
    """
    创建客户分析图表
    
    Args:
        df (pd.DataFrame): 数据框
        
    Returns:
        plotly.graph_objects.Figure: 图表对象
    """
    if '客户类型' not in df.columns:
        return None
    
    # 客户类型分析
    customer_data = df.groupby('客户类型')['销售额'].sum().reset_index() if '销售额' in df.columns else None
    payment_data = df['支付方式'].value_counts().reset_index() if '支付方式' in df.columns else None
    
    if customer_data is not None and payment_data is not None:
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('客户类型销售占比', '支付方式使用情况'),
            specs=[[{"type": "pie"}, {"type": "bar"}]]
        )
        
        # 客户类型饼图
        fig.add_trace(
            go.Pie(labels=customer_data['客户类型'], values=customer_data['销售额'], name='客户类型'),
            row=1, col=1
        )
        
        # 支付方式柱状图
        fig.add_trace(
            go.Bar(x=payment_data['index'], y=payment_data['支付方式'], name='支付方式'),
            row=1, col=2
        )
    else:
        fig = px.pie(
            customer_data,
            values='销售额',
            names='客户类型',
            title="客户类型销售占比"
        )
    
    fig.update_layout(height=400, showlegend=False)
    return fig

def generate_summary_report(df):
    """
    生成数据摘要报告
    
    Args:
        df (pd.DataFrame): 数据框
        
    Returns:
        dict: 摘要报告字典
    """
    report = {}
    
    # 基本信息
    report['数据行数'] = len(df)
    report['数据列数'] = len(df.columns)
    report['时间范围'] = f"{df['日期'].min().date()} 至 {df['日期'].max().date()}" if '日期' in df.columns else "无日期数据"
    
    # 数值型数据统计
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        report['数值型字段统计'] = df[numeric_cols].describe().to_dict()
    
    # 分类数据统计
    categorical_cols = df.select_dtypes(include=['object']).columns
    if len(categorical_cols) > 0:
        report['分类字段统计'] = {}
        for col in categorical_cols:
            report['分类字段统计'][col] = df[col].value_counts().to_dict()
    
    return report

def export_data(df, format='csv'):
    """
    导出数据
    
    Args:
        df (pd.DataFrame): 数据框
        format (str): 导出格式 ('csv', 'excel')
        
    Returns:
        bytes: 导出的数据
    """
    if format == 'csv':
        return df.to_csv(index=False).encode('utf-8')
    elif format == 'excel':
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='数据')
        return output.getvalue()
    else:
        raise ValueError("不支持的导出格式") 