# 素材来源和运行环境

此技能从一部20秒Blender包装装配动画中提炼，保留材质、摄影棚灯光和连续装配制作方法，不包含原产品模型或历史对话。

## 素材

- approved-look.blend 包含纸面、木材、金属、背景、标识材质及两盏灯和世界环境；照片纹理已打包。
- 源工程记录纸照片为CC0/public domain，环境贴图为Poly Haven studio_small_09，木纹名为plywood_diff_2k。此处记录原工程来源，不替代原素材授权文件。
- handling-symbols.png 为技能制作用户提供的四联储运标识图。
- look-manifest.json保存提取时的参数与材质名。参考坐标仅用于按新模型尺寸适配灯光，不代表新产品工程尺寸。

## 依赖

- Blender 4.5.x，Cycles；NVIDIA OptiX可加速，脚本支持CPU回退。
- FFmpeg与ffprobe，支持libx264及AAC。
- 普通Python 3.10+与Pillow（仅视频合成脚本）。其余脚本由Blender内置Python运行。
- CAD格式转换需要使用者自己的CAD导入/转换工具；Blender不能直接读取STEP。

通过PATH或用户配置定位程序，Windows可用Get-Command，macOS/Linux可用command -v。调用时传入本机绝对路径；本技能不携带Blender、FFmpeg等可执行程序。
