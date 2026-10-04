# GitHub + Zenodo 零基础操作手册

> 目的：把 `ivd_repro_audit` 代码仓库发布到 GitHub，通过 Zenodo 获取永久 DOI，  
> 填入投稿稿件的数据可用性声明。全程约 20-30 分钟，只需浏览器 + 一个终端窗口。
>
> 每一步做完都可以回来让 AI 帮您验证是否成功。

---

## 第 0 步：注册 GitHub 账号（已有账号可跳过）

1. 打开 <https://github.com> ，点右上角 **Sign up**。
2. 依次输入：邮箱 → 密码 → 用户名（Username）。
   - 用户名将出现在仓库网址里（`github.com/您的用户名/...`），建议用  
     姓名拼音或常用学术 ID，例如 `zhangsan-lab`。
3. 完成人机验证，选择免费计划（Free），去邮箱点验证链接激活。
4. 登录后停留在 github.com 即可，继续第 1 步。

---

## 第 1 步：设置 git 提交身份（1 分钟）

代码首次提交时用的是占位身份（"IVD Audit Authors"），push 前必须改成您自己，  
否则 GitHub 页面上会显示错误的作者名。

1. 打开 **Git Bash**（开始菜单搜 "Git Bash"，或在文件夹空白处右键 →  
   "Open Git Bash here"——如果右键菜单没有就从开始菜单打开）。
2. 粘贴执行以下三条命令（第一条用来进入项目目录，整体复制即可）：

```bash
cd "D:/edge保存/分析加机器学习/ivd_repro_audit"
git config user.name "Zhang San"
git config user.email "zhangsan@example.com"
```

- `Zhang San` 换成您的姓名拼音（与论文作者署名一致，会公开显示）。
- 邮箱换成您注册 GitHub 用的邮箱。

1. 再执行下面这条，把历史提交里的占位身份一并改掉：

```bash
git commit --amend --reset-author --no-edit
```

1. 验证（应显示您的名字和邮箱）：

```bash
git log --format="%an <%ae>" -1
```



---

## 第 2 步：在 GitHub 建仓库并推送代码（5-10 分钟）

### 2.1 创建空仓库

1. 登录 github.com，点右上角头像左边的 **"+"** → **New repository**。
2. 填写：
   - **Repository name**：`ivd-repro-audit`（建议用这个名字，全小写带连字符）
   - **Description**（可选）：  
     `Reproducibility audit of public human IVD transcriptomes`
   - 选择 **Private**（私有）。
     > 先私有没关系，第 3 步做 Zenodo 存档前再转公开即可（Zenodo 只能存档公开仓库）。
   - **不要勾选** "Add a README file"、".gitignore"、"Choose a license"  
     （仓库里已经有这些文件，勾了会冲突）。
3. 点绿色按钮 **Create repository**。
4. 创建后页面会显示一段以 `git remote add origin ...` 开头的命令——不用抄，  
   用下面 2.2 的命令即可。

### 2.2 推送代码

在 Git Bash 里执行（先确认还在项目目录，不确定就再执行一次 cd 命令）：

```bash
git remote add origin https://github.com/您的用户名/ivd-repro-audit.git
git push -u origin main
```

- 把 `您的用户名` 替换成第 0 步注册的 GitHub 用户名。

**首次推送会弹出登录窗口**（Git Credential Manager）：

- 选择 **"Sign in with your browser"** → 浏览器自动打开 GitHub 授权页 →  
  点 **Authorize** → 回到终端，推送自动继续。
- 如果没有弹窗，而是终端里要求输入 Username / Password：  
  **GitHub 已不接受密码登录**，需要改用令牌：
  1. 浏览器打开 <https://github.com/settings/tokens>
  2. 点 **Generate new token** → **Generate new token (classic)**
  3. Note 填 `push-code`，Expiration 选 90 days，勾选 **repo** 整组权限
  4. 拉到页面底部点 **Generate token**
  5. **立刻复制**那串以 `ghp_` 开头的令牌（只显示一次）
  6. 终端 Username 输入 GitHub 用户名，Password 处**粘贴这串令牌**  
     （粘贴时屏幕不显示字符是正常的，Ctrl+V 或右键粘贴后回车）

看到类似下面的输出就是成功：

```
Enumerating objects: 200, done.
...
To https://github.com/您的用户名/ivd-repro-audit.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```

### 2.3 验证

刷新浏览器里的仓库页面（`github.com/您的用户名/ivd-repro-audit`），  
应该能看到 README.md 的内容显示在首页，顶部有 171 个左右的文件。

---

