<h1 align="center">CVPR-Skills</h1>

<p align="center">
  <a href="README.md"><b>English</b></a>
  &nbsp;|&nbsp;
  <b>简体中文</b>
</p>

<p align="center">
  <b>从一个研究方向到一篇投出去的论文，全部标定在 46 篇已发表的 CVPR 级论文上。</b><br>
  选题 → 查新 → 写代码 → 实验设计 → 画图 → 写作 → 审稿 → 投稿。<br>
  里面每一个数字都是量出来的，不是拍脑袋定的。
</p>

<p align="center">
  <a href="#全流程">全流程</a> ·
  <a href="#快速开始">快速开始</a> ·
  <a href="#安装">安装</a> ·
  <a href="#语料库到底说了什么">实测数据</a> ·
  <a href="#画图那一半">画图</a> ·
  <a href="#faq">FAQ</a>
</p>

<p align="center">
  <a href="https://github.com/ChizkiyahuOhayon/CVPR-Skills/actions/workflows/test.yml"><img alt="tests" src="https://github.com/ChizkiyahuOhayon/CVPR-Skills/actions/workflows/test.yml/badge.svg"></a>
  <img alt="MIT licence" src="https://img.shields.io/badge/licence-MIT-blue.svg">
  <img alt="Python 3.8+" src="https://img.shields.io/badge/python-3.8%2B-blue.svg">
  <img alt="no dependencies" src="https://img.shields.io/badge/dependencies-none-brightgreen.svg">
  <img alt="Claude Code and Codex" src="https://img.shields.io/badge/agents-Claude%20Code%20%7C%20Codex-8A2BE2.svg">
  <a href="https://github.com/ChizkiyahuOhayon/CVPR-Figure"><img alt="companion" src="https://img.shields.io/badge/figures-CVPR--Figure-8A2BE2.svg"></a>
</p>

---

## 这是什么

一套把论文从 **"我有个方向"** 带到 **"投出去了"** 的 skill，回答的是真正会卡住人的问题：

> 一篇 CVPR 论文有几张图，分别放在哪？摘要该写多长？
> 参考文献要多少篇、多新？对比实验放哪、消融实验放哪？
> Appendix 里放什么？统计分析做到什么程度就够了？
> 我的 related work 是不是太单薄？

回答方式不是给意见。我们解析了三个组的 **46 篇已发表论文**的 LaTeX 源码——清华 **MARS**、
**郑文钊**组、**旷视 Megvii**——289 个 figure 环境、300 张表、6726 条带年份的参考文献、
约 20 万词正文。下面每一个阈值都是这个语料库的一个百分位，而
`scripts/audit_paper.py` 会把你的稿子放进去量。

---

## 全流程

```
 ┌──────┐   ┌──────┐   ┌──────┐   ┌──────────┐   ┌──────┐
 │ 选题 │──▶│ 查新 │──▶│ 代码 │──▶│ 实验设计 │──▶│ 画图 │
 └──────┘   └──────┘   └──────┘   └──────────┘   └──────┘
                                                     │
   ┌──────┐   ┌──────┐   ┌──────────┐   ┌──────┐     │
   │ 投稿 │◀──│ 审稿 │◀──│ 自洽性核 │◀──│ 写作 │◀────┘
   └──────┘   └──────┘   └──────────┘   └──────┘
                  │
                  └──▶ rebuttal（如果被打回来）
```

