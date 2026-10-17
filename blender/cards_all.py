"""Render every All-projects card: blender -b --python cards_all.py [-- name ...]"""
import bmesh, bpy, math, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cards
from cards import mat, mesh_obj, text, center, save, reset
import addon_utils
from mathutils import Vector
addon_utils.enable("moblend", default_set=False)
from moblend import api

HERE = os.path.dirname(os.path.abspath(__file__))
UNB = os.path.join(HERE, "fonts", "Unbounded.ttf")
ED = "/home/gertin/Documents/programs/kottman-templates/fonts/editorial-font-editorial/394 EditorialToday/OpenType-TT/EditorialToday-Bold.ttf"


def rt(s):
    s.eevee.use_raytracing = True


def brand_gradient(stops, span=2.5, emit=0.25):
    m = bpy.data.materials.new("Grad")
    m.use_nodes = True
    N, L = m.node_tree.nodes, m.node_tree.links
    p = next(n for n in N if n.type == "BSDF_PRINCIPLED")
    geo, sx, mr, cr = (N.new(t) for t in ("ShaderNodeNewGeometry", "ShaderNodeSeparateXYZ", "ShaderNodeMapRange", "ShaderNodeValToRGB"))
    mr.inputs["From Min"].default_value, mr.inputs["From Max"].default_value = -span, span
    el = cr.color_ramp.elements
    el[0].color, el[1].color = (*stops[0], 1), (*stops[-1], 1)
    for i, c in enumerate(stops[1:-1], 1):
        el.new(i / (len(stops) - 1)).color = (*c, 1)
    L.new(geo.outputs["Position"], sx.inputs[0]); L.new(sx.outputs["X"], mr.inputs["Value"]); L.new(mr.outputs["Result"], cr.inputs["Fac"])
    L.new(cr.outputs["Color"], p.inputs["Base Color"]); L.new(cr.outputs["Color"], p.inputs["Emission Color"])
    p.inputs["Emission Strength"].default_value = emit
    p.inputs["Roughness"].default_value = 0.12
    p.inputs["Coat Weight"].default_value = 1.0
    return m


def mortiflix():
    reset()
    t = text("M", UNB, size=6, depth=0.9, bevel=0.08,
             material=brand_gradient([(0.3, 0.12, 1.0), (1.0, 0.08, 0.45), (0.02, 0.75, 1.0)]))
    t.rotation_euler = (math.radians(90), math.radians(-8), math.radians(-24))
    center(t)


def kottman():
    reset()
    t = text("K", ED, size=7, depth=0.7, bevel=0.05, material=mat("Chrome", (0.92, 0.92, 0.95), rough=0.06, metal=1.0))
    t.rotation_euler = (math.radians(90), 0, math.radians(-28))
    center(t)


def strata():
    s = reset(); rt(s)
    cols = [(0.98, 0.62, 0.12), (0.95, 0.32, 0.2), (0.85, 0.12, 0.38), (0.42, 0.25, 0.95), (0.05, 0.05, 0.06)]
    for i, c in enumerate(cols):
        o = mesh_obj(f"L{i}", lambda bm: bmesh.ops.create_cube(bm, size=1.0), mat(f"L{i}", c, rough=0.15, coat=1.0), smooth=False)
        o.scale = (4.2, 3.0, 0.32)
        o.location = (0.22 * i - 0.44, 0.1 * i, 1.5 - 0.7 * i)
        o.rotation_euler = (0, 0, math.radians(-22 + 6 * i))
        b = o.modifiers.new("b", "BEVEL"); b.width = 0.12; b.segments = 5


def singer():
    s = reset(); rt(s)
    root = bpy.data.objects.new("Mic", None); s.collection.objects.link(root)
    h = mesh_obj("Handle", lambda bm: bmesh.ops.create_cone(bm, cap_ends=True, segments=64, radius1=0.38, radius2=0.55, depth=3.2),
                 mat("Body", (0.04, 0.04, 0.05), rough=0.25, metal=1.0)); h.location = (0, 0, -1.6); h.parent = root
    r = mesh_obj("Ring", lambda bm: bmesh.ops.create_cone(bm, cap_ends=True, segments=64, radius1=0.66, radius2=0.66, depth=0.25),
                 mat("Gold", (1.0, 0.72, 0.35), rough=0.18, metal=1.0)); r.location = (0, 0, 0.05); r.parent = root
    ball = lambda bm: bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=1.05)
    g = mesh_obj("Grille", ball, mat("Grill", (0.85, 0.85, 0.9), rough=0.2, metal=1.0)); g.location = (0, 0, 0.95); g.parent = root
    g.modifiers.new("w", "WIREFRAME").thickness = 0.035
    i = mesh_obj("Inner", ball, mat("In", (0.02, 0.02, 0.02), rough=0.6)); i.scale = (0.93,) * 3; i.location = (0, 0, 0.95); i.parent = root
    root.rotation_euler = (math.radians(-18), math.radians(28), 0)
    root.scale = (1.05,) * 3
    root.location = (0, 0, 0.25)


