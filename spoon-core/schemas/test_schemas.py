#!/usr/bin/env python3
"""
测试 JSON Schema 的示例数据
Test JSON data for the created schemas
"""

import json

# User 示例数据
user_sample = {
    "Experiment": ["exp_001", "exp_002", "exp_003"]
}

# Experiment 示例数据
experiment_sample = {
    "name": "AI模型性能测试",
    "discription": "测试不同AI模型在特定任务上的表现",
    "simulator": "SpoonOS",
    "test_results": ["result_001", "result_002", "result_003"]
}

# TestResult 示例数据
test_result_sample = {
    "name": "模型准确率测试",
    "date": "2024-11-22"
}

print("🧪 JSON Schema 测试数据")
print("=" * 40)

print("\n👤 User 示例:")
print(json.dumps(user_sample, indent=2, ensure_ascii=False))

print("\n🔬 Experiment 示例:")
print(json.dumps(experiment_sample, indent=2, ensure_ascii=False))

print("\n📊 TestResult 示例:")
print(json.dumps(test_result_sample, indent=2, ensure_ascii=False))

print("\n✅ 所有示例数据已生成！")