| 阶段 | 产出 | 参考文件 |
|---|---|---|
| **选题 idea** | 一个五个槽全填满的 idea——问题、为什么没被解决、insight、方法、**证伪方案**——不是给你一堆方向 | [`craft/idea-shaping.md`](references/craft/idea-shaping.md) |
| **查新 novelty** | 被抢 / 相邻 / 干净，附最近三篇论文和"能把你和它区分开的那个实验" | [`audit/novelty.md`](references/audit/novelty.md) |
| **代码 code** | config 驱动还是类驱动、模块名和论文名一致、每个贡献挂在一个开关后面，消融才跑得动 | [`craft/code.md`](references/craft/code.md) |
| **实验设计** | 两个 benchmark、一个能归位到 baseline 的消融、开销表——以及统计分析的**上限** | [`corpus/experiment-design.md`](references/corpus/experiment-design.md) |
| **画图** | 交给 [**CVPR-Figure**](https://github.com/ChizkiyahuOhayon/CVPR-Figure)，它能直接读你的代码出图 | — |
| **写作 write** | 结构、逐节字数预算、句子与语态目标、图题表题长度 | [`corpus/writing-style.md`](references/corpus/writing-style.md) |
| **参考文献** | 要多少篇、多新、哪一节引什么 | [`corpus/bibliography.md`](references/corpus/bibliography.md) |
| **自洽性核对** | 正文数字对表格数字、论断对证据、跨图配色一致 | [`audit/integrity.md`](references/audit/integrity.md) |
| **审稿 review** | 对自己稿子出一份审稿意见，两个分数永不平均 | [`audit/reviewer-simulation.md`](references/audit/reviewer-simulation.md) |
| **投稿 submit** | 页数、匿名、字体嵌入、矢量图 | [`audit/submission.md`](references/audit/submission.md) |
| **rebuttal** | 新数字放最前面，一份 AC 能核对的修改台账 | [`craft/rebuttal.md`](references/craft/rebuttal.md) |

**顺序有两处是刻意的。** *代码在实验之前*——因为消融本质是个代码结构问题：如果每个贡献
不是从第一天起就挂在一个开关后面，deadline 那周的消融表就会变成四个半坏的分支。
*画图在写作之前*——因为框架图会逼着你在描述方法之前先把方法拆干净。

---

## 快速开始

```bash
python3 scripts/audit_paper.py path/to/paper/       # 目录、main.tex、或者一个 PDF
```

```
paper/main.tex  (article)
  4193 words | 169 sentences (median 22 words) | abstract 330 words
  2 figures | 6 tables | 0 equations | 19 references (13 \cite calls)
  first person 8.1/1k words | hedges 23.8/10k words

WARN  abstract-length   摘要 330 词；语料库区间是 149-187
WARN  impersonal        第一人称每千词只有 8.1 次；语料库是 17.0-22.1
WARN  structure         没有 Method / Experiments 章节
WARN  thin-citations    19 篇参考文献；语料库是 40-56
NOTE  few-figures       2 张图；语料库中位数是 6

0 error(s), 4 warning(s), 3 note(s)
```

三个等级含义不同：

| | |
|---|---|
| `error` | **语料库里没有任何一篇论文这么写。** 改掉。 |
| `warn` | 落在四分位区间或 90 分位之外。改掉，或者说得出理由。 |
| `note` | 值得看一眼；经常是有意为之。 |

它读 `.tex` 源码（去注释、展开 `\input`、屏蔽公式和浮动体），在只有 PDF 的情况下也能读
**编译好的 PDF**——用字号层级找章节标题，并且会明确告诉你哪些检查因此跳过了。

### 它是标定过的，而且标定过程你可以复核

跑在全部 45 篇语料库论文上：**0 个 error**，平均每篇 4.7 个 warning。
跑在一篇同等长度、故意用 AI 腔写的稿子上：**11 个 error**。

这个差距就是设计目标。会在已发表论文上疯狂报错的审计器，量的是作者本人的品味，
不是这个会议的规范。

---

## 语料库到底说了什么

### 一篇论文的形状

| | p25 | 中位数 | p75 |
|---|---|---|---|
| 正文词数（不含浮动体、公式、引用） | 4,011 | **4,351** | 4,869 |
| 摘要 | 149 词 | **177 词、9 句** | 187 词 |
| 章节数 | — | **6** | — |
| 公式 | — | **8** | 11 |
| `algorithm` 环境 | — | **0** | — |
| 图 / 表 | — | **6 / 6** | — |
| 去重参考文献 | 40 | **46** | 56 |

46 篇里 16 篇正好是 `Introduction > Related Work > Method > Experiments > Conclusion`，
另有 10 篇只是把 Method 叫成 Approach。八页纸大部分是浮动体：正文只有约 4400 词。
而且 algorithm 框是例外不是常态——方法靠公式加一张图承载。

### 证据放在哪

| | 图 | 表 |
|---|---|---|
| Experiments | 32% | **69%** |
| Introduction（teaser） | 16% | — |
| Method | 15% | 9% |
| Related Work | 7% | — |
| Appendix | 2% | 2% |

表格几乎纯粹是 Experiments 的东西。图会散开，因为 teaser 和方法图各自都在承载论证。
teaser 位于全文 **6.9%** 处，46 篇里 41 篇是单张图，图题约 **49 词**。

Experiments 内部的表格顺序：主对比 → **第一张消融表大约在全部表格的 60% 处** →
设计选择 → 开销。

全部 300 张表在干什么：**33% 对比、22% 消融**、13% benchmark 结果、8% 分项。
这个领域一半以上的表格在回答两件事之一：*我们是不是比他们强*、*是我们哪一部分起了作用*。

### 统计分析做到什么程度——这是上限不是下限

| | 有几篇这么做 |
|---|---|
| 任何显著性检验（p 值、t 检验、ANOVA） | **0 / 46** |
| 提到多个随机种子 | **0 / 46** |
| 误差棒、±、标准差、置信区间 | 5 / 46（11%） |
| **做了消融** | **44 / 46（96%）** |

**不要搭这个领域根本不用的统计装置。** 给每个格子做 bootstrap 置信区间、加 Bonferroni
校正，不会给你加分；同样的精力换成多一行消融，才是审稿人真正会争论的东西。唯一的例外：
主结果的提升不到一个点时，跑两三个种子，用**一句话**说明波动范围——不是一张表，不是一个检验。

### 参考文献

| | |
|---|---|
| 去重篇数 | 40 / **46** / 56（p25 / 中位数 / p75） |
| 参考文献年份中位数 | 2019（p10 2013，p90 2023） |
| **在"最新一篇"三年以内的比例** | **59%** |
| 比最新一篇早十年以上的比例 | 16% |

一份健康的参考文献长这样：**近三年约 60%**，三到十年前约 25%，更早的约 15%。
一个 related work 如果最新引用已经是两年前的，读起来就像这个项目停摆了——而审稿人
恰恰就是写那些新论文的人。

### Appendix

46 篇里只有 **15 篇有 appendix**，所以它是可选的。有的那些里面放的是：更多定性结果
（73%）、补充对比（73%）、从正文挤出去的实现细节（53%）、数据集细节（33%）、失败案例
（27%）、证明推导（27%）、更多消融（20%）。

规律是：appendix 放的是**正文已有内容的更多份**，不是另一种论证。只存在于 appendix 的
结果不会被读。如果审稿人需要它才肯接收，那它就该在正文里——同时正文得砍掉点别的。

### 文字

| | |
|---|---|
| 句子长度中位数 | **19 词**（p90 33） |
| 第一人称（we/our/us） | **每千词 20 次**——占全部词汇 2% |
| Hedge（may、might、could、possibly…） | **每万词 9.6 次** |
| 图题 | **39 词** |
| 表题 | **19 词** |

Hedge 是**定量配给**不是禁用：整篇论文四五个，花在真实的适用范围限制上。
这些论文说 **we**；通篇无人称被动的稿子在这个分布里非常扎眼，读起来像翻译腔。

另外图题长度是表题的**两倍**。表格数字自己会说话；图题必须承载论断，因为快速翻阅的
读者在那一页只会读 teaser 的图题。四个词的 "Overview of our framework." 是初稿里
最常见的自伤。

---

## 画图那一半

画图是独立的 skill，因为它是独立的引擎：
**[CVPR-Figure](https://github.com/ChizkiyahuOhayon/CVPR-Figure)**，建立在同一个语料库上。
它画框架图、pipeline、teaser、模块图，并导出成 **Visio `.vsdx` 和 PowerPoint `.pptx`
原生可编辑格式**，外加给 LaTeX 用的 PDF。

它能**直接从你的模型代码**出一版架构草图——不 import、不执行，两个 reader 都用 `ast` 解析：

```bash
python3 ../CVPR-Figure/scripts/from_code.py models/ --model MyNet -o fig.yaml
python3 ../CVPR-Figure/scripts/from_code.py configs/model.py --mm -o fig.yaml
python3 ../CVPR-Figure/scripts/render.py fig.yaml -o build/fig -f svg,pdf,pptx
```

同一次扫描里的相关发现：语料库 **290 张图里只有 1 张用 TikZ**，而且是个柱状图。所有
架构图都是外部矢量稿，嵌入字体表说明它们出自 PowerPoint、Visio 或 diagrams.net。
所以 `.pptx` 导出不是顺手加的功能——那就是这个领域真正在用的格式。

---

## 安装

### 作为 Claude Code skill

```bash
./install.sh                       # -> ~/.claude/skills/cvpr-skills
```

之后直接提问即可。论文写作、修改、实验设计、审稿、rebuttal、投稿检查都会触发，
中英文都行。

> 项目名是 **CVPR-Skills**；安装后的 skill id 是全小写的 `cvpr-skills`，因为
> Claude Code 的 skill id 规定是 lowercase-kebab。

把画图那一半也装上：

```bash
git clone https://github.com/ChizkiyahuOhayon/CVPR-Figure.git && ./CVPR-Figure/install.sh
```

### 配合 Codex / Cursor / Aider / 纯 API loop

```bash
cp -r . ~/.codex/skills/cvpr-skills
```

`AGENTS.md` 是给不读 `SKILL.md` frontmatter 的 agent 用的入口。

### 不用 agent，直接手工用

```bash
python3 scripts/audit_paper.py paper/
python3 scripts/audit_paper.py paper/ --json | jq '.findings[] | select(.level=="error")'
```

### 依赖

Python 3.8+，只用标准库。两个**可选**扩展：

```bash
pip install academic-refchecker[llm]   # 参考文献核对
pip install pymupdf                    # 没有 .tex、只能审 PDF 时
```

---

## 用你自己的语料库重建

自带的数字描述的是三个主要做 3D 视觉的组。如果你的子领域不同，用你自己的阅读清单重建：

```bash
python3 scripts/build_profile.py /path/to/arxiv/sources -o my-profile.json
python3 scripts/audit_paper.py paper/ --profile my-profile.json
```

每个一级子目录算一篇论文。profile 和审计器由**同一个 reader**
（`scripts/cvprskills/tex.py`）产出，所以永远是同口径比较——这个细节在开发过程中
抓到过一个真实的错误，记在 [CHANGELOG.md](CHANGELOG.md) 里。

---

## 关于"AI 味"，有一件事值得知道

这是个副产品，但很有用。网上流传的 "signs of AI writing" 清单是从网页文本总结的。
拿它对照**这个会议**的 45 篇已发表论文，会发现其中好几条头部条目根本就是这个领域的
正常写法：

| 通用工具会标红的 | 45 篇里有几篇在用 |
|---|---|
| `leverage` | 29 |
| `utilize` | 35 |
| `robust` | 26 |
| `state-of-the-art` | 40 |
| 三段式排比 "A, B, and C" | 42 |
| 句尾 ", …ing" 从句 | **45 / 45** |

把这些删掉，只会让稿子**更不像**这个会议。真正缺席的是：`pivotal`（**0 / 45**）、
"the landscape of"（0）、`tapestry`（0），以及破折号——**45 篇里 43 篇一个都没有**，
这让它成为成本最低、也最可靠的一个信号。

细节在 [`craft/humanizing.md`](references/craft/humanizing.md)。这件事的目的不是骗过
AI 检测器——那类工具对非母语英语写作的误报率高到针对它们优化既没意义也不公平。
目的是写得像这个会议。

---

## 目录结构

```
SKILL.md / AGENTS.md      Claude Code / 其他 agent 的入口
manifest.yaml             哪个阶段加载哪个片段
install.sh

references/
  corpus/                 测量结果
    profile.json            机器可读的分布
    README.md               测了什么，百分位该怎么读
    venue-conventions.md    结构、篇幅预算、浮动体、图表题
    writing-style.md        句子、语态、词频基线
    experiment-design.md    benchmark、消融、统计上限、浮动体位置、appendix 放什么
    bibliography.md         参考文献要多少、多新、哪一节引什么
    code-and-release.md     论文附带什么代码，46 个仓库的实测
  craft/                  怎么做
    idea-shaping.md         一个 idea 必须填满的五个槽
    code.md                 仓库形态、命名、让消融跑得动的开关
    anti-defensive.md       hedge，附具体数字
    humanizing.md           这个领域里哪些 AI 味是真的
    rebuttal.md             结构、语气、修改台账
  audit/                  怎么检查
    novelty.md              搜机制，不要搜话题
    citation-audit.md       RefChecker，以及工具查不了的部分
    integrity.md            数字对数字，论断对证据
    reviewer-simulation.md  四个问题、两个不平均的分数
    submission.md           各会议版面尺寸与检查清单
  workflow/routing.md     一个交付物一个 owner

scripts/
  audit_paper.py          审计器
  build_profile.py        从语料库重建 profile.json
  cvprskills/
    tex.py                LaTeX -> 正文、结构、浮动体
    pdf.py                编译好的 PDF -> 同上，减去 PDF 丢失的部分
    prose.py              稿子 vs profile

templates/
  paper-skeleton.tex      注释里标好语料库字数预算的论文骨架
  experiment-plan.md      开跑之前先填的实验计划

tests/test_audit.py       回归测试，零依赖
```

---

## 测试

```bash
python3 tests/test_audit.py
```

零依赖，约一秒。覆盖 LaTeX reader（去注释、展开 `\input`、嵌套环境、花括号配平的
caption、公式屏蔽）、词频计数器、自带 profile 的内部一致性、审计器在残稿 / AI 腔稿件 /
正常会议用语上的行为——其中明确检查了 `leverage`、`utilize`、`robust`、
`state-of-the-art` **不会**被当成 AI 味——词频下限、CLI 的退出码与 JSON，以及文档和
manifest 里声明的每一个路径都真实存在。

CI 在 Python 3.9 / 3.11 / 3.13 上**不装任何依赖**跑这些测试。

---

## 这套东西从哪来的

蒸馏，并且在测量结果不一致的地方做了**修正**：

| 来源 | 取了什么 | 改了什么 |
|---|---|---|
| **CCFA-skills** | 单 owner 路由、阶段划分 | 从 CCF-A 全领域收窄到 CVPR 级；所有阈值换成实测值 |
| **anti-defensive-writing** | 写作姿态；必要限制 vs 防御性限制 | 给了它一个数字：约每万词 10 个 hedge |
| **humanizer** | 结构性信号——段落长度一致、列表对称、模糊归因 | 词表在本领域上被实测推翻了大半 |
| **IdeaSpark** | 一个 idea + 一个证伪方案，不是一个菜单 | contribution 形态从这个语料库读出来 |
| **RefChecker** | 参考文献核对 | 作为可选外部 CLI 集成，没有 vendoring |
| **nature-skills / ARS** | 按需加载 reference 的组织方式 | 这里的规范是 CVPR 的，和 Nature 不同 |
| **CVPR-Figure** | — | 保持独立；它负责图，共用同一个语料库 |

---

## FAQ

**它是不是覆盖了 CCFA-skills 的全部功能？**
阶段层面是的——选题、查新、实验、写作、审稿、rebuttal、投稿、自洽性、引用核对——
再加上代码结构和画图（这两块 CCFA 的切法不同）。刻意没有搬过来的是：项目脚手架、
文献**监控**（常驻的 arXiv 订阅）、skill-forger，以及 CCFA 那个基于图像模型的画图模块——
CVPR-Figure 用确定性引擎替代了它。如果你需要常驻 arXiv 监控，把 CCFA 一起装着即可，
两者不冲突。

**审计器报 warning，是不是我论文有问题？**
不是。已发表论文平均每篇也有 4.7 个 warning。warning 的意思是*落在常见区间之外*，
而落在常见区间之外经常是对的。真正有意义的是 error。

**我不是做 3D 视觉的。**
重建 profile。结构性结论——图题表题的不对称、表格集中在 Experiments、消融是必需品、
hedge 要配给、参考文献偏新——比具体词数更通用。

**它能判断我的科学做得对不对吗？**
不能，而且它明说不能。它测的是结构和文字。数字能不能支撑论断，在
[`audit/integrity.md`](references/audit/integrity.md)，那是人工的一遍。

**这些数字从哪来的？**
[`references/corpus/README.md`](references/corpus/README.md)，
`scripts/build_profile.py` 就是生成它们的脚本。源文件是别人的论文，不随仓库分发。

---

## 许可

MIT，见 [LICENSE](LICENSE)。
