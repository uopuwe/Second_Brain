# Razavi PLL 第 8.9–8.10 节：Spur 与相位噪声传递函数（四问整理）

基于当前聊天四轮技术问答整理

2026-08-06

> **文档定位**　本文将当前聊天中的四个问题整理为一套连续的 PLL 分析框架：先解释为什么 $I_{p}/C_{2}$ 主导 reference spur，再从小相位调制推导一阶单边带幅度 $\beta/2$，继而推导闭环分母 $D(s)$，最后建立统一噪声注入模型并推导各噪声源到输出相位的传递函数。公式均按可编辑 Word 原生公式组织，插图均为重新绘制的出版级示意图。

## 内容结构

1.  **为何** $I_{p}/C_{2}$ **决定 reference spur**：误差电荷、控制电压纹波、VCO 相位调制与带宽-spur 权衡。

2.  **为何一阶单边带幅度约为** $\beta/2$：小角度展开、积化和差、Bessel 函数与 dBc 换算。

3.  $D(s)$ **的完整表达式**：含 $C_{2}$ 的三阶模型与常用二阶近似。

4.  **PLL 各噪声源 phase-noise transfer function**：统一模型、逐项推导、PSD 汇总与设计结论。

## 符号与假设

| **符号**         | **含义**                     | **单位或说明**             |
|------------------|------------------------------|----------------------------|
| I_p              | Charge pump 主电流           | A                          |
| K_phi = I_p/(2π) | PFD/CP 平均相位-电流增益     | A/rad                      |
| K_VCO            | VCO 控制增益                 | rad/s/V                    |
| M                | 反馈分频比                   | 无量纲                     |
| R1, C1, C2       | 被动环路滤波器参数           | C2 直接接在控制节点        |
| ω_n, ζ           | 二阶近似的自然频率、阻尼系数 | rad/s、无量纲              |
| ω_p3             | C2 引入的额外极点            | rad/s                      |
| D(s)             | 闭环特征多项式               | 文中分别给出二阶、三阶形式 |

> **模型边界**　除特别说明外，采用连续时间、小信号、Type-II CPPLL 模型；CP 周期门控、aliasing、fractional pattern spur、VCO 非线性和供电路径相关性在对应小节单独说明。

# 1　为何 $I_{p}/C_{2}$ 决定 Reference Spur

## 1.1 从“周期性误差电荷”开始

锁定状态下，理想 PFD/CP 的平均净输出电荷为零。然而 UP/DN 电流失配、reset 延迟、clock feedthrough、charge injection、有限输出电阻和 leakage 等非理想，会在每个参考周期向环路滤波器注入一个确定性的误差电荷包。若误差电流近似为幅度 $I_{e}$、持续时间 $\tau_{e}$ 的窄脉冲，则

$$\Delta Q = \int i_{e}(t)\, dt \approx I_{e}\tau_{e}.\quad\quad(1.1)$$

若误差电流是 CP 主电流的固定比例，写成

$$I_{e} = \varepsilon I_{p},\quad\quad(1.2)$$

则

$$\Delta Q \approx \varepsilon I_{p}\tau_{e}.\quad\quad(1.3)$$

这里真正危险的不是平均电流，而是**每个参考周期重复出现的确定性电荷面积**。随机噪声会形成连续相噪底，周期性误差则会在 $f_{REF}$ 及其谐波处形成离散 spur。

<img src="media/rId22.png" title="PLL 技术示意图 1" style="width:6.8in;height:2.94667in" alt="PLL 技术示意图 1，用于说明 reference spur、相位调制或噪声传递函数。" />

图 1　Reference spur 从 CP 周期误差到输出边带的物理链条。

## 1.2 为什么快速误差主要由 $C_{2}$ 承担

三阶被动滤波器的两条支路分别为

$$Z_{1}(s) = R_{1} + \frac{1}{sC_{1}},\quad\quad Z_{2}(s) = \frac{1}{sC_{2}}.\quad\quad(1.4)$$

在 CP 开关边沿附近，误差脉冲包含大量高频成分。此时

$$\left| Z_{2}(j\omega) \right| = \frac{1}{\omega C_{2}} \rightarrow 0,\quad\quad Z_{1}(j\omega) \rightarrow R_{1}.\quad\quad(1.5)$$

因此快速电荷优先进入直接连接在 $V_{cont}$ 节点上的 $C_{2}$，使控制电压产生近似阶跃：

$$\Delta V_{cont} \approx \frac{\Delta Q}{C_{2}} \approx \frac{\varepsilon I_{p}\tau_{e}}{C_{2}}.\quad\quad(1.6)$$

由此得到第 8.9 节使用的核心比例：

$$\Delta V_{cont} \propto \frac{I_{p}}{C_{2}}.\quad\quad(1.7)$$

> **物理直觉**　$I_{p}$ 决定一次误差事件可能搬运多少电荷，$C_{2}$ 决定同样的电荷会造成多大的控制电压跳变。$C_{1}$ 主要建立积分状态与低频环路动态；$C_{2}$ 则直接面对 CP 边沿产生的快速扰动。

