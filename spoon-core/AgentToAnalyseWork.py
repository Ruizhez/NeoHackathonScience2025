#!/usr/bin/env python3
"""
AgentToAnalyseWork - 使用 SpoonOS AI 分析工作需求
分析 description 和 userdemand 来判断怎样使用 simulator,
确定需要哪些输出并解释原因
"""

import os
import sys
import asyncio
from typing import List, Dict, Any
from dataclasses import dataclass

# 设置 SpoonOS 环境 - 安全地从环境变量加载
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 从环境变量获取 API 密钥（不再硬编码）
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    print("⚠️  警告: 未找到 OPENAI_API_KEY 环境变量")
    print("请设置环境变量: export OPENAI_API_KEY='your-api-key'")
    # 可以选择退出或要求用户输入
    openai_api_key = input("请输入 OpenAI API 密钥: ").strip()

os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ["OPENAI_MODEL"] = os.getenv("OPENAI_MODEL", "gpt-4o-mini")  # 使用默认值
os.environ["PYTHONPATH"] = "/Users/ruizhezheng/Documents/trae_projects/spoon-core"

# 确保使用正确的 Python 环境
spoon_python_path = "/Users/ruizhezheng/Documents/trae_projects/spoon-core"
if spoon_python_path not in sys.path:
    sys.path.insert(0, spoon_python_path)

# 导入 SpoonOS 核心模块
try:
    import spoon_ai
    from spoon_ai import ChatBot, Message, LLMResponse
    print(f"✅ 成功导入 SpoonOS 核心模块，版本: {spoon_ai.__version__}")
except ImportError as e:
    print(f"❌ 无法导入 SpoonOS 核心模块: {e}")
    spoon_ai = None

@dataclass
class AnalysisResult:
    """分析结果"""
    outputs: List[str]
    reasons: str

class AgentToAnalyseWork:
    """使用 SpoonOS AI 的工作分析代理"""
    
    def __init__(self):
        """初始化 SpoonOS AI"""
        self.chatbot = None
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
            print("✅ SpoonOS AI 已成功初始化")
            print(f"📦 SpoonOS 版本: {spoon_ai.__version__}")
            
        except Exception as e:
            print(f"❌ SpoonOS AI 初始化失败: {e}")
            self.chatbot = None
    
    async def analyse_work(self, description: str, userdemand: str, simulator: str) -> AnalysisResult:
        """
        使用 SpoonOS AI 分析工作需求
        
        Args:
            description: 工作描述
            userdemand: 用户需求
            simulator: 模拟器文件路径
            
        Returns:
            AnalysisResult: 包含输出列表和原因
        """
        print(f"🤖 使用 SpoonOS AI 分析工作...")
        print(f"描述: {description}")
        print(f"用户需求: {userdemand}")
        print(f"模拟器: {simulator}")
        
        if not self.chatbot:
            return AnalysisResult(
                outputs=[],
                reasons="SpoonOS AI 未初始化，无法进行智能分析。请检查 SpoonOS 安装。"
            )
        
        try:
            # 构建分析提示
            analysis_prompt = self._build_analysis_prompt(description, userdemand, simulator)
            
            # 使用 SpoonOS AI 进行分析
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
    
    def _build_analysis_prompt(self, description: str, userdemand: str, simulator_path: str) -> str:
        """构建分析提示"""
        
        # 尝试读取模拟器文件内容
        simulator_info = ""
        try:
            if os.path.exists(simulator_path):
                with open(simulator_path, 'r', encoding='utf-8') as f:
                    simulator_content = f.read()
                    # 只取前25行避免提示过长
                    lines = simulator_content.split('\n')[:25]
                    simulator_info = "\\n".join(lines)
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
    
    def _parse_ai_response(self, ai_response: str) -> tuple[List[str], str]:
        """解析 AI 响应"""
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
        """从文本中智能提取输出"""
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
    
    def ask_for_clarification(self, question: str) -> str:
        """请求澄清不确定的问题"""
        return f"❓ 需要澄清: {question}"

async def main():
    """示例用法"""
    print("🚀 启动 SpoonOS AI 工作分析代理")
    print("=" * 50)
    
    agent = AgentToAnalyseWork()
    
    if not agent.chatbot:
        print("❌ 无法使用 SpoonOS AI，请检查安装")
        return
    
    # 示例输入
    description = "需要评估AI模型在图像分类任务上的性能表现"
    userdemand = "希望了解模型的准确率、召回率以及运行效率，还需要内存使用情况"
    simulator = "/Users/ruizhezheng/Documents/trae_projects/spoon-core/examples/chatbot_streaming_demo.py"
    
    result = await agent.analyse_work(description, userdemand, simulator)
    
    print("\n📊 SpoonOS AI 分析结果:")
    print(f"输出列表: {result.outputs}")
    print(f"原因解释: {result.reasons}")
    
    # 如果有不确定的地方，可以提问
    if len(result.outputs) == 0:
        print(agent.ask_for_clarification("能否提供更具体的需求描述？"))

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"\n程序执行出错: {e}")