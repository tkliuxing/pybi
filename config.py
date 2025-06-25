"""
BI系统配置文件
包含系统设置、常量和其他配置项
"""

# 页面配置
PAGE_CONFIG = {
    "page_title": "BI数据分析系统",
    "page_icon": "📊",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# 数据字段配置
REQUIRED_FIELDS = ['日期', '销售额']
OPTIONAL_FIELDS = ['产品类别', '产品名称', '数量', '地区', '客户类型', '支付方式']

# 支持的文件格式
SUPPORTED_FILE_TYPES = ['csv', 'xlsx', 'xls']

# 图表配置
CHART_CONFIG = {
    "height": 400,
    "template": "plotly_white",
    "color_scale": "Blues"
}

# 筛选器配置
FILTER_CONFIG = {
    "max_selections": 10,
    "default_all": True
}

# 示例数据配置
SAMPLE_DATA_CONFIG = {
    "start_date": "2023-01-01",
    "end_date": "2023-12-31",
    "categories": ['电子产品', '服装', '食品', '家居', '图书'],
    "products": ['iPhone', 'MacBook', 'T恤', '牛仔裤', '面包', '牛奶', '沙发', '台灯', '小说', '教材'],
    "regions": ['北京', '上海', '广州', '深圳', '杭州'],
    "customer_types": ['个人', '企业', 'VIP'],
    "payment_methods": ['信用卡', '支付宝', '微信', '现金'],
    "sales_range": (100, 5000),
    "quantity_range": (1, 10)
}

# 主题配置
THEME_CONFIG = {
    "primary_color": "#1f77b4",
    "secondary_color": "#ff7f0e",
    "background_color": "#f8f9fa",
    "text_color": "#333333"
}

# CSS样式
CUSTOM_CSS = """
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    .stButton > button {
        background-color: #1f77b4;
        color: white;
        border-radius: 0.5rem;
        border: none;
        padding: 0.5rem 1rem;
    }
    .stButton > button:hover {
        background-color: #1565c0;
    }
</style>
"""

# 服务器配置
SERVER_CONFIG = {
    "port": 8501,
    "address": "localhost",
    "enable_cors": True,
    "enable_xsrf_protection": True
}

# 缓存配置
CACHE_CONFIG = {
    "ttl": 3600,  # 1小时
    "max_entries": 100
}

# 导出配置
EXPORT_CONFIG = {
    "max_rows": 10000,
    "formats": ['csv', 'excel'],
    "encoding": 'utf-8'
}

# 错误消息
ERROR_MESSAGES = {
    "file_not_found": "文件未找到",
    "invalid_format": "文件格式不支持",
    "missing_fields": "缺少必需字段",
    "data_error": "数据处理错误",
    "upload_failed": "文件上传失败"
}

# 成功消息
SUCCESS_MESSAGES = {
    "file_uploaded": "文件上传成功",
    "data_loaded": "数据加载成功",
    "export_success": "数据导出成功"
} 