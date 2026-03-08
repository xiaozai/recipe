# Tech Trend Analyzer

AI 驱动的技术趋势分析工具，搜索和分析技术在不同平台上的使用情况，提供洞察和建议。

## 功能特性

- 🔍 **多数据源搜索**: GitHub、Hacker News、Reddit、Web 搜索
- 🤖 **AI 智能分析**: 支持 Anthropic Claude、OpenAI GPT 及 OpenAI 兼容服务
- 📊 **可视化图表**: 来源分布图、关键词云、热度分布图
- 🌐 **中英文切换**: 支持中英文界面切换，默认中文
- ⚙️ **设置页面**: 可视化配置 API、数据源等
- 📈 **趋势分析**: 识别上升、稳定、下降趋势
- 💡 **机会发现**: 发现未被开发的市场机会
- 📝 **报告导出**: 导出 Markdown 格式报告

## 快速开始

### 后端设置

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 复制环境配置
cp .env.example .env
# 编辑 .env 填入 API 密钥

# 启动服务
python main.py
```

### 前端设置

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

访问 http://localhost:5173 开始使用。

### Docker 部署

```bash
# 设置环境变量
export API_KEY=your_key

# 启动服务
docker-compose up -d
```

## 配置

在 `backend/.env` 文件中配置：

### Anthropic Claude

```env
API_KEY=sk-ant-xxx
BASE_URL=https://api.anthropic.com
MODEL_NAME=claude-sonnet-4-6
API_TYPE=anthropic
```

### OpenAI GPT

```env
API_KEY=sk-xxx
BASE_URL=https://api.openai.com/v1
MODEL_NAME=gpt-4-turbo
API_TYPE=openai
```

### OpenAI 兼容服务 (DeepSeek、智谱、Ollama 等)

```env
API_KEY=your_key
BASE_URL=https://api.deepseek.com/v1
MODEL_NAME=deepseek-chat
API_TYPE=openai
```

### 本地 Ollama

```env
API_KEY=ollama
BASE_URL=http://localhost:11434/v1
MODEL_NAME=llama2
API_TYPE=openai
```

## 使用指南

### 1. 搜索分析

1. 在首页输入技术关键词（如 `claude-code`、`langchain`）
2. 点击"过滤条件"选择数据源和返回数量
3. 点击"分析"开始搜索

### 2. 查看结果

分析完成后会显示：
- **概览统计**: 收集项目数、洞察数、趋势数、用例数
- **来源分布图**: 各数据源的内容占比
- **关键词云**: 高频关键词展示
- **热度分布图**: 用例热度排行
- **分析总结**: AI 生成的技术总结
- **关键洞察**: 重要的发现和见解
- **热门用例**: 技术的主要应用场景
- **趋势分析**: 技术发展方向
- **机会发现**: 潜在的市场机会

### 3. 设置页面

点击导航栏"设置"可以配置：
- LLM API 配置（密钥、URL、模型）
- 搜索默认配置（数据源、数量）
- 界面语言

## API 接口

### 搜索

- `GET /api/v1/search/{keyword}` - 跨源搜索
- `GET /api/v1/search/sources/list` - 获取数据源列表

### 分析

- `POST /api/v1/analyze/` - 启动异步分析
- `GET /api/v1/analyze/status/{task_id}` - 查询分析状态
- `POST /api/v1/analyze/sync` - 同步分析

### 设置

- `GET /api/v1/settings` - 获取设置
- `PUT /api/v1/settings` - 更新设置

## 项目结构

```
tech-trend-analyzer/
├── backend/
│   ├── app/
│   │   ├── api/v1/        # API 接口
│   │   ├── collectors/    # 数据收集器
│   │   ├── ai/            # AI 分析引擎
│   │   ├── models/        # 数据模型
│   │   └── processors/    # 数据处理
│   └── main.py
├── frontend/
│   ├── src/
│   │   ├── components/    # React 组件
│   │   │   └── Charts/    # 图表组件
│   │   ├── pages/         # 页面组件
│   │   ├── services/      # API 服务
│   │   ├── stores/        # 状态管理
│   │   └── i18n/          # 国际化
│   └── package.json
└── docker-compose.yml
```

## 技术栈

- **后端**: Python 3.10+、FastAPI、Pydantic
- **前端**: React 18、TypeScript、Vite、TailwindCSS
- **图表**: Recharts
- **状态管理**: Zustand
- **AI**: 支持 Anthropic、OpenAI API

## License

MIT