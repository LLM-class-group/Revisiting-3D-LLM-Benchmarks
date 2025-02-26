import cv2
import numpy as np
import pickle
import io
import base64
from plyfile import PlyData
from scipy.spatial import distance
from scipy.ndimage import median_filter, uniform_filter
from skimage.measure import marching_cubes
from scipy.spatial import KDTree
from plyfile import PlyData
from PIL import Image

DETAIL_OUTPUT = False


def load(path, separator=','):
    extension = path.split('.')[-1]
    if extension == 'npy':
        pcl = np.load(path, allow_pickle=True)
    elif extension == 'npz':
        pcl = np.load(path)
        pcl = pcl['arr_0']
    elif extension == 'ply':
        ply = PlyData.read(path)
        vertex = ply['vertex']
        (x, y, z) = (vertex[t] for t in ('x', 'y', 'z'))
        pcl = np.column_stack((x, y, z))
        if 'red' in vertex and 'green' in vertex and 'blue' in vertex:
            (r, g, b) = (vertex[t] for t in ('red', 'green', 'blue'))
            pcl = np.column_stack((pcl, r, g, b))
            pcl[:, 3:] = pcl[:, 3:] / 255 if pcl[:, 3:].max() > 1.0 else pcl
    elif extension == 'txt':
        f = open(path, 'r')
        line = f.readline()
        data = []
        while line:
            x, y, z = line.split(separator)[:3]
            data.append([float(x), float(y), float(z)])
            line = f.readline()
        f.close()
        pcl = np.array(data)
    elif extension == 'pth' or extension == 'pt':
        import torch
        pcl = torch.load(path, map_location='cpu')
        pcl = pcl.detach().numpy()
    elif extension == 'pkl':
        with open(path, 'rb') as f:
            data = pickle.load(f)
        if isinstance(data, dict) and 'points' in data:
            pcl = np.array(data['points'])
        elif isinstance(data, np.ndarray):
            pcl = data
        else:
            raise ValueError(
                "Unsupported .pkl format. Expected dict with 'points' key or NumPy array.")
    else:
        print('unsupported file format.')
        raise FileNotFoundError

    if pcl.shape[0] in [3, 4, 6]:
        pcl = pcl.T

    pcl = np.array(pcl)
    assert pcl.shape[-1] == 3 or pcl.shape[-1] == 6 or pcl.shape[-1] == 4

    if len(pcl.shape) == 3:
        pcl = pcl[0]
        print("the dimension is 3, we select the first element in the batch.")
    return pcl


def color_map(config, pcl):
    n, c = pcl.shape

    if config.white:
        if DETAIL_OUTPUT:
            print("Rendered with white color.")
        color = np.ones((n, 3)) * 0.6
    elif len(config.RGB) == 3:
        if DETAIL_OUTPUT:
            print("Rendered with input RGB color.")
        rgb = np.array(list(map(float, config.RGB))) / 255
        color = np.tile(rgb, (n, 1))
    elif c == 6:
        if DETAIL_OUTPUT:
            print("Rendered with points color.")
        color = pcl[:, 3:]
        if color.max() > 1 + 1e-2:
            color = color / 255
            print("Normalize points color from 255 to 1.")
        color[color < 0] = 0
        color[color > 1] = 1
    elif c == 4:
        color = pcl[:, 3]
        color = (color - np.min(color)) / (np.max(color) - np.min(color))
        # gamma transformation
        color = np.power(color, 0.5)
        print("Rendered with 1-d value color.")
        color = load_self_colormap(color)
    elif config.knn:
        print("Rendered with knn color.")
        color = np.zeros((n, 3))
        knn_center = fps(pcl + 0.5, config.center_num)
        for i in range(n):
            color[i] = generate_knn_pos_colormap(
                pcl[i] + 0.5, config, knn_center)
    else:
        print("Rendered with position color.")
        color = np.zeros((n, 3))
        for i in range(n):
            color[i] = generate_pos_colormap(pcl[i] + 0.5, config)

    return np.concatenate((pcl[:, :3], color), axis=1)


