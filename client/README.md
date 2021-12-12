## 客户端
- 用户注册，注册成功之后，在服务端的指定目录下为此用户创建一个文件夹，该文件夹下以后存储当前用户的数据（类似于网盘）。
- 用户登录
- 查看网盘目录下的所有文件（一级即可），ls命令
- 上传文件，如果网盘已存在则重新上传（覆盖）。
- 下载文件（进度条）

    ```
    先判断要下载本地路径中是否存在该文件。
    - 不存在，直接下载
    - 存在，则让用户选择是否续传（继续下载）。
    	- 续传，在上次的基础上继续下载。
    	- 不续传，从头开始下载。
    ```
- 对用户磁盘进行分配，用户空间可自行设置
未实现，思路如下：
  1.在注册中添加设置用户空间字段（由用户填写），传输至服务端储存，若不设置则使用默认值
  2.在Viewhandles中添加用户自行设置网盘大小的功能
    1 判断用户是否登录，若登录，则执行下面步骤；若未登录，则提醒登录；
    2 用户输入大小（以GB为单位）；
    3 转换成KB并传输大小数据给服务端；
    4 接收返回值并将其返回给服务端； 
  3.上传功能：
    1 在进行判断之后确认文件存在后，获取文件大小，并传输至服务端；
    2 接收服务端返回的flag，进行判断，True则执行上传操作，False则return并告知用户可用空间不足