<<<<<<< HEAD
import pytest
import os
from egasub.ega.entities.ega_enums import EgaEnums

def test_load_enums():
    e = EgaEnums()
    assert len(e.lookup("analysis_types")) == 3
=======
import pytest
import os
from egasub.ega.entities.ega_enums import EgaEnums

def test_load_enums():
    e = EgaEnums()
    assert len(e.lookup("analysis_types")) == 3
>>>>>>> e06fb7c7150bb2f460241499edefe41bd286b60d
