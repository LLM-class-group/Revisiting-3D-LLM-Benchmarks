import bpy
from mathutils import Vector
import sys


def look_at(obj_camera, target_point):
    """
    设置相机朝向目标点
    :param obj_camera: 相机对象
    :param target_point: 目标点的坐标
    """
    direction = target_point - obj_camera.location
    rot_quat = direction.to_track_quat("-Z", "Y")
    obj_camera.rotation_euler = rot_quat.to_euler()


def create_light(name, type, location, energy=1000):
    light_data = bpy.data.lights.new(name=name, type=type)
    light_data.energy = energy
    light_obj = bpy.data.objects.new(name=name, object_data=light_data)
    bpy.context.scene.collection.objects.link(light_obj)
    light_obj.location = location
    return light_obj


# 获取命令行参数
argv = sys.argv
argv = argv[argv.index("--") + 1 :]  # 获取 -- 之后的所有参数
input_ply = argv[0]
output_image = argv[1]
direction_x = int(argv[2])
direction_y = int(argv[3])

# 清除所有现有物体（可选）
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete()

# 导入.ply文件
bpy.ops.wm.ply_import(filepath=input_ply)
obj = bpy.context.view_layer.objects.active

# 创建新材质并设置为使用顶点颜色
material = bpy.data.materials.new(name="Material.001")
material.use_nodes = True
nodes = material.node_tree.nodes
links = material.node_tree.links

# 清除默认节点
nodes.clear()

# 创建节点
vertex_color = nodes.new(type="ShaderNodeVertexColor")
diffuse_bsdf = nodes.new(type="ShaderNodeBsdfDiffuse")
material_output = nodes.new(type="ShaderNodeOutputMaterial")

# 连接节点
links.new(vertex_color.outputs["Color"], diffuse_bsdf.inputs["Color"])
links.new(diffuse_bsdf.outputs["BSDF"], material_output.inputs["Surface"])

obj.data.materials.append(material)

# 添加光源, 创建三点照明
main_light = create_light("Main_Light", "SUN", (10, -10, 10), energy=5)
fill_light = create_light("Fill_Light", "SUN", (-10, -10, 8), energy=3)
back_light = create_light("Back_Light", "SUN", (0, 10, 5), energy=4)

# 计算物体中心点并移动到场景中心
points_co_global = []
points_co_global.extend([obj.matrix_world @ vertex.co for vertex in obj.data.vertices])
x, y, z = [[point_co[i] for point_co in points_co_global] for i in range(3)]


def get_center(l):
    return (max(l) + min(l)) / 2 if l else 0.0


b_sphere_center = (
    Vector([get_center(axis) for axis in [x, y, z]]) if (x and y and z) else None
)
obj.location.x -= b_sphere_center[0]
obj.location.y -= b_sphere_center[1]
obj.location.z -= b_sphere_center[2]

# 计算合适的相机距离
radius = ((max(x) + max(y) + max(z)) - (min(x) + min(y) + min(z))) / 6
camera_radius = 7 * radius

# 创建新相机
cam_data = bpy.data.cameras.new("Camera")
cam = bpy.data.objects.new("Camera", cam_data)
bpy.context.scene.collection.objects.link(cam)
bpy.context.scene.camera = cam  # 设置为活动相机

# 设置相机位置
cam.location = (3 * radius * direction_x, 3 * radius * direction_y, 3 * radius)
origin = Vector((0, 0, 0))
look_at(cam, origin)  # 设置相机朝向
cam.data.lens = 45  # 设置焦距
cam.data.clip_start = 0.1  # 设置裁剪起始位置
cam.data.clip_end = 1000  # 设置裁剪结束位置

# 设置渲染参数
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.render.engine = "CYCLES"  # 使用Cycles渲染引擎
bpy.context.scene.cycles.samples = 128  # 设置采样数

# 确保使用顶点颜色
if obj.data.vertex_colors:
    obj.data.vertex_colors.active_index = 0

# 渲染并保存图片
bpy.context.scene.render.filepath = output_image
bpy.ops.render.render(write_still=True)

# 清理场景
bpy.data.objects.remove(obj)
for light in [main_light, fill_light, back_light]:
    bpy.data.objects.remove(light)
bpy.data.objects.remove(cam)
