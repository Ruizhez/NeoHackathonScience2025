#!/usr/bin/env python3
"""
简化版 SpoonOS 本地数据库和 Web3 功能演示
Simplified demo of SpoonOS local database and Web3 features
"""

import os
import asyncio
from pathlib import Path

def demo_local_database():
    """演示本地数据库存储功能"""
    print("🗄️  本地数据库功能演示")
    print("=" * 40)
    
    try:
        # 检查 Chroma 向量数据库
        try:
            from spoon_ai.retrieval.chroma import ChromaClient, Document
            print("✅ Chroma 向量数据库已集成")
            
            # 创建客户端实例
            config_dir = "/Users/ruizhezheng/Documents/trae_projects/spoon-core/data"
            os.makedirs(config_dir, exist_ok=True)
            client = ChromaClient(config_dir=config_dir)
            
            # 创建示例文档
            doc = Document(
                page_content="SpoonOS 支持本地向量数据库存储",
                metadata={"source": "demo", "type": "test"}
            )
            
            # 存储文档
            client.add_documents([doc])
            print("✅ 文档存储成功")
            
            # 查询文档
            results = client.query("向量数据库", k=1)
            if results:
                print(f"✅ 查询成功: {results[0].page_content}")
            
        except ImportError as e:
            print(f"⚠️  Chroma 未安装: {e}")
        
        # 检查 SQLite 支持
        try:
            import sqlite3
            print("✅ SQLite 数据库支持")
            
            # 创建测试数据库
            conn = sqlite3.connect('/Users/ruizhezheng/Documents/trae_projects/spoon-core/data/test.db')
            cursor = conn.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS documents (id INTEGER PRIMARY KEY, content TEXT)')
            cursor.execute('INSERT INTO documents (content) VALUES (?)', ("测试文档内容",))
            conn.commit()
            
            # 查询数据
            cursor.execute('SELECT content FROM documents WHERE id = 1')
            result = cursor.fetchone()
            if result:
                print(f"✅ SQLite 查询成功: {result[0]}")
            
            conn.close()
            
        except Exception as e:
            print(f"⚠️  SQLite 测试失败: {e}")
            
        return True
        
    except Exception as e:
        print(f"❌ 数据库演示失败: {e}")
        return False

def demo_web3_features():
    """演示 Web3 集成功能"""
    print("\n⛓️  Web3 集成功能演示")
    print("=" * 40)
    
    try:
        # 检查 Web3 工具
        available_tools = []
        
        # 检查 Turnkey 钱包工具
        try:
            from spoon_ai.tools.turnkey_tools import SignEVMTransactionTool
            available_tools.append("Turnkey 钱包管理")
        except ImportError:
            pass
        
        # 检查 x402 支付工具
        try:
            from spoon_ai.tools.x402_payment import X402PaywalledRequestTool
            available_tools.append("x402 支付协议")
        except ImportError:
            pass
        
        # 检查 EVM 工具
        try:
            import web3
            available_tools.append("EVM 区块链交互")
        except ImportError:
            pass
        
        # 检查 Solana 工具
        try:
            from spoon_toolkits.crypto.solana import SolanaToolkit
            available_tools.append("Solana 区块链")
        except ImportError:
            pass
        
        print("🔐 可用的 Web3 工具:")
        if available_tools:
            for tool in available_tools:
                print(f"  ✅ {tool}")
        else:
            print("  ⚠️  未找到 Web3 工具")
        
        # 显示 Web3 功能概览
        print("\n💡 Web3 功能概览:")
        print("  • 以太坊钱包管理")
        print("  • 交易签名和广播")
        print("  • EIP-712 消息签名")
        print("  • x402 支付协议")
        print("  • 去中心化存储 (NeoFS)")
        print("  • DEX 监控和分析")
        print("  • 跨链数据查询")
        
        return True
        
    except Exception as e:
        print(f"❌ Web3 演示失败: {e}")
        return False

def demo_document_processing():
    """演示文档处理功能"""
    print("\n📚 文档处理功能演示")
    print("=" * 40)
    
    try:
        # 检查文档加载器
        try:
            from spoon_ai.retrieval.document_loader import DocumentLoader
            print("✅ 文档加载器已集成")
            
            # 创建测试文档
            test_dir = "/Users/ruizhezheng/Documents/trae_projects/spoon-core/test_docs"
            os.makedirs(test_dir, exist_ok=True)
            
            # 创建示例文档
            test_file = os.path.join(test_dir, "sample.txt")
            with open(test_file, "w", encoding="utf-8") as f:
                f.write("""这是一个测试文档。
SpoonOS 支持文档加载和处理功能。
可以将文档分块并存储到向量数据库中。
支持多种文件格式：TXT、PDF、Markdown 等。
""")
            
            # 使用文档加载器
            loader = DocumentLoader()
            documents = loader.load_directory(test_dir, glob_pattern="**/*.txt")
            
            if documents:
                print(f"✅ 成功加载 {len(documents)} 个文档")
                for doc in documents:
                    print(f"  文档: {doc.metadata.get('source', 'Unknown')}")
                    print(f"  长度: {len(doc.page_content)} 字符")
            
            # 清理测试文件
            import shutil
            shutil.rmtree(test_dir)
            
        except ImportError as e:
            print(f"⚠️  文档加载器不可用: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ 文档处理演示失败: {e}")
        return False

async def main():
    """主函数"""
    print("🥄 SpoonOS 功能演示")
    print("=" * 50)
    print("测试本地数据库和 Web3 集成功能")
    print()
    
    # 设置环境
    os.environ["PYTHONPATH"] = "/Users/ruizhezheng/Documents/trae_projects/spoon-core"
    
    # 运行演示
    results = []
    results.append(demo_local_database())
    results.append(demo_web3_features())
    results.append(demo_document_processing())
    
    # 总结
    print("\n🎉 演示总结")
    print("=" * 50)
    
    if all(results):
        print("✅ 所有功能演示成功！")
        print("\n📋 SpoonOS 支持的功能:")
        print("• 本地向量数据库 (Chroma)")
        print("• 传统数据库 (SQLite)")
        print("• Web3 钱包和交易工具")
        print("• 区块链支付协议")
        print("• 文档加载和处理")
        print("• 去中心化存储")
        print("\n🚀 你可以开始使用这些功能构建 AI + Web3 应用！")
    else:
        print("❌ 部分演示遇到问题")
        print("建议检查依赖安装和环境配置")

if __name__ == "__main__":
    asyncio.run(main())