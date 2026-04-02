# VLAN（虚拟局域网）

## 概念
- VLAN（Virtual LAN）：在二层交换网络上，根据逻辑分组而不是物理位置划分广播域。
- 作用：隔离广播域、提高安全性、简化网络管理、限定流量范围。

## 类型
- 访问端口（Access Port）：连接终端设备，属于单一 VLAN。
- 干道端口（Trunk Port）：在交换机之间传递多个 VLAN 的流量，通常使用 802.1Q 封装。

## VLAN 标识
- VLAN ID 范围（常见）：1-4094（0 与 4095 为保留），默认 VLAN 通常为 1。

## 常见配置示例（Cisco 风格）
- 配置访问端口：

interface FastEthernet0/1
 switchport mode access
 switchport access vlan 10

- 配置干道端口（802.1Q）：

interface GigabitEthernet0/1
 switchport trunk encapsulation dot1q
 switchport mode trunk
 switchport trunk allowed vlan 10,20,30

## Linux 下的 VLAN（示例）
- 使用 iproute2：

ip link add link eth0 name eth0.10 type vlan id 10
ip addr add 192.168.10.2/24 dev eth0.10
ip link set dev eth0.10 up

## 注意事项
- 管理 VLAN 的原生 VLAN 和本地管理 VLAN（例如交换机管理接口）要小心配置，避免使用默认 VLAN 作为管理 VLAN。
- Trunk 上的原生 VLAN（native VLAN）可能产生安全风险（双重标记攻击），建议明确配置并尽量避免使用默认 VLAN。

## 常见故障排查命令
- show vlan brief（查看交换机 VLAN）
- show interfaces trunk（查看 trunk 状态）
- 在主机端：`ip addr` / `ifconfig` / `ip -d link`（查看 VLAN 接口）

## 延伸阅读
- 802.1Q 标准、Private VLAN（PVLAN）和 VLAN 聚合（VLAN pooling）。  
![alt text](image-1.png)
![alt text](image-2.png)