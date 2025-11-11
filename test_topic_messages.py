#!/usr/bin/env python3
"""
测试常见的 ROS2 消息类型
"""
import subprocess
import sys
from collections import defaultdict

# 常见的 ROS2 消息类型
message_types = [
    # 标准消息
    "std_msgs/String",
    "std_msgs/Int32",
    "std_msgs/Float64",
    "std_msgs/Bool",
    "std_msgs/Header",
    "std_msgs/ColorRGBA",
    
    # 几何消息
    "geometry_msgs/Point",
    "geometry_msgs/Pose",
    "geometry_msgs/PoseStamped",
    "geometry_msgs/Twist",
    "geometry_msgs/Vector3",
    "geometry_msgs/Quaternion",
    
    # 传感器消息
    "sensor_msgs/Image",
    "sensor_msgs/LaserScan",
    "sensor_msgs/PointCloud2",
    "sensor_msgs/Imu",
    
    # RCL 接口
    "rcl_interfaces/Log",
    "rcl_interfaces/ParameterEvent",
    
    # 内置接口
    "builtin_interfaces/Time",
    "builtin_interfaces/Duration",
]

print("=" * 80)
print("测试常见 ROS2 消息类型的随机数据生成")
print("=" * 80)
print(f"\n准备测试 {len(message_types)} 个消息类型\n")

results = {
    'success': [],
    'failed': [],
    'error_details': defaultdict(list)
}

for i, msg_type in enumerate(message_types, 1):
    print(f"\n[{i}/{len(message_types)}] 测试: {msg_type}")
    print("-" * 80)
    
    try:
        # 运行生成工具
        result = subprocess.run(
            ['python3', '-m', 'ros2_fuzzer.generate_random_data_by_topic', 
             msg_type, '-n', '1', '-f', 'compact'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print(f"✅ 成功!")
            output = result.stdout.strip()
            if len(output) > 100:
                print(f"生成的数据: {output[:100]}...")
            else:
                print(f"生成的数据: {output}")
            results['success'].append(msg_type)
        else:
            print(f"❌ 失败 (返回码: {result.returncode})")
            error_msg = result.stderr.strip().split('\n')[-1] if result.stderr else "Unknown error"
            print(f"错误: {error_msg[:100]}")
            results['failed'].append(msg_type)
            results['error_details'][error_msg[:100]].append(msg_type)
            
    except subprocess.TimeoutExpired:
        print(f"⏱️  超时")
        results['failed'].append(msg_type)
        results['error_details']['Timeout'].append(msg_type)
    except Exception as e:
        print(f"💥 异常: {e}")
        results['failed'].append(msg_type)
        results['error_details'][str(e)[:100]].append(msg_type)

# 打印总结
print("\n" + "=" * 80)
print("测试总结")
print("=" * 80)
print(f"\n✅ 成功: {len(results['success'])}/{len(message_types)}")
print(f"❌ 失败: {len(results['failed'])}/{len(message_types)}")

if results['success']:
    print(f"\n成功的消息类型 ({len(results['success'])}):")
    for msg in results['success']:
        print(f"  ✅ {msg}")

if results['failed']:
    print(f"\n失败的消息类型 ({len(results['failed'])}):")
    for msg in results['failed']:
        print(f"  ❌ {msg}")

if results['error_details']:
    print("\n错误详情:")
    for error, messages in results['error_details'].items():
        print(f"\n  错误: {error}")
        for msg in messages:
            print(f"    - {msg}")

print("\n" + "=" * 80)

# 返回适当的退出码
sys.exit(0 if len(results['failed']) == 0 else 1)
