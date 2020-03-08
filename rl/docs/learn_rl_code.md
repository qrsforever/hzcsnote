## RL源码分析


### Runner


### Affinity


### Algo


### Sampler


```
                                                    +---------------------------+
                                                    |        BaseSampler        |
                                                    |---------------------------|
                                                    |                           | ◁ --------------+
        +-----------------------------------------▷ |      v initialize         |                 |
        |                                           |      v obtain_samples     |                 |
        |                                           |      v evaluate_agent     |                 |
        |                                           +---------------------------+                 |
        |                                                                 △                       |
        |                                                                 |                       |
        |                                                                 |                       |
        |                                                                 |                       |
        |                                                          +------------------------+     |
        |                  +-------------------------------------▷ |   ParallelSamplerBase  |     |
        |                  |                                       |     (worker process)   |     |
        |                  |                    +----------------▷ |------------------------|     |
        |                  |                    |                  |                        |     |
        |                  |                    |                  +------------------------+     |
        |                  |                    |                         △         △             |
        |                  |                    |                         |         |             |
        |                  |                    |                         |         |             |
        |                  |                    |                         |         |             |
        |                  |       +----------------------+  +----------------+     |             |
        |                  |       | AsyncGpuSamplerBase  |  | GpuSamplerBase |     |             |
        |                  |       |----------------------|  |----------------|     |             |
        |                  |       |                      |  |                |     |             |
        |                  |       +----------------------+  +----------------+     |             |
        |                  |           |        △                    △              |             |
        |                  |           |        |                    |              |             |
        |                  |           |        |                    |              |             |
        |                  |           |        |                    |              |             |
AsyncSerialSampler    AsyncCpuSampler  |   AsyncGpuSampler     GpuSampler    CpuSampler    SerialSampler
           |                    |      |              |
           |                    |      |              |
           |                    |      |              |
           |                    |      |              |
           |                    ▽      ▽              ▽ 
           |       +----------------------------+    +-----------------------------+
           |       | AsyncParallelSamplerMixin  |    |      AsyncActionServer      |
           |       |----------------------------|    |-----------------------------|
           |       |                            |    |                             |
           |       |----------------------------|    |    serve_actions_evaluation |
           |       |       obtain_samples       |    +-----------------------------+
           |       |                            |               |
           |       +----------------------------+               |
           |             |                                      |
           |             |                                      |
           |             |                                      ▽ 
           ▽             ▽                               +--------------+
    +--------------------------+                         | ActionServer |
    |    AsyncSamplerMixin     |                         |              |
    |--------------------------|                         +--------------+
    |                          |
    |--------------------------|
    |    async_initialize      |
    +--------------------------+
```

作用: 收集训练数据 (采样数据)

收集训练数据,就需要在environment中步进,因此environment的实例化工作也在sampler中完成, 另外真正收集训练数据
的工作由Collector类完成, Sampler对Collector做了一层包装.

#### BatchSpec里的 T 和 B 的概念:

B: 构造B个environment对象, 独立的trajectory分段(environment实例的数量)
T: 时间步, 指agent与一个environment交互时,会按时间先后顺序不断地步进到下一个state,走一步即一个step.此值>=1.


#### `env_ranks`的概念

对不同的environment实例,对它们用ε-greedy来选择action的时候,ε可能是不同的.由于rlpyt在不同的并行模式下,
会形成不同的"虚拟environment数量"的概念, 因此在各种场景下都要确定一个对应到实际场景下的 虚拟的environment
数量,这就是`env_ranks`的含义.

### Agent




