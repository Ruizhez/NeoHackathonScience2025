#!/usr/bin/env python3
"""
实验模拟器示例 - 图像分类模型训练
用于测试PDF实验信息解析器
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import time
import json

class ImageClassificationExperiment:
    """图像分类实验类"""
    
    def __init__(self):
        self.experiment_name = "CIFAR10_ResNet50_Classification"
        self.experiment_description = """
        使用ResNet-50在CIFAR-10数据集上进行图像分类的实验。
        该实验比较了不同的优化器和学习率策略对模型性能的影响。
        """
        
        # 实验配置
        self.config = {
            'dataset': 'CIFAR-10',
            'model_architecture': 'ResNet-50',
            'num_classes': 10,
            'batch_size': 64,
            'learning_rate': 0.001,
            'num_epochs': 100,
            'optimizer': 'Adam',
            'loss_function': 'CrossEntropyLoss',
            'data_augmentation': True,
            'device': 'cuda' if torch.cuda.is_available() else 'cpu'
        }
        
        self.results = {}
        self.training_history = []
        
    def prepare_data(self):
        """准备数据集"""
        print("准备CIFAR-10数据集...")
        
        # 数据预处理
        transform_train = transforms.Compose([
            transforms.RandomCrop(32, padding=4),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
        ])
        
        transform_test = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
        ])
        
        # 加载数据集
        train_dataset = datasets.CIFAR10(root='./data', train=True, download=True, transform=transform_train)
        test_dataset = datasets.CIFAR10(root='./data', train=False, download=True, transform=transform_test)
        
        self.train_loader = DataLoader(train_dataset, batch_size=self.config['batch_size'], shuffle=True, num_workers=2)
        self.test_loader = DataLoader(test_dataset, batch_size=self.config['batch_size'], shuffle=False, num_workers=2)
        
        print(f"训练集大小: {len(train_dataset)}")
        print(f"测试集大小: {len(test_dataset)}")
        
    def build_model(self):
        """构建模型"""
        print(f"构建{self.config['model_architecture']}模型...")
        
        # 使用预训练的ResNet-50
        self.model = models.resnet50(pretrained=True)
        
        # 修改最后的全连接层以适应CIFAR-10
        num_features = self.model.fc.in_features
        self.model.fc = nn.Linear(num_features, self.config['num_classes'])
        
        self.model = self.model.to(self.config['device'])
        
        # 定义损失函数和优化器
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.config['learning_rate'])
        self.scheduler = optim.lr_scheduler.StepLR(self.optimizer, step_size=30, gamma=0.1)
        
    def train_epoch(self, epoch):
        """训练一个epoch"""
        self.model.train()
        train_loss = 0
        correct = 0
        total = 0
        
        for batch_idx, (inputs, targets) in enumerate(self.train_loader):
            inputs, targets = inputs.to(self.config['device']), targets.to(self.config['device'])
            
            self.optimizer.zero_grad()
            outputs = self.model(inputs)
            loss = self.criterion(outputs, targets)
            loss.backward()
            self.optimizer.step()
            
            train_loss += loss.item()
            _, predicted = outputs.max(1)
            total += targets.size(0)
            correct += predicted.eq(targets).sum().item()
            
            if batch_idx % 100 == 0:
                print(f'Epoch: {epoch} [{batch_idx}/{len(self.train_loader)}] '
                      f'Loss: {train_loss/(batch_idx+1):.3f} '
                      f'Acc: {100.*correct/total:.3f}%')
        
        epoch_results = {
            'epoch': epoch,
            'train_loss': train_loss / len(self.train_loader),
            'train_accuracy': 100. * correct / total,
            'learning_rate': self.optimizer.param_groups[0]['lr']
        }
        
        return epoch_results
        
    def evaluate(self):
        """评估模型"""
        self.model.eval()
        test_loss = 0
        correct = 0
        total = 0
        all_predictions = []
        all_targets = []
        
        with torch.no_grad():
            for inputs, targets in self.test_loader:
                inputs, targets = inputs.to(self.config['device']), targets.to(self.config['device'])
                outputs = self.model(inputs)
                loss = self.criterion(outputs, targets)
                
                test_loss += loss.item()
                _, predicted = outputs.max(1)
                total += targets.size(0)
                correct += predicted.eq(targets).sum().item()
                
                all_predictions.extend(predicted.cpu().numpy())
                all_targets.extend(targets.cpu().numpy())
        
        # 计算详细指标
        accuracy = accuracy_score(all_targets, all_predictions)
        precision, recall, f1, _ = precision_recall_fscore_support(all_targets, all_predictions, average='weighted')
        
        results = {
            'test_loss': test_loss / len(self.test_loader),
            'test_accuracy': accuracy * 100,
            'precision': precision * 100,
            'recall': recall * 100,
            'f1_score': f1 * 100
        }
        
        return results
        
    def run_experiment(self):
        """运行完整实验"""
        print("="*60)
        print(f"开始实验: {self.experiment_name}")
        print("="*60)
        
        # 准备数据和模型
        self.prepare_data()
        self.build_model()
        
        # 训练循环
        print("开始训练...")
        start_time = time.time()
        
        for epoch in range(1, self.config['num_epochs'] + 1):
            epoch_results = self.train_epoch(epoch)
            self.training_history.append(epoch_results)
            
            # 学习率调度
            self.scheduler.step()
            
            # 每10个epoch评估一次
            if epoch % 10 == 0:
                test_results = self.evaluate()
                print(f"Epoch {epoch} 测试结果:")
                print(f"  测试准确率: {test_results['test_accuracy']:.2f}%")
                print(f"  精确率: {test_results['precision']:.2f}%")
                print(f"  召回率: {test_results['recall']:.2f}%")
                print(f"  F1分数: {test_results['f1_score']:.2f}%")
        
        training_time = time.time() - start_time
        
        # 最终评估
        print("\n最终评估...")
        final_results = self.evaluate()
        
        # 保存实验结果
        self.results = {
            'experiment_name': self.experiment_name,
            'experiment_description': self.experiment_description,
            'config': self.config,
            'final_results': final_results,
            'training_history': self.training_history,
            'training_time': training_time,
            'model_size_mb': sum(p.numel() for p in self.model.parameters()) * 4 / (1024 * 1024)
        }
        
        # 打印最终结果
        print("\n" + "="*60)
        print("实验完成！最终结果:")
        print("="*60)
        print(f"实验名称: {self.experiment_name}")
        print(f"测试准确率: {final_results['test_accuracy']:.2f}%")
        print(f"精确率: {final_results['precision']:.2f}%")
        print(f"召回率: {final_results['recall']:.2f}%")
        print(f"F1分数: {final_results['f1_score']:.2f}%")
        print(f"训练时间: {training_time/3600:.2f}小时")
        print(f"模型大小: {self.results['model_size_mb']:.2f}MB")
        
        return self.results
        
    def save_results(self, filepath='experiment_results.json'):
        """保存实验结果"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        print(f"实验结果已保存到: {filepath}")
        
    def load_results(self, filepath='experiment_results.json'):
        """加载实验结果"""
        with open(filepath, 'r', encoding='utf-8') as f:
            self.results = json.load(f)
        print(f"实验结果已加载: {filepath}")
        return self.results

# 使用示例
if __name__ == "__main__":
    # 创建实验实例
    experiment = ImageClassificationExperiment()
    
    # 运行实验
    results = experiment.run_experiment()
    
    # 保存结果
    experiment.save_results('cifar10_resnet50_results.json')
    
    print("\n实验数据已准备好供PDF解析器提取！")