#!/usr/bin/env python3
"""
PDF Experiment Parser - 使用 SpoonOS AI 从PDF和Simulator文件中提取实验信息
支持提取：实验名称、实验描述、实验数据
"""

import os
import sys
import asyncio
import json
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from pathlib import Path

# 设置 SpoonOS 环境 - 安全地从环境变量加载
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
    from spoon_ai import ChatBot, Message
    print(f"✅ 成功导入 SpoonOS 核心模块，版本: {spoon_ai.__version__}")
except ImportError as e:
    print(f"❌ 无法导入 SpoonOS 核心模块: {e}")
    spoon_ai = None

# PDF处理相关导入
try:
    import PyPDF2
    import pdfplumber
    PDF_AVAILABLE = True
except ImportError:
    print("⚠️  未安装PDF处理库，安装: pip install PyPDF2 pdfplumber")
    PDF_AVAILABLE = False

@dataclass
class ExperimentInfo:
    """实验信息数据结构"""
    experiment_name: str = ""
    experiment_description: str = ""
    experiment_data: List[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.experiment_data is None:
            self.experiment_data = []
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "experiment_name": self.experiment_name,
            "experiment_description": self.experiment_description,
            "experiment_data": self.experiment_data
        }
    
    def to_json(self) -> str:
        """转换为JSON字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

class PDFExperimentParser:
    """PDF实验信息解析器"""
    
    def __init__(self):
        """初始化解析器"""
        self.chatbot = None
        self._initialize_spoonos_ai()
    
    def _initialize_spoonos_ai(self):
        """初始化 SpoonOS AI"""
        try:
            if spoon_ai is None:
                print("❌ SpoonOS 核心模块未正确导入")
                self.chatbot = None
                return
            
            self.chatbot = ChatBot()
            print("✅ SpoonOS PDF解析器已初始化")
            print(f"📦 SpoonOS 版本: {spoon_ai.__version__}")
            
        except Exception as e:
            print(f"❌ SpoonOS AI 初始化失败: {e}")
            self.chatbot = None
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """从PDF文件中提取文本"""
        if not PDF_AVAILABLE:
            raise RuntimeError("PDF处理库不可用")
        
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF文件不存在: {pdf_path}")
        
        try:
            # 使用pdfplumber提取文本（更精确）
            text_parts = []
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(f"=== 第{page_num}页 ===\n{page_text}")
            
            full_text = "\n\n".join(text_parts)
            
            if not full_text.strip():
                # 备用方案：使用PyPDF2
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    text_parts = []
                    for page_num, page in enumerate(pdf_reader.pages, 1):
                        page_text = page.extract_text()
                        if page_text:
                            text_parts.append(f"=== 第{page_num}页 ===\n{page_text}")
                
                full_text = "\n\n".join(text_parts)
            
            print(f"📄 成功提取PDF文本，共{len(full_text)}字符")
            return full_text
            
        except Exception as e:
            print(f"❌ PDF文本提取失败: {e}")
            raise
    
    def extract_text_from_python(self, python_path: str) -> str:
        """从Python文件中提取代码和注释"""
        if not os.path.exists(python_path):
            raise FileNotFoundError(f"Python文件不存在: {python_path}")
        
        try:
            with open(python_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            print(f"🐍 成功读取Python文件，共{len(content)}字符")
            return content
            
        except Exception as e:
            print(f"❌ Python文件读取失败: {e}")
            raise
    
    def build_extraction_prompt(self, pdf_text: str = "", python_text: str = "") -> str:
        """构建信息提取提示"""
        prompt = f"""
你是一名专业的实验信息提取专家。请从以下文档中提取实验相关信息。

=== 提取要求 ===
1. **实验名称**: 提取实验的标题或名称（简洁明了）
2. **实验描述**: 提取实验的目的、方法、过程的详细描述
3. **实验数据**: 提取所有实验数据，包括：
   - 数据集描述
   - 实验结果
   - 性能指标
   - 配置参数
   - 任何数值数据

=== 文档内容 ===
"""
        
        if pdf_text:
            prompt += f"\n=== PDF文档内容 ===\n{pdf_text}\n"
        
        if python_text:
            prompt += f"\n=== Python代码内容 ===\n{python_text}\n"
        
        prompt += """
