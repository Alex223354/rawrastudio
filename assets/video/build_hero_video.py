import subprocess

FFMPEG = r"C:\Users\AlexGuerrero\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.1-full_build\bin\ffmpeg.exe"

GALLERY = r"C:\Users\AlexGuerrero\rawrastudio\assets\projects\casa-manila-gallery"
TEX = r"C:\Users\AlexGuerrero\rawrastudio\assets\video\textures"
LOGO_WHITE = r"C:\Users\AlexGuerrero\rawrastudio\assets\logo-mark-real-dark.png"
LOGO_BLACK = r"C:\Users\AlexGuerrero\rawrastudio\assets\logo-mark-real.png"
OUT = r"C:\Users\AlexGuerrero\rawrastudio\assets\video\hero-reel.mp4"

images = [
    f"{TEX}\\marble.jpg",
    f"{GALLERY}\\hero.jpg",
    f"{TEX}\\walnut.jpg",
    f"{GALLERY}\\05-kitchen-island.jpg",
    f"{TEX}\\linen.jpg",
    f"{GALLERY}\\04-living-room.jpg",
    f"{TEX}\\rattan.jpg",
    f"{GALLERY}\\13-bathroom-moody.jpg",
]

D = 1.6   # seconds each clip is shown
T = 0.4   # crossfade duration
W, H = 2200, 1238

n = len(images)

inputs = []
for img in images:
    inputs += ["-loop", "1", "-t", str(D), "-i", img]
inputs += ["-loop", "1", "-t", "10", "-i", LOGO_BLACK]
inputs += ["-loop", "1", "-t", "10", "-i", LOGO_WHITE]
logo_black_idx = n
logo_white_idx = n + 1

# marble (first clip) is a light background -> black logo until the crossfade
# into the second clip finishes; white logo for the rest of the reel.
black_logo_until = round(1 * (D - T) + T, 3)  # end of first crossfade

filters = []
for i in range(n):
    filters.append(
        f"[{i}:v]scale={W}:{H}:force_original_aspect_ratio=increase,"
        f"crop={W}:{H},setsar=1,fps=30,format=yuv420p[v{i}]"
    )

prev = "v0"
cum = D
for i in range(1, n):
    offset = round(i * (D - T), 3)
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
    f"[dark][logob]overlay=(W-w)/2:(H-h)/2:enable='lt(t,{black_logo_until})'[step1]"
)
filters.append(
    f"[step1][logow]overlay=(W-w)/2:(H-h)/2:enable='gte(t,{black_logo_until})'[withlogo]"
)

# bookend fades
filters.append("[withlogo]fade=t=in:st=0:d=0.5,fade=t=out:st=9.5:d=0.5[vout]")

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
    "-t", "10",
    "-movflags", "+faststart",
    OUT,
]

print("Running ffmpeg...")
result = subprocess.run(cmd, capture_output=True, text=True)
print(result.returncode)
if result.returncode != 0:
    print(result.stderr[-4000:])
else:
    print("OK ->", OUT)
