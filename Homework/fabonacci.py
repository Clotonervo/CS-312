def fab(n):
    if n <= 2:
        return 1
    else:
        return fab(n-1) + fab(n-2) * fab(n-3)


def linFab(n):
  fn = f1 = f2 = f3 = 1
  if n <= 2:
    return 1
  else:
    for x in range(2, n):
      fn = f1 + f2 * f3
      f3 = f2
      f2 = f1
      f1 = fn
  return fn

print("fab(1):")
print(fab(1))
print("fab(2):")
print(fab(2))
print("fab(3):")
print(fab(3))
print("fab(4):")
print(fab(4))
print("fab(10):")
print(fab(10))
print("\n")
print("linFab(1):")
print(linFab(1))
print("linFab(2):")
print(linFab(2))
print("linFab(3):")
print(linFab(3))
print("linFab(4):")
print(linFab(4))
print("linFab(10):")
print(linFab(10))
