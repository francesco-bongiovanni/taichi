import taichi as ti


@ti.all_archs
def _test_py_style_mod(arg1, a, arg2, b, arg3, c):
  z = ti.var(arg3, shape=())
  
  @ti.kernel
  def func(x: arg1, y: arg2):
    z[None] = x % y

  func(a, b)
  assert z[None] == c


@ti.all_archs
def _test_c_style_mod(arg1, a, arg2, b, arg3, c):
  z = ti.var(arg3, shape=())
  
  @ti.kernel
  def func(x: arg1, y: arg2):
    z[None] = ti.raw_mod(x, y)

  func(a, b)
  assert z[None] == c


def test_py_style_mod():
  def func(a, b):
    _test_py_style_mod(ti.i32, a, ti.i32, b, ti.i32, a % b)
  
  func(10, 3)
  func(-10, 3)
  func(10, -3)
  func(-10, -3)


def _c_mod(a, b):
  return a - b * int(float(a) / b)


def test_c_style_mod():
  def func(a, b):
    _test_c_style_mod(ti.i32, a, ti.i32, b, ti.i32, _c_mod(a, b))

  func(10, 3)
  func(-10, 3)
  func(10, -3)
  func(-10, -3)