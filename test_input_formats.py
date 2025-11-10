#!/usr/bin/env python3
"""
测试不同输入格式的兼容性
"""
import subprocess
import sys

print("=" * 80)
print("测试服务类型输入格式的兼容性")
print("=" * 80)

test_cases = [
    {
        'name': '标准格式（不带 /srv/）',
        'input': 'simulation_interfaces/SpawnEntity',
        'description': '原始支持的格式'
    },
    {
        'name': 'ROS2 CLI 格式（带 /srv/）',
        'input': 'simulation_interfaces/srv/SpawnEntity',
        'description': 'ros2 service list -t 输出的格式'
    },
    {
        'name': '标准服务（Trigger）',
        'input': 'std_srvs/Trigger',
        'description': '简单服务'
    },
    {
        'name': '标准服务（带 /srv/）',
        'input': 'std_srvs/srv/Trigger',
        'description': 'ros2 service list -t 格式'
    },
    {
        'name': 'RCL 接口（不带 /srv/）',
        'input': 'rcl_interfaces/GetParameters',
        'description': '参数服务'
    },
    {
        'name': 'RCL 接口（带 /srv/）',
        'input': 'rcl_interfaces/srv/GetParameters',
        'description': 'ros2 service list -t 格式'
    },
]

results = {'success': 0, 'failed': 0}

for i, test in enumerate(test_cases, 1):
    print(f"\n[{i}/{len(test_cases)}] 测试: {test['name']}")
    print(f"输入: {test['input']}")
    print(f"描述: {test['description']}")
    print("-" * 80)
    
    try:
        result = subprocess.run(
            ['python3', '-m', 'ros2_fuzzer.generate_random_data_by_service',
             test['input'], '-n', '1', '-f', 'compact'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0 and result.stdout.strip():
            print(f"✅ 成功!")
            print(f"输出: {result.stdout.strip()[:80]}...")
            results['success'] += 1
        else:
            print(f"❌ 失败")
            if result.stderr:
                print(f"错误: {result.stderr.strip()[:200]}")
            results['failed'] += 1
    except Exception as e:
        print(f"💥 异常: {e}")
        results['failed'] += 1

print("\n" + "=" * 80)
print("测试总结")
print("=" * 80)
print(f"✅ 成功: {results['success']}/{len(test_cases)}")
print(f"❌ 失败: {results['failed']}/{len(test_cases)}")

if results['success'] == len(test_cases):
    print("\n🎉 所有格式都支持！")
    print("\n支持的输入格式:")
    print("  1. package_name/ServiceType           (标准格式)")
    print("  2. package_name/srv/ServiceType       (ros2 CLI 格式)")
    print("\n现在可以直接从 'ros2 service list -t' 的输出复制粘贴服务类型！")
else:
    print("\n⚠️  部分格式测试失败")

sys.exit(0 if results['failed'] == 0 else 1)