def multiplayer():
    s = reset(); rt(s)
    for nm, x, c, rz in [("A", -1.9, (1.0, 0.42, 0.05), -32), ("B", 1.9, (0.12, 0.5, 1.0), 32)]:
        o = mesh_obj("Monkey" + nm, lambda bm: bmesh.ops.create_monkey(bm), mat(nm, c, rough=0.2, coat=1.0))
        o.location = (x, 0, 0); o.rotation_euler = (0, 0, math.radians(rz)); o.scale = (1.35,) * 3
        sub = o.modifiers.new("s", "SUBSURF"); sub.levels = sub.render_levels = 2
    glow = mat("Glow", (0, 0, 0), emit=(0.03, 0.77, 0.17), strength=12)
    l = mesh_obj("Link", lambda bm: bmesh.ops.create_cone(bm, cap_ends=True, segments=24, radius1=0.06, radius2=0.06, depth=1.3), glow)
    l.rotation_euler = (0, math.radians(90), 0); l.location = (0, -0.6, 0.35)


def hollowell():
    s = reset(); rt(s)
    prof = [(0.0, -1.9), (0.95, -1.9), (1.0, -1.8), (1.0, 0.4), (0.9, 0.8), (0.42, 1.25), (0.36, 1.9), (0.42, 2.0), (0.42, 2.1), (0.0, 2.1)]
    def lathe(points, segs=64):
        def b(bm):
            rings = []
            for k in range(segs):
                a = 2 * math.pi * k / segs
                rings.append([bm.verts.new((r * math.cos(a), r * math.sin(a), z)) for r, z in points])
            for k in range(segs):
                A, B = rings[k], rings[(k + 1) % segs]
                for j in range(len(points) - 1):
                    try:
                        bm.faces.new((A[j], B[j], B[j + 1], A[j + 1]))
                    except ValueError:
                        pass
            bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-4)
        return b
    glass = mat("Glass", (0.75, 0.38, 0.08), rough=0.04, coat=1.0, emit=(0.6, 0.25, 0.03), strength=0.35)
    b = mesh_obj("Bottle", lathe(prof), glass)
    liquid = mat("Cider", (0.85, 0.42, 0.05), rough=0.05)
    lq = mesh_obj("Liquid", lathe([(0.0, -1.85), (0.93, -1.85), (0.93, 0.35), (0.0, 0.35)]), liquid)
    cork = mesh_obj("Cork", lambda bm: bmesh.ops.create_cone(bm, cap_ends=True, segments=48, radius1=0.38, radius2=0.42, depth=0.6),
                    mat("Cork", (0.55, 0.36, 0.18), rough=0.8)); cork.location = (0, 0, 2.3)
    lab = mesh_obj("Label", lathe([(1.005, -1.1), (1.005, 0.1)]), mat("Label", (0.93, 0.88, 0.76), rough=0.7))
    root = bpy.data.objects.new("BottleRoot", None); s.collection.objects.link(root)
    for o in (b, lq, cork, lab):
        o.parent = root
    root.rotation_euler = (0, math.radians(12), math.radians(8))
    root.scale = (0.82,) * 3
    root.location.z = -0.3


def music():
    s = reset(); rt(s)
    m = brand_gradient([(0.05, 0.95, 0.55), (0.1, 0.65, 1.0), (0.55, 0.3, 1.0)], span=2.6, emit=0.5)
    t = text("\u266B", "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", size=7, depth=0.7, bevel=0.06, material=m)
    t.rotation_euler = (math.radians(90), math.radians(-6), math.radians(-24))
    center(t)


