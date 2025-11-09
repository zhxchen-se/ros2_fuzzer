# ROS2 Service Random Data Generator

## 概述

`generate_random_data_by_service.py` 是一个独立的命令行工具，用于根据 ROS2 服务类型生成符合格式的随机输入数据。该工具从 `ros_fuzzer.py` 中提取了核心数据生成逻辑，可以独立使用。

## 功能特性

- ✅ 根据服务名自动解析服务请求结构
- ✅ 生成符合格式的随机数据
- ✅ 支持基本类型（int, float, string, bool等）
- ✅ 支持复杂嵌套类型
- ✅ 支持数组和序列
- ✅ 多种输出格式（pretty, json, compact）
- ✅ 可指定随机种子以获得可重现的结果
- ✅ 可批量生成多个样例

## 安装依赖

```bash
pip install hypothesis numpy
```

## 命令行用法

### 基本语法

```bash
python3 -m ros2_fuzzer.generate_random_data_by_service [OPTIONS] <service_type>
```

### 参数说明

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `service_type` | - | ROS2 服务类型（必需） | - |
| `--num-examples` | `-n` | 生成样例数量 | 1 |
| `--format` | `-f` | 输出格式：pretty/json/compact | pretty |
| `--seed` | `-s` | 随机种子（用于可重现结果） | None |
| `--help` | `-h` | 显示帮助信息 | - |

## 使用示例

### 1. 生成单个随机样例（默认格式）

```bash
python3 -m ros2_fuzzer.generate_random_data_by_service example_interfaces/AddTwoInts
```

输出示例：
```
============================================================
Example #1
============================================================
a: 1234567890
b: -9876543210
```

### 2. 生成多个样例

```bash
python3 -m ros2_fuzzer.generate_random_data_by_service example_interfaces/AddTwoInts -n 5
```

### 3. JSON 格式输出

```bash
python3 -m ros2_fuzzer.generate_random_data_by_service example_interfaces/AddTwoInts -f json
```

输出示例：
```json
{
  "a": 1234567890,
  "b": -9876543210
}
```

### 4. 紧凑 JSON 格式（单行）

```bash
python3 -m ros2_fuzzer.generate_random_data_by_service example_interfaces/AddTwoInts -f compact
```

输出示例：
```json
{"a": 1234567890, "b": -9876543210}
```

### 5. 使用随机种子（可重现结果）

```bash
python3 -m ros2_fuzzer.generate_random_data_by_service example_interfaces/AddTwoInts -s 42
```

使用相同的种子会生成相同的数据。

### 6. 组合使用多个选项

```bash
python3 -m ros2_fuzzer.generate_random_data_by_service example_interfaces/AddTwoInts -n 3 -f json -s 42
```

## 支持的服务类型示例

### 简单服务

```bash
# 整数输入
python3 -m ros2_fuzzer.generate_random_data_by_service example_interfaces/AddTwoInts

# 布尔输入
python3 -m ros2_fuzzer.generate_random_data_by_service example_interfaces/SetBool
```

### 复杂嵌套服务

```bash
# 包含嵌套消息类型
python3 -m ros2_fuzzer.generate_random_data_by_service nav_msgs/GetMap

# 包含数组
python3 -m ros2_fuzzer.generate_random_data_by_service sensor_msgs/SetCameraInfo
```

## 输出格式对比

### Pretty 格式（默认）
- 人类可读
- 带缩进的层级结构
- 适合调试和查看

示例：
```
position (geometry_msgs/Point):
  x: 1.234
  y: 5.678
  z: 9.012
name: "test_string"
```

### JSON 格式
- 标准 JSON 格式
- 带缩进，便于阅读
- 适合保存和解析

示例：
```json
{
  "position": {
    "x": 1.234,
    "y": 5.678,
    "z": 9.012
  },
  "name": "test_string"
}
```

### Compact 格式
- 单行 JSON
- 无缩进，节省空间
- 适合日志记录和批处理

示例：
```json
{"position": {"x": 1.234, "y": 5.678, "z": 9.012}, "name": "test_string"}
```

## 应用场景

1. **服务接口测试**：快速生成测试数据验证服务处理逻辑
2. **模糊测试**：生成随机输入发现边界情况和异常
3. **文档生成**：创建服务使用示例
4. **调试辅助**：探索服务请求结构
5. **性能测试**：批量生成测试负载

## 与原 fuzzer 的区别

| 特性 | generate_random_data_by_service.py | ros_fuzzer.py |
|------|-----------------------------------|---------------|
| 目的 | 生成并打印数据 | 发送数据到实际服务 |
| ROS2 节点 | 不需要 | 需要 |
| 输出 | 控制台打印 | 发送到服务端点 |
| 用途 | 数据查看、调试 | 实际 fuzzing 测试 |

## 技术实现

该工具复用了 `ros_commons.py` 中的核心函数：

1. **`ros_interface_loader_str()`**：动态加载服务类型
2. **`map_ros_types()`**：递归解析服务结构并生成 Hypothesis 策略
3. **`dynamic_strategy_generator_ros()`**：生成符合格式的消息实例

新增功能：

1. **`ros_msg_to_dict()`**：将 ROS2 消息转换为字典（支持 JSON 序列化）
2. **`generate_random_service_data()`**：封装数据生成逻辑
3. **`print_service_request()`**：多格式输出
4. **`print_message_pretty()`**：美化打印嵌套消息

## 故障排除

### 找不到服务类型

**错误**：`Error: Could not load service type 'xxx/yyy'`

**解决**：
1. 确保 ROS2 包已安装
2. 确保已 source ROS2 环境：`source /opt/ros/<distro>/setup.bash`
3. 检查服务类型名称是否正确

### 依赖缺失

**错误**：`ModuleNotFoundError: No module named 'hypothesis'`

**解决**：
```bash
pip install hypothesis numpy
```

## 示例脚本

查看 `test_generate_random_data.py` 获取完整的使用示例和说明。

## 贡献

该工具是 ros2_fuzzer 项目的一部分。欢迎提交问题和改进建议！
