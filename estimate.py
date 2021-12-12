import numpy as np
import rioxarray as rxr
import earthpy as et

light_data = rxr.open_rasterio("VNL_v2_npp_2020_global_vcmslcfg_c202102150000.median_masked.tif",
                               masked=True)


def linear_interp(x: float, x0: float, x1: float, y0: float, y1: float) -> float:
    m = (y1 - y0) / (x1 - x0)
    return y0 + (x - x0) * m


def interp_lat_lon(lat: float, lon: float) -> tuple:
    c, lat_size, lon_size = light_data.shape
    # NOTE(meawoppl) - there is almost certainly a builtin verion of this
    # that said light_data.interp does not function as expected...
    lat_idx = int(linear_interp(lat, 75, -65, 0, lat_size))
    lon_idx = int(linear_interp(lon, -180, 180, 0, lon_size))

    return light_data[0,  lat_idx, lon_idx].to_numpy()


print(light_data.rio.bounds())

locations = {
    "NYC": (40.730610, -73.935242),
    "Vegas": (36.114647, -115.172813),
    "null island": (0, 0),
    "Riyadh": (24.774265, 46.738586)
}

if __name__ == "__main__":
    # print(light_data.max())
    for name, loc in locations.items():
        print(name, interp_lat_lon(loc[0], loc[1]))

    # Brightest spot
    # a = light_data.as_numpy()
    # indices = np.unravel_index(a.argmax(), a.shape)
    # print(light_data[indices])

    lat = float(input("Latitude:"))
    lon = float(input("Longitude:"))
    print("Score", interp_lat_lon(lat, lon))