def mask_point(pcl, mask_center=128, mask_ratio=0.5):
    mask_center = fps(pcl[:, :3], mask_center)
    mask_center = mask_center[:int(mask_center * mask_ratio)]
    new_pcl = []
    for i in range(pcl.shape[0]):
        distances = distance.cdist(pcl[i, :3], mask_center, 'euclidean')
        if np.min(distances) > 0.05:
            new_pcl.append(pcl[i])
    new_pcl = np.array(new_pcl)
    return new_pcl


def load_self_colormap(value):
    # You can adjust the Level Curve with gamma transformation
    vec = np.power(value, 2)
    vec = 255 - 255 * (vec - np.min(vec)) / (np.max(vec) -
                                             np.min(vec))  # normalize to [0, 255]
    vec = vec.reshape(1, -1).astype(np.uint8)
    vec = cv2.applyColorMap(vec, cv2.COLORMAP_JET)  # apply colormap
    color = vec.reshape(-1, 3) / 255  # normalize to [0, 1]
    color = 0.5 * color + 0.5 * 0.5
    return color


def generate_pos_colormap(pos, config):
    vec = np.clip(pos, config.contrast, 1.0)
    norm = np.sqrt(np.sum(vec ** 2))
    vec /= norm
    return vec


def generate_knn_pos_colormap(pos, config, knn_center):
    dis = np.linalg.norm(knn_center - pos, axis=1)
    index = np.argmin(dis)
    vec = knn_center[index]

    vec = np.clip(vec, config.contrast, 1.0)
    norm = np.sqrt(np.sum(vec ** 2))
    vec /= norm
    return vec


def standardize_bbox(config, data):
    xyz = data[:, :3]

    if config.median:
        xyz = median_filter_3d(xyz)

    mins = np.amin(xyz, axis=0)
    maxs = np.amax(xyz, axis=0)
    center = (mins + maxs) / 2.
    scale = np.amax(maxs - mins)
    xyz = ((xyz - center) / scale).astype(np.float32)  # [-0.5, 0.5]
    if DETAIL_OUTPUT:
        print("Center: {}, Scale: {}".format(center, scale))

    if data.shape[-1] > 3:
        pcl = np.concatenate((xyz, data[:, 3:]), axis=1)
    else:
        pcl = xyz

    if config.num < pcl.shape[0]:
        print(f'downsample to {config.num} points')
        pt_indices = np.random.choice(pcl.shape[0], config.num, replace=False)
        np.random.shuffle(pt_indices)
        pcl = pcl[pt_indices]

    return pcl, center, scale


def fps(data, k):
    N, C = data.shape
    sample_data = np.zeros((k, C))
    points = data[:, :3]
    color = data[:, 3:]
    barycenter = np.sum(points, axis=0) / points.shape[0]
    distance = np.full((points.shape[0]), np.nan)
    point = barycenter

    for i in range(k):
        distance = np.minimum(distance, np.sum((points - point) ** 2, axis=1))
        index = np.argmax(distance)
        point = points[index]
        sample_data[i] = np.concatenate((point, color[index]), axis=0)
        mask = np.ones((points.shape[0]), dtype=bool)
        mask[index] = False
        points = points[mask]
        distance = distance[mask]
    return sample_data


def median_filter_3d(pcl, channel=3, voxel_size=64, kernel_size=2, level=0.5, times=1):
    print("using median filter")
    for i in range(times):
        voxel = point_cloud_to_voxel(pcl, voxel_size=voxel_size)
        voxel = median_filter(voxel, size=kernel_size)
        median_pcl = voxel_to_point_cloud(voxel, level=level)
        N = median_pcl.shape[0]
        new_pcl = np.zeros((N, channel))
        if channel == 6:
            for i in range(N):
                distances = distance.cdist(
                    median_pcl[i, :3], pcl[:, :3], 'euclidean')
                index = np.argmin(distances)
                new_pcl[i, :3] = median_pcl[i, :3]
                new_pcl[i, 3:] = pcl[index, 3:]
        else:
            new_pcl = median_pcl
        pcl = new_pcl
    print("filtered point cloud shape: ", pcl.shape)
    return pcl


