程序名称：基于 TCP 报文格式的字符串反转通信系统
开发语言：Python 3.x
依赖模块：socket、struct、threading、random、sys

运行方式：
1. 启动服务器：python reversetcpserver.py 8000
2. 启动客户端：python reversetcpclient.py 127.0.0.1 8000 5 10
   参数说明：
   - 127.0.0.1：服务器 IP
   - 8000：端口号
   - 5 10：每个数据块大小的随机范围 [Lmin, Lmax]

文件说明：
- input.txt：待反转的 ASCII 编码输入文本
- output.txt：客户端收到反转后拼接写入的完整文本