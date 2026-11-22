"""Structural and physical checks for the UGV Xacro model."""
import math
import shutil
import subprocess
from pathlib import Path
import xml.etree.ElementTree as ET

import pytest
import xacro

XACRO_FILE = Path(__file__).resolve().parent.parent / 'urdf' / 'terratwin_ugv.urdf.xacro'

REQUIRED_FRAMES = {
    'base_footprint', 'base_link', 'lidar_link', 'imu_link', 'gnss_link',
    'camera_link', 'camera_optical_frame',
}
WHEELS = ['front_left', 'front_right', 'rear_left', 'rear_right']
TOL = 1e-9


def floats(text, default='0 0 0'):
    return [float(v) for v in (text or default).split()]


@pytest.fixture(scope='module')
def urdf_xml(tmp_path_factory):
    xml = xacro.process_file(str(XACRO_FILE)).toxml()
    return xml


@pytest.fixture(scope='module')
def robot(urdf_xml):
    return ET.fromstring(urdf_xml)


@pytest.fixture(scope='module')
def links(robot):
    return {link.get('name'): link for link in robot.findall('link')}


@pytest.fixture(scope='module')
def joints(robot):
    return {joint.get('name'): joint for joint in robot.findall('joint')}


@pytest.fixture(scope='module')
def positions(joints):
    """Position of every link frame relative to base_footprint (translations only)."""
    children = {}
    for joint in joints.values():
        parent = joint.find('parent').get('link')
        child = joint.find('child').get('link')
        origin = joint.find('origin')
        xyz = floats(origin.get('xyz') if origin is not None else None)
        children.setdefault(parent, []).append((child, xyz))
    result = {'base_footprint': [0.0, 0.0, 0.0]}
    stack = ['base_footprint']
    while stack:
        parent = stack.pop()
        for child, xyz in children.get(parent, []):
            result[child] = [a + b for a, b in zip(result[parent], xyz)]
            stack.append(child)
    return result


def test_unique_names_and_required_frames(robot, links):
    link_names = [link.get('name') for link in robot.findall('link')]
    joint_names = [joint.get('name') for joint in robot.findall('joint')]
    assert len(link_names) == len(set(link_names))
    assert len(joint_names) == len(set(joint_names))
    assert REQUIRED_FRAMES <= set(links)


def test_no_prefix_baked_into_link_names(links):
    # The ugv/ TF prefix is applied by robot_state_publisher; baking it in would double it.
    assert not [name for name in links if name.startswith('ugv/')]


def test_single_connected_tree_rooted_at_base_footprint(links, joints, positions):
    child_links = {joint.find('child').get('link') for joint in joints.values()}
    roots = set(links) - child_links
    assert roots == {'base_footprint'}
    assert set(positions) == set(links), 'some links are not connected to the tree'
    assert len(joints) == len(links) - 1


def test_four_continuous_wheel_joints_on_y_axis(joints):
    for wheel in WHEELS:
        joint = joints[f'{wheel}_wheel_joint']
        assert joint.get('type') == 'continuous'
        assert floats(joint.find('axis').get('xyz')) == [0.0, 1.0, 0.0]
        assert joint.find('parent').get('link') == 'base_link'


def test_wheels_are_symmetric(positions):
    for side in ('left', 'right'):
        assert abs(positions[f'front_{side}_wheel_link'][2]
                   - positions[f'rear_{side}_wheel_link'][2]) < TOL
    for end in ('front', 'rear'):
        left = positions[f'{end}_left_wheel_link']
        right = positions[f'{end}_right_wheel_link']
        assert abs(left[0] - right[0]) < TOL
        assert abs(left[1] + right[1]) < TOL
        assert left[1] > 0 > right[1], 'left wheel must be on +y'
    assert positions['front_left_wheel_link'][0] > positions['rear_left_wheel_link'][0]


def test_wheels_touch_the_ground(links, positions):
    for wheel in WHEELS:
        name = f'{wheel}_wheel_link'
        radius = float(links[name].find('collision/geometry/cylinder').get('radius'))
        assert abs(positions[name][2] - radius) < TOL, f'{name} does not rest on z=0'


def test_chassis_clears_ground_and_wheels(links, positions):
    size = floats(links['base_link'].find('collision/geometry/box').get('size'))
    length, width, height = size
    assert positions['base_link'][2] - height / 2 > 0, 'chassis underside below ground'
    for wheel in WHEELS:
        name = f'{wheel}_wheel_link'
        cylinder = links[name].find('collision/geometry/cylinder')
        wheel_width = float(cylinder.get('length'))
        radius = float(cylinder.get('radius'))
        x, y, _ = positions[name]
        assert abs(y) - wheel_width / 2 >= width / 2 - TOL, 'wheel overlaps chassis sideways'
        assert abs(x) + radius <= length / 2 + TOL, 'wheel sticks out past chassis ends'


def test_inertials_are_physical(links):
    for name, link in links.items():
        inertial = link.find('inertial')
        if inertial is None:
            assert name in {'base_footprint', 'camera_optical_frame'}
            continue
        assert float(inertial.find('mass').get('value')) > 0
        inertia = inertial.find('inertia')
        ixx, iyy, izz = (float(inertia.get(k)) for k in ('ixx', 'iyy', 'izz'))
        assert min(ixx, iyy, izz) > 0, name
        assert ixx + iyy >= izz - TOL and iyy + izz >= ixx - TOL and ixx + izz >= iyy - TOL, \
            f'{name}: inertia violates the triangle inequality'


def test_wheel_axial_inertia_is_about_the_axle(links):
    for wheel in WHEELS:
        mass = float(links[f'{wheel}_wheel_link'].find('inertial/mass').get('value'))
        radius = float(links[f'{wheel}_wheel_link']
                       .find('collision/geometry/cylinder').get('radius'))
        inertia = links[f'{wheel}_wheel_link'].find('inertial/inertia')
        assert math.isclose(float(inertia.get('iyy')), mass * radius ** 2 / 2, rel_tol=1e-6)


def test_overall_size_is_about_one_foot(links, positions):
    size = floats(links['base_link'].find('collision/geometry/box').get('size'))
    cylinder = links['front_left_wheel_link'].find('collision/geometry/cylinder')
    overall_width = 2 * abs(positions['front_left_wheel_link'][1]) + float(cylinder.get('length'))
    assert 0.25 <= size[0] <= 0.40
    assert 0.25 <= overall_width <= 0.40


@pytest.mark.skipif(shutil.which('check_urdf') is None, reason='check_urdf not installed')
def test_check_urdf_accepts_model(urdf_xml, tmp_path):
    path = tmp_path / 'ugv.urdf'
    path.write_text(urdf_xml)
    result = subprocess.run(['check_urdf', str(path)], capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
