#####################
  Examples
#####################

.. toctree::
  :glob:
  :hidden:

Serialization
=============

It is as easy as

>>> array.save('test.dat')

and

>>> array = eadf.EADF.load('test.dat')

in order to dump your EADF object to disk and restore it 
completely with all the preprocessing already in place. One
can even do some heavy preprocessing on a cluster, copy the
serialized object to the local disk and do the fun calculations
there.

Visualizing a Synthetic Array
=============================

Generate a Stacked UCA

Loading from DFT Coeffcients
============================

Load from Fourier Data
