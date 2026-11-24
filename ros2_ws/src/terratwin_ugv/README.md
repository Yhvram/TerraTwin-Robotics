# terratwin_ugv

Four-wheel differential-drive (skid-steer) rover, about 1 ft overall. This package currently holds the robot description; Gazebo sensors and `ros2_control` are added in the simulation step.

## View the model

```bash
cd ros2_ws && colcon build --symlink-install && source install/setup.bash
ros2 launch terratwin_ugv display.launch.py            # RViz + joint sliders
ros2 launch terratwin_ugv display.launch.py gui:=false # RViz only
```

Expect a blue-grey box with four black wheels, a blue LiDAR on top, a green GNSS puck at the rear and a small camera on the front face. The Fixed Frame is `ugv/base_footprint`.

## Frames

Link names in the Xacro are plain; `robot_state_publisher` adds the `ugv/` prefix (`frame_prefix`), so the TF tree is:

```
ugv/base_footprint
└── ugv/base_link
    ├── ugv/{front,rear}_{left,right}_wheel_link
    ├── ugv/lidar_link
    ├── ugv/imu_link
    ├── ugv/gnss_link
    └── ugv/camera_link
        └── ugv/camera_optical_frame
```

Conventions: REP-103 (x forward, y left, z up), metres and kilograms. `base_footprint` sits on the ground directly below `base_link`.

## Parameters

All sizes are `xacro:property` values at the top of `urdf/terratwin_ugv.urdf.xacro` (chassis size and mass, ground clearance, wheel radius, width and mass, wheelbase, wheel track). Wheel positions and sensor mount heights are derived from them, so resizing needs no other edits. `test/test_urdf.py` re-checks the geometry after any change.

## Check the model

```bash
colcon test --packages-select terratwin_ugv && colcon test-result --verbose
# optional, if installed:
xacro src/terratwin_ugv/urdf/terratwin_ugv.urdf.xacro > /tmp/ugv.urdf && check_urdf /tmp/ugv.urdf
```

## Not yet done

Gazebo sensor and friction tags, `ros2_control` hardware interface, wheel/caster friction tuning, and motion tests. The mass and inertia values are estimates, not measurements of real hardware.
