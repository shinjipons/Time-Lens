bl_info = {
    "name": "TimeLens",
    "blender": (2, 80, 0),
    "category": "System",
    "author": "ChatGPT",
    "version": (1, 3),
    "description": "Capture your Blender workspace automatically over time in crisp PNGs via an N-panel tab using bpy.app.timers for reliability."
}

import bpy
import os
import datetime

from bpy.props import StringProperty, IntProperty
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
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    full_path = os.path.join(output_dir, f"{base}_{timestamp}.png")
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
        description="Directory to save screenshots. Defaults to the current .blend file directory",
        subtype='DIR_PATH',
        default=""
    )

    interval_minutes: IntProperty(
        name="Interval (minutes)",
        description="Time between screenshots",
        default=10,
        min=1
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "output_directory")
        layout.prop(self, "interval_minutes")


class SCREEN_OT_start_screenshot(Operator):
    bl_idname = "timelens.start_screenshot"
    bl_label = "Start Auto Screenshot"
    bl_description = "Begin taking periodic screenshots"

    def execute(self, context):
        global _timer_active
        if not bpy.data.filepath:
            self.report({'WARNING'}, "Please save the .blend file first.")
            return {'CANCELLED'}
        if _timer_active:
            self.report({'WARNING'}, "TimeLens is already running.")
            return {'CANCELLED'}
        _timer_active = True
        bpy.app.timers.register(timer_callback)
        prefs = context.preferences.addons[__name__].preferences
        self.report({'INFO'}, f"TimeLens started. Interval: {prefs.interval_minutes} min")
        return {'FINISHED'}


class SCREEN_OT_stop_screenshot(Operator):
    bl_idname = "timelens.stop_screenshot"
    bl_label = "Stop Auto Screenshot"
    bl_description = "Stop taking periodic screenshots"

    def execute(self, context):
        global _timer_active
        if not _timer_active:
            self.report({'WARNING'}, "TimeLens is not running.")
            return {'CANCELLED'}
        _timer_active = False
        try:
            bpy.app.timers.unregister(timer_callback)
        except Exception:
            pass
        self.report({'INFO'}, "TimeLens stopped.")
        return {'FINISHED'}


class SCREEN_PT_timelens_panel(Panel):
    bl_label = "TimeLens"
    bl_idname = "SCREEN_PT_timelens_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "TimeLens"

    def draw(self, context):
        layout = self.layout
        layout.operator(SCREEN_OT_start_screenshot.bl_idname, icon='PLAY')
        layout.operator(SCREEN_OT_stop_screenshot.bl_idname, icon='PAUSE')


def register():
    bpy.utils.register_class(AutoScreenshotPreferences)
    bpy.utils.register_class(SCREEN_OT_start_screenshot)
    bpy.utils.register_class(SCREEN_OT_stop_screenshot)
    bpy.utils.register_class(SCREEN_PT_timelens_panel)


def unregister():
    global _timer_active
    # ensure any running timer is stopped before unload
    _timer_active = False
    try:
        bpy.app.timers.unregister(timer_callback)
    except Exception:
        pass
    bpy.utils.unregister_class(SCREEN_PT_timelens_panel)
    bpy.utils.unregister_class(SCREEN_OT_stop_screenshot)
    bpy.utils.unregister_class(SCREEN_OT_start_screenshot)
    bpy.utils.unregister_class(AutoScreenshotPreferences)


if __name__ == "__main__":
    register()
