# -*- coding: utf-8 -*-
"""
Validation and checking functions.
Helper functions for simple validation and display of problems.
Helper functions if setting sbml information was successful.
"""
import os
import logging
import time
import libsbml
from sbmlutils.logutils import bcolors

VALIDATION_NO_UNITS = "VALIDATION_NO_UNITS"


def check(value, message):
    """
    Checks the libsbml return value and prints message if something happened.

    If 'value' is None, prints an error message constructed using
      'message' and then exits with status code 1. If 'value' is an integer,
      it assumes it is a libSBML return status code. If the code value is
      LIBSBML_OPERATION_SUCCESS, returns without further action; if it is not,
      prints an error message constructed using 'message' along with text from
      libSBML explaining the meaning of the code, and exits with status code 1.

    """
    if value is None:
        logging.error('Error: LibSBML returned a null value trying to <' + message + '>.')
    elif type(value) is int:
        if value == libsbml.LIBSBML_OPERATION_SUCCESS:
            return
        else:
            logging.error('Error encountered trying to <' + message + '>.')
            logging.error('LibSBML returned error code {}: {}'.format(str(value),
                          libsbml.OperationReturnValue_toString(value).strip()))
    else:
        return


def check_sbml(filepath, name=None, log_errors=True,
               units_consistency=True,
               modeling_practice=True,
               internal_consistency=True):
    """ Checks the given SBML filepath or string.

    :param doc: SBMLDocument to check
    :param name: identifier or path for report
    :param units_consistency: boolean flag units consistency
    :param modeling_practice: boolean flag modeling practise
    :param internal_consistency: boolean flag internal consistency
    :param log_errors: boolean flag of errors should be logged
    :return: Nall, Nerr, Nwarn (number of all warnings/errors, errors and warnings)
    """
    if name is None:
        filepath = os.path.abspath(filepath)
        if len(filepath) < 100:
            name = filepath
        else:
            name = filepath[0:99] + '...'

    doc = libsbml.readSBML(filepath)
    return check_doc(doc, name=name, log_errors=log_errors,
                     units_consistency=units_consistency,
                     modeling_practice=modeling_practice,
                     internal_consistency=internal_consistency)


def check_doc(doc, name=None, log_errors=True,
              units_consistency=True,
              modeling_practice=True,
              internal_consistency=True):
    """ Checks document and logs errors.

    :param doc: SBMLDocument to check
    :param name: identifier or path for report
    :param log_errors: boolean flag of errors should be logged
    :param units_consistency: boolean flag units consistency
    :param modeling_practice: boolean flag modeling practise
    :param internal_consistency: boolean flag internal consistency
    :return: Nall, Nerr, Nwarn (number of all warnings/errors, errors and warnings)
    """
    if not name:
        name = str(doc)

    # set the unit checking, similar for the other settings
    doc.setConsistencyChecks(libsbml.LIBSBML_CAT_UNITS_CONSISTENCY, units_consistency)
    doc.setConsistencyChecks(libsbml.LIBSBML_CAT_MODELING_PRACTICE, modeling_practice)

    # time
    current = time.clock()

    # all, error, warn
    if internal_consistency:
        Nall_in, Nerr_in, Nwarn_in = _check_consistency(doc, internal_consistency=True)
    else:
        Nall_in, Nerr_in, Nwarn_in = (0, 0, 0)
    Nall_noin, Nerr_noin, Nwarn_noin = _check_consistency(doc, internal_consistency=False)

    # sum up
    Nall = Nall_in + Nall_noin
    Nerr = Nerr_in + Nerr_noin
    Nwarn = Nwarn_in + Nwarn_noin
    valid_status = (Nerr is 0)

    lines = [
        '',
        '-' * 80,
        name,
        "{:<25}: {}".format("valid", str(valid_status).upper()),
    ]
    if Nall > 0:
        lines += [
            "{:<25}: {}".format("validation error(s)", Nerr),
            "{:<25}: {}".format("validation warnings(s)", Nwarn),
        ]
    lines += [
        "{:<25}: {:.3f}".format("check time (s)", time.clock() - current),
        '-' * 80,
        '',
    ]
    info = "\n".join(lines)

    if valid_status:
        info = bcolors.OKGREEN+info+bcolors.ENDC
    else:
        info = bcolors.FAIL + info + bcolors.ENDC
    info = bcolors.BOLD+info+bcolors.ENDC

    # overall validation report
    if Nall > 0:
        if Nerr > 0:
            logging.error(info)
        else:
            logging.warning(info)
    else:
        print(info)

    # individual error and warning report
    if log_errors:
        log_doc_errors(doc)

    return Nall, Nerr, Nwarn


def _check_consistency(doc, internal_consistency=False):
    """ Calculates the type of errors.

    :param doc:
    :param internal_consistency:
    :return:
    """
    Nerr = 0  # error count
    Nwarn = 0  # warning count
    if internal_consistency:
        Nall = doc.checkInternalConsistency()
    else:
        Nall = doc.checkConsistency()

    if Nall > 0:
        for i in range(Nall):
            severity = doc.getError(i).getSeverity()
            if (severity == libsbml.LIBSBML_SEV_ERROR) or (severity == libsbml.LIBSBML_SEV_FATAL):
                Nerr += 1
            else:
                Nwarn += 1

    return Nall, Nerr, Nwarn


def log_doc_errors(doc):
    """ Prints errors of SBMLDocument.

    :param doc:
    :return:
    """
    for k in range(doc.getNumErrors()):
        error = doc.getError(k)
        msg, severity = error_string(error, k)
        if severity == libsbml.LIBSBML_SEV_WARNING:
            logging.warning(msg)
        elif severity in [libsbml.LIBSBML_SEV_ERROR, libsbml.LIBSBML_SEV_FATAL]:
            logging.error(msg)
        else:
            logging.info(msg)


def error_string(error, k=None):
    """ String representation of SBMLError.

    :param error:
    :return:
    """
    package = error.getPackage()
    if package == '':
        package = 'core'

    severity = error.getSeverity()
    lines = [
        bcolors.BGWHITE + bcolors.BLACK + 'E{}: {} ({}, L{}, {})'.format(k, error.getCategoryAsString(), package, error.getLine(), 'code') + bcolors.ENDC + bcolors.ENDC,
        bcolors.FAIL + '[{}] {}'.format(error.getSeverityAsString(), error.getShortMessage()) + bcolors.ENDC,
        bcolors.OKBLUE + error.getMessage() + bcolors.ENDC
    ]
    error_str = '\n'.join(lines)
    return error_str, severity
