# 🐍 Conda环境使用说明

## 📋 前提条件

确保您的系统已安装Anaconda或Miniconda：
- **Anaconda**: https://www.anaconda.com/products/distribution
- **Miniconda**: https://docs.conda.io/en/latest/miniconda.html

## 🚀 快速开始

### 1. 创建Conda环境

**Windows用户：**
```bash
conda_setup.bat
```

**Linux/Mac用户：**
```bash
chmod +x conda_setup.sh
./conda_setup.sh
```

**手动创建：**
```bash
conda env create -f environment.yml
```

### 2. 激活环境

```bash
conda activate pybi
```

### 3. 启动系统

**方法一：使用启动脚本**

Windows:
```bash
conda_start.bat
```

Linux/Mac:
```bash
chmod +x conda_start.sh
./conda_start.sh
```

**方法二：手动启动**
```bash
conda activate pybi
streamlit run app.py
```

**方法三：直接运行（无需激活）**
```bash
conda run -n pybi streamlit run app.py
```

### 4. 访问系统

打开浏览器访问：http://localhost:8501

## 🔧 环境管理

### 查看环境列表
```bash
conda env list
```

### 激活环境
```bash
conda activate pybi
```

### 退出环境
```bash
conda deactivate
```

### 删除环境
```bash
conda env remove -n pybi
```

### 更新环境
```bash
conda env update -f environment.yml
```

## 📦 包管理

### 查看已安装的包
```bash
conda list
```

### 安装新包
```bash
conda install package_name
# 或
pip install package_name
```

### 更新包
```bash
conda update package_name
```

## 🐛 故障排除

### 环境创建失败
1. 检查网络连接
2. 尝试使用国内镜像：
   ```bash
   conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
   conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
   conda config --set show_channel_urls yes
   ```

### 包安装失败
1. 尝试使用pip安装：
   ```bash
   conda activate pybi
   pip install package_name
   ```

2. 使用conda-forge通道：
   ```bash
   conda install -c conda-forge package_name
   ```

### 环境激活失败
1. 检查环境是否存在：
   ```bash
   conda env list
   ```

2. 重新创建环境：
   ```bash
   conda env remove -n pybi
   conda env create -f environment.yml
   ```

## 📁 项目文件说明

| 文件 | 说明 |
|------|------|
| `environment.yml` | Conda环境配置文件 |
| `conda_setup.bat` | Windows环境设置脚本 |
| `conda_setup.sh` | Linux/Mac环境设置脚本 |
| `conda_start.bat` | Windows启动脚本 |
| `conda_start.sh` | Linux/Mac启动脚本 |

## 🎯 优势

使用Conda环境的优势：
- **环境隔离**: 避免包冲突
- **版本管理**: 精确控制依赖版本
- **跨平台**: 支持Windows、Linux、Mac
- **易于部署**: 一键创建相同环境
- **包管理**: 强大的包依赖解析

## 📚 更多资源

- [Conda官方文档](https://docs.conda.io/)
- [Streamlit文档](https://docs.streamlit.io/)
- [项目README](README.md)
- [快速开始指南](快速开始.md)

---

**祝您使用愉快！** 🎊 