"""Studio for the All-projects card renders: one hero object per project on a transparent background."""
import math
import bpy
import bmesh
from mathutils import Vector

OUT = "/home/gertin/Documents/programs/gerrodkottman/blender/cards/"


def reset():
    bpy.ops.wm.read_homefile(use_empty=True)
    s = bpy.context.scene
    s.render.engine = "BLENDER_EEVEE"
    s.render.resolution_x, s.render.resolution_y = 1256, 942
    s.render.film_transparent = True
    s.render.image_settings.file_format = "PNG"
    s.render.image_settings.color_mode = "RGBA"
    s.view_settings.view_transform = "AgX"
    try:
        s.view_settings.look = "AgX - Punchy"
    except TypeError:
        pass
    w = bpy.data.worlds.new("Studio")
    s.world = w
    w.use_nodes = True
    nt = w.node_tree
    bg = next(n for n in nt.nodes if n.type == "BACKGROUND")
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    ramp = nt.nodes.new("ShaderNodeValToRGB")       # soft studio: bright ceiling, dark floor (only seen in reflections)
    ramp.color_ramp.elements[0].position = 0.02
    ramp.color_ramp.elements[0].color = (0.01, 0.01, 0.012, 1)
    ramp.color_ramp.elements[1].position = 0.35
    ramp.color_ramp.elements[1].color = (0.9, 0.9, 0.95, 1)
    nt.links.new(tc.outputs["Generated"], sep.inputs[0])
    nt.links.new(sep.outputs["Z"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], bg.inputs["Color"])
    bg.inputs[1].default_value = 0.8
    cd = bpy.data.cameras.new("Cam")
    cam = bpy.data.objects.new("Camera", cd)
    s.collection.objects.link(cam)
    s.camera = cam
    cd.lens = 60
    aim(cam, (0, -14, 4.5), (0, 0, 0))
    for name, loc, energy, col, size in [("Key", (-6, -7, 8), 1500, (1, 0.96, 0.92), 6),
                                         ("Fill", (7, -5, 2), 500, (0.8, 0.88, 1), 8),
                                         ("Rim", (2, 8, 6), 2200, (1, 1, 1), 5)]:
        ld = bpy.data.lights.new(name, "AREA")
        ld.energy, ld.color, ld.size = energy, col, size
        lo = bpy.data.objects.new(name, ld)
        s.collection.objects.link(lo)
        aim(lo, loc, (0, 0, 0))
    return s


def aim(ob, loc, target):
    ob.location = loc
    ob.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()


def mat(name, color, rough=0.3, metal=0.0, emit=None, strength=0.0, coat=0.0, trans=0.0, ior=1.45):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    p = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    p.inputs["Base Color"].default_value = (*color, 1)
    p.inputs["Roughness"].default_value = rough
    p.inputs["Metallic"].default_value = metal
    p.inputs["Coat Weight"].default_value = coat
    p.inputs["Transmission Weight"].default_value = trans
    p.inputs["IOR"].default_value = ior
    if emit:
        p.inputs["Emission Color"].default_value = (*emit, 1)
        p.inputs["Emission Strength"].default_value = strength
    return m


def mesh_obj(name, build, material=None, smooth=True):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    build(bm)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    if smooth:
        for p in me.polygons:
            p.use_smooth = True
    if material:
        me.materials.append(material)
    return ob


def text(body, font, size=3.0, depth=0.4, bevel=0.04, material=None):
    cu = bpy.data.curves.new(body, "FONT")
    cu.body = body
    cu.font = bpy.data.fonts.load(font, check_existing=True)
    cu.size, cu.extrude, cu.bevel_depth = size, depth, bevel
    cu.align_x, cu.align_y = "CENTER", "CENTER"
    ob = bpy.data.objects.new(body, cu)
    bpy.context.scene.collection.objects.link(ob)
    ob.rotation_euler = (math.radians(90), 0, 0)
    if material:
        cu.materials.append(material)
    return ob


def center(ob):
    """Move the object so its visible bounds sit on the origin (the camera's target)."""
    bpy.context.view_layer.update()
    pts = [ob.matrix_world @ Vector(c) for c in ob.bound_box]
    mid = sum(pts, Vector()) / 8
    ob.location -= mid
    return ob


def save(name):
    s = bpy.context.scene
    s.render.filepath = OUT + name + ".png"
    bpy.ops.render.render(write_still=True)
    return s.render.filepath
