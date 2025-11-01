from abc import ABC, abstractmethod
from typing import List, Dict

class Dependency:
    def __init__(self, name: str, version: str, ecosystem: str):
        self.name = name
        self.version = version
        self.ecosystem = ecosystem

    def __repr__(self):
        return f"Dependency(name='{self.name}', version='{self.version}', ecosystem='{self.ecosystem}')"
