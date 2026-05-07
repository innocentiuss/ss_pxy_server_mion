# personal use of sspanel backend
install with the following shell command


### 1. install libsodium to support high-level encrypt algorithm

For Debian/Ubuntu
```shell
apt install -y libsodium-dev
```

For CentOS/Rocky/Alma/RHEL

```shell
dnf install -y libsodium-devel
```

### 2. configure other environments

For Python2.x

```shell
cd /root
curl -sSL https://bootstrap.pypa.io/pip/2.7/get-pip.py -o get-pip.py
python get-pip.py
git clone https://github.com/innocentiuss/personal_sspanel_backend.git
cd personal_sspanel_backend/shadowsocks
pip install -r requirements.txt
cp apiconfig.py userapiconfig.py
cp config.json user-config.json
```

For Python3.x
```shell
cd /root
yum -y install python3-pip
git clone https://github.com/innocentiuss/personal_sspanel_backend.git
cd personal_sspanel_backend/shadowsocks
pip install -r requirements.txt
cp apiconfig.py userapiconfig.py
cp config.json user-config.json
```

### 3. configure web backend API configuration

```shell
vim userapiconfig.py
```

### 4. test/start

```shell
python server.py
./run.sh
```



