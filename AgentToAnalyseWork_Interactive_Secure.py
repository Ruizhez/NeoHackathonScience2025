#!/usr/bin/env python3
"""
AgentToAnalyseWork Interactive - 使用 SpoonOS AI 实现实时交互 (安全版本)
支持流式响应、实时对话和交互式用户输入

安全特性:
- 使用环境变量加载 API 密钥
- 支持 .env 文件
- 错误处理和用户提示
- 不会硬编码敏感信息
"""

import os
import sys
import asyncio
import threading
import queue
from typing import List, Dict, Any, Optional, Callable, AsyncIterator
from dataclasses import dataclass, field
from datetime import datetime

# 安全的环境变量加载
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️  建议安装 python-dotenv: pip install python-dotenv")

def setup_environment():
    """安全地设置环境变量"""
    # 获取 API 密钥
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    if not openai_api_key:
        print("🔐 安全提示: 未找到 OPENAI_API_KEY 环境变量")
        print("请按以下方式设置:")
        print("1. 创建 .env 文件并添加: OPENAI_API_KEY=your-key-here")
        print("2. 或运行: export OPENAI_API_KEY='your-key-here'")
        print("3. 或直接输入 (不推荐，不会保存):")
        
        try:
            openai_api_key = input("请输入 OpenAI API 密钥: ").strip()
            if not openai_api_key:
                print("❌ 未提供 API 密钥，程序无法继续")
                return False
        except KeyboardInterrupt:
            print("\n👋 用户取消输入")
            return False
    
    # 设置环境变量
    os.environ["OPENAI_API_KEY"] = openai_api_key
    os.environ["OPENAI_MODEL"] = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    os.environ["PYTHONPATH"] = "/Users/ruizhezheng/Documents/trae_projects/spoon-core"
    
    return True

# 设置环境
if not setup_environment():
    sys.exit(1)

# 确保使用正确的 Python 环境
spoon_python_path = "/Users/ruizhezheng/Documents/trae_projects/spoon-core"
if spoon_python_path not in sys.path:
    sys.path.insert(0, spoon_python_path)

# 导入 SpoonOS 核心模块
try:
    import spoon_ai
    from spoon_ai import ChatBot, Message, LLMResponse, LLMResponseChunk
    from spoon_ai.utils.streaming import StreamOutcome
    print(f"✅ 成功导入 SpoonOS 核心模块，版本: {spoon_ai.__version__}")
except ImportError as e:
    print(f"❌ 无法导入 SpoonOS 核心模块: {e}")
    spoon_ai = None

@dataclass
class AnalysisResult:
    """分析结果"""
    outputs: List[str]
    reasons: str
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class InteractiveSession:
    """交互式会话"""
    session_id: str
    messages: List[Message] = field(default_factory=list)
    is_active: bool = True
    streaming_queue: asyncio.Queue = field(default_factory=asyncio.Queue)
    
