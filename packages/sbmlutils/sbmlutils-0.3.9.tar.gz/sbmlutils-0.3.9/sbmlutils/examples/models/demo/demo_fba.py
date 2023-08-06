"""
Check the charge and formula balance of the model.
Run some simple FBA simulations.
"""
import os

import cobra
import libsbml
from sbmlutils import fbc
from sbmlutils.examples.models.demo import model

# SBML file
demo_sbml = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         'results',
                         '{}_{}.xml'.format(model.mid, model.version))


def example(path):
    """
    Example FBA with demo model.

    :param path:
    :type path:
    :return:
    :rtype:
    """
    doc = libsbml.readSBMLFromFile(path)

    # add defaults
    fbc.add_default_flux_bounds(doc)

    import tempfile
    f = tempfile.NamedTemporaryFile('w', suffix='xml')
    libsbml.writeSBMLToFile(doc, f.name)
    f.flush()
    model = cobra.io.read_sbml_model(f.name)

    # mass/charge balance
    for r in model.reactions:
        mb = r.check_mass_balance()
        print(r.id, mb)


if __name__ == "__main__":
    example(path=demo_sbml)