def point_cloud_to_voxel(point_cloud, voxel_size):
    R = voxel_size
    voxel_shape = (R, R, R)

    voxel_data = np.zeros(voxel_shape, dtype=np.int32)

    min_bound = np.min(point_cloud, axis=0)
    point_cloud = point_cloud - min_bound
    max_bound = np.max(np.max(point_cloud, axis=0))

    point_cloud_scaled = point_cloud / max_bound * (R - 1)

    for point in point_cloud_scaled:
        voxel_index = np.floor(point).astype(int)
        voxel_data[voxel_index[0], voxel_index[1], voxel_index[2]] = 1

    return voxel_data


def voxel_to_point_cloud(voxel, level):
    pts, _, _, _ = marching_cubes(voxel, level=level)
    return pts


def rotation(rotation_angle):
    x, y, z = rotation_angle
    x, y, z = int(x), int(y), int(z)
    print(f'rotation angle: {x}, {y}, {z}')
    x_rad, y_rad, z_rad = np.radians(x), np.radians(y), np.radians(z)

    rot_x = np.array([[1, 0, 0], [0, np.cos(x_rad), -
                     np.sin(x_rad)], [0, np.sin(x_rad), np.cos(x_rad)]])
    rot_y = np.array([[np.cos(y_rad), 0, np.sin(y_rad)], [
                     0, 1, 0], [-np.sin(y_rad), 0, np.cos(y_rad)]])
    rot_z = np.array([[np.cos(z_rad), -np.sin(z_rad), 0],
                     [np.sin(z_rad), np.cos(z_rad), 0], [0, 0, 1]])

    rot_matrix = np.dot(np.dot(rot_z, rot_y), rot_x)
    return rot_matrix


def interpolate_point_cloud(points, k=2):
    N = points.shape[0]
    tree = KDTree(points[:, :3])

    dists, indices = tree.query(points[:, :3], k=k)
    alphas = np.random.rand(N, k - 1, 1)

    neighbor_points = points[indices[:, 1:], :3]
    neighbor_attrs = points[indices[:, 1:], 3:]

    original_points = points[:, :3].reshape(N, 1, 3)
    original_attrs = points[:, 3:].reshape(N, 1, -1)

    new_points = alphas * original_points + (1 - alphas) * neighbor_points
    new_attrs = alphas * original_attrs + (1 - alphas) * neighbor_attrs

    new_points = np.concatenate(
        [new_points, new_attrs], axis=2).reshape(-1, points.shape[1])

    return np.vstack((points, new_points))


def filter_point_cloud(point_cloud, angle_threshold_degrees=90, fix=False):
    # Extract XYZ coordinates from the point cloud
    xyz = point_cloud[:, :3]

    # Center the point cloud at the origin and normalize
    center = np.mean(xyz, axis=0)
    normalized_xyz = (xyz - center) / np.linalg.norm(xyz -
                                                     center, axis=1)[:, np.newaxis]

    # Randomly select a point within a sphere of radius
    if fix:
        angles = np.pi / 2
    else:
        angles = np.random.uniform(0, np.pi)
    x = np.sin(angles)
    y = np.cos(angles)
    random_point = np.array([x, y, 0])

    # Calculate angles between the random point and all points in the normalized point cloud
    dot_product = np.dot(normalized_xyz, random_point.T)
    clipped_dot_product = np.clip(dot_product, -1.0, 1.0)
    angles = np.arccos(clipped_dot_product)

    # Filter points based on the angle threshold
    filtered_indices = np.where(np.degrees(
        angles) < angle_threshold_degrees)[0]

    # Keep only the selected points
    selected_points = point_cloud[filtered_indices]

    return selected_points


