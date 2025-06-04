bl_info = {
    "name": "Auto Screenshot Taker",
    "blender": (2, 80, 0),
    "category": "System",
    "author": "ChatGPT",
    "version": (1, 0),
    "description": "Periodically takes PNG screenshots without alpha and with 0% compression."
}

import bpy
import os
import datetime
import threading

from bpy.props import StringProperty, IntProperty
from bpy.types import AddonPreferences, Operator


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


class SCREEN_OT_auto_screenshot(Operator):
    bl_idname = "screen.auto_screenshot"
    bl_label = "Start Auto Screenshot"
    bl_description = "Starts taking screenshots periodically"
    _timer = None

    def modal(self, context, event):
        if event.type == 'TIMER':
            self.take_screenshot(context)
        return {'PASS_THROUGH'}

    def execute(self, context):
        wm = context.window_manager
        self._timer = wm.event_timer_add(
            bpy.context.preferences.addons[__name__].preferences.interval_minutes * 60,
            window=context.window
        )
        wm.modal_handler_add(self)
        self.report({'INFO'}, "Auto Screenshot Started")
        return {'RUNNING_MODAL'}

    def take_screenshot(self, context):
        prefs = bpy.context.preferences.addons[__name__].preferences

        # Get the output directory
        if prefs.output_directory:
            output_dir = bpy.path.abspath(prefs.output_directory)
        else:
            output_dir = os.path.dirname(bpy.data.filepath)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        base_filename = os.path.splitext(os.path.basename(bpy.data.filepath))[0]
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        full_path = os.path.join(output_dir, f"{base_filename}_{timestamp}.png")

        # Set screenshot settings
        bpy.context.preferences.filepaths.image_format = 'PNG'
        bpy.context.preferences.filepaths.save_png_compression = 0
        bpy.context.preferences.filepaths.save_png_color_mode = 'RGB'

        bpy.ops.screen.screenshot(filepath=full_path, full=True)
        print(f"Screenshot saved to: {full_path}")

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)
        self.report({'INFO'}, "Auto Screenshot Stopped")
        return {'CANCELLED'}


def menu_func(self, context):
    self.layout.operator(SCREEN_OT_auto_screenshot.bl_idname)


def register():
    bpy.utils.register_class(AutoScreenshotPreferences)
    bpy.utils.register_class(SCREEN_OT_auto_screenshot)
    bpy.types.TOPBAR_MT_file.append(menu_func)


def unregister():
    bpy.utils.unregister_class(AutoScreenshotPreferences)
    bpy.utils.unregister_class(SCREEN_OT_auto_screenshot)
    bpy.types.TOPBAR_MT_file.remove(menu_func)


if __name__ == "__main__":
    register()
