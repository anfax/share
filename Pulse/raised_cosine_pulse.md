# 升余弦脉冲

升余弦脉冲是一种常用的数字调制中的脉冲整形方法，它可以最小化符号间干扰（ISI）。它的名字来源于它的频域形状，它是一个余弦函数，被“升起”到f{ \displaystyle f}轴之上。

## 数学表达式

升余弦脉冲的数学表达式可以用它的频域或时域来描述。它的频域表达式是一个分段定义的函数，由以下公式给出：

$$p(f) = \begin{cases}
T, & |f|\leq \frac{1-\alpha}{2 T}\\
\frac{T}{2} \left[ 1+\cos\left( \frac{\pi T}{\alpha} \left[ |f| -\frac{1-\alpha }{2 T} \right] \right) \right], & \frac{1-\alpha }{2 T}\leq f\leq \frac{1-\alpha }{2 T}\\
0, & |f|\geq \frac{1+\alpha}{2 T}
\end{cases}$$

Correspondingly, in time domain, the impulse response is given by

$$p(t)=\frac{ \sin\left( \frac{\pi t }{T}\right)}{\frac{\pi t}{T}} \frac{\cos\left( \frac{\pi \alpha t}{T}\right)}{1-\frac{2 \alpha
 t }{T}} $$

## 参考资料

- [Raised-cosine filter - Wikipedia](https://en.wikipedia.org/wiki/Raised-cosine_filter)
-
