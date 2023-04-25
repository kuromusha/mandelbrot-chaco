Mandelbrot Plotting with Panning and Zooming in TraitsUI and Chaco
------------------------------------------------------------------
This is demonstrating the use of panning and zooming a mandelbrot figure in Enthought's
TraitsUI and Chaco.

Setup
=====
- Download [EDM](https://www.enthought.com/edm/)
- Install the requirements and run:

```
$ edm envs import -f requirements.txt mandelbrot-chaco
$ edm shell -e mandelbrot-chaco
$ python setup.py build_ext --inplace
$ python mandelbrot_chaco.py
```

How to Pan and Zoom the Plot
============================

- To pan the plot, click on it with left mouse button and drag it.
- To zoom the plot,
  - use the scroll wheel of the mouse to zoom into the center of it, 
  - or press "z" on the keyboard, then click on it with the left
    mouse button and drag to select a region to zoom into,
  - or press shift + up/down/left/right keys.
