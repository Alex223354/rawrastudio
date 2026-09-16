import subprocess

FFMPEG = r"C:\Users\AlexGuerrero\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.1-full_build\bin\ffmpeg.exe"

GALLERY = r"C:\Users\AlexGuerrero\rawrastudio\assets\projects\casa-manila-gallery"
TEX = r"C:\Users\AlexGuerrero\rawrastudio\assets\video\textures"
LOGO_WHITE = r"C:\Users\AlexGuerrero\rawrastudio\assets\logo-mark-real-dark.png"
LOGO_BLACK = r"C:\Users\AlexGuerrero\rawrastudio\assets\logo-mark-real.png"
OUT = r"C:\Users\AlexGuerrero\rawrastudio\assets\video\hero-reel.mp4"

# (image path, seconds shown, vertical crop bias 0=top..1=bottom, 0.5=center)
# marble opener is held longer than the rest
T = 0.4  # crossfade duration between every pair of clips
clips = [
    (f"{TEX}\\marble.jpg", 3.6, 0.5),
    (f"{GALLERY}\\hero.jpg", 1.6, 0.5),
    (f"{TEX}\\walnut.jpg", 1.6, 0.5),
    (f"{TEX}\\bathroom-vanity-hq.jpg", 1.6, 0.72),
    (f"{TEX}\\linen.jpg", 1.6, 0.5),
    (f"{GALLERY}\\04-living-room.jpg", 1.6, 0.5),
    (f"{TEX}\\rattan.jpg", 1.6, 0.5),
    (f"{GALLERY}\\13-bathroom-moody.jpg", 1.6, 0.5),
]

W, H = 2200, 1238
n = len(clips)

# cumulative timeline: when each xfade completes (i.e. clip i is fully on screen)
durations = [d for _, d, _ in clips]
clip_end = [durations[0]]
for d in durations[1:]:
    clip_end.append(clip_end[-1] + d - T)
total_duration = clip_end[-1]

marble_done_at = clip_end[0]  # when the marble->next crossfade finishes

inputs = []
for img, d, _ in clips:
    inputs += ["-loop", "1", "-t", str(d), "-i", img]
inputs += ["-loop", "1", "-t", str(total_duration), "-i", LOGO_BLACK]
inputs += ["-loop", "1", "-t", str(total_duration), "-i", LOGO_WHITE]
logo_black_idx = n
logo_white_idx = n + 1

filters = []
for i, (img, d, bias) in enumerate(clips):
    filters.append(
        f"[{i}:v]scale={W}:{H}:force_original_aspect_ratio=increase,"
        f"crop=w={W}:h={H}:x=(in_w-{W})/2:y=(in_h-{H})*{bias},"
        f"setsar=1,fps=30,format=yuv420p[v{i}]"
    )

prev = "v0"
for i in range(1, n):
    offset = round(clip_end[i - 1] - T, 3)
    out_label = f"vx{i}"
    filters.append(
        f"[{prev}][v{i}]xfade=transition=fade:duration={T}:offset={offset}[{out_label}]"
    )
    prev = out_label

# darken slightly for logo legibility
filters.append(f"[{prev}]eq=brightness=-0.10:saturation=0.95[dark]")

# scale both logo variants and overlay: black over the marble opener, white afterwards
logo_h = round(260 * H / 1080)
filters.append(f"[{logo_black_idx}:v]scale=-1:{logo_h}[logob]")
filters.append(f"[{logo_white_idx}:v]scale=-1:{logo_h}[logow]")
filters.append(
    f"[dark][logob]overlay=(W-w)/2:(H-h)/2:enable='lt(t,{round(marble_done_at, 3)})'[step1]"
)
filters.append(
    f"[step1][logow]overlay=(W-w)/2:(H-h)/2:enable='gte(t,{round(marble_done_at, 3)})'[withlogo]"
)

# bookend fades
fade_out_start = round(total_duration - 0.5, 3)
filters.append(f"[withlogo]fade=t=in:st=0:d=0.5,fade=t=out:st={fade_out_start}:d=0.5[vout]")

filter_complex = ";".join(filters)

cmd = [
    FFMPEG, "-y",
    *inputs,
    "-filter_complex", filter_complex,
    "-map", "[vout]",
    "-an",
    "-c:v", "libx264",
    "-preset", "slow",
    "-crf", "18",
    "-pix_fmt", "yuv420p",
    "-r", "30",
    "-t", str(total_duration),
    "-movflags", "+faststart",
    OUT,
]

print(f"total_duration={total_duration}s  marble_done_at={marble_done_at}s")
print("Running ffmpeg...")
result = subprocess.run(cmd, capture_output=True, text=True)
print(result.returncode)
if result.returncode != 0:
    print(result.stderr[-4000:])
else:
    print("OK ->", OUT)
