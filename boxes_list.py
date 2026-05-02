from layout import Box
from layout import bin_packing
from visualiser import visualise

# 1. SIMPLE CASE
simple_boxes = [
    Box(50, 70),
    Box(90, 45),
    Box(20, 30),
    Box(10, 50)
]

# 2. SOME MIXED SIZES
mixed_boxes = [
    Box(80, 400),  # Very tall
    Box(100, 100),  # Square
    Box(250, 100),  # Wide
    Box(400, 80),  # Very wide
    Box(60, 60),
    Box(60, 60),
    Box(60, 60),
    Box(20, 50),
    Box(20, 50),
    Box(20, 50),
    Box(10, 10),
    Box(10, 10),
    Box(5, 5)
]

mixed_boxes_2 = [
    Box(85, 120),
    Box(45, 45),
    Box(30, 80),
    Box(60, 60),
    Box(25, 25),
    Box(15, 35),
    Box(40, 100),
    Box(50, 50),
    Box(20, 45),
    Box(35, 65)
]

mixed_boxes_3 = [
    Box(95, 75),
    Box(68, 120),
    Box(45, 45),
    Box(110, 35),
    Box(28, 95),
    Box(55, 55),
    Box(82, 48),
    Box(15, 65),
    Box(38, 38),
    Box(72, 24),
    Box(19, 42),
    Box(90, 60),
    Box(33, 88),
    Box(12, 12),
    Box(48, 115)
]

# 4. ALL SQUARES
square_boxes = [
    Box(50, 50),
    Box(40, 40),
    Box(30, 30),
    Box(30, 30),
    Box(20, 20),
    Box(20, 20),
    Box(20, 20),
    Box(10, 10)
]

# 5. TALL AND NARROW
tall_boxes = [
    Box(10, 100),
    Box(15, 90),
    Box(10, 80),
    Box(20, 70),
    Box(10, 60),
    Box(15, 50)
]

# 6. WIDE AND SHORT
wide_boxes = [
    Box(100, 10),
    Box(90, 15),
    Box(80, 10),
    Box(70, 20),
    Box(60, 10),
    Box(50, 15)
]

# 7. EDGE CASES - almost full width, height etc.
edge_case_boxes = [
    Box(w=118, l=98),
    Box(w=118, l=98),
    Box(w=2, l=1),
]

extreme_aspect_boxes = [
    Box(122, 10),
    Box(10, 197),
    Box(61, 99),
    Box(30, 30),
    Box(25, 25)
]

# should use 100% space
fits_exactly_boxes = [
    Box(123, 99),
    Box(123, 99)
]

# single large item
one_huge_box = [
    Box(120, 190)
]

# 8. MANY SMALL BOXES
import random

random.seed(42)  # For reproducibility
many_small_boxes = [
    Box(random.randint(5, 25), random.randint(5, 25))
    for _ in range(50)
]

# 09. POWER OF 2 SIZES
power_of_2_boxes = [
    Box(64, 64),
    Box(32, 32),
    Box(32, 32),
    Box(16, 16),
    Box(16, 16),
    Box(16, 16),
    Box(16, 16),
    Box(8, 8)
]

# 10. STRESS TEST
random.seed(123)  # Different seed
stress_test_boxes = [
    Box(random.randint(10, 60), random.randint(10, 60))
    for _ in range(100)
]

# 11. IDENTICAL BOXES
identical_boxes = [Box(30, 30) for _ in range(20)]

# 12. GRADIENT SIZES - smooth progression
gradient_boxes = [
    Box(100, 100),
    Box(90, 90),
    Box(80, 80),
    Box(70, 70),
    Box(60, 60),
    Box(50, 50),
    Box(40, 40),
    Box(30, 30),
    Box(20, 20),
    Box(10, 10)
]

# 13. ALTERNATING ORIENTATIONS - portrait vs landscape
alternating_boxes = [
    Box(60, 100),  # Portrait
    Box(100, 60),  # Landscape
    Box(50, 90),  # Portrait
    Box(90, 50),  # Landscape
    Box(40, 80),  # Portrait
    Box(80, 40),  # Landscape
    Box(30, 70),  # Portrait
    Box(70, 30)  # Landscape
]

# 14. SMALL VARIATIONS - nearly identical
small_variations_boxes = [
    Box(50, 50),
    Box(51, 50),
    Box(50, 51),
    Box(52, 50),
    Box(50, 52),
    Box(49, 50),
    Box(50, 49),
    Box(48, 50)
]

