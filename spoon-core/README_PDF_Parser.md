# PDF实验信息解析器使用指南

## 🚀 功能介绍

PDF实验信息解析器使用SpoonOS AI从PDF文件和Python simulator文件中智能提取实验信息，包括：
- **实验名称**: 实验的标题或名称
- **实验描述**: 实验的目的、方法、过程的详细描述  
- **实验数据**: 所有实验相关的数据、结果、配置参数等

## 📋 主要特性

### ✅ 支持的输入格式
- **PDF文件**: 直接解析PDF文档内容
- **Python文件**: 提取代码中的实验信息和注释
- **手动文本**: 直接输入文本内容进行解析
- **组合输入**: 同时支持多种输入方式的组合

### 🤖 AI智能提取
- 使用SpoonOS GPT模型进行智能信息提取
- 自动识别实验名称、描述和数据
- 支持结构化JSON输出
- 中文语境优化

### 🛡️ 安全特性
- 环境变量管理API密钥
- 完善的错误处理机制
- 文件验证和安全检查

## 🛠️ 安装要求

```bash
# 安装PDF处理库
pip install PyPDF2 pdfplumber

# 确保SpoonOS环境已配置
cp .env.example .env
# 编辑.env文件添加您的OpenAI API密钥
```

## 💡 快速开始

### 1. 基础使用示例

```python
import asyncio
from PDF_Experiment_Parser import PDFExperimentParser

async def main():
    # 创建解析器
    parser = PDFExperimentParser()
    
    # 解析Python文件
    result = await parser.parse_experiment_info(
        python_path="path/to/your/simulator.py"
    )
    
    # 打印结果
    print(f"实验名称: {result.experiment_name}")
    print(f"实验描述: {result.experiment_description}")
    print(f"实验数据数量: {len(result.experiment_data)}")

asyncio.run(main())
```

### 2. 解析PDF文件

```python
# 解析PDF文档
result = await parser.parse_experiment_info(
    pdf_path="experiment_report.pdf"
)

# 获取JSON格式结果
json_result = result.to_json()
print(json_result)
```

### 3. 手动文本输入

```python
# 直接输入文本
experiment_text = """
实验名称: 催化剂性能测试
实验描述: 测试新型催化剂在不同条件下的性能表现
实验数据:
- 温度: 200-400°C
- 效率: 94.5%
- 选择性: 89.2%
"""

result = await parser.parse_experiment_info(
    manual_text=experiment_text
)
```

### 4. 组合解析

```python
# 同时提供多种输入
result = await parser.parse_experiment_info(
    python_path="simulator.py",
    pdf_path="report.pdf",
    manual_text="补充信息..."
)
```

## 📊 输出格式

解析结果包含三个主要部分：

### 实验名称 (experiment_name)
- 简洁明了的实验标题
- 自动从文档中提取

### 实验描述 (experiment_description)
- 详细的实验目的和方法描述
- 包含实验背景和关键信息

### 实验数据 (experiment_data)
结构化数据列表，每项包含：
```json
{
  "type": "数据集/结果/参数等",
  "name": "数据名称", 
  "value": "数值或描述",
  "description": "详细说明"
}
```

## 🎯 实际测试结果

### Python文件解析示例
```
🔬 实验名称: CIFAR10_ResNet50_Classification
📝 实验描述: 使用ResNet-50在CIFAR-10数据集上进行图像分类的实验...
📊 实验数据数量: 15

实验数据包括:
1. 数据集: CIFAR-10训练集和测试集
2. 模型架构: ResNet-50  
3. 配置参数: 学习率0.001, 批量大小64等
4. 性能指标: 训练历史记录
5. 结果数据: 模型大小、训练时间等
```

### 手动文本解析示例
```
🔬 实验名称: 新型催化剂性能测试
📝 实验描述: 本实验旨在测试新型催化剂在不同温度和压力条件下的催化效率...
📊 实验数据数量: 5

实验数据包括:
1. 温度范围: 200-400°C
2. 最佳催化效率: 94.5% (在350°C, 5atm条件下)
3. 选择性: 89.2%
4. 催化剂寿命: 120小时
5. 反应速率常数: 0.85 h⁻¹
```

## 🔧 高级功能

### 错误处理
```python
try:
    result = await parser.parse_experiment_info(pdf_path="file.pdf")
    if not result.experiment_name:
        print("⚠️ 未提取到实验名称")
except FileNotFoundError:
    print("❌ 文件不存在")
except Exception as e:
    print(f"❌ 解析失败: {e}")
```

### 结果验证
```python
# 检查结果完整性
if result.experiment_name and result.experiment_description:
    print("✅ 成功提取关键信息")
else:
    print("⚠️ 信息提取不完整")

# 检查实验数据
if len(result.experiment_data) > 0:
    print(f"📈 提取到 {len(result.experiment_data)} 项实验数据")
```

## 📁 文件结构

```
spoon-core/
├── PDF_Experiment_Parser.py          # 主要解析器
├── test_pdf_parser.py                # 测试脚本
├── pdf_parser_simple_example.py      # 简单使用示例
├── sample_simulator.py               # 示例Python文件
├── sample_experiment.txt            # 示例实验文档
└── README_PDF_Parser.md             # 本文档
```

## 💬 使用建议

1. **文件质量**: 确保PDF文件文本可提取，Python文件包含清晰的注释
2. **文本描述**: 手动输入时尽量提供详细和结构化的描述
3. **组合使用**: 同时使用多种输入方式可以获得更全面的结果
4. **错误处理**: 始终添加适当的错误处理逻辑
5. **结果验证**: 检查提取结果的完整性和准确性

## 🚀 下一步计划

- [ ] 支持更多文件格式（Word、Excel等）
- [ ] 图像和表格数据提取
- [ ] 批量文件处理
- [ ] 自定义提取模板
- [ ] 结果可视化展示
- [ ] 与实验数据库集成

## 🎯 总结

PDF实验信息解析器为科研工作者提供了强大的自动化工具，能够从各种文档格式中快速准确地提取实验信息，大大提高工作效率并减少人工错误。结合SpoonOS AI的智能分析能力，该系统能够处理复杂的科学文档并生成结构化的实验数据。