## 1.3 控制电压纹波如何变成输出 spur

设控制节点的一次谐波纹波为

$$v_{ripple}(t) = V_{1}\cos\omega_{REF}t.\quad\quad(1.8)$$

VCO 的瞬时角频率扰动为

$$\Delta\omega(t) = K_{VCO}V_{1}\cos\omega_{REF}t.\quad\quad(1.9)$$

相位是角频率的积分：

$$\phi_{m}(t) = \int\Delta\omega(t)\, dt = \frac{K_{VCO}V_{1}}{\omega_{REF}}\sin\omega_{REF}t.\quad\quad(1.10)$$

定义相位调制指数

$$\beta = \frac{K_{VCO}V_{1}}{\omega_{REF}}.\quad\quad(1.11)$$

小调制条件下，一阶单边带相对于载波的幅度约为

$$\frac{A_{spur}}{A_{carrier}} \approx \frac{\beta}{2} = \frac{K_{VCO}V_{1}}{2\omega_{REF}}.\quad\quad(1.12)$$

再代入 $V_{1} \propto I_{p}/C_{2}$，得到

$$\frac{A_{spur}}{A_{carrier}} \propto \frac{K_{VCO}}{2\omega_{REF}}\frac{I_{p}}{C_{2}}.\quad\quad(1.13)$$

在 $K_{VCO}$、$f_{REF}$、误差脉宽与波形形状近似不变时，reference spur 的线性幅度便近似正比于 $I_{p}/C_{2}$。

## 1.4 20 dB Spur 改善为何采用协同缩放

spur 线性幅度降低 10 倍，对应

$$20\log_{10}\left( \frac{1}{10} \right) = - 20\ dB.\quad\quad(1.14)$$

若只令 $I_{p}$ 降低 10 倍，unity-gain bandwidth 也近似降低 10 倍：

$$\omega_{u} \approx \frac{R_{1}I_{p}K_{VCO}}{2\pi M}.\quad\quad(1.15)$$

这会过度牺牲锁定速度和 VCO 相噪抑制。Razavi 第 8.9 节采用更平衡的缩放：

$$I_{p}\prime = \frac{I_{p}}{\sqrt{10}},\quad\quad C_{2}\prime = \sqrt{10}C_{2},\quad\quad C_{1}\prime = \sqrt{10}C_{1}.\quad\quad(1.16)$$

于是

$$\frac{I_{p}\prime}{C_{2}\prime} = \frac{1}{10}\frac{I_{p}}{C_{2}},\quad\quad(1.17)$$

同时

$$\omega_{u}\prime \approx \frac{\omega_{u}}{\sqrt{10}},\quad\quad\omega_{p3}\prime \approx \frac{\omega_{p3}}{\sqrt{10}},\quad\quad\zeta\prime \approx \zeta.\quad\quad(1.18)$$

<img src="media/rId28.png" title="PLL 技术示意图 2" style="width:6.8in;height:2.94667in" alt="PLL 技术示意图 2，用于说明 reference spur、相位调制或噪声传递函数。" />

图 2　20 dB spur 改善时的协同参数缩放。

因此 $\omega_{p3}/\omega_{u}$ 基本保持不变，第三极点相对于交越频率的位置没有被破坏，阻尼系数也近似不变。

## 1.5 “由 $I_{p}/C_{2}$ 决定”成立的边界

更完整的 spur 关系应写成

$$A_{spur} \propto \frac{K_{VCO}}{\omega_{REF}}\frac{I_{p}\tau_{e}}{C_{2}}\, k_{wave},\quad\quad(1.19)$$

其中 $k_{wave}$ 表示纹波波形的一次傅里叶系数以及 UP/DN 极性、脉冲形状等因素。因此 $I_{p}/C_{2}$ 是第 8.9 节缩放分析中的主导比例，而不是对所有 spur 机制都适用的普遍定律。以下情况可能不服从该比例：

- divider 或数字时钟直接耦合到 VCO 输出或谐振腔；

- VCO、buffer 或供电网络的周期性扰动占主导；

- fractional-N 序列、DTC/DAC 非线性产生的 fractional spur；

- CP 误差脉宽 $\tau_{e}$ 随 $I_{p}$、器件尺寸或控制电压显著变化；

- VCO 的 $K_{VCO}$ 非线性把高次纹波下变频为一阶边带。

# 2　为何一阶单边带幅度约为 $\beta/2$

## 2.1 相位调制信号

设 VCO 输出为

$$v(t) = A_{c}\cos\left\lbrack \omega_{c}t + \beta\sin\left( \omega_{m}t \right) \right\rbrack,\quad\quad(2.1)$$

其中 $A_{c}$ 是未调制载波峰值，$\omega_{m}$ 在 PLL reference-spur 问题中通常等于 $\omega_{REF}$，$\beta$ 是峰值相位偏移，单位为 rad。

<img src="media/rId34.png" title="PLL 技术示意图 3" style="width:6.8in;height:3.44533in" alt="PLL 技术示意图 3，用于说明 reference spur、相位调制或噪声传递函数。" />

