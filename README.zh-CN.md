<h1 align="center">CVPR-skills</h1>

<p align="center">
  <a href="README.md"><b>English</b></a>
  &nbsp;|&nbsp;
  <b>简体中文</b>
</p>

<p align="center">
  <b>面向 CVPR 级会议的论文生产 skill，全部阈值来自 46 篇已发表论文的实测。</b><br>
  每一条建议背后都有一个百分位，并且配一个能真跑的审计器，把你的稿子放到这个分布里量。
</p>

<p align="center">
  <a href="#最重要的一条命令">快速开始</a> ·
  <a href="#安装">安装</a> ·
  <a href="#语料库测出了什么">实测数据</a> ·
  <a href="#对通用-humanizer-的修正">AI 味</a> ·
  <a href="#九个阶段">阶段</a> ·
  <a href="#faq">FAQ</a>
</p>

<p align="center">
  <img alt="MIT licence" src="https://img.shields.io/badge/licence-MIT-blue.svg">
  <img alt="Python 3.8+" src="https://img.shields.io/badge/python-3.8%2B-blue.svg">
  <img alt="no dependencies" src="https://img.shields.io/badge/dependencies-none-brightgreen.svg">
  <img alt="Claude Code and Codex" src="https://img.shields.io/badge/agents-Claude%20Code%20%7C%20Codex-8A2BE2.svg">
</p>

---

## 为什么要做这个

大部分论文写作建议，都是把个人品味当成规则来讲。"别加太多 hedge"、"句子要有变化"、
"别用 AI 词"——没有一条说清楚**到底多少算多**，所以没有一条能被检验，而且其中有些
对这个领域来说本身就是错的。

这个 suite 把断言换成了测量。我们解析了三个组的 **46 篇论文** 的 LaTeX 源码——
清华 **MARS**、**郑文钊**组、**旷视 Megvii**——一共 289 个 figure 环境、300 张表、
约 20 万词正文。suite 里每一个阈值，都是这个语料库的一个百分位。

然后把测量结果做成了工具。

## 最重要的一条命令

```bash
python3 scripts/audit_paper.py path/to/paper/     # 或者直接给 main.tex
```

```
paper/main.tex  (article)
  4211 words | 208 sentences (median 19 words) | abstract 141 words
  4 figures | 8 tables | 4 equations | 51 references (62 \cite calls)
  first person 21.8/1k words | hedges 9.5/10k words
  sections: Introduction > Related Work > BEVDepth > Experiments > Conclusion

WARN   abstract-length      abstract is 141 words; the corpus runs 149-187.
WARN   rare-phrase          delve x1 (2.4 per 10k). Only 5 of 45 corpus papers use it at all.
WARN   structure            no Method section; ...

0 error(s), 3 warning(s), 0 note(s)
```

三个等级，含义完全不同：

| | |
|---|---|
| `error` | **语料库里没有任何一篇论文这么写。** 改掉。 |
| `warn` | 落在语料库四分位区间或 90 分位之外。改掉，或者说得出理由。 |
| `note` | 值得看一眼；经常是有意为之。 |

### 它是怎么标定的

把审计器跑在全部 45 篇语料库论文上：**0 个 error**，平均每篇 4.7 个 warning。
跑在一篇同等长度、故意用 AI 腔写的稿子上：**11 个 error、29 个 warning**。

这个差距就是整个设计目标。一个会在已发表论文上疯狂报错的审计器，量的是作者本人的
品味，不是这个会议的规范。

它还会在正文不足 900 词时拒绝计算词频类结论——短稿子里某个词出现一次，说明的是
篇幅，不是文风。

---

## 语料库测出了什么

