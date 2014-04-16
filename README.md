用 epoll 写个提供 echo 服务的 tcp server 

- [test](http://nanny.netease.com/yangjunwei/epoll-emfile/tree/test) 分支用来验证在 `Too many open files` 的情况下CPU占用会飙升。
- [master](http://nanny.netease.com/yangjunwei/epoll-emfile/tree/master) 分支解决这个问题。

具体文件

- server.py 。使用 epoll 来进行多路IO复用。启动服务前，需要 `ulimit -n 20` 限制服务器能够打开的最大文件描述符数是 20，这样除了标准输入、标准输出、标准错误、监听socket对象、epoll对象占用了5个文件描述符，在 test 分支中最多并发能够接受15个连接。由于在 master 中解决方案占用了一个闲置文件描述符，最多并发能够接受14个连接。
- clinet.py 。在 master 分支中，模拟客户端发起15个并发连接。在 test 分支中，模拟客户端发起16个并发连接。