图 3　小相位调制在载波两侧形成幅度为 $A_{c}\beta/2$ 的一阶边带。

## 2.2 小角度展开

当

$$|\beta| \ll 1,\quad\quad(2.2)$$

使用

$$\cos(a + b) = \cos a\cos b - \sin a\sin b,\quad\quad(2.3)$$

以及

$$\cos b \approx 1,\quad\quad\sin b \approx b,\quad\quad(2.4)$$

得到

$$v(t) \approx A_{c}\cos\omega_{c}t - A_{c}\beta\sin\omega_{m}t\sin\omega_{c}t.\quad\quad(2.5)$$

再利用积化和差公式

$$\sin x\sin y = \frac{1}{2}\left\lbrack \cos(y - x) - \cos(y + x) \right\rbrack,\quad\quad(2.6)$$

可得

$$\begin{matrix}
v(t) \approx & A_{c}\cos\omega_{c}t \\
 & - \frac{A_{c}\beta}{2}\cos\left\lbrack \left( \omega_{c} - \omega_{m} \right)t \right\rbrack \\
 & + \frac{A_{c}\beta}{2}\cos\left\lbrack \left( \omega_{c} + \omega_{m} \right)t \right\rbrack.
\end{matrix}\quad\quad(2.7)$$

因此载波幅度约为 $A_{c}$，上下两个一阶边带的幅度均为 $A_{c}\beta/2$：

$$\frac{A_{USB}}{A_{c}} = \frac{A_{LSB}}{A_{c}} \approx \frac{\beta}{2}.\quad\quad(2.8)$$

$1/2$ **的来源**　它来自积化和差公式：相位扰动项是两个正弦的乘积，展开后被平均分配到 $\omega_{c} - \omega_{m}$ 与 $\omega_{c} + \omega_{m}$ 两个频率分量。

## 2.3 幅度比、功率比与 dBc

式 (2.8) 是幅度比。对于相同阻抗，单边 spur 的功率比为

$$\frac{P_{spur}}{P_{carrier}} \approx \left( \frac{\beta}{2} \right)^{2}.\quad\quad(2.9)$$

因此

$$L_{spur} \approx 10\log_{10}\left( \frac{\beta^{2}}{4} \right) = 20\log_{10}\left( \frac{\beta}{2} \right)\ dBc.\quad\quad(2.10)$$

例如，$\beta = 0.01$ 时

$$\frac{A_{spur}}{A_{c}} \approx 0.005,\quad\quad L_{spur} \approx - 46.0\ dBc.\quad\quad(2.11)$$

$\beta$ 降低 10 倍，单边 spur 改善 20 dB。

## 2.4 Bessel 函数的精确表达

完整的正弦相位调制展开为

$$v(t) = A_{c}\sum_{n = - \infty}^{+ \infty}J_{n}(\beta)\cos\left\lbrack \left( \omega_{c} + n\omega_{m} \right)t \right\rbrack.\quad\quad(2.12)$$

其中 $J_{n}(\beta)$ 是第一类 Bessel 函数。精确的载波与一阶边带幅度分别为

$$A_{carrier} = A_{c}J_{0}(\beta),\quad\quad A_{spur} = A_{c}\left| J_{1}(\beta) \right|.\quad\quad(2.13)$$

所以

$$\frac{A_{spur}}{A_{carrier}} = \frac{\left| J_{1}(\beta) \right|}{\left| J_{0}(\beta) \right|}.\quad\quad(2.14)$$

当 $|\beta| \ll 1$ 时，

$$J_{0}(\beta) \approx 1 - \frac{\beta^{2}}{4},\quad\quad J_{1}(\beta) \approx \frac{\beta}{2},\quad\quad(2.15)$$

于是式 (2.14) 退化为 $\beta/2$。当 $\beta$ 不再很小时，必须使用 Bessel 函数，且二阶、三阶边带不再可以忽略。

## 2.5 映射回 PLL

控制电压纹波

$$v_{cont}(t) = V_{1}\cos\omega_{REF}t\quad\quad(2.16)$$

经 VCO 转换后产生

$$\beta = \frac{K_{VCO}V_{1}}{\omega_{REF}}.\quad\quad(2.17)$$

所以

$$\frac{A_{spur}}{A_{carrier}} \approx \frac{K_{VCO}V_{1}}{2\omega_{REF}}.\quad\quad(2.18)$$

这也揭示了两个常被忽略的结论：

1.  相同的控制电压纹波在更高 $f_{REF}$ 下产生更小的相位调制指数；

2.  降低 $K_{VCO}$ 不仅有利于供电敏感度和控制噪声，也直接降低 reference spur 的相位调制效率。

# 3　输入相位传递函数与 $D(s)$

## 3.1 含 $C_{2}$ 的精确环路滤波器阻抗

被动滤波器为串联支路 $R_{1} + 1/\left( sC_{1} \right)$ 与电容 $1/\left( sC_{2} \right)$ 的并联：

$$Z(s) = \left( R_{1} + \frac{1}{sC_{1}} \right) \parallel \frac{1}{sC_{2}}.\quad\quad(3.1)$$

