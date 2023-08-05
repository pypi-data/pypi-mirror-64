Limitations
===========

* Strings (except for :py:class:`pyderasn.NumericString` and
  :py:class:`pyderasn.PrintableString`) are not validated
  in any way, except just trying to be decoded in ``ascii``,
  ``iso-8859-1``, ``utf-8/16/32`` correspondingly
* :py:class:`pyderasn.GeneralizedTime` does not support zero year
* No REAL, RELATIVE OID, EXTERNAL, INSTANCE OF, EMBEDDED PDV, CHARACTER STRING
