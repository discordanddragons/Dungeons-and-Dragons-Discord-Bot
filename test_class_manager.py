import pytest
from class_manager import ClassManager

def test_classes_load():
    cls_mgr = ClassManager()
    assert len(cls_mgr.classes) > 0