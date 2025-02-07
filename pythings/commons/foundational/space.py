from pythings.__base__ import BaseEntity, Entity, BaseAttribute, BaseAbstractEntity, BasePhysicalEntity, \
    BaseRelationship

import numpy as np
from shapely.geometry import Point as ShapelyPoint, Polygon
from shapely.affinity import translate as shapely_translate, rotate as shapely_rotate, scale as shapely_scale
from shapely.validation import explain_validity

# Optional libraries for spatial indexing and GIS integration
try:
    from rtree import index as rtree_index
except ImportError:
    rtree_index = None

try:
    import geopandas as gpd
except ImportError:
    gpd = None


class SpatialEntity:
    """
    Base class for all spatial entities.

    Attributes:
      - dimension: The spatial dimension (2 or 3).

    Subclasses must implement a bounding_box() method.
    """

    def __init__(self, dimension=2):
        self.dimension = dimension

    def bounding_box(self):
        """
        Returns a bounding box.
        For 2D: (minx, miny, maxx, maxy)
        For 3D: (minx, miny, minz, maxx, maxy, maxz)
        """
        raise NotImplementedError("Subclasses should implement bounding_box() method.")


class Point(SpatialEntity):
    """
    Represents a point in 2D or 3D space.

    For 2D points, we leverage Shapely for robust geometric operations.
    For 3D points, we store coordinates in a tuple and use NumPy for distance and transformation computations.
    """

    def __init__(self, x, y, z=None):
        if z is None:
            super().__init__(dimension=2)
            self.coords = (x, y)
            self.geometry = ShapelyPoint(x, y)
        else:
            super().__init__(dimension=3)
            self.coords = (x, y, z)
            # Shapely has limited 3D support (it stores z but ignores it in operations)
            self.geometry = None  # We rely on our own 3D computations.

    def distance(self, other):
        """
        Computes the Euclidean distance to another Point.
        """
        if not isinstance(other, Point):
            raise ValueError("Distance can only be computed between Point instances.")
        if self.dimension == 2 and other.dimension == 2:
            return self.geometry.distance(other.geometry)
        elif self.dimension == 3 and other.dimension == 3:
            return np.linalg.norm(np.array(self.coords) - np.array(other.coords))
        else:
            raise ValueError("Cannot compute distance between points of different dimensions.")

    def translate(self, dx=0, dy=0, dz=0):
        """
        Returns a new Point translated by the specified offsets.
        """
        if self.dimension == 2:
            new_geom = shapely_translate(self.geometry, xoff=dx, yoff=dy)
            return Point(new_geom.x, new_geom.y)
        elif self.dimension == 3:
            new_coords = (self.coords[0] + dx, self.coords[1] + dy, self.coords[2] + dz)
            return Point(*new_coords)

    def __repr__(self):
        if self.dimension == 2:
            return f"Point({self.coords[0]}, {self.coords[1]})"
        else:
            return f"Point({self.coords[0]}, {self.coords[1]}, {self.coords[2]})"

    def bounding_box(self):
        """
        Returns the bounding box for a point (degenerate).
        """
        if self.dimension == 2:
            x, y = self.coords
            return (x, y, x, y)
        else:
            x, y, z = self.coords
            return (x, y, z, x, y, z)


