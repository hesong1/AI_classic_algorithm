# coding = utf-8
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable

class Net(nn.Module):
    #define Net initial function,nn network frame
    def __init__(self):
        super(Net, self).__init__()
        #定义conv1函数是图像卷积函数：输入为图像（1个频道，即灰度图），输出为6张特征图，卷积核为5*5
        self.conv1 = nn.Conv2d(1, 6, 5)
        #定义conv2函数是图像卷积函数：输入为6张特征图，输出为16张特征图，卷积核为5*5
        self.conv2 = nn.Conv2d(6, 16, 5)
        #定义fc1全连接函数1为线性函数：y = Wx + b，并将16*5*5个节点连接到120个节点上
        self.fc1 = nn.Linear(16*5*5, 120)
        #定义fc2全连接函数2为线性函数：y = Wx + b，并将120个节点连接到84个节点上
        self.fc2 = nn.Linear(120, 84)
        #定义fc3全连接函数3为线性函数：y = Wx + b，并将84个节点连接到10个节点上
        self.fc3 = nn.Linear(84, 10)
    #定义前向传播函数，该函数必须定义，一旦定义成功，向后传播函数自动生成（autograd）    
    def forward(self, x):
        # 输入X经过卷积conv1后，经过激活函数Relu，使用2*2的窗口进行最大池化Max pooling，然后更新到x
        x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
        # 输入x经过卷积conv2后，经过激活函数Relu，使用2*2的窗口进行最大池化Max pooling，然后更新到x
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        # view函数将张量x变形成一维的向量形式，总特征不变，为接下来的全连接做准备
        x = x.view(-1, self.fnum_flat_features(x))
        # 输入x经过全连接1，再经过Relu激活函数，然后更新X
        x = F.relu(self.fc1(x))
        # 输入x经过全连接2，再经过Relu激活函数，然后更新x
        x = F.relu(self.fc2(x))
        #输入经过全连接3，然后更新x
        x = self.fc3(x)
        return x

    # 使用num_flat_features函数计算张量x的总特征（把每一个数字看成一个特征，即特征总量），比如x是4*2*2的张量，那么它的特征总量就是16
    def num_flat_features(self, x):
        # 这里要用[1:]，因为pytorch只接受批输入，也就是说，一次性输入好几张图片，那么输入数据张量的维度自然
        # 上升到了4维，[1:]让我们把注意力放在后3维上面
        size = x.size()[1:]
        num_features = 1
        for s in size:
            num_features *= s
        return num_features

net = Net()
net

# 以下代码是为了看一下我们需要训练的参数的数量
print (net)
params = list(net.parameters())

k = 0
for i in params:
    l = 1
    print ("该层的结构：" + str((list(i.size()))))
    for j in i.size():
        l *= j
    print("参数和：" + str(l))
    k = k + l

print ("总参数和：" + str(k))