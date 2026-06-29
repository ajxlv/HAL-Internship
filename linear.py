import pandas as pd


def read_excel(file):
    return pd.read_excel(file)


def find_interval(values, point):
    values = sorted(values.unique())

    if point < values[0] or point > values[-1]:
        print(f"\nError: {point} is outside the available range "
              f"({values[0]} to {values[-1]}).")
        return None, None

    for i in range(len(values)-1):
        if values[i] <= point <= values[i+1]:
            return values[i], values[i+1]


def get_corner_value(df, x, y, z, output):
    row = df[
        (df["X1"] == x) &
        (df["X2"] == y) &
        (df["X3"] == z)
    ]

    return float(row.iloc[0][output])


def linear_interpolation(a, b, t):
    return a * (1 - t) + b * t


def trilinear_interpolation(df, x, y, z, output):

    x0, x1 = find_interval(df["X1"], x)
    y0, y1 = find_interval(df["X2"], y)
    z0, z1 = find_interval(df["X3"], z)
    
    if None in (x0, x1, y0, y1, z0, z1):
        return None


    u = (x - x0) / (x1 - x0)
    v = (y - y0) / (y1 - y0)
    w = (z - z0) / (z1 - z0)

    f000 = get_corner_value(df, x0, y0, z0, output)
    f100 = get_corner_value(df, x1, y0, z0, output)
    f010 = get_corner_value(df, x0, y1, z0, output)
    f110 = get_corner_value(df, x1, y1, z0, output)
    f001 = get_corner_value(df, x0, y0, z1, output)
    f101 = get_corner_value(df, x1, y0, z1, output)
    f011 = get_corner_value(df, x0, y1, z1, output)
    f111 = get_corner_value(df, x1, y1, z1, output)

    c00 = linear_interpolation(f000, f100, u)
    c10 = linear_interpolation(f010, f110, u)
    c01 = linear_interpolation(f001, f101, u)
    c11 = linear_interpolation(f011, f111, u)

    c0 = linear_interpolation(c00, c10, v)
    c1 = linear_interpolation(c01, c11, v)

    return linear_interpolation(c0, c1, w)
    

df = read_excel("data.xlsx")

print("Enter the input values")

x = float(input("X1 : "))
y = float(input("X2 : "))
z = float(input("X3 : "))

predicted_y1 = trilinear_interpolation(df, x, y, z, "Y1")
predicted_y2 = trilinear_interpolation(df, x, y, z, "Y2")

print("\nPrediction")
print("-----------------------")
print(f"Y1 = {predicted_y1:.4f}")
print(f"Y2 = {predicted_y2:.4f}")
print("-----------------------")