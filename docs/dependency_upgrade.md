# 依赖版本升级说明

## 问题描述

旧版本的 `hypothesis==3.82` (2018年发布) 与 Python 3.8+ 不兼容，会导致以下错误：

```
TypeError: an integer is required (got type bytes)
```

这是因为 Python 3.8 对字节码对象的内部结构进行了修改，旧版本的 hypothesis 无法正确处理。

## 解决方案

### 1. 升级依赖版本

已将 `setup.py` 中的依赖更新为：

```python
install_requires=[
    'hypothesis>=6.0.0',    # 从 3.82 升级
    'attrs>=22.2.0',        # 从 19.1.0 升级 (hypothesis 6.x 要求)
    'numpy>=1.16.3',        # 保持不变
],
```

### 2. 修复代码兼容性

移除了 `ros_basic_strategies.py` 中已废弃的 `@st.defines_strategy` 装饰器：

**修改前：**
```python
@st.defines_strategy
def string(min_size=STRING_MIN_SIZE, max_size=STRING_MAX_SIZE):
    ...

@st.defines_strategy
def array(elements=None, min_size=None, max_size=None, ...):
    ...
```

**修改后：**
```python
def string(min_size=STRING_MIN_SIZE, max_size=STRING_MAX_SIZE):
    ...

def array(elements=None, min_size=None, max_size=None, ...):
    ...
```

在 hypothesis 6.x 中，`@st.defines_strategy` 已被移除，直接返回策略即可。

## 安装步骤

### 方法 1: 使用 pip 安装

```bash
# 卸载旧版本
pip3 uninstall -y hypothesis attrs

# 安装新版本
pip3 install 'hypothesis>=6.0.0' 'attrs>=22.2.0' 'numpy>=1.16.3'
```

### 方法 2: 从 setup.py 安装

```bash
cd /path/to/ros2_fuzzer
pip3 install -e .
```

## 验证安装

```bash
# 测试 generate_random_data_by_service 工具
python3 -m ros2_fuzzer.generate_random_data_by_service --help

# 测试原有的 fuzzer
ros2_fuzzer --help  # 如果通过 pip install -e . 安装
```

## 版本兼容性

| Python 版本 | hypothesis 版本 | attrs 版本 | 状态 |
|------------|----------------|-----------|------|
| 3.6 - 3.7  | 3.82          | 19.1.0    | ⚠️ 旧版本，建议升级 |
| 3.8+       | 3.82          | 19.1.0    | ❌ 不兼容 |
| 3.8+       | >=6.0.0       | >=22.2.0  | ✅ 推荐 |

## 新增功能

同时在 `setup.py` 中添加了新的命令行入口点：

```python
entry_points={
    'console_scripts': [
        'ros2_fuzzer=ros2_fuzzer.ros_fuzzer:main',
        'ros2_generate_random_data=ros2_fuzzer.generate_random_data_by_service:main',  # 新增
    ],
},
```

安装后可以直接使用：

```bash
ros2_generate_random_data example_interfaces/AddTwoInts -n 5 -f json
```

## 注意事项

1. **向后兼容性**：新版本的代码与旧版本的 hypothesis API 不兼容，如果需要在 Python 3.6-3.7 上运行，请保持原有版本。

2. **ROS2 环境**：确保已经 source 了 ROS2 环境：
   ```bash
   source /opt/ros/<distro>/setup.bash
   ```

3. **测试覆盖**：升级后建议重新运行所有测试以确保功能正常。

## 相关链接

- [Hypothesis 版本历史](https://hypothesis.readthedocs.io/en/latest/changes.html)
- [Python 3.8 字节码变更](https://docs.python.org/3/whatsnew/3.8.html)
