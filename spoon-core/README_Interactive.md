# SpoonOS AI 实时交互系统

## 🚀 功能特性

### 实时交互功能
- **流式响应**: 实时显示AI分析过程，逐字输出结果
- **交互式聊天**: 支持连续对话，上下文记忆
- **会话管理**: 多会话支持，独立上下文管理
- **流式回调**: 支持自定义回调函数处理实时数据

### 安全特性
- **环境变量**: 使用 `.env` 文件管理API密钥，不再硬编码
- **错误处理**: 完善的错误处理和用户提示
- **安全提示**: 明确的密钥管理指导

## 📋 快速开始

### 1. 环境配置

创建 `.env` 文件：
```bash
cp .env.example .env
```

编辑 `.env` 文件，添加您的API密钥：
```
OPENAI_API_KEY=your-actual-api-key-here
OPENAI_MODEL=gpt-4o-mini
```

### 2. 运行交互式系统

```bash
# 运行安全版本
python AgentToAnalyseWork_Interactive_Secure.py

# 运行演示版本（流式分析演示）
python AgentToAnalyseWork_Interactive.py
```

### 3. 选择交互模式

系统提供4种交互模式：

1. **流式分析演示** - 观看实时分析过程
2. **交互式聊天模式** - 与AI进行自然对话
3. **标准分析模式** - 传统的一次性分析
4. **退出** - 结束程序

## 💡 使用示例

### 流式分析示例
```python
import asyncio
from AgentToAnalyseWork_Interactive_Secure import AgentToAnalyseWorkInteractive

async def main():
    agent = AgentToAnalyseWorkInteractive()
    
    # 流式分析
    async for chunk in agent.stream_analysis(
        description="需要评估AI模型性能",
        userdemand="希望了解准确率和效率",
        simulator="path/to/simulator.py"
    ):
        print(chunk, end="", flush=True)

asyncio.run(main())
```

### 交互式聊天
```bash
🚀 启动 SpoonOS AI 交互式聊天模式
============================================================
💡 提示: 输入 'exit' 或 'quit' 退出，输入 'help' 查看帮助
============================================================

👤 您: 你好，我需要分析一个机器学习项目
🤖 AI: 我理解您的需求。 让我分析一下... 基于我的分析，我建议您关注以下几个方面：
```

### 添加流式回调
```python
def my_callback(content: str):
    print(f"收到实时数据: {content}")

agent.add_streaming_callback(my_callback)
```

## 🔧 高级功能

### 会话管理
- 自动创建会话ID
- 支持多会话并行
- 会话历史记录

### 自定义流式处理
- 注册多个回调函数
- 支持异步回调
- 实时数据处理

### 错误处理
- API密钥验证
- 网络错误处理
- 优雅降级机制

## ⚠️ 安全注意事项

1. **永远不要**将API密钥硬编码在代码中
2. **始终**使用环境变量或安全的密钥管理系统
3. **不要**将 `.env` 文件提交到版本控制
4. **定期**轮换API密钥
5. **使用**只具有必要权限的密钥

## 🛠️ 依赖要求

```bash
pip install python-dotenv  # 环境变量管理
```

## 📁 文件结构

```
spoon-core/
├── AgentToAnalyseWork.py                    # 原始版本
├── AgentToAnalyseWork_Interactive.py        # 交互版本
├── AgentToAnalyseWork_Interactive_Secure.py # 安全版本（推荐）
├── .env.example                            # 环境变量模板
├── .env                                    # 您的实际配置（不提交）
└── README_Interactive.md                  # 本文档
```

## 🎯 下一步计划

- [ ] WebSocket 实时通信支持
- [ ] 浏览器前端界面
- [ ] 多用户并发支持
- [ ] 更丰富的可视化展示
- [ ] 与 SpoonOS 深度集成

## 💬 使用技巧

1. **流式响应**: 适合长时间运行的分析任务
2. **交互模式**: 适合探索和迭代式分析
3. **回调函数**: 适合集成到其他系统中
4. **会话管理**: 适合多任务并行处理

现在您已经拥有了完整的 SpoonOS AI 实时交互系统！🎉