def transitions():
    s = reset(); rt(s)
    mb = bpy.data.metaballs.new("Blob"); mb.resolution = 0.08; mb.render_resolution = 0.04
    ob = bpy.data.objects.new("Blob", mb); s.collection.objects.link(ob)
    rng = random.Random(2)
    for _ in range(14):
        e = mb.elements.new(); e.co = (rng.uniform(-2.4, 2.4), rng.uniform(-0.8, 0.8), rng.uniform(-1.4, 1.4)); e.radius = rng.uniform(0.7, 1.3)
    mb.materials.append(mat("Orange", (1.0, 0.3, 0.06), rough=0.08, coat=1.0))
    mb2 = bpy.data.metaballs.new("Drops"); mb2.render_resolution = 0.04
    ob2 = bpy.data.objects.new("Drops", mb2); s.collection.objects.link(ob2)
    for _ in range(6):
        e = mb2.elements.new(); e.co = (rng.uniform(-3.2, 3.2), rng.uniform(-1.6, -1.0), rng.uniform(-1.8, 1.8)); e.radius = rng.uniform(0.25, 0.45)
    mb2.materials.append(mat("White", (0.95, 0.95, 0.95), rough=0.1, coat=1.0))


def nova():
    s = reset()
    rng = random.Random(9)
    cols = [(1.0, 0.35, 0.05), (1.0, 0.75, 0.2), (1.0, 0.15, 0.35)]
    for i in range(240):
        d = Vector((rng.gauss(0, 1), rng.gauss(0, 1), rng.gauss(0, 1))).normalized()
        r = rng.uniform(1.6, 3.0)
        c = cols[i % 3]
        m = bpy.data.materials.get(f"E{i % 3}") or mat(f"E{i % 3}", (0, 0, 0), emit=c, strength=3.5)
        tail = mesh_obj(f"T{i}", lambda bm: bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=0.0, radius2=0.035, depth=r * 0.55), m)
        tail.location = d * (r * 0.72)
        tail.rotation_euler = d.to_track_quat("Z", "Y").to_euler()
        spark = mesh_obj(f"S{i}", lambda bm: bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.06), m)
        spark.location = d * r
    core = mesh_obj("Core", lambda bm: bmesh.ops.create_icosphere(bm, subdivisions=3, radius=0.35), mat("Core", (0, 0, 0), emit=(1, 0.85, 0.6), strength=8))
    s.view_settings.view_transform = "Standard"


def moblend():
    s = reset(); rt(s)
    cols = {"cube": (1.0, 0.45, 0.65), "ball": (0.55, 0.45, 1.0), "torus": (0.3, 0.9, 0.7), "cone": (1.0, 0.75, 0.3)}
    objs = []
    for k, c in cols.items():
        b = {"cube": lambda bm: bmesh.ops.create_cube(bm, size=0.9),
             "ball": lambda bm: bmesh.ops.create_uvsphere(bm, u_segments=24, v_segments=12, radius=0.5),
             "torus": lambda bm: bmesh.ops.create_cone(bm, cap_ends=True, segments=24, radius1=0.5, radius2=0.0, depth=0.9),
             "cone": lambda bm: bmesh.ops.create_cone(bm, cap_ends=True, segments=24, radius1=0.45, radius2=0.45, depth=0.9)}[k]
        o = mesh_obj("P_" + k, b, mat("P_" + k, c, rough=0.15, coat=0.8), smooth=k != "cube")
        if k == "cube":
            bv = o.modifiers.new("b", "BEVEL"); bv.width = 0.1; bv.segments = 4
        objs.append(o)
    cl = api.create_cloner("grid", objects=[o.name for o in objs], name="Ball",
                           params={"Count X": 7, "Count Y": 7, "Count Z": 7, "Spacing": [0.62, 0.62, 0.62], "Shape": "Sphere", "Order": "Random"})
    api.add_effector("random", cloners=["Ball"], name="Rnd", params={"Rotation": [180, 180, 180], "Position": [0.15, 0.15, 0.15]})
    api.add_effector("plain", cloners=["Ball"], name="Pop", falloff="Sphere", size=2.2, location=[1.5, -2.0, 1.2],
                     params={"Position": [0.6, -1.2, 0.6], "Uniform Scale": 0.35})


ALL = [mortiflix, kottman, strata, singer, multiplayer, hollowell, music, transitions, nova, moblend]
want = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
for fn in ALL:
    if not want or fn.__name__ in want:
        fn()
        print("SAVED", save(fn.__name__), flush=True)