def get_xml(resolution=[1920, 1080], view=[3, 3, 3], radius=0.025, object_type="point", BEV=False):
    width, height = int(resolution[0]), int(resolution[1])
    x, y, z = float(view[0]), float(view[1]), float(view[2])
    position = f"{x}, {y}, {z}"
    if BEV:
        xml_head = \
            f"""
        <scene version="0.6.0">
            <integrator type="path">
                <integer name="maxDepth" value="-1"/>
            </integrator>
            <sensor type="perspective">
                <float name="farClip" value="100"/>
                <float name="nearClip" value="0.1"/>
                <transform name="toWorld">
                    <lookat origin="{position}" target="0,0,0" up="0,1,0"/>
                </transform>
                <float name="fov" value="25"/>
                <sampler type="independent">
                    <integer name="sampleCount" value="256"/>
                </sampler>
                <film type="hdrfilm">
                    <integer name="width" value="{width}"/>
                    <integer name="height" value="{height}"/>
                    <rfilter type="gaussian"/>
                </film>
            </sensor>

            <bsdf type="roughplastic" id="surfaceMaterial">
                <string name="distribution" value="ggx"/>
                <float name="alpha" value="0.05"/>
                <float name="intIOR" value="1.46"/>
                <rgb name="diffuseReflectance" value="1,1,1"/> <!-- default 0.5 -->
            </bsdf>

        """
    else:
        xml_head = \
            f"""
        <scene version="0.6.0">
            <integrator type="path">
                <integer name="maxDepth" value="-1"/>
            </integrator>
            <sensor type="perspective">
                <float name="farClip" value="100"/>
                <float name="nearClip" value="0.1"/>
                <transform name="toWorld">
                    <lookat origin="{position}" target="0,0,0" up="0,0,1"/>
                </transform>
                <float name="fov" value="25"/>
                <sampler type="independent">
                    <integer name="sampleCount" value="256"/>
                </sampler>
                <film type="hdrfilm">
                    <integer name="width" value="{width}"/>
                    <integer name="height" value="{height}"/>
                    <rfilter type="gaussian"/>
                </film>
            </sensor>

            <bsdf type="roughplastic" id="surfaceMaterial">
                <string name="distribution" value="ggx"/>
                <float name="alpha" value="0.05"/>
                <float name="intIOR" value="1.46"/>
                <rgb name="diffuseReflectance" value="1,1,1"/> <!-- default 0.5 -->
            </bsdf>

        """

    xml_ball_segment = \
        """
        <shape type="sphere">
            <float name="radius" value="%s"/>
            <transform name="toWorld">
                <translate x="{}" y="{}" z="{}"/>
            </transform>
            <bsdf type="diffuse">
                <rgb name="reflectance" value="{},{},{}"/>
            </bsdf>
        </shape>
    """ % radius

    xml_cube_segment = \
        """
        <shape type="cube">
        <transform name="toWorld">
            <scale x="%s" y="%s" z="%s" />
            <translate x="{}" y="{}" z="{}"/>
        </transform>
        <bsdf type="diffuse">
            <rgb name="reflectance" value="{},{},{}"/>
        </bsdf>
    </shape>
    """ % (radius, radius, radius)

    xml_tail = \
        """
        <shape type="rectangle">
            <ref name="bsdf" id="surfaceMaterial"/>
            <transform name="toWorld">
                <scale x="100" y="100" z="2"/>
                <translate x="0" y="0" z="-0.3"/>
            </transform>
        </shape>

        <shape type="rectangle">
            <transform name="toWorld">
                <scale x="10" y="10" z="1"/>
                <lookat origin="-4,4,20" target="0,0,0" up="0,0,1"/>
            </transform>
            <emitter type="area">
                <rgb name="radiance" value="6,6,6"/>
            </emitter>
        </shape>
    </scene>
    """

    assert object_type == "point" or object_type == "voxel"
    xml_object_segment = xml_ball_segment if object_type == "point" else xml_cube_segment
    return xml_head, xml_object_segment, xml_tail


def encode_image(image_path):
    if image_path is None:
        return None
    try:
        with Image.open(image_path) as image:
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            return base64.b64encode(buffered.getvalue()).decode('utf-8')
    except Exception as e:
        raise ValueError(f"无法编码图片，错误信息：{e}")


def get_mllm_messages(prompt, base64_image=None):
    if base64_image is None:
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt,
                    }
                ],
            }
        ]
    else:
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    },
                    {
                        "type": "text",
                        "text": prompt,
                    },
                ],
            },
        ]

    return messages
