#!/usr/bin/python

from __future__ import annotations
from typing import Any, Dict, List
from math import sin, cos, sqrt, asin, radians
import unittest


data = {
  "position": [-74.3734, 178.8593],
  "markers": [
    {
      "name": "Studio 33",
      "position": [-74.7007, 4.0000]
    }
    ,
    {
      "name": "Barber Studio",
      "position": [33.9666, -160.2246]
    }
    ,
    {
      "name": "Barber Shop",
      "position": [-41.2233, 154.8337]
    }
    ,
    {
      "name": "Man Cave",
      "position": [-70.1183, -6.3416]
    }
  ]
}



class App:
    def solve(self, _data: Dict[str, Any]):
        result: str = ""
        my_position = Position(*_data.get("position", [0,0]))

        markers_len:int = len(_data.get("markers", []))

        if markers_len == 0 or markers_len >= 100:
            raise ValueError(f"Incorrect markers amount: {markers_len}") 

        result = self._check_distance(_data.get("markers", []), my_position)
            
        return result

    def _check_distance(self, markers:List[Dict[str,Any]],  my_position: Position) -> str:
        current_distance: Distance | None = None
        current_marker_name:str = ""
        for marker in markers:
            distance =  Distance(my_position, Position(*marker.get("position", [0,0])) )
            if not current_distance or distance < current_distance:
                current_distance = distance
                current_marker_name = marker.get("name", "")
        
        return current_marker_name

        
        
class Position:
    def __init__(self, latitude:float, longitude:float) -> None:
        self._latitude = radians(latitude)
        self._longitude = radians(longitude)
        if latitude <= -90 or latitude >= 90:
            raise PositionError(f"-90 <= latitude <= 90")
        if longitude <= -180 or longitude >= 180:
            raise PositionError(f"-180 <= longitude <= 180")

    
    @property
    def latitude(self):
        return self._latitude

    @property
    def longitude(self):
        return self._longitude
 

class Distance:
    def __init__(self, position_one: Position, position_two: Position) -> None:
        self._earth_radius_in_km = 6371
        diff_latitude = position_one.latitude - position_two.latitude
        diff_longitude = position_one.longitude - position_two.longitude
        a = sin(diff_latitude/2)**2 + cos(position_one.latitude) * cos(position_two.latitude) * sin(diff_longitude/2)**2
        c = 2 * asin(sqrt(a))
        self._distance:float = c * self._earth_radius_in_km
    
    @property
    def distance(self):
        return self._distance
    
    def __eq__(self, dist: object) -> bool:
        return self.distance == dist.distance

    def __ne__(self, dist: object):
        return self.distance != dist.distance
    
    def __lt__(self, dist: Distance):
        return self.distance < dist.distance

    def __le__(self, dist: Distance):
        return self.distance <= dist.distance

    def __gt__(self, dist: Distance):
        return self.distance > dist.distance

    def __ge__(self, dist: Distance):
        return self.distance >= dist.distance

    def __str__(self):
        return str(self.distance)

class PositionError(Exception):
    pass



class TestApp(unittest.TestCase):
    def test_resolve(self):
        app = App()
        result = app.solve(data) 
        self.assertEqual(result, "Studio 33")
    
if __name__ == "__main__":
    unittest.main()