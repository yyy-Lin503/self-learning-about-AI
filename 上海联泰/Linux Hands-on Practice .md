#  Linux Hands-on Practice

---

一、输入lscpi

![Uploading image.png…]()



| **地址**         | **系统报的名字**                        | **它是什么**                       |
| -------------- | --------------------------------- | ------------------------------ |
| `0001:00:00.0` | NVIDIA Device **229c** PCI bridge | Tegra/Orin 自己的 PCIe 桥，不是独立 GPU |
| `0001:01:00.0` | Realtek **RTL8822CE**             | 普通 Wi-Fi 网卡                    |
| `0004:00:00.0` | NVIDIA Device **229c** PCI bridge | 又一座桥                           |
| `0004:01:00.0` | WD SN810 / SN850 NVMe             | 固态硬盘，不是计算单元                    |
| `0008:00:00.0` | NVIDIA Device **229c** PCI bridge | 第三座桥                           |
| `0008:01:00.0` | Realtek **RTL8111/8168**          | 普通千兆有线网卡                       |


结论：

1. 没有 DPU。 BlueField / Intel IPU 会写自己的名字。这两张 Realtek 只是家用/板载网卡，等于笔记里「普通网卡」，不是后勤加速卡。
2. GPU 不会出现在这份名单里。 第 1 步内核已经写了 `tegra`：GPU 和 ARM CPU 焊在同一颗 SoC 上，不走 PCIe 插槽。`lspci` 只能看见「插在 PCI 上的东西」，看不见焊在芯片内部的 GPU。

二、输入nvidia-smi
<img width="1475" height="696" alt="e3cb7845c29d0f8e2779db8813478d10" src="https://github.com/user-attachments/assets/eaa01895-803f-4f95-b1d7-734bda3a8c97" />



| **单元**  | **结论**                                            |
| ------- | ------------------------------------------------- |
| **CPU** | ARM（`aarch64`），Tegra/Orin SoC 上的核                 |
| **GPU** | Orin 集成 GPU（`nvgpu`），`nvidia-smi` 看得见，`lspci` 看不见 |
| **NPU** | 这条命令看不到。Orin 里还有 DLA（深度学习加速器），更接近笔记里的 NPU，不在这张表里  |


