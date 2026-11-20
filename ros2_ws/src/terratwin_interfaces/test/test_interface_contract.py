# Copyright 2026 TerraTwin Robotics Maintainers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import math

from terratwin_interfaces.action import ExecuteMission
from terratwin_interfaces.msg import (
    MissionFeedback, MissionRequest, MissionResult, MissionWaypoint,
    RobotStatus, UavTelemetry, UgvTelemetry,
)


def test_mission_request_defaults_and_platform_constants():
    request = MissionRequest()
    assert (request.PLATFORM_UNSPECIFIED, request.UAV, request.UGV) == (0, 1, 2)
    assert request.request_id == ''
    assert request.waypoints == []


def test_waypoint_cartesian_representation():
    waypoint = MissionWaypoint()
    waypoint.coordinate_type = MissionWaypoint.CARTESIAN
    waypoint.frame_id = 'map'
    waypoint.x_m = 1.25
    assert waypoint.coordinate_type == 0
    assert waypoint.frame_id == 'map'
    assert math.isclose(waypoint.x_m, 1.25)


def test_mission_result_terminal_states():
    result = MissionResult()
    assert (result.SUCCEEDED, result.REJECTED, result.FAILED,
            result.CANCELED, result.EXPIRED) == (1, 2, 3, 4, 5)


def test_status_and_telemetry_types_exist():
    assert RobotStatus().READY == 2
    assert UavTelemetry().platform_id == ''
    assert UgvTelemetry().platform_id == ''
    assert MissionFeedback().progress == 0.0


def test_action_goal_result_feedback_exist():
    assert ExecuteMission.Goal().request.request_id == ''
    assert ExecuteMission.Result().result.status == 0
    assert ExecuteMission.Feedback().feedback.progress == 0.0