| | p25 | 中位数 | p75 |
|---|---|---|---|
| 正文词数（不含浮动体、公式、引用） | 4,011 | **4,351** | 4,869 |
| 摘要 | 149 词 | **177 词、9 句** | 187 词 |
| 句子长度中位数 | 18 词 | **19 词** | 21 词 |
| 第一人称 / 千词 | 17.5 | **20.1** | 23.4 |
| Hedge / 万词 | — | **9.6** | 19.4 |
| 去重后的参考文献数 | 40 | **46** | 56 |
| 公式 | — | **8** | 11 |
| 图 / 表 | — | **6 / 6** | — |
| 图题 | 7 词 (p10) | **39 词** | 84 词 (p90) |
| 表题 | — | **19 词** | 45 词 (p90) |

有几条值得单独说。

**Hedge 是定量配给，不是禁用。** 大约每千词一个——整篇论文四五个。45 篇里只有 1 篇
一个都没有，所以"零 hedge"同样是异常值。把这几个额度花在真正的适用范围限制上。

**这些论文说"we"。** 全部词汇的 2% 是第一人称。通篇用无人称被动语态的稿子，在这个
分布里非常扎眼，审稿人读起来就是"翻译腔"或者"机器写的"。

**图题的长度是表题的两倍**，而这个不对称本身就是重点。表格的数字自己会说话；图题必须
承载论断，因为快速翻阅的读者在那一页只会读 teaser 的图题。四个词的
"Overview of our framework." 是初稿里最常见的自伤。

**46 篇里 43 篇做了 ablation。** 对比表占全部表格的 33%，ablation 再占 22%：这个领域
一半以上的表格都在回答两件事之一——*我们是不是比他们强*、*是我们的哪一部分起了作用*。

