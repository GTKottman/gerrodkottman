"""Selected-works slide: Nova FX fireworks bursting behind a mountain ridge. Writes PNG frames to --out."""
import os, sys
EX = os.path.expanduser("~/Documents/programs/nova-fx/examples")
sys.path.insert(0, EX)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from _common import add, advance, look_at, render_settings, start, _render
from mountains import ridge

ARGS = sys.argv[sys.argv.index("--") + 1:]
OUT = ARGS[ARGS.index("--out") + 1]
FIRST, LAST = 150, 150 + 96
sc = start(frame_end=LAST + 2)
show = add("FIREWORKS", "gk_fireworks")
for ob in bpy.data.objects:
    if ob.nova_emitter.enabled:
        ob.nova_emitter.rate = 0.3
ridge("Front", -170, 900, 48, 260, seed=3, peaks=5)
ridge("Back", 40, 1200, 95, 300, seed=9, peaks=4)
import bmesh
bpy.ops.mesh.primitive_plane_add(size=4000, location=(0, 0, -3))
bpy.context.object.data.materials.append(bpy.data.materials["GK Rock"])
w = sc.world
bg = next(n for n in w.node_tree.nodes if n.type == "BACKGROUND")
bg.inputs["Color"].default_value = (0.0015, 0.0015, 0.0025, 1)
cam = sc.camera
cam.location = (0, -220, 22)
look_at(cam, (0, 0, 62))
cam.data.lens = 24
render_settings(res=(860, 645), samples=24)
os.makedirs(OUT, exist_ok=True)
for n, f in enumerate(range(FIRST, LAST)):
    advance([show], f)
    _render(os.path.join(OUT, f"{n:04d}.png"), 100)
print("DONE", OUT, flush=True)
