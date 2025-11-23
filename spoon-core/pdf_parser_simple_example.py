#!/usr/bin/env python3
"""
PDF Experiment Parser 简单使用示例
展示如何直接使用解析函数提取实验信息
"""

import asyncio
import sys
import os

# 添加到路径
sys.path.insert(0, "/Users/ruizhezheng/Documents/trae_projects/spoon-core")

from PDF_Experiment_Parser import PDFExperimentParser

async def simple_example():
    """简单使用示例"""
    print("🚀 PDF实验信息解析器 - 简单使用示例")
    print("="*60)
    
    # 创建解析器实例
    parser = PDFExperimentParser()
    
    if not parser.chatbot:
        print("❌ SpoonOS AI 未初始化")
        return
    
    # 示例1: 解析Python simulator文件
    print("📄 示例1: 解析Python simulator文件")
    print("-"*40)
    
    python_file = "/Users/ruizhezheng/Documents/trae_projects/spoon-core/sample_simulator.py"
    if os.path.exists(python_file):
        result = await parser.parse_experiment_info(python_path=python_file)
        
        print(f"🔬 实验名称: {result.experiment_name}")
        print(f"📝 实验描述: {result.experiment_description[:100]}...")
        print(f"📊 实验数据数量: {len(result.experiment_data)}")
        
        # 显示部分实验数据
        if result.experiment_data:
            print("\n部分实验数据:")
            for i, data in enumerate(result.experiment_data[:3], 1):
                print(f"  {i}. {data.get('name', '未知')}: {data.get('value', '无值')}")
    else:
        print(f"❌ 文件不存在: {python_file}")
    
    # 示例2: 直接解析文本内容
    print("\n📝 示例2: 直接解析文本内容")
    print("-"*40)
    
    experiment_text = """
    实验名称: 新型催化剂性能测试
    
    实验描述: 本实验旨在测试新型催化剂在不同温度和压力条件下的催化效率。
    通过改变反应条件，观察催化剂的活性和选择性变化。
    
    实验条件:
    - 温度范围: 200-400°C
    - 压力范围: 1-10 atm
    - 反应时间: 2-8小时
    
    实验结果:
    - 最佳催化效率: 94.5% (在350°C, 5atm条件下)
    - 选择性: 89.2%
    - 催化剂寿命: 120小时
    - 反应速率常数: 0.85 h⁻¹
    
    数据分析:
    温度对催化效率的影响呈正相关，在350°C时达到峰值。
    压力的影响相对较小，在5atm后趋于稳定。
    """
    
    result = await parser.parse_experiment_info(manual_text=experiment_text)
    
    print(f"🔬 实验名称: {result.experiment_name}")
    print(f"📝 实验描述: {result.experiment_description[:100]}...")
    print(f"📊 实验数据数量: {len(result.experiment_data)}")
    
    # 显示所有实验数据
    if result.experiment_data:
        print("\n所有实验数据:")
        for i, data in enumerate(result.experiment_data, 1):
            print(f"  {i}. [{data.get('type', '未知')}] {data.get('name', '未知')}")
            print(f"     数值: {data.get('value', '无值')}")
            if data.get('description'):
                print(f"     说明: {data.get('description')}")
    
    # 示例3: 组合解析（Python文件 + 额外文本）
    print("\n🔗 示例3: 组合解析")
    print("-"*40)
    
    additional_info = """
    补充实验信息:
    
    实验时间: 2024年11月20-22日
    实验地点: 实验室A区
    实验人员: 张博士、李研究员
    
    质量控制:
    - 空白对照: 3个平行样
    - 标准样品: 每批次包含
    - 重复实验: 3次独立重复
    
    安全注意事项:
    - 高温操作需佩戴防护设备
    - 压力容器定期检查
    - 废气处理后排放
    """
    
    result = await parser.parse_experiment_info(
        python_path=python_file,
        manual_text=additional_info
    )
    
    print(f"🔬 实验名称: {result.experiment_name}")
    print(f"📝 实验描述: {result.experiment_description[:100]}...")
    print(f"📊 实验数据数量: {len(result.experiment_data)}")
    
    # 示例4: 获取JSON格式结果
    print("\n📄 示例4: JSON格式输出")
    print("-"*40)
    
    result = await parser.parse_experiment_info(manual_text=experiment_text)
    json_result = result.to_json()
    
    print("JSON格式结果:")
    print(json_result)
    
    print("\n" + "="*60)
    print("✅ 所有示例完成！")
    print("💡 提示: 你可以在自己的代码中使用PDFExperimentParser类")
    print("📋 支持: Python文件、PDF文件、手动文本输入")

if __name__ == "__main__":
    try:
        asyncio.run(simple_example())
    except KeyboardInterrupt:
        print("\n👋 用户中断")
    except Exception as e:
        print(f"\n❌ 出错: {e}")