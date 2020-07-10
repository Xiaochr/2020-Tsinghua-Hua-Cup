# 2020年第26届清华大学华罗庚杯数学建模竞赛

这学期五一无聊，和岳爷组队做了一个校内的数学建模比赛，最后拿到**二等奖特别鼓励奖**。

## 问题简介

自行收集选取数据，对学者的 h-index（一种衡量学者学术影响力的指标）建立数学模型，对下面问题进行研究：

1. 一些知名学者的 h-index 增长规律，并比较异同。

2. 预测一名学者（不同年龄段，甚至已经去世的学者文章仍然在被引用，h-index 仍然可能增长）未来的h-index 值。

3. 通过收集到的数据，对h-index 指标的合理性和有效性进行评价；若存在不足，有何改进思路？

## Repo 主要内容

- data 文件夹
    - 收集到的学者相关信息原始数据
    - author_info 文件夹
        - 学者当前的 h-index 数据
    - Question_B 文件夹
        - [竞赛题目 pdf 文件](data/Question_B/2020_question_B.pdf)

- other_data 文件夹
    - 进行预测检验的学者数据

- [paper_tex 文件夹](paper_tex/)
    - 只放了论文的 .tex、.bib、所需的图片及最终 pdf 文件，模板为 [ElegantPaper](https://github.com/ElegantLaTeX/ElegantPaper) ![GitHub stars](https://img.shields.io/github/stars/ElegantLaTeX/ElegantPaper?style=social) 

- [pre_slides 文件夹](pre_slides/)
    - 只放了答辩展示的 .tex、.bib、所需的图片及最终 pdf 文件。

- results 文件夹
    - 代码输出结果

- 代码：
    - extract_h_index，从原始数据摘取之后分析所需的信息。
    - naive_reg_model，简单的回归思路。
    - clustering，对学者聚类的过程。
    - arima_model，利用 ARIMA 模型进行预测。
    - draw_plots，画出论文、展示所需的图。
    - test_plot，画出用来验证模型的新学者的 h-index 增长图。
