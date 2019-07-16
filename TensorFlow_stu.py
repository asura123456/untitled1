import os
import tensorflow as tf
import matplotlib as mp


os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
message=tf.constant('Welcome to the exciting world of Deep Neutal Network')
t_random=tf.random_normal([2,3],mean=2.0,stddev=4,seed=7)  #tf.random_shuffle,tf.random_uniform,tf.truncated_normal

with tf.name_scope('input'):
    a=tf.constant(5)
    b=tf.constant(6)
    c=tf.constant(4)

with tf.name_scope('op'):
    add=tf.add(b,c)
    mul=tf.multiply(a,add)      #fetch模式 sess.run([add,mul])

d=tf.placeholder(tf.float32,shape=[2],name=None)
e=tf.constant([6,4],tf.float32)
f=tf.add(d,e)              #占位符模式

var1=tf.Variable([1,3],name="v1")
var2=tf.Variable([2,4],name="v2")
init=tf.initialize_all_variables()
saver=tf.train.Saver()
module_file=tf.train.latest_checkpoint("test/")

I_matrix=tf.eye(10)

#sess=tf.InteractiveSession()
#print (I_matrix.eval())
#print (sess.run(init))


with tf.Session() as sess:
    result=sess.run([add,mul])
    writer = tf.summary.FileWriter('./mylogs', sess.graph)
    print(result)

#with tf.Session() as sess:
#    print(sess.run(t_random))
 #   print(sess.run(f,feed_dict={d:[10,10]}))  #占位符模式

 #   with tf.device("/gpu:2"):  #GPU选择
# sess.run(init)
# save_path=saver.save(sess,"test/save.ckpt")

# saver.restore(sess,module_file)



