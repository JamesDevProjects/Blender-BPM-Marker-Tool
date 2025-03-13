bl_info = {
    "name": "BPM Timeline Marker Generator",
    "blender": (2, 80, 0),
    "category": "Animation",
    "author": "Your Name",
    "version": (1, 0),
    "location": "View3D > Sidebar > BPM Markers",
    "description": "Adds timeline markers based on BPM",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "support": "COMMUNITY",
}

import bpy

# Operator to add BPM markers
class ADD_BPM_MARKERS_OT_AddMarkers(bpy.types.Operator):
    bl_idname = "bpm_markers.add_markers"
    bl_label = "Generate BPM Markers"
    bl_description = "Creates timeline markers based on BPM"
    
    def execute(self, context):
        scene = context.scene
        bpm = scene.bpm_marker_settings.bpm
        fps = scene.bpm_marker_settings.fps
        beats = scene.bpm_marker_settings.beats
        
        # Calculate frames per beat
        frames_per_beat = fps / (bpm / 60)

        # Remove existing markers
        for marker in scene.timeline_markers:
            scene.timeline_markers.remove(marker)

        # Add new BPM markers
        for i in range(beats):
            frame = int(i * frames_per_beat)
            marker = scene.timeline_markers.new(name=f"Beat {i+1}", frame=frame)
        
        self.report({'INFO'}, f"Added {beats} BPM markers at {bpm} BPM")
        return {'FINISHED'}

# Panel for UI in Sidebar
class ADD_BPM_MARKERS_PT_Panel(bpy.types.Panel):
    bl_label = "BPM Markers"
    bl_idname = "ADD_BPM_MARKERS_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BPM Markers"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        settings = scene.bpm_marker_settings
        
        layout.prop(settings, "bpm")
        layout.prop(settings, "fps")
        layout.prop(settings, "beats")
        layout.operator("bpm_markers.add_markers")

# Property group for settings
class BPMMarkerSettings(bpy.types.PropertyGroup):
    bpm: bpy.props.IntProperty(name="BPM", default=128, min=1, max=300)
    fps: bpy.props.IntProperty(name="FPS", default=30, min=1, max=240)
    beats: bpy.props.IntProperty(name="Beats", default=32, min=1, max=512)

# Register and unregister functions
def register():
    bpy.utils.register_class(BPMMarkerSettings)
    bpy.types.Scene.bpm_marker_settings = bpy.props.PointerProperty(type=BPMMarkerSettings)
    
    bpy.utils.register_class(ADD_BPM_MARKERS_OT_AddMarkers)
    bpy.utils.register_class(ADD_BPM_MARKERS_PT_Panel)

def unregister():
    bpy.utils.unregister_class(BPMMarkerSettings)
    del bpy.types.Scene.bpm_marker_settings
    
    bpy.utils.unregister_class(ADD_BPM_MARKERS_OT_AddMarkers)
    bpy.utils.unregister_class(ADD_BPM_MARKERS_PT_Panel)

if __name__ == "__main__":
    register()
