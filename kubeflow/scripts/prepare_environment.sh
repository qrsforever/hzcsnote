
sudo ufw disable
sudo ufw status
sudo iptables -P FORWARD ACCEPT

if [[ -f /etc/selinux/config ]]
then
    sudo setenforce 0
    sudo sed -i 's/SELINUX=enforcing/SELINUX=disable' /etc/selinux/config
fi

sudo swapoff -a
sudo sed -i 's/.*swap.*/#&/' /etc/fstab

cat > /etc/sysctl.d/99-kubernetes-cri.conf <<EOF
net.bridge.bridge-nf-call-iptables  = 1
enet.ipv4.ip_forward                = 1
net.bridge.bridge-nf-call-ip6tables = 1
EOF

sysctl --system

modprobe br_netfilter
lsmod | grep "br_netfilter"
