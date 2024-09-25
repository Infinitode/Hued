from hued.conversions import *

def test_rgb_to_hex():
    print("Testing RGB to HEX...")
    r, g, b = 255, 0, 0  # Red
    expected_hex = "#FF0000"
    result = rgb_to_hex(r, g, b)
    assert result == expected_hex, f"Expected {expected_hex}, but got {result}"
    print(f"RGB({r}, {g}, {b}) -> HEX: {result}")

def test_hex_to_rgb():
    print("Testing HEX to RGB...")
    hex_value = "#00FF00"  # Green
    expected_rgb = (0, 255, 0)
    result = hex_to_rgb(hex_value)
    assert result == expected_rgb, f"Expected {expected_rgb}, but got {result}"
    print(f"HEX {hex_value} -> RGB: {result}")

def test_rgb_to_hsl():
    print("Testing RGB to HSL...")
    r, g, b = 0, 0, 255  # Blue
    expected_hsl = (240, 1, 0.5)
    result = rgb_to_hsl(r, g, b)
    assert result == expected_hsl, f"Expected {expected_hsl}, but got {result}"
    print(f"RGB({r}, {g}, {b}) -> HSL: {result}")

def test_hsl_to_rgb():
    print("Testing HSL to RGB...")
    h, s, l = 240, 1, 0.5  # Blue in HSL
    expected_rgb = (0, 0, 255)
    result = hsl_to_rgb(h, s, l)
    assert result == expected_rgb, f"Expected {expected_rgb}, but got {result}"
    print(f"HSL({h}, {s}, {l}) -> RGB: {result}")

def test_rgb_to_hsv():
    print("Testing RGB to HSV...")
    r, g, b = 255, 255, 0  # Yellow
    expected_hsv = (60, 1, 1)
    result = rgb_to_hsv(r, g, b)
    assert result == expected_hsv, f"Expected {expected_hsv}, but got {result}"
    print(f"RGB({r}, {g}, {b}) -> HSV: {result}")

def test_hsv_to_rgb():
    print("Testing HSV to RGB...")
    h, s, v = 60, 1, 1  # Yellow in HSV
    expected_rgb = (255, 255, 0)
    result = hsv_to_rgb(h, s, v)
    assert result == expected_rgb, f"Expected {expected_rgb}, but got {result}"
    print(f"HSV({h}, {s}, {v}) -> RGB: {result}")

def test_rgb_to_cmyk():
    print("Testing RGB to CMYK...")
    r, g, b = 0, 255, 255  # Cyan
    expected_cmyk = (1.0, 0.0, 0.0, 0.0)
    result = rgb_to_cmyk(r, g, b)
    assert result == expected_cmyk, f"Expected {expected_cmyk}, but got {result}"
    print(f"RGB({r}, {g}, {b}) -> CMYK: {result}")

def test_cmyk_to_rgb():
    print("Testing CMYK to RGB...")
    c, m, y, k = 0, 1, 1, 0  # Red in CMYK
    expected_rgb = (255, 0, 0)
    result = cmyk_to_rgb(c, m, y, k)
    assert result == expected_rgb, f"Expected {expected_rgb}, but got {result}"
    print(f"CMYK({c}, {m}, {y}, {k}) -> RGB: {result}")

def test_hsl_to_hex():
    hsl = (0, 1, 0.5)
    result = hsl_to_hex(hsl)
    assert result == "#FF0000", f"Expected '#FF0000', but got {result}"
    print(f"HSL converted to HEX successfully: {result}")

def test_blend_colors():
    print("Testing blend_colors...")
    color1 = (255, 0, 0)  # Red
    color2 = (0, 0, 255)  # Blue
    ratio = 0.5  # Equal blend
    expected_color = (127, 0, 127)  # Purple (midpoint blend of red and blue)
    result = blend_colors(color1, color2, ratio)
    assert result == expected_color, f"Expected {expected_color}, but got {result}"
    print(f"blend_colors({color1}, {color2}, {ratio}) -> RGB: {result}")

def run_tests():
    test_rgb_to_hex()
    test_hex_to_rgb()
    test_rgb_to_hsl()
    test_hsl_to_rgb()
    test_rgb_to_hsv()
    test_hsv_to_rgb()
    test_rgb_to_cmyk()
    test_cmyk_to_rgb()
    test_hsl_to_hex()
    test_blend_colors()

    print("All tests passed!")

if __name__ == "__main__":
    run_tests()