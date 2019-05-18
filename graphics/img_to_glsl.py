from PIL import Image
from math import ceil

FILE_IN = "in.png"
FILE_OUT = "out.glsl"
STEP = 128
WIDTH, HEIGHT = 128, 128

COLORS = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 255),
    (255, 128, 0),
]

img = Image.open(FILE_IN)
mat = img.load()

l_arr = (WIDTH * HEIGHT) // 10
arr = [0] * l_arr
shift = [2**(3*i) for i in range(10)]

for i in range(HEIGHT):
    for j in range(WIDTH):
        idx = i * WIDTH + j
        color = mat[j, i]
        val = 0
        if color[3] > 200:
            best = 770
            for cid in range(7):
                diff = sum(abs(color[c] - COLORS[cid][c]) for c in range(3))
                if diff < best:
                    val = cid
                    best = diff
            val += 1
        arr[idx // 10] += shift[idx % 10] * val

selectindex = "\n".join(
"""if(pos >= {low}u && pos < {high}u) {{
  const int[{step}] indexv = int[{step}] ({indexvec});
  index = (indexv[pos % {step}u] >> (3u * off)) & 7; }}"""\
.format(
    indexvec=",".join(map(lambda x: "%d" % x, arr[stid*STEP:(stid+1)*STEP])),
    low=stid*STEP, high=(stid+1)*STEP, step=STEP
)
for stid in range(l_arr//STEP)
)

code = """vec3 pikachuText(int idx_x, int idx_y, vec3 col) {{
const vec3[7] colors = vec3[7]({colorvec});
int idx = idx_y * {width} + idx_x;
uint off = uint(idx % 10);
uint pos = uint(idx / 10);
int index;
{selectindex}
if(index == 0) return col;
else return colors[index-1];
}}
""".format(
    colorvec=",".join("vec3(%s)" % ",".join(map(lambda x: "%.3f" % (x / 255.1), col))
                      for col in COLORS),
    width=WIDTH, selectindex=selectindex
)

with open(FILE_OUT, "w") as f_write:
    f_write.write(code)
