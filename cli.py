#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""小学奥数出题器 CLI - 简单易用的命令行接口"""

import click
import json
import sys
import subprocess
from pathlib import Path

# 检查依赖
def ensure_dependency(mod, pip):
      try:
                __import__(mod)
except ImportError:
        click.echo(f"正在安装 {pip}...", err=True)
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", pip], check=False)

ensure_dependency("docx", "python-docx")

SCRIPT_DIR = Path(__file__).parent / "scripts"

@click.group()
def cli():
      """小学奥数出题器 🎓

              快速生成课本风格的小学奥数题目、练习和作业。
                  """
      pass

@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('-o', '--output', default=None, help='输出Word文件路径（默认根据JSON中的filename）')
def generate(input_file, output):
      """根据JSON配置生成Word文档"""
      try:
                # 调用build_doc.py
                result = subprocess.run(
                              [sys.executable, str(SCRIPT_DIR / "build_doc.py"), input_file],
                              capture_output=True,
                              text=True
                )
                if result.returncode != 0:
                              click.echo(f"❌ 生成失败: {result.stderr}", err=True)
                              sys.exit(1)

                # 读取JSON获取输出文件名
                with open(input_file, encoding='utf-8') as f:
                              data = json.load(f)
                          output_file = data.get('filename', 'output.docx')
                click.echo(f"✅ 生成成功: {output_file}")
except Exception as e:
        click.echo(f"❌ 错误: {e}", err=True)
        sys.exit(1)

@cli.command()
@click.argument('spec_file', type=click.Path(exists=True))
@click.option('-o', '--output', default='output.png', help='输出图片路径')
def draw(spec_file, output):
      """根据几何图规范生成PNG图片"""
      try:
                result = subprocess.run(
                              [sys.executable, str(SCRIPT_DIR / "draw_figure.py"), spec_file],
                              capture_output=True,
                              text=True
                )
                if result.returncode != 0:
                              click.echo(f"❌ 绘图失败: {result.stderr}", err=True)
                              sys.exit(1)
                          click.echo(f"✅ 图片生成成功: {output}")
except Exception as e:
        click.echo(f"❌ 错误: {e}", err=True)
        sys.exit(1)

@cli.command()
def template():
      """显示题目JSON模板"""
      template_json = {
          "title": "三年级 · 巧求面积 · 举一反三",
          "filename": "output.docx",
          "examples": [
              {
                  "stem": "一个长方形，长为10cm，宽为5cm，求面积。",
                  "figure": "fig_example.png",
                  "analysis": "长方形面积 = 长 × 宽",
                  "solution": "面积 = 10 × 5 = 50cm²",
                  "practices": ["练习1：长8cm，宽4cm", "练习2：长6cm，宽3cm"]
              }
          ],
          "homework": [],
          "answers": []
      }
      click.echo(json.dumps(template_json, ensure_ascii=False, indent=2))

@cli.command()
def examples():
      """显示3个完整的Prompt模板"""
      templates = {
          "example": """
  给我生成一个小学三年级关于【巧求面积】的例题：
  - 包含一个几何图（矩形或组合图形）
  - 难度：中等（需要学生思考）
  - 生成格式为JSON，包含：title、examples(包含stem/figure/analysis/solution)、practices、homework、answers
          """,
          "practice": """
  生成5道关于【平行四边形面积】的练习题（小学四年级难度）：
  - 每题配一个几何图
  - 答案详细
  - 按难度递进（简→难）
  - 输出为JSON格式，包含examples和practices
          """,
          "homework": """
  生成小学五年级【梯形面积】的课堂作业（12题）：
  - 前6题基础（直接计算）
  - 后6题提高（需要分解或组合）
  - 包含标准答案
  - 输出为JSON格式
          """
      }

    click.echo("\n" + "="*50)
    click.echo("📝 Prompt 模板 1: 生成例题（配图解）")
    click.echo("="*50)
    click.echo(templates["example"])

    click.echo("\n" + "="*50)
    click.echo("📝 Prompt 模板 2: 生成练习题（递进难度）")
    click.echo("="*50)
    click.echo(templates["practice"])

    click.echo("\n" + "="*50)
    click.echo("📝 Prompt 模板 3: 生成作业（基础+提高）")
    click.echo("="*50)
    click.echo(templates["homework"])

@cli.command()
def quickstart():
      """快速开始指南"""
      guide = """
  🚀 快速开始指南
  ================

  ## 1️⃣ 安装
     pip install -r requirements.txt

  ## 2️⃣ 获取Prompt模板
     python cli.py examples

  ## 3️⃣ 使用AI生成题目JSON
     - 复制上面的Prompt模板
     - 粘贴到Claude/ChatGPT
     - 获得符合格式的JSON输出

  ## 4️⃣ 生成Word文档
     python cli.py generate problems.json
     # 输出: 输出文件名.docx

  ## 5️⃣ 生成几何图
     python cli.py draw spec.json
     # 输出: output.png

  ## 📖 查看JSON模板
     python cli.py template

  ## 🎨 完整工作流
     1. 使用Prompt模板让AI生成题目JSON
     2. 保存为 my_problems.json
     3. 运行: python cli.py generate my_problems.json
     4. 生成Word文档完成！
  """
      click.echo(guide)

if __name__ == '__main__':
      cli()