化简得

$$Z(s) = \frac{1 + sR_{1}C_{1}}{s\left( C_{1} + C_{2} + sR_{1}C_{1}C_{2} \right)}.\quad\quad(3.2)$$

进一步写成极点-零点形式：

$$Z(s) = \frac{1 + sR_{1}C_{1}}{s\left( C_{1} + C_{2} \right)\left( 1 + s\frac{R_{1}C_{1}C_{2}}{C_{1} + C_{2}} \right)}.\quad\quad(3.3)$$

因此

$$\omega_{z} = \frac{1}{R_{1}C_{1}},\quad\quad\omega_{p3} = \frac{C_{1} + C_{2}}{R_{1}C_{1}C_{2}}.\quad\quad(3.4)$$

当 $C_{1} \gg C_{2}$ 时，

$$\omega_{p3} \approx \frac{1}{R_{1}C_{2}}.\quad\quad(3.5)$$

<img src="media/rId43.png" title="PLL 技术示意图 4" style="width:6.8in;height:3.44533in" alt="PLL 技术示意图 4，用于说明 reference spur、相位调制或噪声传递函数。" />

图 4　Type-II CPPLL、三阶环路滤波器及 $D(s)$ 的两种模型。

## 3.2 开环增益

定义

$$K_{\phi} = \frac{I_{p}}{2\pi}.\quad\quad(3.6)$$

包含反馈分频器的 return ratio 为

$$L(s) = \frac{K_{\phi}K_{VCO}}{Ms}Z(s).\quad\quad(3.7)$$

代入式 (3.2)：

$$L(s) = \frac{K_{\phi}K_{VCO}\left( 1 + sR_{1}C_{1} \right)}{Ms^{2}\left( C_{1} + C_{2} + sR_{1}C_{1}C_{2} \right)}.\quad\quad(3.8)$$

输入相位到输出相位的闭环传递函数为

$$\frac{\Phi_{out}}{\Phi_{in}}(s) = M\frac{L(s)}{1 + L(s)}.\quad\quad(3.9)$$

## 3.3 精确三阶闭环分母

由 $1 + L(s) = 0$ 得到未归一化特征多项式

$$D_{raw}(s) = R_{1}C_{1}C_{2}s^{3} + \left( C_{1} + C_{2} \right)s^{2} + \frac{K_{\phi}K_{VCO}R_{1}C_{1}}{M}s + \frac{K_{\phi}K_{VCO}}{M}.\quad\quad(3.10)$$

定义

$$\omega_{n}^{2} = \frac{K_{\phi}K_{VCO}}{M\left( C_{1} + C_{2} \right)},\quad\quad(3.11)$$

$$2\zeta\omega_{n} = \frac{K_{\phi}K_{VCO}R_{1}C_{1}}{M\left( C_{1} + C_{2} \right)},\quad\quad(3.12)$$

以及

$$\frac{1}{\omega_{p3}} = \frac{R_{1}C_{1}C_{2}}{C_{1} + C_{2}}.\quad\quad(3.13)$$

将式 (3.10) 除以 $C_{1} + C_{2}$，得到归一化三阶分母

$$D_{3}(s) = \frac{s^{3}}{\omega_{p3}} + s^{2} + 2\zeta\omega_{n}s + \omega_{n}^{2}.\quad\quad(3.14)$$

分子为

$$M\left( 2\zeta\omega_{n}s + \omega_{n}^{2} \right),\quad\quad(3.15)$$

因此

$$\frac{\Phi_{out}}{\Phi_{in}}(s) = M\frac{2\zeta\omega_{n}s + \omega_{n}^{2}}{\frac{s^{3}}{\omega_{p3}} + s^{2} + 2\zeta\omega_{n}s + \omega_{n}^{2}}.\quad\quad(3.16)$$

## 3.4 常用二阶近似

若环路作用频率范围满足

$$|s| \ll \omega_{p3},\quad\quad(3.17)$$

则 $s^{3}/\omega_{p3}$ 可忽略，闭环分母退化为

$$D_{2}(s) = s^{2} + 2\zeta\omega_{n}s + \omega_{n}^{2}.\quad\quad(3.18)$$

从而

$$\frac{\Phi_{out}}{\Phi_{in}}(s) \approx M\frac{2\zeta\omega_{n}s + \omega_{n}^{2}}{s^{2} + 2\zeta\omega_{n}s + \omega_{n}^{2}}.\quad\quad(3.19)$$

这一形式正是后续噪声传递函数推导的基础。

## 3.5 如何选择二阶还是三阶模型

| **设计状态**                      | **推荐模型**               | **原因**                               |
|-----------------------------------|----------------------------|----------------------------------------|
| ω_p3 ≥ 5ω_u，且只需手算趋势       | 二阶 D2(s)                 | 第三极点对交越附近相位影响较小         |
| ω_p3 仅略高于 ω_u                 | 三阶 D3(s)                 | 第三极点直接影响相位裕度与 peaking     |
| 分析 C2 缩放、spur-bandwidth 权衡 | 三阶 D3(s)                 | C2 正是分析变量，不能先把它删除        |
| 估算带内 reference、CP 噪声       | 二阶通常足够               | 关注低频平台和主闭环带宽               |
| 签核稳定性、瞬态、PVT             | 完整传递函数与离散时间模型 | 连续时间二阶近似可能低估延迟和采样效应 |

