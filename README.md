PyEphEmber
========================================

PyEphEmber is a Python module implementing an interface to the [EPH Control Systems Ember API](http://emberapp.ephcontrols.com/).  It allows a user to interact with their EPH heating system for the purposes of monitoring their heating system. This requires you to have the EPH Gateway to provide external internet access for your heating system.


Example basic usage
-------------------

    >>> from pyephember.pyephember import EphEmber
    >>> e = EphEmber('my@username.com', 'mypassword')
    >>> e.getZoneTemperature("MyZone")
