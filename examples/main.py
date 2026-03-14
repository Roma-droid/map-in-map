import cartopy.crs as ccrs
import matplotlib.pyplot as plt

#ax = plt.axes(projection=ccrs.PlateCarree())
ax = plt.axes(projection=ccrs.Mollweide())
ax.coastlines()

plt.savefig("map.png")