from hued.analysis import is_neutral, brightness, is_pastel, is_muted, is_vibrant, color_contrast, get_text_color_from_background

def test_is_neutral():
    print("Testing Neutral Color Check...")
    neutral_color = (128, 128, 128)  # Gray
    non_neutral_color = (255, 0, 0)  # Red
    assert is_neutral(neutral_color) == True, "Expected neutral color to return True."
    assert is_neutral(non_neutral_color) == False, "Expected non-neutral color to return False."
    print(f"Neutral Color Test Passed: {neutral_color} is neutral.")

def test_brightness():
    print("Testing Brightness Calculation...")
    color = (255, 255, 255)  # White
    expected_brightness = 1.0  # Fully bright
    result = brightness(color)
    assert result == expected_brightness, f"Expected brightness {expected_brightness}, but got {result}."
    print(f"Brightness of {color}: {result}")

def test_is_pastel():
    print("Testing Pastel Color Check...")
    pastel_color = (255, 200, 200)  # Light red
    non_pastel_color = (255, 0, 0)  # Red
    assert is_pastel(pastel_color) == True, "Expected pastel color to return True."
    assert is_pastel(non_pastel_color) == False, "Expected non-pastel color to return False."
    print(f"Pastel Color Test Passed: {pastel_color} is pastel.")

def test_is_muted():
    print("Testing Muted Color Check...")
    muted_color = (100, 100, 100)  # Dark gray
    non_muted_color = (255, 0, 0)  # Red
    assert is_muted(muted_color) == True, "Expected muted color to return True."
    assert is_muted(non_muted_color) == False, "Expected non-muted color to return False."
    print(f"Muted Color Test Passed: {muted_color} is muted.")

def test_is_vibrant():
    print("Testing Vibrant Color Check...")
    vibrant_color = (0, 255, 0)  # Green
    non_vibrant_color = (128, 128, 128)  # Gray
    assert is_vibrant(vibrant_color) == True, "Expected vibrant color to return True."
    assert is_vibrant(non_vibrant_color) == False, "Expected non-vibrant color to return False."
    print(f"Vibrant Color Test Passed: {vibrant_color} is vibrant.")

def test_color_contrast():
    print("Testing Color Contrast...")
    color1 = (0, 255, 0)  # Green
    color2 = (128, 128, 128)  # Gray
    assert color_contrast(color1, color2) == 2.839124370809266, "Expected a contrast ratio of 2.839124370809266."
    print("Color Contrast Test Passed.")

def test_text_mode():
    print("Testing Text Color, Based On A Background Color...")
    background_color = (0, 0, 255) # Vibrant Blue
    assert get_text_color_from_background(background_color) == "light", "Expected text color, to be `light`."
    print("Text Background Color Test Passed.")

def run_tests():
    test_is_neutral()
    test_brightness()
    test_is_pastel()
    test_is_muted()
    test_is_vibrant()
    test_color_contrast()
    test_text_mode()
    print("All tests passed!")

if __name__ == "__main__":
    run_tests()