> **常见误区**　“PLL 是二阶环”描述的是原点积分器数目和主导动态，不代表实际闭环一定只有两个极点。加入 $C_{2}$ 后，物理电路通常是三阶，只是在第三极点足够高时才近似为二阶。

# 4　PLL 各噪声源的 Phase-Noise Transfer Function

## 4.1 统一二阶模型

本章采用式 (3.18) 的二阶分母：

$$D(s) = s^{2} + 2\zeta\omega_{n}s + \omega_{n}^{2}.\quad\quad(4.1)$$

定义

$$B(s) = 2\zeta\omega_{n}s + \omega_{n}^{2}.\quad\quad(4.2)$$

开环 return ratio、闭环 tracking function 和 sensitivity function 分别为

$$L(s) = \frac{B(s)}{s^{2}},\quad\quad(4.3)$$

$$T(s) = \frac{L(s)}{1 + L(s)} = \frac{B(s)}{D(s)},\quad\quad(4.4)$$

$$S(s) = \frac{1}{1 + L(s)} = \frac{s^{2}}{D(s)}.\quad\quad(4.5)$$

并且

$$T(s) + S(s) = 1.\quad\quad(4.6)$$

这个互补关系是理解 PLL 噪声整形的核心：环路能跟踪的低频扰动进入 $T(s)$，VCO 自己产生而被反馈纠正的误差进入 $S(s)$。

<img src="media/rId52.png" title="PLL 技术示意图 5" style="width:6.8in;height:3.74in" alt="PLL 技术示意图 5，用于说明 reference spur、相位调制或噪声传递函数。" />

图 5　各主要噪声源在 PLL 中的等效注入位置。

## 4.2 含多噪声源的统一闭环方程

令

- $\Phi_{n,PFD}$：等效加在 PFD 输入端的相位噪声；

- $\Phi_{n,div}$：divider 输出、PFD 反馈端的附加相位噪声；

- $I_{n,CP}$：CP 输出端噪声电流；

- $V_{n,ctrl}$：直接串入 VCO 控制端的噪声电压；

- $\Phi_{n,VCO}$：直接加在 VCO 输出相位上的自由振荡相位噪声。

PFD 看到的相位误差为

$$\Phi_{e} = \Phi_{ref} + \Phi_{n,PFD} - \frac{\Phi_{out}}{M} - \Phi_{n,div}.\quad\quad(4.7)$$

CP 输出电流为

$$I_{CP} = K_{\phi}\Phi_{e} + I_{n,CP}.\quad\quad(4.8)$$

VCO 输出相位为

$$\Phi_{out} = \frac{K_{VCO}}{s}\left\lbrack Z(s)I_{CP} + V_{n,ctrl} \right\rbrack + \Phi_{n,VCO}.\quad\quad(4.9)$$

整理后：

$$\begin{matrix}
(1 + L)\Phi_{out} = & ML\left( \Phi_{ref} + \Phi_{n,PFD} - \Phi_{n,div} \right) \\
 & + Z(s)\frac{K_{VCO}}{s}I_{n,CP} \\
 & + \frac{K_{VCO}}{s}V_{n,ctrl} + \Phi_{n,VCO}.
\end{matrix}\quad\quad(4.10)$$

各噪声传递函数只需从式 (4.10) 逐项读取。

## 4.3 Reference 输入相位噪声

令其余噪声为零：

$$H_{ref}(s) = \frac{\Phi_{out}}{\Phi_{ref}} = M\frac{L}{1 + L} = MT(s).\quad\quad(4.11)$$

即

$$H_{ref}(s) = M\frac{2\zeta\omega_{n}s + \omega_{n}^{2}}{D(s)}.\quad\quad(4.12)$$

低频极限为

$$H_{ref}(0) = M.\quad\quad(4.13)$$

所以带内相位 PSD 被乘以 $M^{2}$：

$$S_{\phi,out,ref} \approx M^{2}S_{\phi,ref}.\quad\quad(4.14)$$

但绝对时间抖动并不乘以 $M$，因为相同的边沿时间位移在更短的输出周期中对应更大的相位角。

## 4.4 Divider 与 PFD 噪声

若 divider 噪声定义在 divider 输出、PFD 反馈端：

$$H_{div}(s) = \frac{\Phi_{out}}{\Phi_{n,div}} = - MT(s).\quad\quad(4.15)$$

负号表示反馈极性，计算 PSD 时只保留幅度平方。

若 PFD 噪声等效为输入相位噪声，则

$$H_{PFD,\phi}(s) = MT(s).\quad\quad(4.16)$$

若 PFD 的 reset、门延迟与脉冲面积波动等效为 CP 输出端电流噪声，则应使用下一节的电流噪声传递函数。预算时只能选择一种等效方式，避免重复计入同一噪声。