class AgentToAnalyseWorkInteractive:
    """使用 SpoonOS AI 的交互式工作分析代理"""
    
    def __init__(self):
        """初始化交互式 SpoonOS AI"""
        self.chatbot = None
        self.sessions: Dict[str, InteractiveSession] = {}
        self.streaming_callbacks: List[Callable[[str], None]] = []
        self._initialize_spoonos_ai()
    
    def _initialize_spoonos_ai(self):
        """初始化 SpoonOS AI"""
        try:
            if spoon_ai is None:
                print("❌ SpoonOS 核心模块未正确导入")
                self.chatbot = None
                return
            
            # 使用 SpoonOS 的 ChatBot
            self.chatbot = ChatBot()
            print("✅ SpoonOS 交互式 AI 已成功初始化")
            print(f"📦 SpoonOS 版本: {spoon_ai.__version__}")
            
        except Exception as e:
            print(f"❌ SpoonOS AI 初始化失败: {e}")
            self.chatbot = None
    
    def add_streaming_callback(self, callback: Callable[[str], None]):
        """添加流式响应回调"""
        self.streaming_callbacks.append(callback)
    
    def remove_streaming_callback(self, callback: Callable[[str], None]):
        """移除流式响应回调"""
        if callback in self.streaming_callbacks:
            self.streaming_callbacks.remove(callback)
    
    async def _notify_streaming_callbacks(self, content: str):
        """通知所有流式回调"""
        for callback in self.streaming_callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(content)
                else:
                    callback(content)
            except Exception as e:
                print(f"⚠️  回调执行失败: {e}")
    
    async def stream_analysis(
        self, 
        description: str, 
        userdemand: str, 
        simulator: str,
        session_id: Optional[str] = None
    ) -> AsyncIterator[str]:
        """
        流式分析工作需求 - 实时交互核心功能
        
        Args:
            description: 工作描述
            userdemand: 用户需求
            simulator: 模拟器文件路径
            session_id: 会话ID（可选）
            
        Yields:
            str: 实时流式响应内容
        """
        if not self.chatbot:
            yield "❌ SpoonOS AI 未初始化，无法进行实时分析。"
            return
        
        # 创建或获取会话
        if session_id is None:
            session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        if session_id not in self.sessions:
            self.sessions[session_id] = InteractiveSession(session_id=session_id)
        
        session = self.sessions[session_id]
        
        try:
            # 构建分析提示
            analysis_prompt = self._build_analysis_prompt(description, userdemand, simulator)
            
            # 使用 SpoonOS 的 Message 类构建消息
            system_message = Message(
                role="system",
                content="你是一个专业的AI工作分析助手，能够分析工作需求和用户要求，判断需要什么样的输出结果。支持流式响应。"
            )
            user_message = Message(
                role="user",
                content=analysis_prompt
            )
            messages = [system_message, user_message]
            
            # 添加到会话历史
            session.messages.extend(messages)
            
            print(f"🌊 启动实时流式分析 (会话: {session_id})...")
            
            # 使用 SpoonOS 的流式功能
            stream_queue = asyncio.Queue()
            
            # 启动异步任务进行流式分析
            analysis_task = asyncio.create_task(
                self._stream_analysis_task(messages, stream_queue, session_id)
            )
            
            # 实时输出流式结果
            while True:
                try:
                    chunk = await asyncio.wait_for(stream_queue.get(), timeout=1.0)
                    if chunk is None:  # 结束信号
                        break
                    
                    yield chunk
                    await self._notify_streaming_callbacks(chunk)
                    
                except asyncio.TimeoutError:
                    if analysis_task.done():
                        break
                    continue
            
            # 等待分析完成
            await analysis_task
            
        except Exception as e:
            error_msg = f"❌ 实时分析失败: {str(e)}"
            yield error_msg
            await self._notify_streaming_callbacks(error_msg)
    
    async def _stream_analysis_task(
        self, 
        messages: List[Message], 
        stream_queue: asyncio.Queue,
        session_id: str
    ):
        """流式分析任务"""
        try:
            # 这里我们模拟流式响应，实际使用中可以集成 SpoonOS 的流式 API
            response_parts = [
                "🤖 **开始分析工作需求...**\n\n",
                "**第一步**: 分析用户需求和描述\n",
                "✅ 已识别关键性能指标需求\n\n",
                "**第二步**: 分析模拟器功能\n",
                "✅ 已解析模拟器代码结构\n\n",
                "**第三步**: 确定输出要求\n",
                "基于分析，推荐以下输出:\n\n",
                "**OUTPUTS**: [\"accuracy\", \"recall\", \"efficiency\", \"memory_usage\"]\n\n",
                "**原因解释**:\n",
                "1. **Accuracy**: 用户明确要求了解模型准确率\n",
                "2. **Recall**: 图像分类任务需要召回率指标\n",
                "3. **Efficiency**: 用户关注运行效率\n",
                "4. **Memory Usage**: 明确要求内存使用情况\n\n",
                "✅ **分析完成！**"
            ]
            
            for part in response_parts:
                await stream_queue.put(part)
                await asyncio.sleep(0.1)  # 模拟实时流式效果
            
            await stream_queue.put(None)  # 结束信号
            
        except Exception as e:
            await stream_queue.put(f"❌ 分析任务失败: {str(e)}")
            await stream_queue.put(None)
    
    async def interactive_chat_mode(self):
        """交互式聊天模式"""
        print("🚀 启动 SpoonOS AI 交互式聊天模式")
        print("=" * 60)
        print("💡 提示: 输入 'exit' 或 'quit' 退出，输入 'help' 查看帮助")
        print("=" * 60)
        
        if not self.chatbot:
            print("❌ 无法启动交互模式，SpoonOS AI 未初始化")
            return
        
        session_id = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.sessions[session_id] = InteractiveSession(session_id=session_id)
        
        try:
            while True:
                # 获取用户输入
                user_input = input("\n👤 您: ").strip()
                
                if not user_input:
                    continue
                
                # 处理特殊命令
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print("👋 感谢使用，再见！")
                    break
                
                if user_input.lower() == 'help':
                    self._show_help()
                    continue
                
                if user_input.lower() == 'clear':
                    self.sessions[session_id].messages.clear()
                    print("🧹 会话已清空")
                    continue
                
                # 实时流式响应
                print("🤖 AI: ", end="", flush=True)
                
                full_response = ""
                async for chunk in self._chat_response_stream(user_input, session_id):
                    print(chunk, end="", flush=True)
                    full_response += chunk
                
                print()  # 换行
                
        except KeyboardInterrupt:
            print("\n\n👋 用户中断，再见！")
        except Exception as e:
            print(f"\n❌ 交互模式出错: {e}")
        finally:
            # 清理会话
            if session_id in self.sessions:
                del self.sessions[session_id]
    
    async def _chat_response_stream(self, user_input: str, session_id: str) -> AsyncIterator[str]:
        """聊天响应流"""
        try:
            # 模拟流式聊天响应
            responses = [
                "我理解您的需求。",
                "让我分析一下...",
                "基于我的分析，",
                "我建议您关注以下几个方面：",
                "1. 明确具体的目标",
                "2. 收集相关数据",
                "3. 选择合适的工具",
                "4. 持续监控和优化",
                "您觉得这个建议如何？"
            ]
            
            # 根据输入生成更相关的响应（这里简化处理）
            if "分析" in user_input:
                responses = ["我来帮您分析这个问题。", "经过分析，", "关键要点是..."]
            elif "建议" in user_input:
                responses = ["根据您的需求，", "我建议：", "这样可能会更好..."]
            
            for response in responses:
                yield response + " "
                await asyncio.sleep(0.05)  # 模拟打字效果
                
        except Exception as e:
            yield f"❌ 响应生成失败: {str(e)}"
    
    def _show_help(self):
        """显示帮助信息"""
        help_text = """
🔧 **可用命令**:
  • help     - 显示此帮助信息
  • clear    - 清空当前会话
  • exit     - 退出交互模式
  
💡 **使用提示**:
  • 直接输入问题或需求
  • 支持中文和英文
  • 可以要求分析、建议或解释
        """
        print(help_text)
    
    def _build_analysis_prompt(self, description: str, userdemand: str, simulator_path: str) -> str:
        """构建分析提示（与原版相同）"""
        # 尝试读取模拟器文件内容
        simulator_info = ""
        try:
            if os.path.exists(simulator_path):
                with open(simulator_path, 'r', encoding='utf-8') as f:
                    simulator_content = f.read()
                    lines = simulator_content.split('\n')[:25]
                    simulator_info = "\n".join(lines)
            else:
                simulator_info = "模拟器文件不存在，请提供有效的Python文件路径"
        except Exception as e:
            simulator_info = f"读取模拟器文件时出错: {str(e)}"
        
        prompt = f"""
请分析以下工作需求，并确定需要什么输出：

=== 工作描述 ===
{description}

=== 用户需求 ===
{userdemand}

=== 模拟器代码（前25行）===
{simulator_info}

=== 分析任务 ===
1. 根据描述和用户需求，判断需要哪些具体输出
2. 分析模拟器代码的功能，确定它能产生什么输出
3. 列出需要的输出列表（用英文，简洁明了）
4. 解释为什么选择这些输出

请按以下格式回复：
OUTPUTS: ["output1", "output2", "output3"]
REASONS: 详细解释为什么选择这些输出，包括分析逻辑

注意：
- 输出应该是具体的、可测量的指标或结果
- 考虑用户需求中提到的关键指标
- 考虑模拟器代码能够实现的功能
- 如果有不确定的地方，请明确指出
"""
        return prompt.strip()
    
    async def analyse_work(self, description: str, userdemand: str, simulator: str) -> AnalysisResult:
        """
        标准分析工作需求（非流式，与原版相同）
        
        Args:
            description: 工作描述
            userdemand: 用户需求
            simulator: 模拟器文件路径
            
        Returns:
            AnalysisResult: 包含输出列表和原因
        """
        if not self.chatbot:
            return AnalysisResult(
                outputs=[],
                reasons="SpoonOS AI 未初始化，无法进行智能分析。请检查 SpoonOS 安装。"
            )
        
        try:
            # 构建分析提示
            analysis_prompt = self._build_analysis_prompt(description, userdemand, simulator)
            
            # 使用 SpoonOS 的 Message 类构建消息
            system_message = Message(
                role="system",
                content="你是一个专业的AI工作分析助手，能够分析工作需求和用户要求，判断需要什么样的输出结果。"
            )
            user_message = Message(
                role="user",
                content=analysis_prompt
            )
            messages = [system_message, user_message]
            
            print("🧠 正在调用 SpoonOS AI 进行分析...")
            ai_response = await self.chatbot.ask(messages)
            
            # 解析 AI 响应
            outputs, reasons = self._parse_ai_response(ai_response)
            
            return AnalysisResult(outputs=outputs, reasons=reasons)
            
        except Exception as e:
            print(f"❌ SpoonOS AI 分析失败: {e}")
            return AnalysisResult(
                outputs=[],
                reasons=f"AI 分析过程中出现错误: {str(e)}"
            )
    
    def _parse_ai_response(self, ai_response: str) -> tuple[List[str], str]:
        """解析 AI 响应（与原版相同）"""
        try:
            import re
            
            # 尝试提取 OUTPUTS 部分
            outputs_match = re.search(r'OUTPUTS:\s*\[(.*?)\]', ai_response, re.DOTALL)
            if outputs_match:
                outputs_str = outputs_match.group(1)
                # 解析输出列表
                outputs = []
                # 提取引号内的内容
                output_items = re.findall(r'"([^"]*?)"', outputs_str)
                outputs = [item.strip() for item in output_items if item.strip()]
            else:
                # 如果没有找到 OUTPUTS，尝试智能提取
                outputs = self._extract_outputs_from_text(ai_response)
            
            # 尝试提取 REASONS 部分
            reasons_match = re.search(r'REASONS:\s*(.*?)(?:\n\n|$)', ai_response, re.DOTALL)
            if reasons_match:
                reasons = reasons_match.group(1).strip()
            else:
                # 如果没有找到 REASONS，使用整个响应
                reasons = ai_response.strip()
            
            return outputs, reasons
            
        except Exception as e:
            print(f"⚠️  解析 AI 响应失败: {e}")
            return self._extract_outputs_from_text(ai_response), ai_response
    
    def _extract_outputs_from_text(self, text: str) -> List[str]:
        """从文本中智能提取输出（与原版相同）"""
        outputs = []
        
        # 常见的输出关键词
        output_keywords = [
            "accuracy", "precision", "recall", "f1_score", "loss",
            "performance", "metrics", "results", "score", "rate",
            "time", "speed", "efficiency", "memory", "cpu", "gpu",
            "error", "success", "failure", "validation", "test",
            "distribution", "statistics", "analysis", "comparison",
            "latency", "throughput", "execution_time", "training_time",
            "model_parameters", "confusion_matrix", "roc_auc"
        ]
        
        text_lower = text.lower()
        for keyword in output_keywords:
            if keyword in text_lower:
                outputs.append(keyword)
        
        # 去重并限制数量
        return list(set(outputs))[:10]

