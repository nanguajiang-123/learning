# IP 地址与子网（IPv4 / IPv6）

## 概念
- IP（Internet Protocol）：用于主机之间的寻址与路由选择。
- IPv4：32 位地址，常用点分十进制表示（例如 192.168.1.1）。
- IPv6：128 位地址，解决 IPv4 地址耗尽问题，表示为冒号十六进制（例如 2001:db8::1）。

## 子网与掩码
- 子网掩码示例：255.255.255.0 等价于 /24。
- CIDR（无类域间路由）：用斜杠表示前缀长度（例如 10.0.0.0/8）。

## 子网划分（快速示例）
- 若需要 4 个子网，从 /24 划分为 /26，每个子网有 62 个可用主机（64-2）。

## 地址类型
- 单播（Unicast）、广播（Broadcast，仅 IPv4）、组播（Multicast）、任播（Anycast，常见于 IPv6）。

## 常见命令
- Windows：`ipconfig /all`、`route print`。
- Linux：`ip addr`、`ip route`、`route -n`、`ss`/`netstat`。

## 静态 IP 配置示例（Linux）

ip addr add 192.168.100.10/24 dev eth0
ip route add default via 192.168.100.1

## DHCP 与地址分配
- DHCP 服务用于自动分配 IPv4 地址、子网掩码、网关和 DNS。
- IPv6 常用 SLAAC（无状态地址自动配置）和 DHCPv6。

## 子网计算快速方法
- 可用主机数 = 2^(32 - 前缀长度) - 2（特殊情况：/31、/32）。
- 网络地址：将主机地址与掩码按位与。

## 安全与实践
- 避免在公网设备上使用私有 IP 曝露服务，使用 NAT 或公网地址池。
- 对关键服务器使用静态 IP 并在 DHCP 服务器中做登记。

## 延伸工具
- `ipcalc`、在线子网计算器、Wireshark（抓包分析 IP 层问题）。