=== 输出格式 ===
请以JSON格式回复，结构如下：
{
  "experiment_name": "实验名称",
  "experiment_description": "实验的详细描述",
  "experiment_data": [
    {
      "type": "数据集/结果/参数等",
      "name": "数据名称",
      "value": "数值或描述",
      "description": "数据说明"
    }
  ]
}

=== 注意事项 ===
- 如果没有找到相关信息，请返回空字符串或空数组
- 实验数据部分要尽可能详细和完整
- 保持JSON格式正确
- 使用中文回复
"""
        return prompt.strip()
    
    async def parse_experiment_info(
        self, 
        pdf_path: Optional[str] = None, 
        python_path: Optional[str] = None,
        manual_text: Optional[str] = None
    ) -> ExperimentInfo:
        """
        解析实验信息
        
        Args:
            pdf_path: PDF文件路径
            python_path: Python文件路径
            manual_text: 手动输入的文本（当文件不可用时）
            
        Returns:
            ExperimentInfo: 实验信息对象
        """
        if not self.chatbot:
            return ExperimentInfo(
                experiment_name="",
                experiment_description="SpoonOS AI 未初始化",
                experiment_data=[]
            )
        
        # 收集文本内容
        texts = []
        
        if manual_text:
            texts.append(f"=== 手动输入内容 ===\n{manual_text}")
        
        if pdf_path:
            try:
                if not PDF_AVAILABLE:
                    texts.append("⚠️ PDF处理库未安装，无法解析PDF内容")
                else:
                    pdf_text = self.extract_text_from_pdf(pdf_path)
                    texts.append(pdf_text)
            except Exception as e:
                texts.append(f"⚠️ PDF解析失败: {str(e)}")
        
        if python_path:
            try:
                python_text = self.extract_text_from_python(python_path)
                texts.append(python_text)
            except Exception as e:
                texts.append(f"⚠️ Python文件读取失败: {str(e)}")
        
        if not texts:
            return ExperimentInfo(
                experiment_name="",
                experiment_description="未提供任何输入内容",
                experiment_data=[]
            )
        
        # 构建提示
        combined_text = "\n\n".join(texts)
        prompt = self.build_extraction_prompt(
            pdf_text=combined_text if pdf_path else "",
            python_text=combined_text if python_path else ""
        )
        
        try:
            print("🤖 正在使用 SpoonOS AI 提取实验信息...")
            
            # 使用 SpoonOS 的 Message 类构建消息
            system_message = Message(
                role="system",
                content="你是一个专业的实验信息提取专家，能够从文档中准确提取实验名称、描述和数据。"
            )
            user_message = Message(
                role="user",
                content=prompt
            )
            messages = [system_message, user_message]
            
            # 调用 AI
            ai_response = await self.chatbot.ask(messages)
            
            # 解析 AI 响应
            experiment_info = self._parse_ai_response(ai_response)
            
            print(f"✅ 实验信息提取完成: {experiment_info.experiment_name}")
            return experiment_info
            
        except Exception as e:
            print(f"❌ AI 提取失败: {e}")
            return ExperimentInfo(
                experiment_name="",
                experiment_description=f"AI提取失败: {str(e)}",
                experiment_data=[]
            )
    
    def _parse_ai_response(self, ai_response: str) -> ExperimentInfo:
        """解析 AI 响应"""
        try:
            # 尝试解析JSON响应
            import json
            
            # 清理响应文本，提取JSON部分
            response_text = ai_response.strip()
            
            # 查找JSON开始和结束位置
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start != -1 and json_end != 0:
                json_str = response_text[json_start:json_end]
                parsed_data = json.loads(json_str)
                
                return ExperimentInfo(
                    experiment_name=parsed_data.get("experiment_name", ""),
                    experiment_description=parsed_data.get("experiment_description", ""),
                    experiment_data=parsed_data.get("experiment_data", [])
                )
            else:
                # 如果没有找到JSON，尝试手动提取
                return self._extract_info_from_text(response_text)
                
        except json.JSONDecodeError as e:
            print(f"⚠️  JSON解析失败: {e}")
            return self._extract_info_from_text(ai_response)
        except Exception as e:
            print(f"⚠️  响应解析失败: {e}")
            return ExperimentInfo(
                experiment_name="",
                experiment_description="解析失败",
                experiment_data=[]
            )
    
    def _extract_info_from_text(self, text: str) -> ExperimentInfo:
        """从文本中手动提取信息"""
        import re
        
        # 尝试提取实验名称（寻找标题模式）
        name_patterns = [
            r'实验名称["\']?\s*[:：]\s*["\']?([^"\'\n]+)["\']?',
            r'["\']?experiment_name["\']?\s*[:：]\s*["\']?([^"\'\n]+)["\']?',
            r'标题["\']?\s*[:：]\s*["\']?([^"\'\n]+)["\']?',
            r'Title["\']?\s*[:：]\s*["\']?([^"\'\n]+)["\']?'
        ]
        
        experiment_name = ""
        for pattern in name_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                experiment_name = match.group(1).strip()
                break
        
        # 尝试提取实验描述
        desc_patterns = [
            r'实验描述["\']?\s*[:：]\s*["\']?([^"\']+)["\']?',
            r'["\']?experiment_description["\']?\s*[:：]\s*["\']?([^"\']+)["\']?',
            r'描述["\']?\s*[:：]\s*["\']?([^"\']+)["\']?',
            r'Description["\']?\s*[:：]\s*["\']?([^"\']+)["\']?'
        ]
        
        experiment_description = ""
        for pattern in desc_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                experiment_description = match.group(1).strip()
                break
        
        # 如果没有找到明确的描述，使用文本的前半部分
        if not experiment_description and len(text) > 100:
            experiment_description = text[:min(len(text)//2, 500)].strip()
        
        return ExperimentInfo(
            experiment_name=experiment_name,
            experiment_description=experiment_description,
            experiment_data=[]
        )

# 演示和测试函数
async def demo_pdf_parser():
    """演示PDF解析功能"""
    print("🚀 启动 SpoonOS AI PDF实验信息解析器演示")
    print("=" * 60)
    
    parser = PDFExperimentParser()
    
    if not parser.chatbot:
        print("❌ 无法演示，SpoonOS AI 未初始化")
        return
    
    # 演示模式选择
    print("选择演示模式:")
    print("1. 手动输入文本")
    print("2. 使用Python文件")
    if PDF_AVAILABLE:
        print("3. 使用PDF文件")
    print("4. 退出")
    
    try:
        choice = input("\n请输入选择 (1-4): ").strip()
        
        if choice == "1":
            # 手动输入模式
            print("\n📝 手动输入模式")
            print("请输入实验相关文本（或按Ctrl+D结束输入）:")
            
            lines = []
            try:
                while True:
                    line = input()
                    lines.append(line)
            except EOFError:
                pass
            
            manual_text = "\n".join(lines)
            
            if manual_text.strip():
                result = await parser.parse_experiment_info(manual_text=manual_text)
                print_result(result)
            else:
                print("❌ 未输入任何内容")
        
        elif choice == "2":
            # Python文件模式
            python_path = input("请输入Python文件路径: ").strip()
            if python_path:
                result = await parser.parse_experiment_info(python_path=python_path)
                print_result(result)
        
        elif choice == "3" and PDF_AVAILABLE:
            # PDF文件模式
            pdf_path = input("请输入PDF文件路径: ").strip()
            if pdf_path:
                result = await parser.parse_experiment_info(pdf_path=pdf_path)
                print_result(result)
        
        elif choice == "4":
            print("👋 再见！")
        else:
            print("❌ 无效选择或PDF功能不可用")
    
    except KeyboardInterrupt:
        print("\n\n👋 用户中断，再见！")
    except Exception as e:
        print(f"\n❌ 演示出错: {e}")

def print_result(result: ExperimentInfo):
    """打印解析结果"""
    print("\n" + "="*60)
    print("📊 实验信息提取结果:")
    print("="*60)
    print(f"🔬 实验名称: {result.experiment_name or '未找到'}")
    print(f"📝 实验描述: {result.experiment_description[:200]}{'...' if len(result.experiment_description) > 200 else ''}")
    
    if result.experiment_data:
        print(f"\n📈 实验数据 ({len(result.experiment_data)} 项):")
        for i, data in enumerate(result.experiment_data, 1):
            print(f"  {i}. [{data.get('type', '未知')}] {data.get('name', '未命名')}: {data.get('value', '无值')}")
            if data.get('description'):
                print(f"     说明: {data['description']}")
    else:
        print("\n📈 实验数据: 未找到")
    
    print(f"\n📄 完整JSON格式:")
    print(result.to_json())
    print("="*60)

async def main():
    """主函数"""
    await demo_pdf_parser()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 程序被用户中断")
    except Exception as e:
        print(f"\n❌ 程序执行出错: {e}")