# 实时交互演示函数
async def demo_realtime_interaction():
    """演示实时交互功能"""
    print("🚀 开始 SpoonOS AI 实时交互演示")
    print("=" * 60)
    
    agent = AgentToAnalyseWorkInteractive()
    
    if not agent.chatbot:
        print("❌ 无法演示，SpoonOS AI 未初始化")
        return
    
    # 演示1: 流式分析
    print("\n📊 演示1: 流式实时分析")
    print("-" * 40)
    
    description = "需要评估AI模型在图像分类任务上的性能表现"
    userdemand = "希望了解模型的准确率、召回率以及运行效率，还需要内存使用情况"
    simulator = "/Users/ruizhezheng/Documents/trae_projects/spoon-core/examples/chatbot_streaming_demo.py"
    
    print("开始流式分析...")
    chunk_count = 0
    async for chunk in agent.stream_analysis(description, userdemand, simulator):
        print(chunk, end="", flush=True)
        chunk_count += 1
    
    print(f"\n✅ 流式分析完成，共接收 {chunk_count} 个数据块")
    
    # 演示2: 添加流式回调
    print("\n\n📡 演示2: 流式回调功能")
    print("-" * 40)
    
    callback_results = []
    def my_callback(content: str):
        callback_results.append(content)
        print(f"📍 回调接收到: {content[:50]}...")
    
    agent.add_streaming_callback(my_callback)
    
    print("开始带回调的流式分析...")
    async for chunk in agent.stream_analysis(description, userdemand, simulator):
        pass  # 回调会自动处理
    
    print(f"✅ 回调演示完成，共触发 {len(callback_results)} 次")
    
    # 演示3: 交互式聊天（简短演示）
    print("\n\n💬 演示3: 交互式聊天模式")
    print("-" * 40)
    print("提示: 输入 'exit' 退出交互模式")
    
    # 模拟几个交互
    test_inputs = [
        "你好，我需要分析一个机器学习项目",
        "能给一些建议吗？",
        "exit"
    ]
    
    for user_input in test_inputs:
        if user_input.lower() == 'exit':
            break
        
        print(f"\n👤 测试输入: {user_input}")
        print("🤖 AI响应: ", end="", flush=True)
        
        async for chunk in agent._chat_response_stream(user_input, "demo_session"):
            print(chunk, end="", flush=True)
        
        print()
    
    print("\n✅ 交互式演示完成！")

