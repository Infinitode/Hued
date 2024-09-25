from hued.palettes import ColorPalette

def test_generate_complementary():
    print("Testing Complementary Palette...")
    base_color = (255, 60, 52)  # Red
    palette = ColorPalette(base_color)
    expected_complementary = [(255, 60, 52), (51, 247, 255)]  # Adjust as needed
    result = palette.generate_complementary()
    assert result == expected_complementary, f"Expected {expected_complementary}, but got {result}"
    print(f"Complementary Palette: {result}")

def test_generate_analogous():
    print("Testing Analogous Palette...")
    base_color = (255, 60, 52)  # Red
    palette = ColorPalette(base_color)
    expected_analogous = [(255, 51, 145), (255, 60, 52), (255, 161, 51)]  # Adjust as needed
    result = palette.generate_analogous()
    assert result == expected_analogous, f"Expected {expected_analogous}, but got {result}"
    print(f"Analogous Palette: {result}")

def test_generate_triadic():
    print("Testing Triadic Palette...")
    base_color = (255, 60, 52)  # Red
    palette = ColorPalette(base_color)
    expected_triadic = [(255, 60, 52), (51, 255, 59), (59, 51, 255)]  # Adjust as needed
    result = palette.generate_triadic()
    assert result == expected_triadic, f"Expected {expected_triadic}, but got {result}"
    print(f"Triadic Palette: {result}")

def test_generate_monochromatic():
    print("Testing Monochromatic Palette...")
    base_color = (255, 60, 52)  # Red
    palette = ColorPalette(base_color)
    expected_monochromatic = [(51, 2, 0), (73, 3, 0), (95, 4, 0), (118, 5, 0),
                              (140, 5, 0), (162, 6, 0), (184, 7, 0), (206, 8, 0),
                              (228, 9, 0), (251, 10, 0), (255, 27, 18), (255, 48, 40),
                              (255, 70, 62), (255, 91, 84), (255, 112, 106),
                              (255, 134, 129), (255, 155, 151), (255, 176, 173),
                              (255, 197, 195), (255, 219, 217), (255, 240, 239),
                              (255, 255, 255)]  # Adjust as needed
    result = palette.generate_monochromatic()
    assert result == expected_monochromatic, f"Expected {expected_monochromatic}, but got {result}"
    print(f"Monochromatic Palette: {result}")

def test_generate_tetradic():
    print("Testing Tetradic Palette...")
    base_color = (255, 60, 52)  # Example base color (Red)
    palette = ColorPalette(base_color)
    expected_tetradic = [
        (255, 60, 52), # Base color
        (145, 255, 51), # Tetradic 1
        (51, 247, 255), # Tetradic 2
        (161, 51, 255)  # Tetradic 3
    ]
    result = palette.generate_tetradic()
    assert result == expected_tetradic, f"Expected {expected_tetradic}, but got {result}"
    print(f"Tetradic Palette: {result}")

def test_generate_square():
    print("Testing Square Palette...")
    base_color = (255, 60, 52)  # Example base color (Red)
    palette = ColorPalette(base_color)
    expected_square = [
        (255, 60, 52), # Base color
        (145, 255, 51), # Square 1
        (51, 247, 255), # Square 2
        (161, 51, 255) # Square 3
    ]
    result = palette.generate_square()
    assert result == expected_square, f"Expected {expected_square}, but got {result}"
    print(f"Square Palette: {result}")

def test_generate_split_complementary():
    print("Testing Split-Complementary Palette...")
    base_color = (255, 60, 52)  # Example base color (Red)
    palette = ColorPalette(base_color)
    expected_split_complementary = [
        (255, 60, 52),  # Base color
        (51, 255, 161),  # Split Complementary 1
        (51, 145, 255)   # Split Complementary 2
    ]
    result = palette.generate_split_complementary()
    assert result == expected_split_complementary, f"Expected {expected_split_complementary}, but got {result}"
    print(f"Split-Complementary Palette: {result}")

def test_palette_to_hex():
    print("Testing Palette to HEX conversion...")
    base_color = (255, 60, 52)  # Red
    palette = ColorPalette(base_color)
    palette.generate_monochromatic()  # Generate to test conversion
    expected_hex = ['#330200', '#490300', '#5F0400', '#760500',
                    '#8C0500', '#A20600', '#B80700', '#CE0800',
                    '#E40900', '#FB0A00', '#FF1B12', '#FF3028',
                    '#FF463E', '#FF5B54', '#FF706A', '#FF8681',
                    '#FF9B97', '#FFB0AD', '#FFC5C3', '#FFDBD9',
                    '#FFF0EF', '#FFFFFF']  # Adjust as needed
    result = palette.palette_to_hex()
    assert result == expected_hex, f"Expected {expected_hex}, but got {result}"
    print(f"Palette in HEX: {result}")

def test_generate_random_palette():
    print("Testing Random Palette Generation...")
    palette = ColorPalette((0, 0, 0))  # Base color not used in random generation
    result = palette.generate_random_palette()
    assert isinstance(result, dict), "Expected a dictionary for the random palette."
    print("Random Palette:", result)

def test_generate_random_color():
    print("Testing Random Color Generation...")
    palette = ColorPalette((0, 0, 0))
    result = palette.generate_random_color()
    assert isinstance(result, dict), "Expected a dictionary for the random color."
    print("Random Color:", result)

def test_generate_random_hex_colors():
    print("Testing Random HEX Colors Generation...")
    palette = ColorPalette((0, 0, 0))
    result = palette.generate_random_hex_colors()
    assert isinstance(result, list), "Expected a list for the random HEX colors."
    print("Random HEX Colors:", result)

def run_tests():
    test_generate_complementary()
    test_generate_analogous()
    test_generate_triadic()
    test_generate_monochromatic()
    test_generate_tetradic()
    test_generate_square()
    test_generate_split_complementary()
    test_palette_to_hex()
    test_generate_random_palette()
    test_generate_random_color()
    test_generate_random_hex_colors()
    print("All tests passed!")

if __name__ == "__main__":
    run_tests()