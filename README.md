# DBMS_final
新學期開始,想要買二手教科書卻只能瀏覽臉書的台大二手書交流版,沒有固
定格式也容易被大量貼文洗掉,找不到自己想要的二手書嗎?不妨來使用看看
「NTUSHB」。「NTUSHB」是一個給大學生的二手書平台,目的是為了提供大學生一個
方便交流二手書的平台。
本系統分為 User 和 Admin 兩種身份別。User 為一般使用者,包含二手書賣家和
買家,使用者需要先註冊成會員,忘記密碼時也能要求系統重新驗證、重置。使用者
賣家可以發文上架欲出售的書籍,提供書名、作者、價格之外,也會提供該書及對應
到的課程供買家參考,賣家也能隨時刪除已上架的書籍。有購書需求的買家能透過查
詢功能,根據書名、作者、價格等條件去篩選目標書籍。如果沒有符合條件的上架書
籍,買家能發文徵求想要的二手書,如果有賣家願意出售,就會利用使用者提供的電
子郵件去聯絡後續購書事宜。交易完成後也提供買家評價賣家的功能,可供未來使用
者在選擇賣家時的參考依據。每一筆交易資訊都會被記錄至「NTUSHB」中,使用者
能隨時查詢過去的歷史訂單。Admin 為系統管理者,有權限查看所有使用者的相關資
訊。如果有使用者或上架書籍違反規定,Admin 能強制刪除該用戶或是該書及的上架
貼文。可查詢所有已完成的交易紀錄,期望能提供良好的使用者經驗。
## 安裝
1. Clone專案到本地機器：

```
git clone https://github.com/your-username/your-project-name.git
```
2. 進入專案目錄：
```
cd your-project-name
```
3. 創建一個虛擬環境：
```
python -m venv venv
```

4. 啟動虛擬環境：

在 Windows 上：
```
.\venv\Scripts\activate
```
在 Unix 或 MacOS 上：

```
source venv/bin/activate
```
5.安裝依賴項：

```
pip install -r requirements.txt
```
## 建立 PostgreSQL 資料庫

在安裝 PostgreSQL 後，我們將為 Django 專案建立資料庫來儲存所需資料。

### 使用 pgAdmin 管理 PostgreSQL

在安裝過程中，系統會自動安裝 pgAdmin 工具，方便開發人員管理 PostgreSQL 資料庫。

1. **開啟 pgAdmin：**
   - 在 Windows，您可以透過搜尋「pgAdmin」來開啟它。
   - 或者，在安裝目錄（例如：`C:\\Program Files\\PostgreSQL\\12\\pgAdmin 4\\bin`）中找到 `pgAdmin4` 執行檔。

2. **登入 pgAdmin：**
   - 啟動 pgAdmin 後，系統會提示您輸入 PostgreSQL 的密碼。成功登入後，您將看到 pgAdmin 的主界面。

3. **建立 Server Group (伺服器群組)：**
   - 在 PostgreSQL 資料庫架構中，最頂層為 Server Group。您需要首先建立一個 Server Group。
   - 按照提示，輸入自訂的 Server Group 名稱。


4. **在 Server Group 下新增 Server (伺服器)：**
   - 在您創建的 Server Group 下，新增一個 Server。
   - 您需要為 Server 輸入自訂名稱，並設定位址及密碼。若在本地端執行，位址為 `localhost`。


5. **建立資料庫：**
   - 在新建立的 Server 下，建立一個資料庫。
   - 輸入資料庫名稱並儲存。


6. **導入資料庫結構和資料：**
   - 在命令行界面中，確保你位於包含 `DBMS_final_project_backup_v4.1.sql` 文件的目錄中。
   - 執行以下命令導入資料庫結構和資料到剛建立的資料庫中：
   ```bash
   psql -U your_postgres_username -d DBMS_final_project_backup_v4.1 -f DBMS_final_project_backup_v4.1.sql


完成以上步驟後，您將擁有一個 PostgreSQL 資料庫，適用於 Django 專案。
## 設定 Django 連接 PostgreSQL

在建立好 PostgreSQL 資料庫之後，我們需要設定 Django 以便它可以與資料庫溝通。

### 安裝 psycopg2 套件

首先，安裝 `psycopg2` 套件，這個套件允許 Python 應用程式與 PostgreSQL 資料庫進行連接。

執行以下指令來安裝 `psycopg2`：

```
$ pip install psycopg2
```
### 更新 Django 設定

安裝完 `psycopg2` 後，您需要更新 Django 專案的 `ntushb/settings.py` 檔案，以使用 PostgreSQL 資料庫。

打開 `ntushb/settings.py`，並將 `DATABASES` 設定更改為以下內容：
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # PostgreSQL
        'NAME': 'BOOKSTORE',  # 資料庫名稱
        'USER': 'postgres',  # 資料庫帳號
        'PASSWORD': '****',  # 資料庫密碼
        'HOST': 'localhost',  # Server(伺服器)位址
        'PORT': '5432'  # PostgreSQL Port號
    }
}

```
### 執行 Django Migration

接著，執行 Django Migration (資料遷移) 指令，將 Django Model 中的資料模型同步至 PostgreSQL 資料庫中。
```
 python manage.py migrate
```
完成這些步驟後，您的 Django 專案應該已經成功連接到 PostgreSQL 資料庫。

## 運行開發服務器：
執行以下命令來啟動 Django 開發服務器：
```
python manage.py runserver
```
現在，您可以通過訪問 http://127.0.0.1:8000/ 在瀏覽器中查看您的網站。

## 登入
