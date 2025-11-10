#!/usr/bin/env python3
"""
测试所有 ROS2 服务类型的随机数据生成
"""
import subprocess
import sys
from collections import defaultdict

# 从 ros2 service list -t 获取的服务类型
service_types = [
    "simulation_interfaces/DeleteEntity",
    "simulation_interfaces/GetAvailableWorlds",
    "simulation_interfaces/GetCurrentWorld",
    "simulation_interfaces/GetEntities",
    "simulation_interfaces/GetEntitiesStates",
    "simulation_interfaces/GetEntityInfo",
    "simulation_interfaces/GetEntityState",
    "simulation_interfaces/GetSimulationState",
    "simulation_interfaces/GetSimulatorFeatures",
    "rcl_interfaces/DescribeParameters",
    "rcl_interfaces/GetParameterTypes",
    "rcl_interfaces/GetParameters",
    "rcl_interfaces/ListParameters",
    "rcl_interfaces/SetParameters",
    "rcl_interfaces/SetParametersAtomically",
    "simulation_interfaces/LoadWorld",
    "simulation_interfaces/ResetSimulation",
    "simulation_interfaces/SetEntityState",
    "simulation_interfaces/SetSimulationState",
    "std_srvs/Trigger",
    "simulation_interfaces/SpawnEntity",
    "simulation_interfaces/StepSimulation",
    "simulation_interfaces/UnloadWorld",
]

# 去重
unique_service_types = sorted(set(service_types))

print("=" * 80)
print("测试所有 ROS2 服务类型的随机数据生成")
print("=" * 80)
print(f"\n找到 {len(unique_service_types)} 个唯一的服务类型\n")

results = {
    'success': [],
    'failed': [],
    'error_details': defaultdict(list)
}

for i, srv_type in enumerate(unique_service_types, 1):
    print(f"\n[{i}/{len(unique_service_types)}] 测试: {srv_type}")
    print("-" * 80)
    
    try:
        # 运行生成工具
        result = subprocess.run(
            ['python3', '-m', 'ros2_fuzzer.generate_random_data_by_service', 
             srv_type, '-n', '1', '-f', 'compact'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print(f"✅ 成功!")
            print(f"生成的数据: {result.stdout.strip()[:100]}...")
            results['success'].append(srv_type)
        else:
            print(f"❌ 失败 (返回码: {result.returncode})")
            error_msg = result.stderr.strip().split('\n')[-1] if result.stderr else "Unknown error"
            print(f"错误: {error_msg}")
            results['failed'].append(srv_type)
            results['error_details'][error_msg].append(srv_type)
            
    except subprocess.TimeoutExpired:
        print(f"⏱️  超时")
        results['failed'].append(srv_type)
        results['error_details']['Timeout'].append(srv_type)
    except Exception as e:
        print(f"💥 异常: {e}")
        results['failed'].append(srv_type)
        results['error_details'][str(e)].append(srv_type)

# 打印总结
print("\n" + "=" * 80)
print("测试总结")
print("=" * 80)
print(f"\n✅ 成功: {len(results['success'])}/{len(unique_service_types)}")
print(f"❌ 失败: {len(results['failed'])}/{len(unique_service_types)}")

if results['success']:
    print(f"\n成功的服务类型 ({len(results['success'])}):")
    for srv in results['success']:
        print(f"  ✅ {srv}")

if results['failed']:
    print(f"\n失败的服务类型 ({len(results['failed'])}):")
    for srv in results['failed']:
        print(f"  ❌ {srv}")

if results['error_details']:
    print("\n错误详情:")
    for error, services in results['error_details'].items():
        print(f"\n  错误: {error}")
        for srv in services:
            print(f"    - {srv}")

print("\n" + "=" * 80)

# 返回适当的退出码
sys.exit(0 if len(results['failed']) == 0 else 1)