## 4.5 Charge Pump 输出电流噪声

噪声电流直接注入滤波器节点：

$$H_{CP}(s) = \frac{\Phi_{out}}{I_{n,CP}} = Z(s)\frac{K_{VCO}}{s}S(s).\quad\quad(4.17)$$

对二阶滤波器 $Z(s) = R_{1} + 1/\left( sC_{1} \right)$，得到

$$H_{CP}(s) = \frac{K_{VCO}}{C_{1}}\frac{1 + sR_{1}C_{1}}{D(s)}.\quad\quad(4.18)$$

也可写成

$$H_{CP}(s) = \frac{2\pi M}{I_{p}}T(s).\quad\quad(4.19)$$

因此带内低频增益为

$$H_{CP}(0) = \frac{2\pi M}{I_{p}}.\quad\quad(4.20)$$

这说明提高 $I_{p}$ 可降低 CP 电流噪声到输出相位的带内转换增益，但同时会提高滤波器面积或 spur 压制难度，仍然是系统级权衡。

### 4.5.1 CP 白噪声的周期门控与 aliasing

锁定时 UP、DN 电流源每周期只导通 $T_{res}$，定义 duty factor

$$d = \frac{T_{res}}{T_{ref}}.\quad\quad(4.21)$$

若单支路白噪声电流 PSD 为 $S_{i,CP}$，两支路近似相等，则带内输出相位 PSD 为

$$S_{\phi,CP,white} \approx 2S_{i,CP}d\left( \frac{2\pi M}{I_{p}} \right)^{2}.\quad\quad(4.22)$$

白噪声只乘一次 $d$，不是 $d^{2}$，因为周期门控会把高频白噪声谱 alias 回基带。

### 4.5.2 CP Flicker Noise

若 flicker corner 远低于 $f_{REF}/2$，可忽略 aliasing，慢噪声的幅度平均乘 $d$，PSD 因而乘 $d^{2}$：

$$S_{\phi,CP,1/f} \approx 2S_{i,CP,1/f}d^{2}\left( \frac{2\pi M}{I_{p}} \right)^{2}.\quad\quad(4.23)$$

## 4.6 VCO 自身相位噪声

VCO 自由振荡相位噪声直接加在输出，因此

$$H_{VCO}(s) = \frac{\Phi_{out}}{\Phi_{n,VCO}} = S(s) = \frac{s^{2}}{D(s)}.\quad\quad(4.24)$$

幅度平方为

$$\left| H_{VCO}(j\omega) \right|^{2} = \frac{\omega^{4}}{\left( \omega_{n}^{2} - \omega^{2} \right)^{2} + 4\zeta^{2}\omega_{n}^{2}\omega^{2}}.\quad\quad(4.25)$$

低频时

$$H_{VCO}(s) \approx \frac{s^{2}}{\omega_{n}^{2}},\quad\quad(4.26)$$

所以慢速 VCO 相位漂移被强烈抑制；高频时 $H_{VCO} \rightarrow 1$，环路来不及纠正。

自由振荡 VCO 相噪常写成

$$S_{\phi,VCO}(\omega) = \frac{\alpha}{\omega^{3}} + \frac{\beta_{v}}{\omega^{2}}.\quad\quad(4.27)$$

低频乘以 $\left| H_{VCO} \right|^{2} \propto \omega^{4}$ 后，$1/\omega^{3}$ 项变成正比于 $\omega$，$1/\omega^{2}$ 项变成正比于 $\omega^{2}$，因此 shaped VCO contribution 从低频接近零处上升，并在环路带宽附近与自由振荡谱相接。

## 4.7 Loop-Filter Resistor 与一般控制端电压噪声

直接串入 VCO 控制端的电压噪声经历

$$H_{ctrl}(s) = \frac{\Phi_{out}}{V_{n,ctrl}} = \frac{K_{VCO}}{s}S(s).\quad\quad(4.28)$$

因此

$$H_{ctrl}(s) = \frac{K_{VCO}s}{D(s)}.\quad\quad(4.29)$$

这是带通响应：低频受反馈抑制，高频又因 VCO 的频率到相位积分而下降。

$R_{1}$ 的单边热噪声电压 PSD 为

$$S_{v,R_{1}} = 4kTR_{1}.\quad\quad(4.30)$$

其输出相位 PSD 为

$$S_{\phi,R_{1}}(\omega) = \left| H_{ctrl}(j\omega) \right|^{2}\, 4kTR_{1}.\quad\quad(4.31)$$

在 $\omega = \omega_{n}$ 处，幅度达到

$$\left| H_{ctrl}\left( j\omega_{n} \right) \right| = \frac{K_{VCO}}{2\zeta\omega_{n}}.\quad\quad(4.32)$$

对应峰值相位 PSD：

$$S_{\phi,R_{1},peak} = \frac{16kT\pi^{2}M^{2}}{R_{1}I_{p}^{2}}.\quad\quad(4.33)$$

