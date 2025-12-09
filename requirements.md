我要根据一个唯一标识（字符串）比如 instance_id, 去找所有docker images里包含这个id的
然后我要docker cp 到一个~/temp_container/<instacne_id>
然后我的agent的所有修改都会对上面的路径，然后有些命令需要运行在docker环境里，就是你上面看到的不过我写死了。
然后我要导出本地的git diff。然后我删除docker容器。
帮我写一个完整的脚本，重复一遍我的诉求
