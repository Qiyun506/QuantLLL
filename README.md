# QMT A股全自动数据仓库 (新手操作指南)

欢迎！这个项目可以帮你把券商软件 (QMT) 里的股票数据“偷”出来，存到你自己的极速数据库 (DuckDB) 里。

即使你没有任何代码经验，只要跟着下面的步骤点鼠标及复制粘贴，也能轻松搞定。

## 准备工作 (只需做一次)

在开始之前，请确保你的电脑上安装了以下三个软件：

1. **VS Code** (写代码的工具)
2. **Python** ([官网下载](https://www.python.org/downloads/))
* *注意：安装时一定要勾选底部的 **"Add Python to PATH"**！*


3. **QMT 交易终端** (你的券商提供的软件，如国金、中信等)
* *注意：安装后登录时，必须勾选 **"极简模式" (MiniQMT)**。*



---

## 第一步：把代码下载到本地 (Clone)

我们要把放在 GitHub 上的代码拉到你的电脑里。

1. 打开 **VS Code**。
2. 点击左侧边栏的 **"源代码管理" (Source Control)** 图标 (长得像个树杈 ᛦ)。
3. 点击蓝色的按钮 **"克隆仓库" (Clone Repository)**。
4. 在上方弹出的框里，粘贴本项目的 GitHub 链接：
* `这里替换成你的GitHub仓库地址` (例如: `https://github.com/你的名字/项目名.git`)


5. 选择一个你电脑上的文件夹（比如 D盘），点击“选择作为仓库位置”。
6. 下载完成后，右下角会弹窗提示，点击 **"打开 (Open)"**。

---

## 第二步：配置 Python 环境 (只需做一次)

我们要给这个项目建立一个独立的运行环境。

1. 在 VS Code 顶部菜单栏，点击 **Terminal (终端)** -> **New Terminal (新建终端)**。
* *你会看到下方出现一个黑色的命令行窗口。*


2. **依次**复制下面的命令，粘贴到终端里并按回车（一行行运行）：
**命令 A：创建虚拟环境**
```powershell
python -m venv .venv

```


**命令 B：激活环境 (看到行首出现 (.venv) 变绿即成功)**
* *Windows系统复制这行:*


```powershell
.venv\Scripts\activate

```


* *Mac系统复制这行:*


```bash
source .venv/bin/activate

```


**命令 C：安装必须的工具包**
```powershell
pip install -r requirements.txt

```


*(这一步需要等待一会儿，看到 Successfully installed... 代表成功)*

---

## 第三步：初始化股票名单 (只需做一次)

我们要把想抓取的股票名单（放在 `stock_list.csv` 里的）导入到数据库里。

1. 确保你刚才的终端里，行首有 `(.venv)` 字样。
2. 输入并运行：
```powershell
python setup_universe.py

```


3. 如果屏幕显示：`Successfully migrated ... stocks to DuckDB!`，恭喜你，数据库建立成功！

---

## 第四步：日常抓取数据 (每天收盘后点一下)

这是你以后每天唯一需要做的工作。

1. **打开 QMT 交易软件**，登录并确保是 **"极简模式"** (MiniQMT)，保持软件开启。
2. 打开 VS Code。
3. 打开终端（如果没有打开的话），输入：
```powershell
python main.py

```


4. 看着屏幕滚动 `Processing Batch...`，这说明正在疯狂下载数据。
5. 等程序跑完，今天的数据就存好了。

---

## 第五步：查看战果 (怎么看数据？)

你想确认数据是不是真的存进去了？

**简单方法：**
在终端输入：

```powershell
python check_data.py

```

它会直接打印出数据库里的前5行数据。如果能看到日期和价格，说明一切正常！

**高级方法 (像Excel一样看)：**

1. 在 VS Code 左侧扩展商店 (Extensions) 搜索并安装 **"DuckDB"** 插件。
2. 安装好后，在左侧文件列表里，直接双击 `market_data.duckdb` 文件。
3. 它会像 Excel 表格一样直接在 VS Code 里显示出来。

---

## 常见报错解决

**Q: 运行 `main.py` 报错："无法连接xtquant服务"？**

* **原因**：QMT 软件没开，或者登录时没选 "极简模式"。
* **解决**：关掉 QMT，重新打开，勾选 "极简模式/MiniQMT" 登录，然后再试。

**Q: 报错 "IO Error: Could not open database"？**

* **原因**：你可能正在用别的软件（比如 DBeaver 或 VSCode 插件）查看数据库。
* **解决**：DuckDB 不允许“一边看一边写”。请先**关闭**所有查看数据的窗口，然后再运行下载代码。