class SpatialRegion(SpatialEntity):
    """
    Represents a 2D spatial region defined by a polygon.

    Provides rich spatial relations (contains, overlaps, adjacent, disjoint, intersects)
    and transformation methods (translate, rotate, scale).
    Also integrates with GeoPandas for GIS data conversion.
    """

    def __init__(self, vertices):
        """
        Parameters:
          - vertices: list of tuples [(x, y), ...] defining the polygon's boundary.
        """
        super().__init__(dimension=2)
        if len(vertices) < 3:
            raise ValueError("A region must be defined by at least three vertices.")
        self.vertices = vertices
        self.geometry = Polygon(vertices)
        if not self.geometry.is_valid:
            raise ValueError(f"Invalid polygon: {explain_validity(self.geometry)}")

    def contains(self, entity):
        """
        Returns True if this region entirely contains the given spatial entity.
        """
        if hasattr(entity, 'geometry') and entity.geometry is not None:
            return self.geometry.contains(entity.geometry)
        raise ValueError("Entity does not have valid geometry.")

    def overlaps(self, other):
        """
        Returns True if this region overlaps with another SpatialRegion.
        """
        if isinstance(other, SpatialRegion):
            return self.geometry.overlaps(other.geometry)
        raise ValueError("overlaps() requires another SpatialRegion instance.")

    def adjacent_to(self, other):
        """
        Returns True if this region is adjacent (touches but does not intersect interiors) to another region.
        """
        if isinstance(other, SpatialRegion):
            return self.geometry.touches(other.geometry)
        raise ValueError("adjacent_to() requires another SpatialRegion instance.")

    def disjoint(self, other):
        """
        Returns True if this region is completely disjoint from another region.
        """
        if isinstance(other, SpatialRegion):
            return self.geometry.disjoint(other.geometry)
        raise ValueError("disjoint() requires another SpatialRegion instance.")

    def intersects(self, other):
        """
        Returns True if this region intersects with another region.
        """
        if isinstance(other, SpatialRegion):
            return self.geometry.intersects(other.geometry)
        raise ValueError("intersects() requires another SpatialRegion instance.")

    def distance(self, entity):
        """
        Returns the minimum distance to another spatial entity.
        """
        if hasattr(entity, 'geometry') and entity.geometry is not None:
            return self.geometry.distance(entity.geometry)
        raise ValueError("Entity does not have valid geometry.")

    def translate(self, xoff=0, yoff=0):
        """
        Returns a new SpatialRegion translated by the specified offsets.
        """
        new_geom = shapely_translate(self.geometry, xoff=xoff, yoff=yoff)
        return SpatialRegion(list(new_geom.exterior.coords))

    def rotate(self, angle, origin='center'):
        """
        Returns a new SpatialRegion rotated by 'angle' degrees.
        The origin of rotation can be 'center' or a specific (x, y) tuple.
        """
        new_geom = shapely_rotate(self.geometry, angle, origin=origin)
        return SpatialRegion(list(new_geom.exterior.coords))

    def scale(self, xfact=1, yfact=1, origin='center'):
        """
        Returns a new SpatialRegion scaled by xfact and yfact factors.
        """
        new_geom = shapely_scale(self.geometry, xfact=xfact, yfact=yfact, origin=origin)
        return SpatialRegion(list(new_geom.exterior.coords))

    def bounding_box(self):
        """
        Returns the 2D bounding box as (minx, miny, maxx, maxy).
        """
        return self.geometry.bounds

    def to_geodataframe(self, crs="EPSG:4326"):
        """
        Converts this region to a GeoDataFrame (requires geopandas).
        """
        if gpd is None:
            raise ImportError("geopandas is not installed.")
        return gpd.GeoDataFrame([{'geometry': self.geometry}], crs=crs)

    @classmethod
    def from_geodataframe(cls, gdf):
        """
        Creates a list of SpatialRegion instances from a GeoDataFrame containing polygon geometries.
        """
        regions = []
        for geom in gdf.geometry:
            if geom.geom_type == 'Polygon':
                regions.append(cls(list(geom.exterior.coords)))
            else:
                raise ValueError("Unsupported geometry type in GeoDataFrame.")
        return regions

    def __repr__(self):
        return f"SpatialRegion(vertices={self.vertices})"


class SpatialVolume(SpatialEntity):
    """
    Represents a simple 3D spatial region as an axis-aligned bounding box (AABB).

    Note: This is a simplified 3D representation. For full 3D polyhedral operations,
    consider integrating with a dedicated 3D geometry library.
    """

    def __init__(self, minx, miny, minz, maxx, maxy, maxz):
        super().__init__(dimension=3)
        if minx > maxx or miny > maxy or minz > maxz:
            raise ValueError("Invalid bounding box coordinates.")
        self.minx, self.miny, self.minz = minx, miny, minz
        self.maxx, self.maxy, self.maxz = maxx, maxy, maxz

    def contains(self, point):
        """
        Returns True if the volume contains the given 3D Point.
        """
        if not isinstance(point, Point) or point.dimension != 3:
            raise ValueError("Argument must be a 3D Point.")
        x, y, z = point.coords
        return (self.minx <= x <= self.maxx and
                self.miny <= y <= self.maxy and
                self.minz <= z <= self.maxz)

    def distance(self, point):
        """
        Computes the Euclidean distance from a 3D point to the volume.
        Returns 0 if the point lies inside the volume.
        """
        if not isinstance(point, Point) or point.dimension != 3:
            raise ValueError("Argument must be a 3D Point.")
        x, y, z = point.coords
        dx = max(self.minx - x, 0, x - self.maxx)
        dy = max(self.miny - y, 0, y - self.maxy)
        dz = max(self.minz - z, 0, z - self.maxz)
        return np.sqrt(dx * dx + dy * dy + dz * dz)

    def translate(self, dx=0, dy=0, dz=0):
        """
        Returns a new SpatialVolume translated by the specified offsets.
        """
        return SpatialVolume(
            self.minx + dx, self.miny + dy, self.minz + dz,
            self.maxx + dx, self.maxy + dy, self.maxz + dz
        )

    def scale(self, factor):
        """
        Scales the volume about its center by the given factor.
        """
        center_x = (self.minx + self.maxx) / 2
        center_y = (self.miny + self.maxy) / 2
        center_z = (self.minz + self.maxz) / 2
        half_x = (self.maxx - self.minx) * factor / 2
        half_y = (self.maxy - self.miny) * factor / 2
        half_z = (self.maxz - self.minz) * factor / 2
        return SpatialVolume(
            center_x - half_x, center_y - half_y, center_z - half_z,
            center_x + half_x, center_y + half_y, center_z + half_z
        )

    def bounding_box(self):
        """
        Returns the 3D bounding box as (minx, miny, minz, maxx, maxy, maxz).
        """
        return (self.minx, self.miny, self.minz, self.maxx, self.maxy, self.maxz)

    def __repr__(self):
        return (f"SpatialVolume(min=({self.minx}, {self.miny}, {self.minz}), "
                f"max=({self.maxx}, {self.maxy}, {self.maxz}))")


