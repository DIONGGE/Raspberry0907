# Gemini 啟動說明

本文件說明如何啟動 `raspberry0907` 專案。

## 1. 使用 Python 直譯器直接執行

這是最直接的啟動方式，適用於已安裝 Python 環境的系統。

```bash
python main.py
```

## 2. 使用虛擬環境 (Virtual Environment)

建議使用虛擬環境來管理專案依賴，以避免與系統其他 Python 專案產生衝突。

### 2.1 建立並啟用虛擬環境

如果尚未建立虛擬環境，請執行以下指令：

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

### 2.2 安裝依賴 (如果有的話)

目前 `pyproject.toml` 中沒有明確的依賴，但如果未來有新增，請在啟用虛擬環境後執行：

```bash
pip install -e .
```

### 2.3 執行專案

在虛擬環境啟用後，即可執行 `main.py`：

```bash
python main.py
```

### 2.4 停用虛擬環境

完成工作後，可以停用虛擬環境：

```bash
deactivate
```

## 3. 使用 `pipx` (如果專案被設計為 CLI 工具)

如果 `raspberry0907` 專案未來被設計為一個可執行的命令列工具，`pipx` 是一個很好的選擇，它會將專案安裝到獨立的環境中。

### 3.1 安裝 `pipx` (如果尚未安裝)

```bash
python -m pip install --user pipx
python -m pipx ensurepath
```

### 3.2 安裝專案

```bash
pipx install .
```

### 3.3 執行專案

安裝後，可以直接在任何地方執行專案名稱：

```bash
raspberry0907
```

### 3.4 移除專案

```bash
pipx uninstall raspberry0907
```