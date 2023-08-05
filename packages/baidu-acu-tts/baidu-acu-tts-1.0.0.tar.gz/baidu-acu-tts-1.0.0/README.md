[TOC]
# 运行环境
python 版本 3.xx

# 错误码

| 错误码 | 说明 | 备注 |
| --- | --- | --- |
| 500 | 不支持输入 | - |
| 501 | 输入参数不正确 | - |
| 503 | 合成后端错误 | - |

# 其他
proto生成代码命令
```
 python -m grpc_tools.protoc --python_out=. --grpc_python_out=. -I. tts-streaming.proto
```