from types import SimpleNamespace

import pytest
import rclpy
from builtin_interfaces.msg import Time
from rclpy.action import GoalResponse

from terratwin_interface_examples.mission_action_server import MissionActionServer
from terratwin_interfaces.msg import MissionRequest, MissionWaypoint


@pytest.fixture(scope="module")
def server():
    rclpy.init()
    node = MissionActionServer()
    yield node
    node.destroy_node()
    rclpy.shutdown()


def make_goal(**overrides):
    request = MissionRequest()
    request.request_id = "req-1"
    request.mission_id = "mission-1"
    request.platform = MissionRequest.UGV
    request.waypoints = [MissionWaypoint()]
    request.max_speed_mps = 0.5
    for name, value in overrides.items():
        setattr(request, name, value)
    return SimpleNamespace(request=request)


def test_valid_mission_is_accepted(server):
    assert server.goal_callback(make_goal()) == GoalResponse.ACCEPT


@pytest.mark.parametrize(
    "overrides",
    [
        {"request_id": ""},
        {"mission_id": ""},
        {"waypoints": []},
        {"platform": MissionRequest.PLATFORM_UNSPECIFIED},
        {"max_speed_mps": -1.0},
    ],
)
def test_invalid_mission_is_rejected(server, overrides):
    assert server.goal_callback(make_goal(**overrides)) == GoalResponse.REJECT


def test_expired_mission_is_rejected(server):
    expired = Time(sec=1, nanosec=0)
    assert server.goal_callback(make_goal(expires_at=expired)) == GoalResponse.REJECT
