from hued.colors import ColorManager

# Initialize the ColorManager
color_manager = ColorManager()

def test_hex_to_rgb():
    print("Testing HEX to RGB...")
    hex_value = "#FF5733"  # A sample hex color
    expected_rgb = (255, 87, 51)
    result = color_manager.hex_to_rgb(hex_value)
    assert result == expected_rgb, f"Expected {expected_rgb}, but got {result}"
    print(f"HEX {hex_value} -> RGB: {result}")

def test_rgb_to_hex():
    print("Testing RGB to HEX...")
    r, g, b = 0, 128, 0  # Green
    expected_hex = "#008000"
    result = color_manager.rgb_to_hex(r, g, b)
    assert result == expected_hex, f"Expected {expected_hex}, but got {result}"
    print(f"RGB({r}, {g}, {b}) -> HEX: {result}")

def test_closest_color_name():
    print("Testing Closest Color Name...")
    hex_value = "#FF0000"  # Red
    expected_name = "Red"
    result = color_manager.closest_color_name(hex_value)
    assert result == expected_name, f"Expected {expected_name}, but got {result}"
    print(f"Closest color to {hex_value} is {result}")

def test_get_color_by_name():
    print("Testing Get Color by Name...")
    color_name = "Blue"
    expected_result = {
        'Name': "Blue",
        'Hex': "#0000FF",
        'RGB': (0, 0, 255)
    }
    result = color_manager.get_color_by_name(color_name)
    assert result == expected_result, f"Expected {expected_result}, but got {result}"
    print(f"{color_name} -> {result}")

def run_tests():
    test_hex_to_rgb()
    test_rgb_to_hex()
    test_closest_color_name()
    test_get_color_by_name()
    print("All tests passed!")

if __name__ == "__main__":
    run_tests()