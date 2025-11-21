# check_file.py
import sys

print("Checking chart_calculator.py...")

file_path = 'app/astrology/chart_calculator.py'

try:
    with open(file_path, 'r') as f:
        content = f.read()
        print(f"File size: {len(content)} bytes")
        print(f"Number of lines: {len(content.splitlines())}")
        
        if 'class VedicChartCalculator' in content:
            print("✅ VedicChartCalculator class found in file")
        else:
            print("❌ VedicChartCalculator class NOT found in file")
        
        # Show first 500 characters
        print("\nFirst 500 characters of file:")
        print("="*60)
        print(content[:500])
        print("="*60)
        
except FileNotFoundError:
    print(f"❌ File not found: {file_path}")
except Exception as e:
    print(f"❌ Error reading file: {e}")

# Try to import and see the actual error
print("\n\nAttempting import with detailed error:")
try:
    import app.astrology.chart_calculator as module
    print("Module imported successfully")
    print("Available attributes:", dir(module))
except Exception as e:
    import traceback
    print("Full error traceback:")
    traceback.print_exc()