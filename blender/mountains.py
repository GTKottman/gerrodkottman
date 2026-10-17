"""Dark rocky mountain ridge used in front of every slide, matching the Davies template's mountain art."""
import math
import random

import bmesh
import bpy
from mathutils import noise, Vector


def rock_material():
    mat = bpy.data.materials.get("GK Rock")
    if mat:
        return mat
    mat = bpy.data.materials.new("GK Rock")
    mat.use_nodes = True
    nt = mat.node_tree
    b = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    b.inputs["Roughness"].default_value = 0.9
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 40.0
    nz.inputs["Detail"].default_value = 12.0
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].color = (0.006, 0.006, 0.007, 1)
    ramp.color_ramp.elements[1].color = (0.06, 0.06, 0.065, 1)
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.6
    nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
    nt.links.new(nz.outputs["Fac"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
    nt.links.new(nz.outputs["Fac"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], b.inputs["Normal"])
    return mat


def ridge(name, y, width, height, depth, seed=1, peaks=4, xs=480, ys=90):
    """A mountain ridge centred on x=0 at distance y (front edge), `height` tall at its peaks."""
    rng = random.Random(seed)
    tops = [(rng.uniform(-0.5, 0.5) * width, rng.uniform(0.55, 1.0) * height, rng.uniform(0.12, 0.3) * width)
            for _ in range(peaks)]
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    rows = []
    for j in range(ys + 1):
        v = j / ys
        row = []
        for i in range(xs + 1):
            u = i / xs
            x = (u - 0.5) * width
            yy = y + v * depth
            h = max(t[1] * max(0.0, 1 - abs(x - t[0]) / t[2]) ** 1.25 for t in tops)
            p = Vector((x / width * 14 + seed, yy / depth * 4, seed * 0.37))
            rid = noise.ridged_multi_fractal(p, 0.9, 2.2, 8, 1.0, 2.0)
            fine = noise.fractal(p * 6, 0.6, 2.3, 5)
            fall = min(1.0, v * 2.2) if v < 0.45 else 1.0
            h = max(0.0, (h * (0.75 + 0.25 * rid) + rid * height * 0.12 + fine * height * 0.03) * fall)
            row.append(bm.verts.new((x, yy, h - height * 0.05)))
        rows.append(row)
    for j in range(ys):
        for i in range(xs):
            bm.faces.new((rows[j][i], rows[j][i + 1], rows[j + 1][i + 1], rows[j + 1][i]))
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = True
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    me.materials.append(rock_material())
    return ob