# 15. DECREASING SIZES - largest to smallest
decreasing_boxes = [
    Box(100, 100),
    Box(80, 80),
    Box(60, 60),
    Box(40, 40),
    Box(30, 30),
    Box(20, 20),
    Box(15, 15),
    Box(10, 10),
    Box(5, 5)
]

# 16. Others
challenging_boxes = [
    Box(61, 61),
    Box(62, 62),
    Box(40, 150),
    Box(120, 30),
    Box(25, 25),
    Box(25, 25),
    Box(25, 25),
    Box(25, 25),
    Box(80, 80),
    Box(15, 198),
    Box(123, 15)
]

challenging_boxes_v2 = [
    Box(w=25, l=25, filename='bld_016-1f2e3d4c-5b6a-7f8e-9d0c-1b2a3f4e5d6c.stl'),
    Box(w=25, l=25, filename='bld_016-1f2e3d4c-5b6a-7f8e-9d0c-1b2a3f4e5d6c.stl'),
    Box(w=25, l=25, filename='bld_016-1f2e3d4c-5b6a-7f8e-9d0c-1b2a3f4e5d6c.stl'),
    Box(w=25, l=25, filename='bld_016-1f2e3d4c-5b6a-7f8e-9d0c-1b2a3f4e5d6c.stl'),
    Box(w=25, l=25, filename='bld_016-1f2e3d4c-5b6a-7f8e-9d0c-1b2a3f4e5d6c.stl'),
    Box(w=25, l=25, filename='bld_016-1f2e3d4c-5b6a-7f8e-9d0c-1b2a3f4e5d6c.stl'),
    Box(w=25, l=25, filename='bld_016-1f2e3d4c-5b6a-7f8e-9d0c-1b2a3f4e5d6c.stl'),
    Box(w=25, l=25, filename='bld_016-1f2e3d4c-5b6a-7f8e-9d0c-1b2a3f4e5d6c.stl'),
    Box(w=4, l=51, filename='bld_016-7f8e9d0c-1b2a-3f4e-5d6c-7b8a9f0e1d2c.stl'),
    Box(w=5, l=5, filename='bld_016-9b0c1d2e-3f4a-5b6c-7d8e-9f0a1b2c3d4e.stl'),
    Box(w=5, l=5, filename='bld_016-9b0c1d2e-3f4a-5b6c-7d8e-9f0a1b2c3d4e.stl'),
    Box(w=5, l=5, filename='bld_016-9b0c1d2e-3f4a-5b6c-7d8e-9f0a1b2c3d4e.stl'),
    Box(w=5, l=5, filename='bld_016-9b0c1d2e-3f4a-5b6c-7d8e-9f0a1b2c3d4e.stl'),
    Box(w=5, l=5, filename='bld_016-9b0c1d2e-3f4a-5b6c-7d8e-9f0a1b2c3d4e.stl'),
    Box(w=5, l=5, filename='bld_016-9b0c1d2e-3f4a-5b6c-7d8e-9f0a1b2c3d4e.stl'),
]

# Test dictionary
test_cases = {
    'simple': simple_boxes,
    'mixed': mixed_boxes,
    'mixed2': mixed_boxes_2,
    'mixed3': mixed_boxes_3,
    'squares': square_boxes,
    'tall': tall_boxes,
    'wide': wide_boxes,
    'edge_case': edge_case_boxes,
    'extreme_aspect': extreme_aspect_boxes,
    'fits_exactly': fits_exactly_boxes,
    'one_huge': one_huge_box,
    'many_small': many_small_boxes,
    'power_of_2': power_of_2_boxes,
    'stress_test': stress_test_boxes,
    'identical': identical_boxes,
    'gradient': gradient_boxes,
    'alternating': alternating_boxes,
    'small_variations': small_variations_boxes,
    'decreasing': decreasing_boxes,
    'other': challenging_boxes,
    'other2': challenging_boxes_v2,
}

# Run all tests
if __name__ == '__main__':

    for name, boxes in test_cases.items():
        print(f"\n{'=' * 60}")
        print(f"Testing: {name}")
        print(f"{'=' * 60}")
        result = bin_packing(boxes)
        if result:
            packed = result.get('occupied')
            spaces = result.get('empty_slots')
            print(f"✓ Packed {len(packed)}/{len(boxes)} boxes")
            visualise(packed, f'./newimages_/{name}.png')
