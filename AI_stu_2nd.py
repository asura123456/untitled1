import numpy as np
import matplotlib.pyplot as plt

N=200
D=2
K=3
x=np.zeros((N*K,D))
y=np.zeros(N*K,dtype='uint8')

h=100 #隐层大小
W=0.01*np.random.randn(D,h)
b=np.zeros((1,h))
W2=0.01*np.random.randn(h,K)
b2=np.zeros((1,K))

#需要自己敲定的步长和正则化系数
reg=1e-3 #正则化系数
step_size=1e-0

#梯度下降迭代循环
num_examples=x.shape[0]
for i in range(10000):
    hidden_layer=np.maximum(0,np.dot(x,W)+b) #使用的RELU神经元
    scores=np.dot(hidden_layer,W2)+b2
    #计算类别概率
    exp_scores=np.exp(scores)
    probs = exp_scores / np.sum(exp_scores, axis=1, keepdims=True)
    # 计算损失loss（包括互熵损失和正则化部分）
    corect_logprobs = -np.log(probs[range(num_examples), y])
    data_loss = np.sum(corect_logprobs) / num_examples
    reg_loss = 0.5 * reg * np.sum(W * W)
    loss = data_loss + reg_loss
    if i % 10 == 0:
        print("iteration %d: loss %f" % (i, loss))
    # 计算得分上的梯度
    dscores = probs
    dscores[range(num_examples),y] -= 1
    dscores /= num_examples
    #梯度回传
    dW2 = np.dot(hidden_layer.T, dscores)
    db2 = np.sum(dscores, axis=0, keepdims=True)

    dhidden=np.dot(dscores,W2.T)

    dhidden[hidden_layer<=0]=0
    #拿到 最后W，b上的梯度
    dW=np.dot(x.T,dhidden)
    db=np.sum(dhidden,axis=0,keepdims=True)

    #加上正则化梯度部分
    dW2+=reg*W2
    dW+=reg*W
    #参数迭代和更新

    # 参数迭代和更新
    W+=-step_size*dW
    b+=-step_size*db
    W2 += -step_size * dW2
    b2 += -step_size * db2
#计算分类准确度
hidden_layer=np.maximum(0,np.dot(x,W)+b)
scores=np.dot(hidden_layer,W2)+b2
predicted_class=np.argmax(scores,axis=1)
print('training accuracy: %.2f' %(np.mean(predicted_class==y)))