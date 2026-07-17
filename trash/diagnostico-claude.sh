#!/usr/bin/env bash

set +e

OUT="claude-diagnostico-$(date +%Y%m%d-%H%M%S).txt"
PCAP="anthropic-$(date +%Y%m%d-%H%M%S).pcap"

exec > >(tee "$OUT") 2>&1

echo "======================================================"
echo "TAP-OS - DIAGNÓSTICO COMPLETO"
echo "======================================================"
echo

echo "DATA"
date

echo
echo "HOSTNAME"
hostnamectl

echo
echo "KERNEL"
uname -a

echo
echo "UPTIME"
uptime

echo
echo "======================================================"
echo "REDE"
echo "======================================================"

ip addr
echo
ip route
echo
ip neigh
echo
ip link

echo
echo "======================================================"
echo "DNS"
echo "======================================================"

cat /etc/resolv.conf
echo
resolvectl status

echo
echo "======================================================"
echo "FIREWALL"
echo "======================================================"

sudo iptables -S
echo
sudo iptables -L -n -v
echo
sudo iptables -t nat -L -n -v
echo
sudo nft list ruleset

echo
echo "======================================================"
echo "DOCKER"
echo "======================================================"

docker version
echo
docker info
echo
docker ps -a
echo
docker network ls

echo
echo "======================================================"
echo "CLAUDE"
echo "======================================================"

claude --version
echo
claude doctor
echo
claude mcp list

echo
echo "======================================================"
echo "TLS"
echo "======================================================"

openssl version
echo
curl --version

echo
echo "======================================================"
echo "TESTES DNS"
echo "======================================================"

nslookup api.anthropic.com
echo
nslookup api.openai.com
echo
nslookup google.com

echo
echo "======================================================"
echo "PING"
echo "======================================================"

ping -c 4 8.8.8.8
echo
ping -c 4 google.com

echo
echo "======================================================"
echo "GOOGLE"
echo "======================================================"

curl -I https://www.google.com

echo
echo "======================================================"
echo "OPENAI"
echo "======================================================"

curl -4 -v https://api.openai.com

echo
echo "======================================================"
echo "ANTHROPIC"
echo "======================================================"

curl -4 -v https://api.anthropic.com

echo
echo "======================================================"
echo "OPENSSL OPENAI"
echo "======================================================"

openssl s_client -connect api.openai.com:443 \
-servername api.openai.com </dev/null

echo
echo "======================================================"
echo "OPENSSL ANTHROPIC"
echo "======================================================"

openssl s_client -connect api.anthropic.com:443 \
-servername api.anthropic.com </dev/null

echo
echo "======================================================"
echo "CAPTURA TCP"
echo "======================================================"

echo "Iniciando tcpdump..."

sudo timeout 15 tcpdump \
-i ens33 \
-nn \
-s0 \
-w "$PCAP" \
host 160.79.104.10 &
PID=$!

sleep 2

echo
echo "Executando curl enquanto tcpdump captura..."

curl -4 -v https://api.anthropic.com

wait $PID

echo
echo "======================================================"
echo "SOCKETS"
echo "======================================================"

ss -tanp
echo
ss -lntp

echo
echo "======================================================"
echo "LOGS DOCKER"
echo "======================================================"

journalctl -u docker --since "2 hours ago" --no-pager

echo
echo "======================================================"
echo "NETWORKMANAGER"
echo "======================================================"

journalctl -u NetworkManager --since "2 hours ago" --no-pager

echo
echo "======================================================"
echo "SYSTEMD NETWORKD"
echo "======================================================"

journalctl -u systemd-networkd --since "2 hours ago" --no-pager

echo
echo "======================================================"
echo "DMESG"
echo "======================================================"

sudo dmesg | tail -300

echo
echo "======================================================"
echo "PROCESSOS"
echo "======================================================"

ps aux --sort=-%cpu | head -40

echo
echo "======================================================"
echo "MEMÓRIA"
echo "======================================================"

free -h

echo
echo "======================================================"
echo "DISCO"
echo "======================================================"

df -h

echo
echo "======================================================"
echo "ARQUIVOS GERADOS"
echo "======================================================"

echo "$OUT"

ls -lh "$PCAP"

echo
echo "FIM"