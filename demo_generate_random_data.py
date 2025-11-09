#!/usr/bin/env python3
"""
演示 generate_random_data_by_service 工具的使用

注意：需要先安装并 source ROS2 环境才能运行实际的服务数据生成
"""

print("""
===============================================================================
ROS2 Service Random Data Generator - 演示
===============================================================================

已修复的问题：
✅ hypothesis 版本从 3.82 升级到 >=6.0.0 (兼容 Python 3.8+)
✅ attrs 版本从 19.1.0 升级到 >=22.2.0
✅ 移除废弃的 @st.defines_strategy 装饰器
✅ 添加新的命令行入口点

工具现在可以正常运行！

===============================================================================
使用示例（需要 ROS2 环境）：
===============================================================================

1. 简单服务 - AddTwoInts:
   $ python3 -m ros2_fuzzer.generate_random_data_by_service example_interfaces/AddTwoInts
   
   输出示例:
   ============================================================
   a: 1234567890
   b: -9876543210

2. 生成多个样例:
   $ python3 -m ros2_fuzzer.generate_random_data_by_service example_interfaces/AddTwoInts -n 3
   
3. JSON 格式输出:
   $ python3 -m ros2_fuzzer.generate_random_data_by_service example_interfaces/AddTwoInts -f json
   
   输出示例:
   {
     "a": 1234567890,
     "b": -9876543210
   }

4. 使用随机种子（可重现结果）:
   $ python3 -m ros2_fuzzer.generate_random_data_by_service example_interfaces/AddTwoInts -s 42

5. 复杂服务示例（如果有 nav_msgs）:
   $ python3 -m ros2_fuzzer.generate_random_data_by_service nav_msgs/GetMap -f json

===============================================================================
命令行参数：
===============================================================================

必需参数:
  service_type          ROS2 服务类型，格式: package_name/ServiceName
                        例如: example_interfaces/AddTwoInts

可选参数:
  -n, --num-examples    生成样例数量 (默认: 1)
  -f, --format          输出格式: pretty/json/compact (默认: pretty)
  -s, --seed            随机种子，用于可重现的结果
  -h, --help            显示帮助信息

===============================================================================
故障排除：
===============================================================================

❌ 如果看到: "TypeError: an integer is required (got type bytes)"
   → 这是旧版本 hypothesis 的问题，已通过升级修复

❌ 如果看到: "ROS2 service module: xxx does not exist"
   → 确保已安装对应的 ROS2 包
   → 确保已 source ROS2 环境: source /opt/ros/<distro>/setup.bash

❌ 如果看到: "ModuleNotFoundError: No module named 'hypothesis'"
   → 运行: pip3 install 'hypothesis>=6.0.0' 'attrs>=22.2.0'

===============================================================================
安装方式：
===============================================================================

方法 1 - 开发模式安装:
  cd /path/to/ros2_fuzzer
  pip3 install -e .
  
  安装后可以使用简短命令:
  ros2_generate_random_data example_interfaces/AddTwoInts

方法 2 - 直接使用（无需安装）:
  python3 -m ros2_fuzzer.generate_random_data_by_service <service_type>

===============================================================================
支持的数据类型：
===============================================================================

✅ 基本类型: int8, int16, int32, int64, uint8, uint16, uint32, uint64
✅ 浮点类型: float32, float64
✅ 字符串类型: string
✅ 布尔类型: boolean
✅ 字节类型: octet
✅ 数组类型: 固定长度数组 (例如: int32[5])
✅ 序列类型: 可变长度数组 (例如: int32[])
✅ 嵌套类型: 包含其他消息的消息
✅ 多层嵌套: 任意深度的嵌套结构

===============================================================================
""")

# 测试依赖是否已正确安装
try:
    import hypothesis
    import attrs
    import numpy
    print(f"✅ 依赖已安装:")
    print(f"   - hypothesis: {hypothesis.__version__}")
    print(f"   - attrs: {attrs.__version__}")
    print(f"   - numpy: {numpy.__version__}")
    print()
    
    # 检查 hypothesis 版本
    from packaging import version
    if version.parse(hypothesis.__version__) >= version.parse("6.0.0"):
        print("✅ hypothesis 版本兼容 (>= 6.0.0)")
    else:
        print("⚠️  hypothesis 版本过旧，建议升级: pip3 install --upgrade 'hypothesis>=6.0.0'")
    
    if version.parse(attrs.__version__) >= version.parse("22.2.0"):
        print("✅ attrs 版本兼容 (>= 22.2.0)")
    else:
        print("⚠️  attrs 版本过旧，建议升级: pip3 install --upgrade 'attrs>=22.2.0'")
        
except ImportError as e:
    print(f"❌ 缺少依赖: {e}")
    print("   请运行: pip3 install 'hypothesis>=6.0.0' 'attrs>=22.2.0' 'numpy>=1.16.3'")
except:
    pass

print("\n" + "="*79)