## 第 3 步：Zenodo 绑定并获取 DOI（10 分钟）

### 3.1 把仓库转为公开（Zenodo 只能存档公开仓库）

> 如果论文还在审稿中不想提前公开代码——但数据可用性声明里承诺了链接，  
> 投稿时编辑可能会点开检查，所以**建议在投稿前就公开**。

1. 打开仓库页面 → 顶部 **Settings** 标签。
2. 左侧选 **General**（默认就是），拉到最底部 **Danger Zone** 区域。
3. 点 **Change repository visibility** → **Make public**。
4. 按提示输入仓库名确认。

### 3.2 绑定 Zenodo

1. 打开 <https://zenodo.org> → 点 **Log in** → 选 **"Log in with GitHub"** →  
   授权。
2. 登录后点右上角头像 → **GitHub**（直达链接：  
   <https://zenodo.org/account/settings/github/> ）。
3. 页面列出您的 GitHub 仓库。如果没看到 `ivd-repro-audit`，  
   点 **"Sync now"** 按钮刷新。
4. 把 `ivd-repro-audit` 那一行右侧的开关拨到 **On**。

### 3.3 创建一个 Release（版本发布）

1. 回到 GitHub 仓库页面，点右侧栏的 **Releases**（或 "Create a new release"）。
2. 点 **"Choose a tag"** 下拉框 → 输入 `v1.0.0` → 点下方出现的  
   **"Create new tag: v1.0.0 on publish"**。
3. **Release title** 填：`v1.0.0 - JBI submission snapshot`。
4. 描述框（可选）填：  
   `Code, derived results and submission package accompanying the manuscript (initial submission).`
5. 点绿色按钮 **Publish release**。

### 3.4 拿到 DOI

1. 等 1-2 分钟，回到 <https://zenodo.org/account/settings/github/> 。
2. `ivd-repro-audit` 那一行现在会显示一个蓝色的 **DOI 徽章**，形如  
   `10.5281/zenodo.1234567`。
3. 点徽章进入存档页，页面上会同时看到两种 DOI：
   - **版本 DOI**：只指向 v1.0.0 这个快照（例如 `10.5281/zenodo.1234568`）
   - **概念 DOI（Concept DOI）**：永远指向最新版本  
     两个都有效，**投稿建议填概念 DOI**（以后修改代码发新版，稿件里的链接  
     依然指向最新版）。如果分不清，把两个都发给 AI，由 AI 判断填写。
4. 把这个 DOI 字符串（`10.5281/zenodo.xxxxxxx`）复制下来 → 进入第 4 步。

> ⚠️ 常见坑：一定要先开 Zenodo 开关、再创建 Release。如果顺序反了，  
> 存档不会发生；补救办法是再创建一个小版本 Release（如 v1.0.1）即可触发。

---

## 第 4 步：把 DOI 交给 AI 回填（您只需发一条消息）

回到 WorkBuddy 对话，直接发：

> DOI 是 10.5281/zenodo.xxxxxxx，GitHub 仓库是  
> <https://github.com/您的用户名/ivd-repro-audit，作者署名是> Zhang San

AI 会自动完成：

1. `JBI_Declarations.md` 数据声明里的 `[repository URL and DOI]` 占位符替换；
2. 正文 Data Availability 部分补充正式存档语句；
3. `CITATION.cff` 和 `README.md` 里的 TODO 占位符替换；
4. `LICENSE` 里的作者名替换；
5. 重新运行构建脚本 + 重新导出 PDF；
6. 把回填后的改动再提交一个 git commit（您再执行一次 `git push` 即可同步）。

---

## 附：遇到问题时的自助排查

| 症状                                                                      | 原因与解决                                                                               |
| ----------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| `git push` 提示 `remote: Support for password authentication was removed` | 用了密码而非令牌；按 2.2 的令牌流程操作                                                              |
| 推送窗口一闪而过/没有弹窗                                                           | 在终端执行 `git config --global credential.helper manager` 后重试                           |
| Zenodo 仓库列表是空的                                                          | 点 **Sync now**；还是没有就检查 Zenodo 是否获得了该仓库授权（GitHub → Settings → Applications → Zenodo） |
| Release 发了但 Zenodo 没反应                                                  | 开关是在 Release 之后才开的；再发一个 v1.0.1                                                      |
| 忘记复制令牌                                                                  | 令牌无法找回，只能按 2.2 重新生成一个                                                               |
| 想把仓库改回私有                                                                | Settings → Danger Zone → Change visibility；但注意投稿前需要重新公开，否则编辑打不开链接                   |
