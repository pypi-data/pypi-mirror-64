from __future__ import annotations

class Definition:
    _callback: callable
    _shared: bool = True

    def __init__(self, callback):
        self._callback = callback
    
    def get_callback(self) -> callable:
        return self._callback
    
    def is_shared(self) -> bool:
        return self._shared

    def not_shared(self) -> Definition:
        self._shared = False
        return self
