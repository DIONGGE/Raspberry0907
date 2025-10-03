# Gemini CLI 啟動說明

本文件說明如何設定 Python 環境並使用 Google Generative AI SDK 來與 Gemini API 互動，以建立您自己的 Gemini CLI 工具或腳本。

## 1. 設定開發環境

### 1.1 建立並啟用虛擬環境

建議使用虛擬環境來管理專案依賴，以避免與系統其他 Python 專案產生衝突。

```bash
python -m venv .venv
```

啟用虛擬環境：

*   **Linux / macOS:**
    ```bash
    source .venv/bin/activate
    ```
*   **Windows (Command Prompt):**
    ```bash
    .venv\Scripts\activate.bat
    ```
*   **Windows (PowerShell):**
    ```bash
    .venv\Scripts\Activate.ps1
    ```

### 1.2 安裝 Google Generative AI SDK

在虛擬環境啟用後，安裝必要的函式庫：

```bash
pip install google-generativeai
```

## 2. 取得 Gemini API 金鑰

要使用 Gemini API，您需要一個 API 金鑰。請按照以下步驟取得：

1.  前往 [Google AI Studio](https://aistudio.google.com/)。
2.  登入您的 Google 帳戶。
3.  建立一個新的 API 金鑰。
4.  複製您的 API 金鑰。

## 3. 設定 API 金鑰

為了安全起見，建議將 API 金鑰儲存在環境變數中，而不是直接寫在程式碼裡。

*   **Linux / macOS:**
    ```bash
    export GOOGLE_API_KEY="您的API金鑰"
    ```
*   **Windows (Command Prompt):**
    ```bash
    set GOOGLE_API_KEY="您的API金鑰"
    ```
*   **Windows (PowerShell):**
    ```bash
    $env:GOOGLE_API_KEY="您的API金鑰"
    ```
    或者，您也可以在 Python 程式碼中直接設定：
    ```python
    import google.generativeai as genai
    genai.configure(api_key="您的API金鑰")
    ```
    **注意：** 將 API 金鑰直接寫入程式碼不建議用於生產環境。

## 4. 建立您的 Gemini CLI 腳本

建立一個 Python 檔案 (例如 `gemini_cli.py`) 並加入以下內容：

```python
import google.generativeai as genai
import os

# 從環境變數中讀取 API 金鑰
# 如果您選擇直接在程式碼中設定，請移除此行並取消註解下面的 genai.configure
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    print("錯誤：請設定 GOOGLE_API_KEY 環境變數或在程式碼中設定 API 金鑰。")
    exit()

genai.configure(api_key=API_KEY)

def chat_with_gemini(prompt):
    model = genai.GenerativeModel('gemini-pro')
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"與 Gemini 互動時發生錯誤: {e}"

if __name__ == "__main__":
    print("歡迎使用 Gemini CLI！輸入 'exit' 結束對話。")
    while True:
        user_input = input("您：")
        if user_input.lower() == 'exit':
            break
        
        response_text = chat_with_gemini(user_input)
        print(f"Gemini：{response_text}")
```

## 5. 執行您的 Gemini CLI 腳本

在啟用虛擬環境並設定好 API 金鑰後，執行您的腳本：

```bash
python gemini_cli.py
```

現在您可以透過命令列與 Gemini 進行互動了！