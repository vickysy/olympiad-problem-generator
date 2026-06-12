# 🎓 小学奥数出题器 - 快速开始指南

> 一句话出例题/练习/作业，自带课本风格几何图引擎

## ⚡ 30秒快速开始

### 1. 安装
```bash
pip install -r requirements.txt
```

### 2. 查看Prompt模板
```bash
python cli.py examples
```

### 3. 复制模板，让AI生成JSON
粘贴任一Prompt模板到 Claude/ChatGPT，获得JSON输出

### 4. 生成Word文档
```bash
python cli.py generate problems.json
```

✅ 完成！输出Word文件已生成

---

## 📋 3个常用Prompt模板

### 📝 模板1：生成【例题】（配图解析）

```
给我生成一个小学三年级关于【巧求面积】的例题，要求：
- 包含1个几何图规范(可以是矩形、三角形或组合图形)
- 难度：中等（需要学生思考）
- 格式：JSON，包含以下字段：
  {
      "title": "题目标题",
          "filename": "输出文件名.docx",
              "examples": [
                    {
                            "stem": "题目内容",
                                    "figure": "图片文件名",
                                            "analysis": "分析思路",
                                                    "solution": "详细解答",
                                                            "practices": ["练习1", "练习2"]
                                                                  }
                                                                      ],
                                                                          "homework": [],
                                                                              "answers": []
                                                                                }
                                                                                ```

                                                                                ---

                                                                                ### ✍️ 模板2：生成【练习题】（递进难度）

                                                                                ```
                                                                                生成5道关于【平行四边形面积】的练习题（小学四年级难度），要求：
                                                                                - 难度递进：简单(2题) → 中等(2题) → 提高(1题)
                                                                                - 每题配1个几何图
                                                                                - 包含详细答案
                                                                                - 格式为JSON（只需examples和practices部分）
                                                                                ```

                                                                                ---

                                                                                ### 📚 模板3：生成【作业】（12道完整作业）

                                                                                ```
                                                                                生成小学五年级【梯形面积】的课堂作业，要求：
                                                                                - 共12道题
                                                                                - 结构：基础题(6道) + 提高题(6道)
                                                                                - 前6道：直接代入公式计算
                                                                                - 后6道：需要分解或组合图形
                                                                                - 包含标准答案和解题步骤
                                                                                - JSON格式：homework字段12行，answers字段详细
                                                                                ```

                                                                                ---

                                                                                ## 🛠️ 命令参考

                                                                                ### 查看JSON模板
                                                                                ```bash
                                                                                python cli.py template
                                                                                ```

                                                                                ### 生成Word文档
                                                                                ```bash
                                                                                python cli.py generate problems.json -o output.docx
                                                                                ```

                                                                                ### 生成几何图
                                                                                ```bash
                                                                                python cli.py draw spec.json -o output.png
                                                                                ```

                                                                                ### 显示所有命令
                                                                                ```bash
                                                                                python cli.py --help
                                                                                ```

                                                                                ---

                                                                                ## 💡 完整工作流示例

                                                                                ### Step1: 准备Prompt
                                                                                从上面的3个模板中选一个，复制Prompt文本

                                                                                ### Step2: AI生成JSON
                                                                                粘贴到 Claude 或 ChatGPT

                                                                                ```
                                                                                🤖 Claude: "给我生成一个小学三年级关于【巧求面积】的例题..."
                                                                                💬 回复: 整个JSON代码块
                                                                                ```

                                                                                ### Step3: 保存JSON
                                                                                ```bash
                                                                                # 复制AI输出的JSON，保存为 problems.json
                                                                                cat > problems.json << 'EOF'
                                                                                {
                                                                                  "title": "...",
                                                                                    ...
                                                                                    }
                                                                                    EOF
                                                                                    ```

                                                                                    ### Step4: 生成Word
                                                                                    ```bash
                                                                                    python cli.py generate problems.json
                                                                                    # 输出: 3年级_巧求面积_举一反三_练习题.docx ✅
                                                                                    ```

                                                                                    ---

                                                                                    ## ❓ 常见问题

                                                                                    **Q: 生成的图片怎么放到题目里？**
                                                                                    A: 在JSON中指定 `"figure": "图片文件名.png"`，确保图片在同目录

                                                                                    **Q: 怎么自定义Word样式？**
                                                                                    A: 编辑 `scripts/build_doc.py` 中的样式设置

                                                                                    **Q: 支持什么几何图形？**
                                                                                    A: 支持：矩形、三角形、圆形、多边形等，见 `draw_figure.py` 规范

                                                                                    **Q: 如何批量生成多个题目？**
                                                                                    A: 为每个题目创建不同的JSON文件，逐个运行 `cli.py generate`

                                                                                    ---

                                                                                    ## 🎯 核心三个硬保证

                                                                                    ✅ **图用代码，不用文生图** - draw_figure.py自带课本风格几何图引擎
                                                                                    ✅ **标注自动，不用手工** - 图注自动对应到题目，自动标注-45°斜向阴影等
                                                                                    ✅ **格式统一，不用调整** - 自动排版，输出Word直接可用

                                                                                    ---

                                                                                    **Happy Generating! 🚀**
