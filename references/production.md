# 执行、检查与交付

## 项目组织

每次建立新的工作目录：input/原模型、source/新blend与脚本、assets/纹理和标识、audio/音轨与事件表、renders/preview、renders/final、qa/检查、delivery/视频与封面。输入文件不覆盖，依具体任务制作说明，不用本技能模板掩盖未完成部分。

## 渲染默认

Blender 4.5.3 Cycles。有可用OptiX GPU时使用GPU+OptiX降噪；不可用时明确采用CPU/OpenImageDenoise并重新估时。

预览：24 samples、自适应阈值 .09、min4，通常50%尺寸。正式：原生1080×1920、64 samples、阈值 .03、min8。原片：max bounces8、diffuse3、glossy4、transparent16，固定seed7017，persistent data，motion blur shutter .35。尺寸、帧率和时长遵循新要求。

每帧PNG RGB8，禁止放大低分辨率预览冒充高清。先渲染近景、装配中、闭合后代表帧估计耗时，再完整运行。脚本将scene SHA256与渲染参数写进signature；源文件或参数变了必须换输出目录，不能混用旧帧。纹理应pack到blend，外部依赖变化也需要新版本。程序终端结束前先检查退出码与进度，不因等待超时盲目重开同一渲染。

CLI（用实际绝对路径替代尖括号；脚本参数必须在Blender的`--`后）：

    blender -b scene.blend --python scripts/inspect_scene.py -- --out scene.json
    blender -b scene.blend --python scripts/apply_look.py -- --config mapping.json --out revised.blend
    blender -b revised.blend --python scripts/render_frames.py -- --out preview --preview --frames 1,120,360,480
    blender -b revised.blend --python scripts/render_frames.py -- --out final
    python scripts/encode_video.py --frames final --fps 24 --start 1 --count 480 --audio audio/main_mix.wav --out delivery/video.mp4 --ffmpeg ffmpeg.exe

encode_video默认把新WAV音轨编码成AAC320k。修订旧片需原音轨时用`--audio 原片.mp4 --copy-audio`，只在声音长度和时序一致时使用。输出存在会报错，换版本名。

## 验收

先看近景纸纹、槽口、金属、标识，再看完整运动：入场、路径、接触落位、遮挡、闭合、相机连续性、留白和最后停留。检查全片编码后的成品，不只看工程预览。逐帧总览用于发现问题，关键动作边界加密检查；静止停留的重复帧可能是设计，不要一律当失败。

编码：H.264 High、CRF16、BT.709、yuv420p、faststart；声音AAC48kHz立体声。完整解码并核对分辨率、帧数、24fps及实际时长。原音轨复制要比较packet hash。声画整体改变的新版不能沿用旧检查结论。

交付可播放MP4、可编辑blend(贴图pack)、制作说明、检查记录，按需封面、无声版和独立音轨。网页式编辑器并非这类Blender工程的必需交付。

## 局部标识修订

同片只改箱面时，先哈希确认原视频匹配哪版工程。删除真正的字体/贴图而非用不贴合的屏幕遮挡；新增标识跟随箱体，保留透视、遮挡和运动模糊。已保存原始无损帧时可只渲染覆盖旧字和新图的区域，再合成到原帧；每帧投影边界应留运动模糊和降噪余量，画外帧要记录原因。混合边缘要在改动区域之外；多角度、阴影或透明变化影响更广时改用整帧渲染。

不要把轴部件旧片的固定帧326–480或箱面坐标当通用参数。
