""" This submoduls contains most of the user-facing code, as the objects
`Sky` and `Instrument` can be used for most of the functionality of the
code, without delving into the difference `Model` objects.

Objects:
    Sky
"""
import toml
import numpy as np
from astropy.utils import data
from . import units as u
from .utils import normalize_weights, bandpass_unit_conversion

from .constants import DATAURL
from .models import *


def remove_class_from_dict(d):
    """Return a copy of dictionary without the key "class" """
    return {k: d[k] for k in d.keys() if k != "class"}


def create_components_from_config(config, nside, map_dist=None):
    output_components = []
    for model_name, model_config in config.items():
        try:
            class_name = model_config["class"]
        except KeyError:  # multiple components
            partial_components = []
            for each_config in model_config.values():
                class_name = each_config["class"]
                component_class = globals()[class_name]
                partial_components.append(
                    component_class(
                        **remove_class_from_dict(each_config),
                        nside=nside,
                        map_dist=map_dist
                    )
                )
            output_component = Sky(
                component_objects=partial_components, nside=nside, map_dist=map_dist
            )
        else:
            component_class = globals()[class_name]
            output_component = component_class(
                **remove_class_from_dict(model_config), nside=nside, map_dist=map_dist
            )
        output_components.append(output_component)
    return output_components


with data.conf.set_temp("dataurl", DATAURL):
    PRESET_MODELS = toml.load(data.get_pkg_data_filename("data/presets.cfg"))


class Sky(Model):
    """ This class is a convenience object that wraps together a group of
    component models. It acts like a single `pysm.Model` object, in that it
    is sub-classed from the `pysm.Model` template, and therefore has the same
    functionality.

    Attributes
    ----------
    components: list(pysm.Model object)
        List of `pysm.Model` objects.
    """

    def __init__(
        self,
        nside=None,
        component_objects=None,
        component_config=None,
        preset_strings=None,
        output_unit=u.uK_RJ,
        map_dist=None,
    ):
        if nside is None and not component_objects:  # not None and not []
            raise Exception("Need to specify nside in Sky")
        elif nside is None:
            nside = component_objects[0].nside
        elif component_objects:
            for comp in component_objects:
                assert (
                    nside == comp.nside
                ), "Component objects should have same NSIDE of Sky"

        super().__init__(nside=nside, map_dist=map_dist)
        self.components = component_objects if component_objects is not None else []
        # otherwise instantiate the sky object from list of predefined models,
        # identified by their strings. These are defined in `pysm.presets`.
        if component_config is None:
            component_config = {}
        elif not isinstance(component_config, dict):
            component_config = toml.load(component_config)
        if preset_strings is not None:
            assert isinstance(preset_strings, list), "preset_strings should be a list"
            for string in preset_strings:
                component_config[string] = PRESET_MODELS[string]
        if len(component_config) > 0:
            self.components += create_components_from_config(
                component_config, nside=nside, map_dist=map_dist
            )
        self.output_unit = u.Unit(output_unit)

    def add_component(self, component):
        self.components.append(component)

    def get_emission(self, freq, weights=None):
        """ This function returns the emission at a frequency, set of
        frequencies, or over a bandpass.
        """
        output = self.components[0].get_emission(freq, weights=weights)
        for comp in self.components[1:]:
            output += comp.get_emission(freq, weights=weights)
        return output * bandpass_unit_conversion(freq, weights, self.output_unit)
