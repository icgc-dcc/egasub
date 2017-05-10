from egasub.ega.entities.ega_enums import EgaEnums

def test_load_enums():
    e = EgaEnums()
    assert len(e.lookup("analysis_types")) == 3
