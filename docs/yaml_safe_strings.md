# 修复 YAML 解析错误 - 字符串生成策略

## 问题

使用生成的数据调用 `ros2 service call` 时出现 YAML 解析错误：

```bash
yaml.scanner.ScannerError: while scanning a double-quoted scalar
  in "<unicode string>", line 1, column 12:
    {"names": ["\f!\IiO"]}
               ^
found unknown escape character 'I'
```

### 根本原因

之前使用 `string.printable` 生成字符串，包含了：
- `\n` (换行符, ASCII 10)
- `\t` (制表符, ASCII 9)  
- `\r` (回车符, ASCII 13)
- `\f` (换页符, ASCII 12)
- `\v` (垂直制表符, ASCII 11)
- `\\` (反斜杠)

这些字符在 YAML 中需要特殊转义，导致 `ros2 service call` 解析失败。

## 解决方案

修改字符串生成策略，使用**更安全的字符集**。

### 修改后的字符集

```python
# 安全字符集
safe_punctuation = '-_.,:;!?@#$%&*()[]{}+=/<>|~'
alphabet = ascii_letters + digits + ' ' + safe_punctuation
```

包括：
- ✅ **字母**: `a-z`, `A-Z` (52个)
- ✅ **数字**: `0-9` (10个)
- ✅ **空格**: ` ` (1个)
- ✅ **安全标点**: `-_.,:;!?@#$%&*()[]{}+=/<>|~` (30个)

**总共 93 个字符**

排除：
- ❌ 控制字符: `\n`, `\t`, `\r`, `\f`, `\v` 
- ❌ 反斜杠: `\\` (会造成转义问题)
- ❌ 引号: `"`, `'` (会造成字符串边界问题)
- ❌ 反引号: `` ` `` (shell 特殊字符)

## 对比测试

### 修改前（有问题）

```json
{
  "names": ["\f!\IiO"]
}
```

错误：
```
yaml.scanner.ScannerError: found unknown escape character 'I'
```

### 修改后（正常）

```json
{
  "names": ["E#", "@M;MX}Fzim", "bQ{jXO:"]
}
```

✅ 可以被正确解析和使用

## 实际测试结果

```bash
# 生成测试数据
$ python3 -m ros2_fuzzer.generate_random_data_by_service rcl_interfaces/GetParameters -n 5 --random -f json

{
  "names": ["W1"]
}
{
  "names": ["R", "@M;MX}Fzim", "bQ{jXO:"]
}
{
  "names": ["UK"]
}
{
  "names": ["#Z=", "tH!xH", "jb; s~"]
}
```

所有字符串都是安全的：
- ✅ 无控制字符
- ✅ 无转义问题
- ✅ JSON 解析正常
- ✅ YAML 解析正常
- ✅ 可用于 `ros2 service call`

## 字符示例

### 常见生成的字符串

```
"Etnq_p9f#Q]"      - 混合字母数字标点
"[n~>Cw"           - 括号和符号
"@M;MX}Fzim"       - 各种标点
"tH!xH"            - 感叹号
"jb; s~"           - 空格和波浪号
"UK"               - 纯字母
"W1"               - 字母数字
"#Z="              - 符号开头
```

### 支持的标点符号

| 符号 | 描述 | 示例 |
|------|------|------|
| `-` | 连字符 | `test-name` |
| `_` | 下划线 | `var_name` |
| `.` | 点 | `file.txt` |
| `,` | 逗号 | `a,b,c` |
| `:` | 冒号 | `key:value` |
| `;` | 分号 | `cmd;cmd` |
| `!` | 感叹号 | `alert!` |
| `?` | 问号 | `is_ok?` |
| `@` | at符号 | `user@host` |
| `#` | 井号 | `#tag` |
| `$` | 美元符 | `$var` |
| `%` | 百分号 | `50%` |
| `&` | 和号 | `a&b` |
| `*` | 星号 | `*.txt` |
| `()` | 圆括号 | `(test)` |
| `[]` | 方括号 | `[0]` |
| `{}` | 花括号 | `{key}` |
| `+` | 加号 | `a+b` |
| `=` | 等号 | `x=1` |
| `/` | 斜杠 | `path/to` |
| `<>` | 尖括号 | `<tag>` |
| `|` | 竖线 | `a|b` |
| `~` | 波浪号 | `~user` |

## 兼容性

### ✅ 兼容的工具

- ROS2 CLI (`ros2 service call`)
- JSON 解析器
- YAML 解析器
- Python string 操作
- Shell 命令（建议加引号）
- 日志系统
- 数据库存储

### ⚠️ 注意事项

虽然这些字符是安全的，但在某些特殊场景下仍需注意：

1. **Shell 命令行**：某些符号（如 `$`, `&`, `|`, `*`, `?`, `<`, `>`, `;`）在 shell 中有特殊含义
   - 建议：使用引号包裹
   - 示例：`ros2 service call /service "name: 'test$var'"`

2. **正则表达式**：某些符号（如 `.`, `*`, `+`, `?`, `[]`, `{}`, `|`, `()`）在正则中有特殊含义
   - 建议：需要时进行转义

3. **文件路径**：某些符号（如 `:`, `*`, `?`, `<`, `>`, `|`）在 Windows 路径中不合法
   - 建议：如果字符串用作文件名，额外过滤

## 如何自定义字符集

如果需要更严格的字符集，可以修改 `ros_basic_strategies.py`：

### 仅字母数字和常见符号
```python
alphabet = string_module.ascii_letters + string_module.digits + ' _-.'
```

### 仅小写字母数字
```python
alphabet = string_module.ascii_lowercase + string_module.digits
```

### URL 安全字符
```python
alphabet = string_module.ascii_letters + string_module.digits + '-_.~'
```

### 文件名安全字符
```python
alphabet = string_module.ascii_letters + string_module.digits + '-_.'
```

## 总结

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| YAML 解析错误 | 包含 `\f`, `\n` 等控制字符 | 使用安全字符集 |
| 转义字符错误 | `\I` 等非法转义序列 | 排除反斜杠 |
| JSON 解析问题 | 引号冲突 | 排除引号字符 |

✅ **现在生成的字符串可以安全用于**：
- `ros2 service call` 命令
- JSON 数据交换
- YAML 配置文件
- 日志和调试输出
- 实际的 ROS2 服务测试

🎯 **推荐使用方式**：
```bash
python3 -m ros2_fuzzer.generate_random_data_by_service <service_type> --random -f compact
```
