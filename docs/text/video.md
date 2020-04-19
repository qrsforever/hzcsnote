视频是一系列静止图象的集合, 以某一速度顺序播放这些图象, 从而觉得图象里的内容有连动的感觉. 通常我们说的一帧画面, 其意思就是视频中的一张静止图象, 每秒播放的图象个数用帧率表示(FPS), 帧率越大, 表示一秒内包含的图象数量越多, 那么这一秒的*动画*就含有的信息更多, 一般电影或者电视节目都是以每秒24帧的速度播放就能满足要求, 而对于一些体育运动,娱乐项目,游戏等视频, 对"动作"细节要求偏高, 所以FPS一般为30或者更高.

既然我们了解了视频是由连贯的图象(帧)组成, 是不是对视频一些任务(如: 视频内容任务分类)就可以通过对视频进行截帧, 在将每一帧画像送入到成熟的图象分类模型(如CNN)就可以实现, 其实这是一种最简单的方式, 但是一张图在整个视频中只是很小的一部分, 况且有可能这张图相对你的任务是内容无关的, 从而影响了图象分类器的判断认知.

再通过一个例子我们更能理解, 对视频内容的分析仅仅对一帧图象(2D)进行分析是不够的: 一个人手握门把的一张图(空间), 我们是不知道这个人想要是开门, 还是关门的, 无法预测这个人的接下来的动作, 如果把这个帧之后相关的几个帧同时考虑(时空), 然后放入到处理这些帧的模型中(如: 3D CNNs), 最后预测出结果.

视频内容承载了人物, 场景, 动作, 语音, 字幕等信息, 可以综合应用所有有用信息的特征对视频内容进行了解. 


















## 1

https://www.sciencedirect.com/journal/pattern-recognition/special-issue/10BXH4KTJ46

We are living in a world where we are surrounded by so many intelligent video-capturing devices. These devices capture data about how we live and what we do. For example, thanks to surveillance and action cameras, as well as smart phones and even old-fashioned camcorders, we are able to record videos at an unprecedented scale and pace. There is exceedingly rich information and knowledge embedded in all those videos. With the recent advances in computer vision, we now have the ability to mine such massive visual data to obtain valuable insight about what is happening in the world. Due to the remarkable successes of deep learning techniques, we are now able to boost video analysis performance significantly and initiate new research directions to analyze video content. For example, convolutional neural networks have demonstrated superiority on modeling high-level visual concepts, while recurrent neural networks have shown promise in modeling temporal dynamics in videos. Deep video analytics, or video analytics with deep learning, is becoming an emerging research area in the field of pattern recognition.

The goal of this special issue is to call for a coordinated effort to understand the opportunities and challenges emerging in video analysis with deep learning techniques, identify key tasks and evaluate the state of the art, showcase innovative methodologies and ideas, introduce large scale real systems or applications, as well as propose new real-world datasets and discuss future directions. The video data of interest cover a wide spectrum, ranging from first-person wearable videos, web videos (aka user-generated content), commercial video programs, to surveillance videos. Video analytics plays an important role in public security, entertainment, healthcare, and so on. We solicit manuscripts in all fields of video analytics that explore the synergy of video understanding and deep learning techniques.


## 2

https://www.einfochips.com/blog/top-3-emerging-trends-in-video-analytics-artificial-intelligence-tracking-micro-expressions/


As the amount of video data generated tends to be pretty huge, with no way to handle and process all of it in a short span of time using manpower alone due to limitations in human capacity, video analytics is serving as a useful asset to make generated video data more valuable.

Video analytics can be done in three different scenarios like on-board real-time analytics, offline VMS forensics and an emerging field called on-demand analytics using a cloud.

Here, we will discuss three applications where video analytics are playing a pre-eminent role.

- Artificial Intelligence (Deep Learning, Machine learning)

- Combination of video analytics with other tagging and tracking technologies

- Micro Expression Analysis


## 3

https://www.forbes.com/sites/forbestechcouncil/2020/03/25/artificial-intelligence-machine-learning-and-deep-learning-whats-the-difference/#344c16d77bd0

Video analytics represents something of a holy grail to those in the security industry. Computers have long been able to scan text and even audio for keywords or phrases, but analyzing video -- especially in real time -- is considerably more challenging. In recent years, however, major improvements to artificial intelligence (AI), machine learning and deep learning capabilities have given rise to impressive new tools capable of analyzing video with minimal input from security personnel.


For those in the security industry, the advent of deep learning has proven to be the key to more effective video surveillance and analytics.



## 4

https://www.dqindia.com/video-analytics-next-wave-video-surveillance/


## 5

https://zhuanlan.zhihu.com/p/31688901

【人脸识别】

人脸识别现在在人工智能这块应用较为广泛，如身份认证、手机刷脸、系统登录等；另外是人脸的搜索，比如在一段视频里快速确定有没有出现某个关键人物，或一个图片集里有没有包含这样的人。人脸识别主要的流程一般如下，首先对这个图片进行人脸的检测，然后提取关键点，包括眼睛、鼻子、嘴巴、耳朵、轮廓等，切分处理以后，再给到卷积网络提取特征，最后再做人脸识别，目前我们在公司考勤、政治任务识别方面已有相关的应用。


【自动标签】

针对用户自主上传的图片，自动标签则发挥出重要作为。用户在上传图片的时候，往往只会标注一到两个关键词，对图片进行描述，而图片里边包含的大量其他的内容和信息，是没办法检索出来的，因为现在很多后台的搜索是基于关键字的。通过计算机视觉的场景识别功能，可以很好的将图片的隐藏信息挖掘出来，让图片有更多的关键字，能够被更多的场景检索出来，发挥其作用。

【字幕识别】

字幕识别的应用非常直接而实用，例如身份证、发票、名片的识别，可以减少手写录入的工作量，而类似视频字幕识别这种，则可以帮助计算机更好地去理解视频的内容。


## 6

https://www.analyticsvidhya.com/blog/2019/09/step-by-step-deep-learning-tutorial-video-classification-python/






## 00

阿里安全图灵实验室高级算法专家析策表示，为提升AI技术在实际场景中针对视频识别的精度，提出一种新的基于图（Graph）的视频建模方法，能表达含有复杂事件内容的长视频。

析策表示，这一方法的主要思路是通过“深度卷积图神经网络”（下称“DCGN”）对视频的帧、镜头、事件进行多级的建模，逐渐地从帧级、镜头级，一直到视频级进行抽象，从而获得视频全局的表达，进而进行分类。

他举例称，“比如一段美食节目视频中，包含厨师长、主持人聊天、食物、观众等内容，AI在学习视频内容时会先根据内容对视频进行逐帧的语义表达，形成特征序列，用不用的标签进行打标，随后在通过多层次的网络对这些不同打标的内容进行关系表达，深度理解这些内容之间的关联度，将相似的节点衔接起来，最终组合出对整个视频的理解。”


https://www.techsmith.com/blog/frame-rate-beginners-guide/

https://www.wired.com/story/technique-easier-ai-understand-videos/


感知动态动作可能是软件如何理解世界的巨大进步。

