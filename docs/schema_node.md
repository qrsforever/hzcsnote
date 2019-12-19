
## Schema Note Tree

```
                                                   page
                                                    |
                                                    |
                                    +---------------+----------------+
                                    |                                |
                      object        v                                v
                         ^         tab                              tab
                         |          |
                         |          |
             +----------------------+--------------------------+----------------+
             |                      |                          |                |
             |                      |                          |                |
             v                      v                          v                v
          accordion            navigation      object     <<k12type>>      <<layout>>
             |                      |            ^                              |
             |                      |            |                              |
             |                      |            |                  +-----------+-----------+
     +-------+------+      +--------+--------+--------------+       |           |           |
     |              |      |                 |              |       |           |           |
     |              |      |                 |              |       v           v           v
     |              |      v                 v              v       H           HV          V
     |              |  <<k12type>>      <<k12type>>    <<layout>>
     v              v                        |
<<k12type>>    navigation                    |
                                             |
                            +----------------+------------------+
                            |                    |              |
                            v                    |              v
      link             <<basictype>>             v       <<complextype>>
        ^                   |                  object           |
        |                   |                                   |
        |                   |                                   |
    +--------+-------+------+-------+---------+                 +---> bool-trigger
    |        |       |              |         |                 |
    |        |       |              |         |                 |
    v        v       v              v         v                 +---> string-enum-trigger
int[-array] bool  float[-array]  string   string-enum           |
                                                                |
                                                                +---> string-enum-array-trigger
                                                                |
                                                                |
                                                                +---> string-enum-group-trigger

```

**符号"<< >>"的节点是虚节点(不存在), 只是为了描述树图**

1. 一个节点树中只能还有一个page节点, 且page节点的子节点只能是tab节点, 可以是多个tab.
2. 一个tab节点可以包含多个除page以外的其他任意节点.
3. 一个navigation节点可以包含多个`"<<k12type>>"`节点. (实际上可以嵌套包含accordion/navigation, 但不推荐)
4. `<<layout>>`节点可以用来指定该节点下的内容布局方式, 如: 横向(H), 竖向(V), 基础类型和复杂类型分层(HV)
5. `<<basictype>>` 基本类型(叶子节点), 包括 int, float, string等, 节点特点简单只是用来存值
6. `<<complextype>>` 复杂类型, 包括 bool-trigger(当值为true时, 触发新的配置项/节点),
   string-enum-trigger(当选中其中一个值时会触发相应的配置项/节点), ...


## Node Struct

### 一般节点模型

```json
{
    "description": "",  // [O] 字符串, 节点描述
    "_id_": "a.b.c",    // [C] 字符串, 中间节点是可选[O], 叶子几点必选[M], 其值有重要意义, 用来还原配置
    "name": {},         // [O] 对象, 形如: {en:"test", cn:"测试"}
    "type": "page",     // [M] 字符串, 节点的类型
    "objs": [],         // [M] 对象数组, 子节点内容
}
```

### 叶子节点模型

A. 布尔型(bool)

```json
{
    "_id_": "a.b.c",   // [C] 字符串, 中间节点是可选[O], 叶子几点必选[M], 其值有重要意义, 用来还原配置
    "name": {},        // [O] 对象, 形如: {en:"test", cn:"测试"}
    "type": "bool",    // [M] 字符串, 节点的类型
    "default": false,  // [M] 布尔型, 默认值
}
```

B. 整型(int)

```json
{
    "_id_": "a.b.c",   // [C] 字符串, 中间节点是可选[O], 叶子几点必选[M], 其值有重要意义, 用来还原配置
    "name": {},        // [O] 对象, 形如: {en:"test", cn:"测试"}
    "type": "int",     // [M] 字符串, 节点的类型
    "min": 1,          // [O] 整型, 最大可设置的值
    "max": 100,        // [O] 整型, 最小可设置的值
    "default": 10,     // [M] 整型, 默认值
}
```

C. 浮点型(float)

```json
{
    "_id_": "a.b.c",   // [C] 字符串, 中间节点是可选[O], 叶子几点必选[M], 其值有重要意义, 用来还原配置
    "name": {},        // [O] 对象, 形如: {en:"test", cn:"测试"}
    "type": "float",   // [M] 字符串, 节点的类型
    "min": 1.0,        // [O] 浮点型, 最大可设置的值
    "max": 100.0,      // [O] 浮点型, 最小可设置的值
    "default": 10.0,   // [M] 浮点型, 默认值
}
```

D. 文本型(string), 文本枚举(string-enum)

```json
{
    "_id_": "a.b.c",   // [C] 字符串, 中间节点是可选[O], 叶子几点必选[M], 其值有重要意义, 用来还原配置
    "name": {},        // [O] 对象, 形如: {en:"test", cn:"测试"}
    "type": "string",  // [M] 字符串, 节点的类型
    "default": "text", // [M] 字符串, 默认值
}
```
