bl_info = {
    "name": "Time Lens",
    "blender": (2, 80, 0),
    "category": "System",
    "author": "Shinji Pons",
    "version": (0, 1),
    "description": "Capture your Blender workspace automatically via an N-panel tab and File menu"
}

import bpy
import os
import datetime

from bpy.props import StringProperty, IntProperty, BoolProperty
from bpy.types import AddonPreferences, Operator, Panel

# Timer control flag and fixed output directory
_timer_active = False



def take_screenshot():
    """Take a screenshot immediately, using only window/screen override for context."""
    
    # Determine output directory dynamically
    prefs = bpy.context.preferences.addons[__name__].preferences
    raw = prefs.output_directory
    if raw:
        output_dir = os.path.expanduser(bpy.path.abspath(raw))
    else:
        blend_path = bpy.data.filepath
        if not blend_path:
            return
        output_dir = os.path.dirname(blend_path)
    os.makedirs(output_dir, exist_ok=True)

    # Build filename
    base = os.path.splitext(os.path.basename(bpy.data.filepath))[0]
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H.%M.%S")
    name = f"{base} {date_str} at {time_str}"

    prefs = bpy.context.preferences.addons[__name__].preferences
    if prefs.include_dimensions:
        win = bpy.context.window
        dims = f"{win.width}x{win.height}"
        name = f"{name} ({dims})"

    full_path = os.path.join(output_dir, f"{name}.png")

        # Ensure PNG, 8-bit RGB, 0% compression using render settings
    scene = bpy.context.scene
    img_set = scene.render.image_settings
    img_set.file_format = 'PNG'
    img_set.color_mode = 'RGB'
    img_set.color_depth = '8'
    img_set.compression = 0
    # Context override: use only window and screen
    for window in bpy.context.window_manager.windows:
        override = {'window': window, 'screen': window.screen}
        try:
            bpy.ops.screen.screenshot(override, filepath=full_path)
            return
        except Exception:
            continue
    # Fallback
    try:
        bpy.ops.screen.screenshot(filepath=full_path)
    except Exception as e:
        print(f"TimeLens: screenshot failed - {e}")


def timer_callback():
    global _timer_active
    if not _timer_active:
        return None
    take_screenshot()
    prefs = bpy.context.preferences.addons[__name__].preferences
    return prefs.interval_minutes * 60


class AutoScreenshotPreferences(AddonPreferences):
    bl_idname = __name__

    interval_minutes: IntProperty(
        name="Interval (minutes)",
        description="Time between screenshots (max 10 minutes)",
        default=10,
        min=1,
        max=10
    )
    include_dimensions: BoolProperty(
        name="Include Dimensions",
        description="Append window dimensions to filename",
        default=False
    )
    output_directory: StringProperty(
        name="Output Directory",
        description="Directory to save screenshots. Defaults to .blend location",
        subtype='DIR_PATH',
        default=""
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "interval_minutes")
        layout.prop(self, "include_dimensions")


class TIME_OT_start_screenshot(Operator):
    bl_idname = "timelens.start_screenshot"
    bl_label = "Start Time Lens"
    bl_description = "Begin taking periodic screenshots"

    def execute(self, context):
        global _timer_active
        prefs = context.preferences.addons[__name__].preferences
        # Validate directory at start
        prefs = context.preferences.addons[__name__].preferences
        raw = prefs.output_directory
        if raw:
            pass
        else:
            blend_path = bpy.data.filepath
            if not blend_path:
                self.report({'WARNING'}, "Please save the .blend first.")
                return {'CANCELLED'}
        if _timer_active:
            self.report({'WARNING'}, "Time Lens already running.")
            return {'CANCELLED'}
        # Immediate screenshot
        take_screenshot()
        _timer_active = True
        bpy.app.timers.register(timer_callback)
        self.report({'INFO'}, f"Time Lens started. Next in {prefs.interval_minutes} min.")
        # Refresh UI
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()
        return {'FINISHED'}


class TIME_OT_stop_screenshot(Operator):
    bl_idname = "timelens.stop_screenshot"
    bl_label = "Stop Time Lens"
    bl_description = "Stop taking periodic screenshots"

    def execute(self, context):
        global _timer_active, _output_dir
        if not _timer_active:
            self.report({'WARNING'}, "Time Lens is not running.")
            return {'CANCELLED'}
        _timer_active = False
        _output_dir = None
        try:
            bpy.app.timers.unregister(timer_callback)
        except Exception:
            pass
        self.report({'INFO'}, "Time Lens stopped.")
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()
        return {'FINISHED'}


class SCREEN_PT_timelens_panel(Panel):
    bl_label = "Time Lens"
    bl_idname = "SCREEN_PT_timelens_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Time Lens"

    def draw(self, context):
        layout = self.layout
        prefs = context.preferences.addons[__name__].preferences
        running = _timer_active
        col = layout.column(align=True)
        col.enabled = not running
        col.operator("timelens.start_screenshot", text="Start Time Lens", icon='PLAY')
        col2 = layout.column(align=True)
        col2.enabled = running
        col2.operator("timelens.stop_screenshot", text="Stop Time Lens", icon='CANCEL')
        layout.separator()
        layout.prop(prefs, "output_directory", text="Output Directory")


def menu_draw(self, context):
    layout = self.layout
    layout.separator()
    layout.operator("timelens.start_screenshot", icon='PLAY')
    layout.operator("timelens.stop_screenshot", icon='CANCEL')


def register():
    bpy.utils.register_class(AutoScreenshotPreferences)
    bpy.utils.register_class(TIME_OT_start_screenshot)
    bpy.utils.register_class(TIME_OT_stop_screenshot)
    bpy.utils.register_class(SCREEN_PT_timelens_panel)
    bpy.types.TOPBAR_MT_file.append(menu_draw)


def unregister():
    global _timer_active, _output_dir
    _timer_active = False
    _output_dir = None
    try:
        bpy.app.timers.unregister(timer_callback)
    except Exception:
        pass
    bpy.types.TOPBAR_MT_file.remove(menu_draw)
    bpy.utils.unregister_class(SCREEN_PT_timelens_panel)
    bpy.utils.unregister_class(TIME_OT_stop_screenshot)
    bpy.utils.unregister_class(TIME_OT_start_screenshot)
    bpy.utils.unregister_class(AutoScreenshotPreferences)


if __name__ == "__main__":
    register()
