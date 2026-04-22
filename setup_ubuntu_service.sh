#!/bin/bash
# 讓 WOL 程式在 Ubuntu 背景運行的自動設定腳本

USER=$(whoami)
DIR=$(pwd)
SERVICE_NAME="wol.service"

echo "=========================================="
echo "開始在 Ubuntu 上設定 WOL 背景執行服務..."
echo "=========================================="

echo "目前使用者: $USER"
echo "專案路徑: $DIR"

# 建立暫存的 service 檔案
cat > /tmp/$SERVICE_NAME << EOF
[Unit]
Description=Wake-on-LAN Web App
After=network.target

[Service]
User=$USER
WorkingDirectory=$DIR
ExecStart=/usr/bin/python3 $DIR/app.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

echo "設定服務檔需要系統管理員權限 (sudo)，請依照提示輸入密碼："
sudo cp /tmp/$SERVICE_NAME /etc/systemd/system/$SERVICE_NAME

# 重新載入 Systemd 並啟動服務
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
sudo systemctl start $SERVICE_NAME

echo "=========================================="
echo "✅ 服務安裝完成且已在背景啟動！"
echo "您的服務將會在 Ubuntu 開機時自動執行。"
echo ""
echo "常用指令："
echo "查看狀態: sudo systemctl status $SERVICE_NAME"
echo "停止服務: sudo systemctl stop $SERVICE_NAME"
echo "重啟服務: sudo systemctl restart $SERVICE_NAME"
echo "查看日誌: journalctl -u $SERVICE_NAME -f"
echo "=========================================="
