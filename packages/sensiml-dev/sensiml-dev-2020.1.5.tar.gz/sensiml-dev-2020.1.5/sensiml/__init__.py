from sensiml.client import SensiML
try:
    from sensiml_widgets import DashBoard
except:
    # dev version fails here so lets import a dummy
    from sensiml.datasegments import DataSegments as DashBoard

name = "sensiml"

__version__ = "2020.2.0"
__all__ = ["SensiML", "DashBoard"]
