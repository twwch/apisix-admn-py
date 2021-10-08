docker docker run -it -m 1800m --restart=always -d --net=host --name apisix_admin_py \
        -v /opt/apisix-admin-py:/root/projects/xiaoduo/xiaoduo-mp/apisix-admin-py/ \
        -v /etc/localtime:/etc/localtime \
        -v /var/log/xiaoduo:/var/log/xiaoduo \
        -w /root/projects/xiaoduo/xiaoduo-mp/apisix-admin-py/src \
        -e LANG="en_US.UTF-8" \
        registry-vpc.cn-zhangjiakou.aliyuncs.com/xiaoduoai/growth:v1.0.8.2 /usr/local/python3/bin/python3 app.py --numprocs=1 --port=9913 -c ../config/apisix-admin-py.conf