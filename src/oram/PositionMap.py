from typing import Dict, List


class PositionMap:
    def __init__(self):
        #  x := self._position_map[a] means that block a is currently mapped to the x-th leaf node
        self._position_map: Dict[str, int] = dict()

    def get(self, key: str):
        if not self.contains(key):
            raise KeyError(key)

        return self._position_map[key]

    def set(self, key: str, value: int):
        if self.contains(key):
            raise KeyError(key, f"Key <{key}> is already exists")

        self._position_map[key] = value

    def size(self) -> int:
        return len(self._position_map)

    def contains(self, key: str):
        return key in self._position_map

    def remove(self, key: str):
        if not self.contains(key):
            return None  # TODO maybe raise KeyError(key)

        del self._position_map[key]

    def clear(self):
        self._position_map.clear()

    def keys(self) -> List[str]:
        return self._position_map.keys()

    def values(self) -> List[int]:
        return self._position_map.values()
