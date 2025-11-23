#!/usr/bin/env python3
"""
PDF Experiment Parser 测试 - 直接测试Python文件解析
"""

import os
import sys
import asyncio
sys.path.insert(0, "/Users/ruizhezheng/Documents/trae_projects/spoon-core")

# 从PDF解析器导入
from PDF_Experiment_Parser import PDFExperimentParser, print_result

async def test_python_parser():
    """测试Python文件解析"""
    print("🚀 测试Python文件解析功能")
    print("="*60)
    
    parser = PDFExperimentParser()
    
    if not parser.chatbot:
        print("❌ SpoonOS AI 未初始化")
        return
    
    # 使用示例simulator文件
    python_path = "/Users/ruizhezheng/Documents/trae_projects/spoon-core/sample_simulator.py"
    
    if os.path.exists(python_path):
        print(f"📄 解析文件: {python_path}")
        result = await parser.parse_experiment_info(python_path=python_path)
        print_result(result)
    else:
        print(f"❌ 文件不存在: {python_path}")
        
    # 也测试手动输入模式
    print("\n" + "="*60)
    print("📝 测试手动输入模式")
    print("="*60)
    
    manual_text = """
    实验名称: 深度学习模型优化实验
    
    实验描述: 本实验旨在通过调整超参数来优化深度学习模型的性能。
    我们使用了网格搜索方法来找到最佳的学习率、批量大小和网络架构。
    
    实验数据:
    - 最佳学习率: 0.001
    - 最佳批量大小: 32
    - 最高准确率: 95.2%
    - 训练时间: 2.5小时
    - GPU内存使用: 6.8GB
    """
    
    result = await parser.parse_experiment_info(manual_text=manual_text)
    print_result(result)

if __name__ == "__main__":
    try:
        asyncio.run(test_python_parser())
    except KeyboardInterrupt:
        print("\n👋 用户中断")
    except Exception as e:
        print(f"\n❌ 测试出错: {e}")