class SpatialIndex:
    """
    A spatial index built on top of Rtree for efficient querying of spatial entities.

    Entities added must implement a bounding_box() method.
    """

    def __init__(self, dimension=2):
        if rtree_index is None:
            raise ImportError("rtree is not installed. Install it to use SpatialIndex.")
        self.dimension = dimension
        p = rtree_index.Property()
        p.dimension = dimension  # Parameterize by dimension if needed.
        self.index = rtree_index.Index(properties=p)
        self.entities = {}

    def add(self, entity, entity_id):
        """
        Adds an entity to the spatial index.
        """
        bbox = entity.bounding_box()
        self.index.insert(entity_id, bbox)
        self.entities[entity_id] = entity

    def query(self, bbox):
        """
        Queries the index for entities intersecting the given bounding box.

        For 2D, bbox is (minx, miny, maxx, maxy).
        Returns a list of entities.
        """
        ids = list(self.index.intersection(bbox))
        return [self.entities[i] for i in ids]

    def __repr__(self):
        return f"SpatialIndex(num_entities={len(self.entities)})"


# =========================================
# Example usage demonstrating all enhancements
# =========================================
if __name__ == "__main__":
    # ---- 2D Examples ----
    # Create two 2D Points.
    p1 = Point(1, 1)
    p2 = Point(4, 5)
    print("2D Points:", p1, p2)
    print("Distance between p1 and p2:", p1.distance(p2))

    # Create a 2D SpatialRegion (a square).
    region = SpatialRegion(vertices=[(0, 0), (5, 0), (5, 5), (0, 5)])
    print("SpatialRegion:", region)
    print("Does region contain p1?", region.contains(p1))
    print("Distance from region to p2:", region.distance(p2))

    # Spatial transformations.
    translated_region = region.translate(xoff=2, yoff=2)
    rotated_region = region.rotate(angle=45)
    scaled_region = region.scale(xfact=2, yfact=2)
    print("Translated Region:", translated_region)
    print("Rotated Region:", rotated_region)
    print("Scaled Region:", scaled_region)

    # Convert the region to a GeoDataFrame if geopandas is available.
    if gpd is not None:
        gdf = region.to_geodataframe()
        print("GeoDataFrame from SpatialRegion:")
        print(gdf)

    # ---- 3D Examples ----
    # Create two 3D Points.
    p3 = Point(1, 1, 1)
    p4 = Point(4, 5, 6)
    print("3D Points:", p3, p4)
    print("3D Distance between p3 and p4:", p3.distance(p4))

    # Create a SpatialVolume representing an axis-aligned box.
    volume = SpatialVolume(0, 0, 0, 10, 10, 10)
    print("SpatialVolume:", volume)
    print("Does volume contain p3?", volume.contains(p3))
    print("Distance from volume to p4:", volume.distance(p4))
    translated_volume = volume.translate(dx=1, dy=1, dz=1)
    scaled_volume = volume.scale(0.5)
    print("Translated Volume:", translated_volume)
    print("Scaled Volume:", scaled_volume)

    # ---- Spatial Index Example (2D) ----
    if rtree_index is not None:
        index = SpatialIndex(dimension=2)
        index.add(region, entity_id=1)
        index.add(translated_region, entity_id=2)
        queried = index.query((0, 0, 10, 10))
        print("SpatialIndex query for bbox (0, 0, 10, 10):", queried)
