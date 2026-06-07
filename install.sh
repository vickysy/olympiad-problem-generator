#!/usr/bin/env bash
# 小学奥数出题器 · 一键安装到 OpenClaw
# 用法: curl -fsSL https://raw.githubusercontent.com/vickysy/olympiad-problem-generator/main/install.sh | bash
set -e
DEST="$HOME/.openclaw/skills/olympiad-problem-generator"
REPO="https://github.com/vickysy/olympiad-problem-generator.git"
mkdir -p "$HOME/.openclaw/skills"
if [ -d "$DEST/.git" ]; then
  echo "已安装，正在更新到最新版…"
  git -C "$DEST" pull --ff-only
else
  rm -rf "$DEST"
  git clone --depth 1 "$REPO" "$DEST"
fi
echo ""
echo "✅ 安装完成：$DEST"
echo "确认：运行  openclaw skills list | grep olympiad"