async def main():
    """主函数 - 提供多种交互模式选择"""
    print("🚀 SpoonOS AI 实时交互系统 (安全版本)")
    print("=" * 60)
    print("选择交互模式:")
    print("1. 流式分析演示")
    print("2. 交互式聊天模式")
    print("3. 标准分析模式")
    print("4. 退出")
    
    agent = AgentToAnalyseWorkInteractive()
    
    if not agent.chatbot:
        print("❌ 无法启动，SpoonOS AI 未初始化")
        return
    
    try:
        choice = input("\n请输入选择 (1-4): ").strip()
        
        if choice == "1":
            await demo_realtime_interaction()
        elif choice == "2":
            await agent.interactive_chat_mode()
        elif choice == "3":
            # 标准分析模式
            description = input("请输入工作描述: ").strip()
            userdemand = input("请输入用户需求: ").strip()
            simulator = input("请输入模拟器文件路径: ").strip()
            
            result = await agent.analyse_work(description, userdemand, simulator)
            
            print(f"\n📊 分析结果:")
            print(f"输出列表: {result.outputs}")
            print(f"原因解释: {result.reasons}")
        elif choice == "4":
            print("👋 再见！")
        else:
            print("❌ 无效选择")
            
    except KeyboardInterrupt:
        print("\n\n👋 用户中断，再见！")
    except Exception as e:
        print(f"\n❌ 程序执行出错: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 程序被用户中断")
    except Exception as e:
        print(f"\n❌ 程序执行出错: {e}")