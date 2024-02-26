bl_info = {
    "name": "Rigify Mesh Retargetter",
    "blender": (2, 80, 0),
    "category": "Object",
    "description": "Retargets Meshes attached to meta rigs to their rigify rig counterparts. You need to run Rigify's 'Generate Rig' first.",
    "author": "Cubedparadox",
    "version": (1, 0),
    "location": "Properties > Object Data"
}

import bpy


def get_or_create_collection(collection_name, view_layer, hide=False):
    """Create or get a collection and optionally hide it in the viewport."""
    if collection_name not in bpy.data.collections:
        new_collection = bpy.data.collections.new(collection_name)
        bpy.context.scene.collection.children.link(new_collection)
    else:
        new_collection = bpy.data.collections[collection_name]
    
    layer_collection = view_layer.layer_collection.children.get(collection_name)
    if layer_collection is not None:
        layer_collection.hide_viewport = hide
    
    return new_collection

def update_armature_modifier(obj, old_armature_name, new_armature_name):
    for modifier in obj.modifiers:
        if modifier.type == 'ARMATURE' and modifier.object and modifier.object.name == old_armature_name:
            new_armature = bpy.data.objects.get(new_armature_name)
            if new_armature:
                modifier.object = new_armature

def delete_existing_copy(obj_name, collection):
    if obj_name in collection.objects:
        bpy.data.objects.remove(collection.objects[obj_name], do_unlink=True)

def move_armature_to_collection(armature_name, target_collection):
    armature = bpy.data.objects.get(armature_name)
    if armature:
        # Check if armature is already in the target collection
        if armature.name not in target_collection.objects:
            # Unlink from all current collections
            for col in armature.users_collection:
                col.objects.unlink(armature)
            # Link to the target collection
            target_collection.objects.link(armature)

def process_armature_and_children(armature, view_layer):
    original_rig_collection_name = f"ORIGINAL-{armature.name}"
    ik_rig_collection_name = f"IK-{armature.name}"
    
    original_rig_collection = get_or_create_collection(original_rig_collection_name, view_layer, hide=True)
    ik_rig_collection = get_or_create_collection(ik_rig_collection_name, view_layer)
    
    for child in armature.children:
        if child.type == 'MESH':
            new_name = f"IK-{child.name}"
            delete_existing_copy(new_name, ik_rig_collection)
            
            new_mesh = child.copy()
            new_mesh.data = child.data.copy()
            new_mesh.animation_data_clear()
            new_mesh.name = new_name
            
            for vg in new_mesh.vertex_groups:
                vg.name = f"DEF-{vg.name}"
            
            ik_rig_collection.objects.link(new_mesh)
            
            if child.parent.name == armature.name:
                new_parent_name = f"RIG-{armature.name}"
                new_parent = bpy.data.objects.get(new_parent_name)
                if new_parent:
                    new_mesh.parent = new_parent
                    new_mesh.matrix_parent_inverse = new_parent.matrix_world.inverted()

            update_armature_modifier(new_mesh, armature.name, new_parent_name)
            
            for col in child.users_collection:
                col.objects.unlink(child)
                
            original_rig_collection.objects.link(child)

    # Move the RIG-armature object to the IK collection
    rig_armature_name = f"RIG-{armature.name}"
    move_armature_to_collection(rig_armature_name, ik_rig_collection)

    # Move the original armature to the ORIGINAL collection
    for col in armature.users_collection:
        col.objects.unlink(armature)
    original_rig_collection.objects.link(armature)

    print("Process completed.")

class RetargetMeshesOperator(bpy.types.Operator):
    """Retargets Meshes attached to meta rigs to their rigify rig counterparts. You need to run Rigify's 'Generate Rig' first"""
    bl_idname = "object.retarget_meshes"
    bl_label = "Retarget Meshes from Metarig"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        armature = context.object
        if armature and armature.type == 'ARMATURE':
            process_armature_and_children(armature, context.view_layer)
            self.report({'INFO'}, "Meshes retargeted successfully.")
        else:
            self.report({'ERROR'}, "Please select an armature.")
        return {'FINISHED'}

def draw_retarget_meshes_button(self, context):
    self.layout.operator(RetargetMeshesOperator.bl_idname)

def register():
    bpy.utils.register_class(RetargetMeshesOperator)
    # Append the draw method to the Rigify panel
    bpy.types.DATA_PT_rigify.append(draw_retarget_meshes_button)

def unregister():
    bpy.utils.unregister_class(RetargetMeshesOperator)
    # Remove the draw method from the Rigify panel
    bpy.types.DATA_PT_rigify.remove(draw_retarget_meshes_button)

if __name__ == "__main__":
    register()
