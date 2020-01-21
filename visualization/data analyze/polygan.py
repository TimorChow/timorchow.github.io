import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
import matplotlib as mpl
import mplleaflet
#coordinates
#p1 43.724273, -79.439645
#p2 43.718720, -79.436757
#p3 43.719388, -79.433503
#p4 43.724543, -79.432646
# Generate data. In this case, we'll make a bunch of center-points and generate
# verticies by subtracting random offsets from those center-points
numpoly, numverts = 1, 3
centers = 100 * (np.random.random((1,2)) - 0.5)
print(centers)
offsets = 10 * (np.random.random((numverts,numpoly,2)) - 0.5)
print("offsets",offsets.shape)
verts = centers + offsets
print("verts1",verts.shape)

verts = np.swapaxes(verts, 0, 1)

poly_in_map = [[[ -79.439645,43.724273],[ -79.436757,43.718720,],[-79.433503,43.719388],[-79.432646,43.724543]]]
#poly_in_map = np.swapaxes(poly_in_map,0,1)

poly_in_map = np.asarray(poly_in_map)
poly_in_map = np.reshape(poly_in_map,(1,4,2))
ply = [[[-45.63685129, -79.07310697],[-41.95639862 ,-79.75092634],[-38.60766527, -79.53043112]]]
ply=np.asarray(ply)
print(ply.shape)
ply=ply.reshape(1,3,2)
print(poly_in_map)
print("final_v",verts)

# In your case, "verts" might be something like:
# verts = zip(zip(lon1, lat1), zip(lon2, lat2), ...)
# If "data" in your case is a numpy array, there are cleaner ways to reorder
# things to suit.

# Color scalar...
# If you have rgb values in your "colorval" array, you could just pass them
# in as "facecolors=colorval" when you create the PolyCollection
z = np.random.random(numpoly) * 500
print(z)
fig, ax = plt.subplots()

# Make the collection and add it to the plot.
coll = PolyCollection(poly_in_map)
ax.add_collection(coll)


# Add a colorbar for the PolyCollection
#fig.colorbar(coll, ax=ax)
#plt.show()
mplleaflet.show(tiles='cartodb_positron', path='pot_holes.html')
