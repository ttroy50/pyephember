PyEphEmber
========================================

PyEphEmber is a Python module implementing an interface to the [EPH Control Systems Ember API](http://emberapp.ephcontrols.com/).  It allows a user to interact with their EPH heating system for the purposes of monitoring their heating system. This requires you to 
have the EPH Gateway to provide external internet access for your heating system.

[![Build Status](https://travis-ci.org/ttroy50/pyephember.svg?branch=master)](https://travis-ci.org/ttroy50/pyephember)



Example basic usage
-------------------

    >>> from pyephember.pyephember import EphEmber
    >>> e = EphEmber('my@username.com', 'mypassword')
    >>> e.getZoneTemperature("MyZone")

API
---

The API is a basic HTTPS API returning data in JSON format. For more details see [here](API.md)

Disclaimer: I have no connection with EPH Controls so cannot guarentee that these API calls will always be valid.
