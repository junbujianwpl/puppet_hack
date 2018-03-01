


## 说点啥呢
开源的东西，原理讲太多，很多路径可能会被封禁。取窗口句柄是一个稍微麻烦点的事。如果一个窗口的句柄很难用稳定的方法取到，有一个新思路，用pywinauto将所有对应类型的窗口遍历，再取属性进行比对，做一个筛选。见puppet中main中的CVirtualGridCtrl。能取到所有表格信息。




<hr/>

## 关于改进
pywinauto底层也用消息，但是会判断消息的返回值，会有超时、异常等信息。所以<font color=red >使用pywinauto比直接使用ctypes发消息健壮性要强一些</font>。

故而将买卖设置文本的部分换成了pywinauto的方式。

从健壮性的角度来讲，所有有返回值的函数的返回值都应当判断一下，对于非预期的返回值需要做分支处理，异常处理等。

另外，设计底层的函数还是要给出充足的信息才好。hack后的代码还有些地方还可以完善下，比如所有操作类函数加个返回值，至少表征下操作是否完成。：）


<hr/>
## 关于文件
    1.全部的工程文件还有一个入口函数，会进入一个总体的线程循环，此线程将周期操作保持客户端alive。
    同时会监听任务队列是否有任务，如果有任务则将任务执行完毕。
    由于包含个人信息未上传。这也是为啥这几个文件都用上传而不用commit->push。  ：）

    2.另外将来还计划做一个策略系统，每天生成固定的策略，比如每天定时打新，简单的高抛低吸。然后进阶出一些基于行情数据的策略。
  
    3.最终，还计划写一个选股系统。用tushare获取数据然后做一些筛选
  
  
<hr/>
  puppet_v35是别人的代码，拿来hack了一下。：）
