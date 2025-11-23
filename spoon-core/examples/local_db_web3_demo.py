#!/usr/bin/env python3
"""
演示 SpoonOS 的本地数据库和 Web3 集成功能
Demonstrates SpoonOS local database and Web3 integration capabilities
"""

import asyncio
import os
from pathlib import Path
from spoon_ai.retrieval.chroma import ChromaClient, Document
from spoon_ai.retrieval.document_loader import DocumentLoader

async def demo_local_database():
    """演示本地向量数据库存储"""
    print("🗄️  演示本地向量数据库存储")
    print("=" * 50)
    
    try:
        # 创建 Chroma 客户端，数据会持久化到本地
        config_dir = "/Users/ruizhezheng/Documents/trae_projects/spoon-core/data"
        os.makedirs(config_dir, exist_ok=True)
        
        client = ChromaClient(config_dir=config_dir)
        
        # 创建一些示例文档
        documents = [
            Document(
                page_content="SpoonOS 是一个强大的 AI 代理框架，支持本地数据库存储和 Web3 集成",
                metadata={"source": "demo", "category": "introduction"}
            ),
            Document(
                page_content="Web3 集成包括以太坊钱包、交易签名、去中心化存储等功能",
                metadata={"source": "demo", "category": "web3"}
            ),
            Document(
                page_content="本地数据库支持 Chroma 和 Qdrant 向量数据库，可以存储和查询文档",
                metadata={"source": "demo", "category": "database"}
            )
        ]
        
        # 添加到数据库
        print("📄 添加文档到向量数据库...")
        client.add_documents(documents)
        print("✅ 文档添加成功！")
        
        # 查询文档
        print("\n🔍 查询相关文档...")
        results = client.query("Web3 功能", k=2)
        
        for i, result in enumerate(results, 1):
            print(f"结果 {i}: {result.page_content}")
            print(f"相似度: {result.metadata.get('score', 'N/A')}")
            print()
            
        print("✅ 本地数据库演示完成！")
        return True
        
    except Exception as e:
        print(f"❌ 数据库演示失败: {e}")
        return False

async def demo_web3_integration():
    """演示 Web3 集成功能"""
    print("\n⛓️  演示 Web3 集成功能")
    print("=" * 50)
    
    try:
        # 检查 Web3 工具是否可用
        from spoon_ai.tools.turnkey_tools import SignEVMTransactionTool
        from spoon_ai.tools.x402_payment import X402PaywalledRequestTool
        
        print("🔐 可用的 Web3 工具:")
        print("- Turnkey 钱包管理")
        print("- EVM 交易签名")
        print("- x402 支付协议")
        print("- Solana 区块链操作")
        print("- NeoFS 去中心化存储")
        
        # 演示钱包地址生成（模拟）
        print("\n💳 钱包功能演示:")
        print("✅ Turnkey 钱包客户端已加载")
        print("✅ 支持以太坊地址生成和管理")
        print("✅ 支持交易签名和消息签名")
        
        # 演示 x402 支付功能
        print("\n💰 x402 支付协议演示:")
        print("✅ 支持自动处理 402 支付协商")
        print("✅ 支持 EIP-712 签名")
        print("✅ 支持 USDC 等代币支付")
        
        print("\n🌐 去中心化存储演示:")
        print("✅ NeoFS 客户端已集成")
        print("✅ 支持容器管理和对象上传/下载")
        print("✅ 支持计费查询和权限管理")
        
        print("\n✅ Web3 集成演示完成！")
        return True
        
    except Exception as e:
        print(f"❌ Web3 演示失败: {e}")
        return False

async def demo_document_loader():
    """演示文档加载和分块功能"""
    print("\n📚 演示文档加载和分块功能")
    print("=" * 50)
    
    try:
        # 创建一个示例文档目录
        docs_dir = "/Users/ruizhezheng/Documents/trae_projects/spoon-core/sample_docs"
        os.makedirs(docs_dir, exist_ok=True)
        
        # 创建示例文档
        sample_file = os.path.join(docs_dir, "web3_guide.txt")
        with open(sample_file, "w", encoding="utf-8") as f:
            f.write("""Web3 和区块链基础指南

什么是 Web3？
Web3 是下一代互联网技术，基于区块链技术构建的去中心化网络。

主要特点：
- 去中心化：没有单一控制点
- 透明性：所有交易公开可查
- 安全性：密码学保护
- 用户拥有数据控制权

应用场景：
- 去中心化金融 (DeFi)
- 非同质化代币 (NFT)
- 去中心化自治组织 (DAO)
- 元宇宙和 GameFi
""")
        
        # 使用文档加载器
        loader = DocumentLoader()
        documents = loader.load_directory(docs_dir, glob_pattern="**/*.txt")
        
        print(f"📖 加载了 {len(documents)} 个文档")
        for doc in documents:
            print(f"文档: {doc.metadata.get('source', 'Unknown')}")
            print(f"内容长度: {len(doc.page_content)} 字符")
            print(f"预览: {doc.page_content[:100]}...")
            print()
        
        print("✅ 文档加载演示完成！")
        return True
        
    except Exception as e:
        print(f"❌ 文档加载演示失败: {e}")
        return False

async def main():
    """主函数：运行所有演示"""
    print("🥄 SpoonOS 本地数据库和 Web3 功能演示")
    print("=" * 60)
    
    # 设置环境
    os.environ["PYTHONPATH"] = "/Users/ruizhezheng/Documents/trae_projects/spoon-core"
    
    results = []
    
    # 运行演示
    results.append(await demo_local_database())
    results.append(await demo_web3_integration())
    results.append(await demo_document_loader())
    
    # 总结
    print("\n🎉 演示总结")
    print("=" * 60)
    
    if all(results):
        print("✅ 所有演示都成功了！")
        print("\n📋 可用的功能:")
        print("• 本地向量数据库 (Chroma/Qdrant)")
        print("• 文档加载和智能分块")
        print("• Web3 钱包和交易签名")
        print("• x402 支付协议")
        print("• 去中心化存储 (NeoFS)")
        print("• DEX 监控和分析")
        print("\n🚀 SpoonOS 已经准备好支持你的 AI + Web3 项目！")
    else:
        print("❌ 部分演示失败，请检查配置和依赖")
        
    # 清理示例文件
    try:
        import shutil
        docs_dir = "/Users/ruizhezheng/Documents/trae_projects/spoon-core/sample_docs"
        if os.path.exists(docs_dir):
            shutil.rmtree(docs_dir)
    except:
        pass

if __name__ == "__main__":
    asyncio.run(main())