式 (4.33) 表明，虽然裸电阻噪声 $4kTR_{1}$ 随 $R_{1}$ 增大，但闭环传递函数同时变化，最终峰值反而与 $1/R_{1}$ 成正比。

## 4.8 Supply Noise

### 4.8.1 VCO Supply Noise

定义 VCO 供电角频率敏感度

$$K_{VDD} = \frac{\partial\omega_{out}}{\partial V_{DD}}.\quad\quad(4.34)$$

供电噪声先产生自由振荡相位扰动 $K_{VDD}V_{n}/s$，再经历 $S(s)$：

$$H_{VDD,VCO}(s) = \frac{K_{VDD}}{s}S(s) = \frac{K_{VDD}s}{D(s)}.\quad\quad(4.35)$$

因此 VCO supply noise 与控制端电压噪声一样呈带通，并在 $\omega_{n}$ 附近最敏感。

### 4.8.2 Charge-Pump Supply Noise

若供电变化使 UP、DN 电流产生差分变化

$$\Delta I_{CP} = K_{I,VDD}V_{n,VDD},\quad\quad(4.36)$$

则

$$H_{VDD,CP}(s) = K_{I,VDD}H_{CP}(s).\quad\quad(4.37)$$

即

$$H_{VDD,CP}(s) = K_{I,VDD}\frac{K_{VCO}}{C_{1}}\frac{1 + sR_{1}C_{1}}{D(s)}.\quad\quad(4.38)$$

如果供电仅造成 UP、DN 完全相同的 common-mode 电流变化，且两脉冲宽度、skew、compliance 和输出阻抗完全对称，理论上净电荷可以抵消；实际失配会把 common-mode supply bounce 转换成 differential charge error。

### 4.8.3 同一供电源的相关路径

若 VCO 与 CP 共用供电，同一个 $V_{n,VDD}$ 同时经过两条路径，不能把两项 PSD 当成独立噪声简单相加。应先相加复数传递函数：

$$S_{\phi,out,VDD} = \left| H_{VDD,VCO} + H_{VDD,CP} \right|^{2}S_{VDD}.\quad\quad(4.39)$$

两条路径可能增强，也可能在部分频段抵消。

## 4.9 PLL 后级 Buffer 与 Clock Tree 噪声

若噪声在 PLL 输出采样点之后加入，反馈环路无法观察和修正：

$$H_{post}(s) = 1.\quad\quad(4.40)$$

因此后级 divider、buffer、clock tree 和 package coupling 必须独立预算。

<img src="media/rId68.png" title="PLL 技术示意图 6" style="width:6.8in;height:3.71733in" alt="PLL 技术示意图 6，用于说明 reference spur、相位调制或噪声传递函数。" />

图 6　低通、高通与带通三类核心噪声整形函数。

## 4.10 总输出 Phase-Noise PSD

若各噪声源互不相关，则

$$\begin{matrix}
S_{\phi,out} = & \left| H_{ref} \right|^{2}S_{\phi,ref} + \left| H_{div} \right|^{2}S_{\phi,div} \\
 & + \left| H_{PFD} \right|^{2}S_{\phi,PFD} + \left| H_{CP} \right|^{2}S_{i,CP} \\
 & + \left| H_{VCO} \right|^{2}S_{\phi,VCO} + \left| H_{ctrl} \right|^{2}S_{v,ctrl} \\
 & + \left| H_{VDD} \right|^{2}S_{VDD} + S_{\phi,post}.
\end{matrix}\quad\quad(4.41)$$

对于相关噪声源，必须保留 cross-spectrum 项，而不能只做功率求和。

## 4.11 从相位 PSD 到积分抖动

采用单边相位 PSD 时，积分相位方差为

$$\sigma_{\phi}^{2} = \int_{f_{1}}^{f_{2}}S_{\phi,out}^{(1)}(f)\, df.\quad\quad(4.42)$$

输出 rms 时间抖动为

$$\sigma_{t} = \frac{\sigma_{\phi}}{2\pi f_{out}} = \frac{1}{2\pi f_{out}}\sqrt{\int_{f_{1}}^{f_{2}}S_{\phi,out}^{(1)}(f)\, df}.\quad\quad(4.43)$$

若从 SSB phase noise $\mathcal{L}(f)$ 转换，必须明确单边/双边 PSD 定义；常见小相位近似为 $\mathcal{L}(f) \approx S_{\phi}(f)/2$，但不同工具的定义可能相差 3 dB。

# 5　统一总结与设计结论

## 5.1 噪声传递函数总表

令

$$B(s) = 2\zeta\omega_{n}s + \omega_{n}^{2},\quad\quad D(s) = s^{2} + 2\zeta\omega_{n}s + \omega_{n}^{2}.\quad\quad(5.1)$$

