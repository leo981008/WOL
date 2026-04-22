# Wake-on-LAN (WOL) 網頁應用程式

這是一個基於 Python 與 Flask 的輕量級 Wake-on-LAN (網路喚醒) 網頁應用程式，專為 Raspberry Pi 或其他常時運作的小型伺服器設計。透過這個網頁介面，您可以輕鬆地喚醒區域網路內指定的裝置。

## 功能特色
- **網頁操作介面**：提供簡單直覺的網頁介面來觸發喚醒指令。
- **設定檔管理**：使用 `config.json` 統一管理目標設備的 MAC 地址與廣播設定，無須修改程式碼。
- **輕量化架構**：基於 Flask 框架開發，資源佔用低。

## 系統需求
- Python 3.x
- Flask 套件

## 安裝與設定流程

1. **取得專案**
   將此專案複製到您的本機或 Raspberry Pi 裝置上。

2. **安裝依賴套件**
   確保您的環境已安裝 Python 3，接著使用 pip 安裝 Flask：
   ```bash
   pip install flask
   ```

3. **配置設定檔 (`config.json`)**
   專案根目錄下有一個 `config.json` 檔案。請根據您要喚醒的設備修改此檔案：
   ```json
   {
     "mac_address": "00:11:22:33:44:55",
     "broadcast_ip": "255.255.255.255",
     "port": 9
   }
   ```
   - `mac_address`: 要喚醒裝置的 MAC 網路卡卡號。
   - `broadcast_ip`: 廣播 IP 位址（預設為 `255.255.255.255`，一般不需更改）。
   - `port`: WOL 封包傳送的 UDP 埠號（通常為 `9`）。

## 啟動與使用

1. 在專案根目錄執行以下指令啟動 Flask 伺服器：
   ```bash
   python3 app.py
   ```
2. 伺服器將會預設運行在 `0.0.0.0:5000`。
3. 開啟瀏覽器，輸入伺服器的 IP 位址與埠號（例如：`http://<您的伺服器IP>:5000`），即可看到控制介面，並點擊按鈕來喚醒指定的裝置。

## 設定開機自動啟動與背景執行 (Ubuntu / Raspberry Pi)

專案內提供了 systemd 服務設定檔，讓您可以將此應用程式設定為在背景執行，並且開機自動啟動。

### 方法一：使用自動化配置腳本 (推薦，特別是 Ubuntu 系統)

我們提供了一個可以自動化完成設定的腳本：

1. 賦予腳本執行權限：
   ```bash
   chmod +x setup_ubuntu_service.sh
   ```
2. 執行自動化安裝腳本：
   ```bash
   ./setup_ubuntu_service.sh
   ```
   *(腳本會自動檢測目前目錄和使用者，並要求 sudo 密碼來設定 `/etc/systemd/system/wol.service`)*

### 方法二：手動設定 (進階)

如果您想手動設定，可以使用專案中提供的 `wol.service` 範本檔。

1. **修改服務設定檔**
   打開專案根目錄下的 `wol.service` 檔案，並根據您的環境修改：
   - `User`：您的系統使用者名稱（例如 `pi` 或 `ubuntu`）。
   - `WorkingDirectory`：此專案目錄的絕對路徑。
   - `ExecStart`：Python 的執行路徑。如果您使用虛擬環境，請將路徑指向虛擬環境的 python 執行檔。

2. **複製服務檔到 systemd 目錄**
   ```bash
   sudo cp wol.service /etc/systemd/system/
   ```

3. **重新載入 systemd 設定並啟用服務**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable wol.service
   sudo systemctl start wol.service
   ```

4. **檢查服務狀態**
   ```bash
   sudo systemctl status wol.service
   ```
