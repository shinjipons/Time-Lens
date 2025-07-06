# Time Lens for Blender

This simple addon is a quick and easy way to automatically capture your entire current Blender editor window as you work. It will screenshot your Blender window silently in the background and place those screenshots in your desired directory.

## Features
- Easily record a timelapse of your Blender work at a click of a button
- Access through the N-panel of the 3D viewport or through the File menu if you work outside of the 3D viewport (like in the Compositor or the Shading Editor)
- All screenshots are saved to the disk in `*.png` format at no compression for the best image quality

### File name scheme
The naming scheme for the PNG screenshots is very simple:
`{name-of-blend-file} YYYY-MM-DD at HH.MM.SS ({width x height}).png`

A real file example would look something like this:
`Default Cube 2025-06-18 at 18.19.51 (1256x708).png`

It's possible to remove the image dimensions from the filename inside of the addon's preferences.

## How to install
Download the `TimeLens.zip` from the Releases on this repository and install it in Blender like any other add-on.

## How to use Time Lens in Blender
![User Interface](https://github.com/shinjipons/Time-Lens/blob/main/repo-assets/n-panel.png?raw=true)
Once the add-on is installed, simply click on the "Start Time Lens" button to start immediately taking snapshots of your Blender window. To stop taking screenshots, just click on the "Stop Time Lens" button.

You can choose which directory to save the screenshots on a per `.blend` file basis. If left empty, Time Lens will save the screenshots next to where the `.blend` file is saved.

I recommend to save your Blender file before starting to take screenshots, so that the name of the file is written in the name of the screenshot.

## How to request features
(To be written)

## How to log issues
(To be written)

## Licence
(To be added later, but it will be as permissive as possible)