| **噪声源及定义位置**         | **到输出相位的传递函数** | **形状**   | **低频极限**    |
|------------------------------|--------------------------|------------|-----------------|
| Reference phase              | M·B(s)/D(s)              | 低通       | M               |
| Divider phase，PFD 反馈端    | −M·B(s)/D(s)             | 低通       | −M              |
| PFD 等效输入 phase           | M·B(s)/D(s)              | 低通       | M               |
| CP/PFD 等效输出 current      | (K_VCO/C1)(1+sR1C1)/D(s) | 低通带零点 | 2πM/I_p         |
| VCO intrinsic phase          | s²/D(s)                  | 高通       | 0，按 s²        |
| 控制端 voltage noise         | K_VCO·s/D(s)             | 带通       | 0，按 s         |
| R1 thermal noise             | 同控制端 voltage noise   | 带通       | 0               |
| VCO supply noise             | K_VDD·s/D(s)             | 带通       | 0               |
| CP supply differential noise | K_I,VDD·H_CP(s)          | 低通带零点 | K_I,VDD·2πM/I_p |
| PLL 后级 buffer noise        | 1                        | 不整形     | 1               |

## 5.2 三条核心心智模型

> **第一条：环路前面的噪声，PLL 会跟着它走，因此低通。**　Reference、divider 和等效输入 PFD 噪声在带内被传到输出，并带有 $M$ 的相位增益。
>
> **第二条：VCO 自己产生的相位错误，PLL 会试图纠正，因此高通。**　低频 VCO 漂移被强反馈压制，高频 VCO 相噪基本原样通过。
>
> **第三条：直接改变 VCO 频率的电压噪声，低频被反馈纠正，高频又受积分器衰减，因此带通。**　Loop-filter resistor、VCO supply 和一般 control-node voltage noise 常在 $\omega_{n}$ 附近形成 hump。

## 5.3 Bandwidth 的本质权衡

增大环路带宽：

- 优点：抑制更多 VCO 近端相噪和慢速供电/控制扰动；

- 代价：通过更多 reference、divider、PFD 和 CP 带内噪声；

- 额外风险：reference ripple、spur、采样延迟与第三极点对稳定性的影响更严重。

减小环路带宽：

- 优点：降低 reference-side 噪声积分面积和周期纹波的输出转换；

- 代价：VCO 相噪抑制变差，积分 jitter 可能上升，锁定更慢。

因此最优带宽通常位于 reference-side contribution 与 VCO-side contribution 的平衡点，并同时满足 spur、相位裕度、锁定时间与面积约束。

## 5.4 与 Spur 设计的统一关系

本聊天四个问题实际上构成同一条逻辑链：

$$\frac{I_{p}}{C_{2}} \rightarrow V_{cont}\ ripple \rightarrow \beta \rightarrow \frac{A_{spur}}{A_{c}} \approx \frac{\beta}{2} \rightarrow bandwidth\ redesign.\quad\quad(5.2)$$

与此同时，环路参数决定

$$D(s),\quad T(s),\quad S(s),\quad\quad(5.3)$$

而所有随机噪声则根据注入位置，被 $T(s)$、$S(s)$ 或 $s/D(s)$ 整形。Reference spur 与 phase noise 不是两个孤立话题：前者是周期性确定扰动的离散谱线，后者是随机扰动的连续谱密度；二者共享同一环路动态和同一组设计参数。

## 5.5 常见错误清单

1.  把 $A_{spur}/A_{c} = \beta/2$ 当成功率比，造成 6 dB 或更大的换算错误。

2.  同时使用 $20\log$ 和平方后的功率比，重复平方。

3.  在分析 $C_{2}$ 的 spur-bandwidth 权衡时直接采用二阶模型，等于先删除待研究对象。

4.  divider 噪声未注明定义位置，盲目乘或除 $M$。

5.  把同一个 PFD 噪声同时作为输入相位源和 CP 电流源计入两次。

6.  对 CP 白噪声使用 duty factor 平方，忽略 aliasing；或对低频 flicker noise 只乘一次 duty factor。

7.  只看器件噪声源大小，不乘闭环 transfer function。例如仅凭 $4kTR_{1}$ 判断增大 $R_{1}$ 一定更差。

8.  将同一供电噪声通过 CP 和 VCO 的两条路径当成不相关源进行 PSD 相加。

9.  忽略 $K_{VCO}$ 单位是 Hz/V 还是 rad/s/V，导致额外的 $2\pi$ 因子。

10. 在 $\omega_{p3}$ 接近 $\omega_{u}$ 时仍以二阶模型估算相位裕度和 peaking。

## 5.6 教材依据与式号索引

本文内容主要对应 Behzad Razavi, *Design of CMOS Phase-Locked Loops: From Circuit Level to Architecture Level*, Cambridge University Press, 2020：

- 第 8.9 节：带宽与 spur 的权衡，教材式 (8.31)–(8.39)；

- 第 8.10.1 节：输入相位噪声低通整形与 $M^{2}$ 带内放大；

- 第 8.10.2 节：VCO 相位噪声高通整形，教材式 (8.47)；

- 第 8.10.3 节：CP 噪声传递函数与周期门控，教材式 (8.58)–(8.63)；

- 第 8.10.4 节：环路滤波器电阻噪声，教材式 (8.66)–(8.68)；

- 第 8.10.5 节：CP 与 VCO 供电噪声路径，教材式 (8.69)–(8.71)。
