# Time Lens for Blender

This simple addon is a quick and easy way to automatically capture your entire current Blender editor window as you work. It will screenshot your Blender window silently in the background and place those screenshots in your desired directory.

## Features
- Easily record a timelapse of your Blender work at a click of a button
- Access through the N-panel of the 3D viewport or through the File menu if you work outside of the 3D viewport (like in the Compositor or the Shading Editor)
- All screenshots are saved to the disk in `*.png` format at no compression for the best image quality
- Change how frequently you want the addon to take snapshots

### File name scheme
The naming scheme for the PNG screenshots is very simple:<br>
`{name-of-blend-file} YYYY-MM-DD at HH.MM.SS ({width x height}).png`

A real file example would look something like this:<br>
`Default Cube 2025-06-18 at 18.19.51 (1256x708).png`

It's possible to remove the image dimensions from the filename inside of the addon's preferences.

## How to install
Download the `TimeLens.zip` from the Releases on this repository and install it in Blender like any other add-on.

## How to use Time Lens in Blender
![User Interface](https://github.com/shinjipons/Time-Lens/blob/main/repo-assets/n-panel.png?raw=true)
Once the add-on is installed, simply click on the "Start Time Lens" button to start immediately taking snapshots of your Blender window. To stop taking screenshots, just click on the "Stop Time Lens" button.

You can choose which directory to save the screenshots on a per `.blend` file basis. If left empty, Time Lens will save the screenshots next to where the `.blend` file is saved.

I recommend to save your Blender file before starting to take screenshots, so that the name of the file is written in the name of the screenshot.

Inside of the addon's user preferences, you can set how frequently you would like Time Lens to take snapshots of your window and if you want to have the image's dimensions included in the filename. **Warning:** you will have to click on "Start Time Lens" button each time you start Blender.

![User Preferences](https://github.com/shinjipons/Time-Lens/blob/main/repo-assets/user-prefs.png?raw=true)

## Small Warning
Taking lossless `.png` screenshots at full size can take quite a lot of space if you leave the addon running for a long time. For example, a screenshot at 1710 x 1069 pixels (a 15" MacBook Air display) can take up to 1.7 MB!

## Tentative Roadmap
If the Blender API allows it and if enough people request it, I might try to add a way so that you don't have to start the addon manually each session.

## How to request features
Time Lens is very much a side project, so requesting features is not guaranteed. However:
- if your request makes sense
- enough people make the same request
- it's not too large of an effort to implement

I will consider it.

## How to log issues
Please use Github Issues to submit issues. Please be as descriptive as possible with:
- your OS and OS version
- your Blender version
- steps to reproduce
- expected behavior
- current behavior
- workaround if any

## Licence

This project is released under **CC0 1.0 Universal**. See [LICENSE](./LICENSE.md) for details.
