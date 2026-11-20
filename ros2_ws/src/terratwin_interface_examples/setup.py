from setuptools import find_packages, setup

package_name = "terratwin_interface_examples"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    extras_require={"test": ["pytest"]},
    zip_safe=True,
    maintainer="TerraTwin Robotics Maintainers",
    maintainer_email="maintainers@example.com",
    description="Runnable examples for TerraTwin ROS 2 interfaces.",
    license="Apache-2.0",
    entry_points={
        "console_scripts": [
            "status_publisher = terratwin_interface_examples.status_publisher:main",
            "status_subscriber = terratwin_interface_examples.status_subscriber:main",
            "mission_action_server = terratwin_interface_examples.mission_action_server:main",
            "mission_action_client = terratwin_interface_examples.mission_action_client:main",
        ],
    },
)
