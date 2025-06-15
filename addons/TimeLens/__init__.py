bl_info = {
    "name": "TimeLens",
    "blender": (2, 80, 0),
    "category": "System",
    "author": "ChatGPT",
    "version": (1, 7),
    "description": "Capture your Blender workspace automatically over time in crisp PNGs via an N-panel tab and File menu using bpy.app.timers."
}

import bpy
import os
import datetime

from bpy.props import StringProperty, IntProperty, BoolProperty
from bpy.types import AddonPreferences, Operator, Panel

# Timer control flag
_timer_active = False


def take_screenshot():
    prefs = bpy.context.preferences.addons[__name__].preferences
    raw_dir = prefs.output_directory
    output_dir = os.path.expanduser(bpy.path.abspath(raw_dir)) if raw_dir else os.path.dirname(bpy.data.filepath)
    if not output_dir:
        return
    os.makedirs(output_dir, exist_ok=True)

    base = os.path.splitext(os.path.basename(bpy.data.filepath))[0]
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%Hh%Mm%Ss")
    name = f"{base}_{timestamp}"
    if prefs.include_dimensions:
        win = bpy.context.window
        dims = f"{win.width}x{win.height}"
        name = f"{name}_{dims}"
    full_path = os.path.join(output_dir, f"{name}.png")
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

    output_directory: StringProperty(
        name="Output Directory",
        description="Directory to save screenshots. Defaults to .blend location",
        subtype='DIR_PATH',
        default=""
    )
    interval_minutes: IntProperty(
        name="Interval (minutes)",
        description="Time between screenshots",
        default=10,
        min=1
    )
    include_dimensions: BoolProperty(
        name="Include Dimensions",
        description="Append window dimensions to filename",
        default=False
    )
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "output_directory")
        layout.prop(self, "interval_minutes")
        layout.prop(self, "include_dimensions")


class TIME_OT_start_screenshot(Operator):
    bl_idname = "timelens.start_screenshot"
    bl_label = "Start Time Lens"
    bl_description = "Begin taking periodic screenshots"

    def execute(self, context):
        global _timer_active
        prefs = context.preferences.addons[__name__].preferences
        if not bpy.data.filepath:
            self.report({'WARNING'}, "Please save the .blend first.")
            return {'CANCELLED'}
        if _timer_active:
            self.report({'WARNING'}, "Time Lens already running.")
            return {'CANCELLED'}
        _timer_active = True
        bpy.app.timers.register(timer_callback)
        self.report({'INFO'}, f"Time Lens started every {prefs.interval_minutes} min.")
        # Force UI refresh
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()
        return {'FINISHED'}


class TIME_OT_stop_screenshot(Operator):
    bl_idname = "timelens.stop_screenshot"
    bl_label = "Stop Time Lens"
    bl_description = "Stop taking periodic screenshots"

    def execute(self, context):
        global _timer_active
        if not _timer_active:
            self.report({'WARNING'}, "Time Lens is not running.")
            return {'CANCELLED'}
        _timer_active = False
        try:
            bpy.app.timers.unregister(timer_callback)
        except Exception:
            pass
        self.report({'INFO'}, "Time Lens stopped.")
        # Force UI refresh
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()
        return {'FINISHED'}


class SCREEN_PT_timelens_panel(Panel):
    bl_label = "TimeLens"
    bl_idname = "SCREEN_PT_timelens_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "TimeLens"

    def draw(self, context):
        layout = self.layout
        running = _timer_active
        col = layout.column(align=True)
        col.enabled = not running
        col.operator(
            "timelens.start_screenshot",
            text="Start Time Lens",
            icon='PLAY',
            depress=not running
        )
        col2 = layout.column(align=True)
        col2.enabled = running
        col2.operator(
            "timelens.stop_screenshot",
            text="Stop Time Lens",
            icon='PAUSE',
            depress=running
        )


def menu_draw(self, context):
    layout = self.layout
    layout.separator()
    layout.operator("timelens.start_screenshot", icon='PLAY')
    layout.operator("timelens.stop_screenshot", icon='PAUSE')


def register():
    bpy.utils.register_class(AutoScreenshotPreferences)
    bpy.utils.register_class(TIME_OT_start_screenshot)
    bpy.utils.register_class(TIME_OT_stop_screenshot)
    bpy.utils.register_class(SCREEN_PT_timelens_panel)
    bpy.types.TOPBAR_MT_file.append(menu_draw)


def unregister():
    global _timer_active
    _timer_active = False
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