**几乎没人用 TikZ 画图**——290 张图里只有 1 张，而且是个柱状图。所有架构图都是外部
矢量稿。这正是这个项目的另一半：
[CVPR-Figure](https://github.com/ChizkiyahuOhayon/CVPR-Figure)。

---

## 对通用 humanizer 的修正

这一节会真正改变你的操作。

网上流传的 "signs of AI writing" 清单，是从百科和网页文本里总结出来的。拿它去对照
45 篇已发表的 CVPR 级论文，会清楚地裂成两半。

### humanizer 会标红、但在这里**完全正常**的——别动它们

| | 45 篇里有几篇用 | 中位数 / 万词 |
|---|---|---|
| "we propose" | **44** | 10.5 |
| `state-of-the-art` / SOTA | 40 | 6.4 |
| `utilize` | 35 | 5.7 |
| `significantly` | 35 | 2.6 |
| `enable(s)` | 33 | 2.4 |
| `moreover` | 31 | 2.5 |
| `comprehensive` | 31 | 2.4 |
| `leverage` | 29 | 2.3 |
| `robust` | 26 | 2.4 |
| `novel` | 24 | 1.9 |
| 三段式排比 "A, B, and C" | **42** | 9.8 |
| 句尾 ", …ing" 从句 | **45 / 45** | 36.6 |

把三段式排比和 "-ing" 从句从 method 章节里清理掉——这两条是所有通用清单上叫得最响的
——恰恰会让稿子**偏离**这个会议的写法。语料库里每一篇论文都在用这两种结构。

### 真正**缺席**的模式——这些才是真信号

| | 45 篇里有几篇用 |
|---|---|
| `pivotal` | **0** |
| `tapestry` | **0** |
| "the landscape of" | **0** |
| **破折号 em dash（—）** | **2** |
| `nuanced`、`realm`、`cutting-edge`、`meticulous` | 各 1 |
| `innovative`、`seamless` | 2–3 |
| `importantly`、`intricate`、`remarkably`、`substantially` | 3–4 |
| "in conclusion"、"it is worth noting" | 各 4 |
| `delve`、`showcase`、`holistic`、`vital`、"for the first time" | 各 5 |

**先从破折号开始。** 45 篇里 43 篇一个都没有。这是成本最低的修改，也是这套信号里最
可靠的一个。

另外注意审计器实际标记的是什么：不是某个词出现了，而是**频率**远超语料库 90 分位。
300 词的摘要里出现三次 `comprehensive` 是机器写的；4400 词的论文里出现一次是人写的。

> 这不是为了骗过 AI 检测器。那类工具对非母语英语写作的误报率高到——针对它们做优化
> 既没有意义，对被误判的人也不公平。目标是写出读起来像这个会议的文字；这是个写作
> 目标，而且恰好是同一件事。

---

## 安装

### 作为 Claude Code skill

```bash
./install.sh                       # -> ~/.claude/skills/cvpr-skills
```

之后直接提问即可。这个 skill 会在论文写作、修改、审稿、rebuttal、投稿检查等请求上
触发，中英文都可以。

> 项目名是 **CVPR-skills**；安装后的 skill id 是全小写的 `cvpr-skills`，因为
> Claude Code 的 skill id 规定是 lowercase-kebab。

### 配合 Codex / Cursor / Aider / 纯 API loop

```bash
cp -r . ~/.codex/skills/cvpr-skills
```

`AGENTS.md` 是给不读 `SKILL.md` frontmatter 的 agent 用的入口，内容相同，只是去掉了
Claude 专属的元数据。

### 不用 agent，直接手工用

审计器就是一个普通的 CLI：

```bash
python3 scripts/audit_paper.py paper/
python3 scripts/audit_paper.py paper/ --json | jq '.findings[] | select(.level=="error")'
```

### 依赖

Python 3.8+，只用标准库。一个**可选**的外部工具：

```bash
pip install academic-refchecker[llm]     # 参考文献核对
```

---

## 九个阶段

一个交付物只有一个 owner。"帮我改好一点" 和 "这篇有什么问题" 是两个不同的请求，
而且后者不负责改写。

| 阶段 | 加载 | 负责 |
|---|---|---|
| **idea** | `references/craft/idea-shaping.md` | 一个能被证伪的 idea，不是一堆方向 |
| **novelty** | `references/audit/novelty.md` | 被抢/相邻/干净，附最近三篇的对比表 |
| **experiments** | `references/corpus/experiment-design.md` | benchmark、ablation、开销表 |
| **figure** | *CVPR-Figure skill* | 框架图、pipeline、teaser、模块图 |
| **write** | `references/corpus/writing-style.md`、`references/craft/anti-defensive.md` | 正文 |
| **audit** | `scripts/audit_paper.py`、`references/audit/integrity.md` | 测量与自洽性 |
| **citations** | `references/audit/citation-audit.md` | RefChecker，加上工具查不了的那一层 |
| **review** | `references/audit/reviewer-simulation.md` | 评估，绝不改写 |
| **rebuttal** | `references/craft/rebuttal.md` | 回复信与修改台账 |
| **submit** | `references/audit/submission.md` | 格式、匿名、字体嵌入、页数 |

默认顺序：

```
idea -> novelty -> experiments -> (做实验) -> figure -> write
     -> integrity -> citations -> review -> submit
```

**先画图，后写正文。** 框架图会逼着你在描述方法之前先把方法拆干净；而且对着一张画完的
图写 method 章节，比反过来快得多。

---

## 用你自己的语料库重建 profile

自带的数字描述的是三个主要做 3D 视觉的组。如果你的子领域不同，用你自己的阅读清单
重建：

```bash
python3 scripts/build_profile.py /path/to/arxiv/sources -o my-profile.json
python3 scripts/audit_paper.py paper/ --profile my-profile.json
```

源目录下每一个一级子目录算作一篇论文。profile 和审计器由**同一个 reader**
（`scripts/cvprskills/tex.py`）产出，所以稿子永远是跟同口径的测量在比——这个细节比听上去
重要，开发过程中它抓到了一个真实的错误。

---

## 目录结构

```
SKILL.md                  Claude Code 入口（frontmatter 路由）
AGENTS.md                 Codex / 其他 agent 入口
manifest.yaml             哪个阶段加载哪个片段
install.sh                一条命令装成 Claude Code skill

references/
  corpus/
    profile.json          机器可读的分布
    README.md             测了什么，以及百分位该怎么读
    venue-conventions.md  结构、篇幅预算、浮动体、图表题
    writing-style.md      句子、语态、词频基线
    experiment-design.md  benchmark、ablation、表格是干什么的
    code-and-release.md   论文附带什么代码，46 个仓库的实测
  craft/
    anti-defensive.md     hedge，附具体数字
    humanizing.md         在这个领域里哪些 AI 味是真的
    idea-shaping.md       一个 idea 必须填满的五个槽
    rebuttal.md           结构、语气、修改台账
  audit/
    novelty.md            搜机制，不要搜话题
    citation-audit.md     RefChecker，以及工具查不了的部分
    integrity.md          数字对数字，论断对证据
    reviewer-simulation.md  四个问题、两个互不平均的分数
    submission.md         各会议版面尺寸与检查清单
  workflow/
    routing.md            一个交付物一个 owner

scripts/
  audit_paper.py          审计器
  build_profile.py        从语料库重建 profile.json
  cvprskills/
    tex.py                LaTeX -> 正文、结构、浮动体
    prose.py              稿子 vs profile

templates/
  paper-skeleton.tex      按语料库比例标注了字数预算的论文骨架
  experiment-plan.md      开跑之前先填的实验计划

tests/test_audit.py       回归测试，零依赖
```

---

## 测试

```bash
python3 tests/test_audit.py
```

零依赖，一秒左右。覆盖 LaTeX reader（去注释、展开 `\input`、嵌套环境、花括号配平的
caption、公式屏蔽）、词频计数器、自带 profile 的内部一致性、审计器在残稿/AI 腔稿件/
正常会议用语上的行为——其中明确检查了 `leverage`、`utilize`、`robust`、
`state-of-the-art` **不会**被当成 AI 味、词频下限、CLI 的退出码与 JSON 输出，以及文档
和 manifest 里声明的每一个路径都真实存在。

---

## 和其他 skill 的关系

这个 suite 是把若干来源蒸馏并**修正**之后重写的，不是套壳：

| 来源 | 取了什么 | 改了什么 |
|---|---|---|
| **CCFA-skills** | 单一 owner 的路由架构与阶段划分 | 从 CCF-A 全领域收窄到 CVPR 级；所有阈值换成实测值 |
| **anti-defensive-writing** | 写作姿态，以及"必要限制 vs 防御性限制"的区分 | 给了它一个数字：约每万词 10 个 hedge |
| **humanizer** | 结构性信号——段落长度一致、排比列表对称、模糊归因 | 词表在本领域上被**实测推翻了大半** |
| **IdeaSpark** | 一个 idea + 一个证伪方案，而不是一个菜单 | contribution 的形态是从这个语料库里读出来的 |
| **RefChecker** | 参考文献核对 | 作为可选外部 CLI 集成，没有 vendoring |
| **nature-skills / ARS** | 按需加载 reference 的组织方式 | 这里的规范是 CVPR 的，和 Nature 不同 |
| **CVPR-Figure** | — | 保持为独立 skill；它负责图，并共用同一个语料库 |

---

## FAQ

**审计器报 warning，是不是我论文有问题？**
不是。已发表论文平均每篇也有 4.7 个 warning。warning 的意思是*落在常见区间之外*，而
落在常见区间之外经常是对的。真正有意义的是 error：语料库里没有任何一篇论文这么写。

**我不是做 3D 视觉的。**
那就重建 profile。结构性结论——图题表题的不对称、图是外部矢量稿、ablation 是必需品、
hedge 要定量配给——比具体词数更通用。

**为什么不直接用通用写作助手？**
因为它会让你删掉 `leverage`、改写你的三段式列表，而它完全不知道你投的这个会议里
45 篇有 45 篇都在用它标红的那个句式。

**它能判断我的科学做得对不对吗？**
不能，而且它明说不能。它测的是结构和文字。数字能不能支撑论断，在
`references/audit/integrity.md`，那是人工的一遍。

**这些数字从哪来的？**
`references/corpus/README.md`，`scripts/build_profile.py` 就是生成它们的脚本。源文件是
别人的论文，不随仓库分发。

---

## 许可

MIT，见 [LICENSE](LICENSE)。
