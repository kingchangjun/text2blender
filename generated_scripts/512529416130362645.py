```
import bpy
import mathutils

# Create a new mesh
mesh = bpy.data.meshes.new("TreeMesh")

# Define vertices
verts = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (-1, 0, 0), (0, -1, 0)]
edges = [(0, 1), (2, 3), (4, 0)]

# Create the mesh from vertices and edges
mesh.from_pydata(verts, [], edges)
mesh.update()

# Create a new object
obj = bpy.data.objects.new("Tree", mesh)

# Set the object's location
obj.location = mathutils.Vector((0, 0, 1))

# Add the object into the scene
scene = bpy.context.scene
scene.collection.objects.link(obj)