# 恋爱记录网站

一个帮助情侣记录恋爱点滴的网站应用。

## 功能特点

- 用户注册和登录
- 个人资料管理
- 恋爱关系管理
  - 发送恋爱申请
  - 接受/拒绝恋爱申请
  - 查看恋爱状态
- 地点记录
  - 记录共同去过的地方
  - 上传地点照片
  - 添加地点描述
- 活动记录
  - 记录共同参与的活动
  - 上传活动照片
  - 添加活动描述
- 心愿清单
  - 创建共同的心愿
  - 标记心愿完成状态
- 纪念日管理
  - 记录重要的日期
  - 自动计算纪念日

## 技术栈

- Python 3.8+
- Django 4.2
- Bootstrap 5
- MySQL
- Font Awesome 5

## 安装说明

1. 克隆项目:
```bash
git clone [repository-url]
cd love-site
```

2. 创建并激活 Conda 环境:
```bash
# 创建环境
conda create -n love-site python=3.8

# 激活环境
conda activate love-site
```

3. 安装依赖:
```bash
# 安装基础依赖
conda install django=4.2
conda install pymysql
conda install pillow

# 安装其他依赖
pip install -r requirements.txt
```

4. 配置数据库:
```bash
# 创建 MySQL 数据库
mysql -u root -p
CREATE DATABASE love_site CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 修改 config/settings.py 中的数据库配置
```

5. 数据库迁移:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. 运行开发服务器:
```bash
python manage.py runserver
```

## 项目结构

```
love-site/
├── config/             # 项目配置
├── core/              # 主应用
│   ├── migrations/    # 数据库迁移
│   ├── templates/    # HTML模板
│   ├── models.py     # 数据模型
│   ├── views.py      # 视图函数
│   ├── forms.py      # 表单类
│   └── urls.py       # URL配置
├── static/           # 静态文件
├── media/           # 用户上传文件
├── manage.py        # Django管理脚本
└── requirements.txt # 项目依赖
```

## 使用说明

1. 注册账号并登录
2. 完善个人资料
3. 发送恋爱申请给伴侣
4. 等待伴侣接受申请
5. 开始记录你们的点点滴滴:
   - 记录共同去过的地方
   - 记录共同参与的活动
   - 创建共同的心愿清单
   - 标记重要的纪念日

## 贡献指南

欢迎提交 Issue 和 Pull Request 来帮助改进项目。

## 许可证

MIT License