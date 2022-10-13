import numpy

# https://pypi.org/project/numpy-stl/
import stl
from stl import mesh


print_bed_mm = [200, 300]
stl_unit = 1
padding_mm = 10
stl_mesh = mesh.Mesh.from_file('drip-tip.stl')


def translate(_solid, step, padding, multiplier, axis):
    if 'x' == axis:
        items = 0, 3, 6
    elif 'y' == axis:
        items = 1, 4, 7
    elif 'z' == axis:
        items = 2, 5, 8
    else:
        raise RuntimeError('Unknown axis %r, expected x, y or z' % axis)

    _solid.points[:, items] += (step * multiplier) + (padding * multiplier)


# get the bounding box of the stl (x, y)
x_size = stl_mesh.x.max() - stl_mesh.x.min()
y_size = stl_mesh.y.max() - stl_mesh.y.min()
x_size *= stl_unit
y_size *= stl_unit

# plateauSize.x / (bounds.x + padding)
# NOTE: there is 1 extra padding for nothing here, maybe use (plateauSize - padding)
X = print_bed_mm[0] / (x_size + padding_mm)
Y = print_bed_mm[1] / (y_size + padding_mm)
X = int(X)
Y = int(Y)

# copy and translate the stl (X, Y) times
copies = []
for row in range(0, X):
    for col in range(0, Y):
        _copy = mesh.Mesh(stl_mesh.data.copy())
        translate(_copy, x_size, padding_mm, row, 'x')
        translate(_copy, y_size, padding_mm, col, 'y')
        copies.append(_copy)

combined = mesh.Mesh(numpy.concatenate([copy.data for copy in copies]))

combined.save('combined.stl', mode=stl.Mode.ASCII)  # save as ASCII
print("{X} copies on the X axis, {Y} copies on the Y axis".format(X=X, Y=Y))
