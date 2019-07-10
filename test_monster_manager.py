import pytest
from monster_manager import MonsterManager

def test_load_monsters():
    mgr = MonsterManager()
    assert len(mgr.monsters) > 0
