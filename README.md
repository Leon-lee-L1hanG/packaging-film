# Packaging Film · 包装写实装配视频

将分件三维包装或产品模型制作为写实装配视频的 Codex Skill。保存真实纸面材质、金属加工纹理、暖色摄影灯光和连续装配镜头方法，并提供检查、赋材质、渲染及编码脚本。

## 安装与使用

将整个仓库下载或克隆到 Codex 的个人技能目录，文件夹命名为 packaging-film：

- Windows：`%USERPROFILE%\.codex\skills\packaging-film`
- macOS / Linux：`~/.codex/skills/packaging-film`

如果设置了CODEX_HOME，改放在其skills子目录。在新任务中提供模型文件并输入：

> 用 $packaging-film 将这个模型制作成写实包装装配视频。

默认20秒、1080×1920竖屏、24fps、无字幕无解说，搭配轻节奏音乐和装配音效。模型结构、材质分区、UV和动作需要依据实际输入适配；本技能并非任意文件一键转换器。

## 包含内容

- `SKILL.md`：技能入口与完整执行路线。
- `assets/approved-look.blend`：已打包纹理的材质和灯光库，不包含原产品模型。
- `assets/handling-symbols.png`：四联包装标识。
- `references/`：材质、运镜、渲染、来源和参数。
- `scripts/`：Blender场景检查、明确映射赋材质、断点渲染、FFmpeg编码和完整解码验证。

## 运行依赖

Blender 4.5.x、FFmpeg/ffprobe、Python 3.10+；普通Python安装`requirements.txt`中的Pillow。Blender脚本使用Blender自带Python。OptiX为可选加速；STEP等CAD格式需先通过合适工具转换为分件网格。

命令示例见 `references/production.md`。请先保存模型副本；脚本拒绝覆盖已有输出，渲染目录会记录源工程指纹。

## 验证范围

已用独立测试模型验证材质库加载、灯光尺度适配、两帧渲染、视频编码和完整解码。每个新产品仍需完整的材质、装配路径、镜头与声音检查。

素材来源见 `references/provenance.md`。本仓库未额外授予第三方素材或用户提供图像的再分发许可。
