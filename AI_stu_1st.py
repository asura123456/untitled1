import numpy as np
import matplotlib.pyplot as plt

N=200
D=2
K=3
x=np.zeros((N*K,D))
y=np.zeros(N*K,dtype='uint8')
W=0.01*np.random.randn(D,K)
b=np.zeros((1,K))
#梯度下降迭代循环
num_examples=x.shape[0]
#需要自己敲定的步长和正则化系数
reg=1e-3 #正则化系数
step_size=1e-0

for j in range(K):
    ix=range(N*j,N*(j+1))
    r=np.linspace(0,1,N)
    t=np.linspace(j*4,(j+1)*4,N)+np.random.randn(N)*0.25+np.pi
    x[ix]=np.c_[r*np.sin(t),r*np.cos(t)]
    y[ix]=j

plt.scatter(x[:,0],x[:,1],c=y,s=40,cmap=plt.cm.Spectral)
plt.show()

for i in range(400):
    # 计算类别得分，结果矩阵为【N*K】
    scores=np.dot(x,W)+b
    #计算类别概率
    exp_scores=np.exp(scores)
    probs=exp_scores/np.sum(exp_scores,axis=1,keepdims=True)
    #计算损失loss（包括互熵损失和正则化部分）
    corect_logprobs=-np.log(probs[range(num_examples),y])
    data_loss=np.sum(corect_logprobs)/num_examples
    reg_loss=0.5*reg*np.sum(W*W)
    loss=data_loss+reg_loss
    if i%10==0:
        print("iteration %d: loss %f" %(i,loss))
    #计算得分上的梯度
    dscores=probs
    dscores[range(num_examples),y]-=1
    dscores/=num_examples
    # 计算和回传梯度
    dW=np.dot(x.T,dscores)
    db=np.sum(dscores,axis=0,keepdims=True)
    dW+=reg*W #正则化梯度
    # 参数更新
    W+=-step_size*dW
    b+=-step_size*db
 #评估准确度
scores=np.dot(x,W)+b
predicted_class=np.argmax(scores,axis=1)
print('training accuracy: %.2f' %(np.mean(predicted_class==y)))