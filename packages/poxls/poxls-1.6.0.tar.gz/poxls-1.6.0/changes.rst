Changelog
=========

1.5.0 - November 10, 2019
-------------------------

- Support both OpenPyxl < 2.5.0b1 and newer versions. Patch from Felix Slager.
- Fix handling of the comment column in xls-to-po. Patch from Jens Mertelmeyer.
- Correct typos in README. Patch from Robin Meier.

1.4.2 - May 11, 2017
-------------------------

- Fix another problem with message context handling in po-to-xls.


1.4.1 - May 11, 2017
-------------------------

- Fix po-to-xls handling of messages with a context.


1.4.0 - December 23, 2016
-------------------------

- Fix compatibility with current OpenPyxl releases.

- Fix Python 3 compatibility.


1.3.0 - July 6, 2015
--------------------

- Fix another ReST syntax error in package description.

- Correcty handle rows with a missing translation.


1.2.0 - June 12, 2015
---------------------

- Fix ReST syntax error in package description.

- Skip rows without a message id.


1.1.0 - 25 March 2015
---------------------

- Use `openpyxl <http://openpyxl.readthedocs.org/>`_ instead of xlrd/xlwt. This
  fixes warnings about cell type conversions when opening generated xlsx files
  in Apple Numbers (and possibly others).


1.0.0 - 15 March 2015
---------------------

- Split po-excel conversion tools out from `lingua <https://github.com/wichert/lingua>`_.

- Simplify CLI interfaces.
