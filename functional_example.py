#!/usr/bin/env python3
"""
Example demonstrating the functional approach
"""

from data_loader import load_resume_data, load_config_data, get_default_config
from style_generator import create_all_styles


def demonstrate_functional_approach():
    """Demonstrate the functional approach with a simple example"""
    print("🚀 Functional Resume Generation Example")
    print("=" * 50)
    
    # Step 1: Load data (pure function)
    print("1. Loading resume data...")
    try:
        resume_data = load_resume_data("inputs/dheeraj_chand_software_engineer/resume_data.json")
        print(f"   ✅ Loaded data for: {resume_data.personal_info['name']}")
    except Exception as e:
        print(f"   ❌ Error loading data: {e}")
        return False
    
    # Step 2: Load configuration (pure function)
    print("2. Loading configuration...")
    try:
        config_data = load_config_data("inputs/dheeraj_chand_software_engineer/config.json")
        print(f"   ✅ Loaded config with {len(config_data.colors)} colors")
        print(f"   Color scheme: {config_data.metadata.get('scheme_name', 'unknown')}")
    except Exception as e:
        print(f"   ❌ Error loading config: {e}")
        # Fall back to default config
        config_data = get_default_config()
        print(f"   ✅ Using default config with {len(config_data.colors)} colors")
    
    # Step 3: Create styles (pure function)
    print("3. Creating paragraph styles...")
    try:
        styles = create_all_styles(config_data)
        print(f"   ✅ Created {len(styles)} paragraph styles")
        print(f"   Available styles: {list(styles.keys())}")
    except Exception as e:
        print(f"   ❌ Error creating styles: {e}")
        return False
    
    # Step 4: Demonstrate immutability
    print("4. Demonstrating immutability...")
    original_name = resume_data.personal_info['name']
    print(f"   Original name: {original_name}")
    
    # Try to modify (this should not affect the original)
    personal_info_copy = resume_data.personal_info.copy()
    personal_info_copy['name'] = 'Modified Name'
    print(f"   Modified copy: {personal_info_copy['name']}")
    print(f"   Original unchanged: {resume_data.personal_info['name']}")
    
    # Step 5: Demonstrate function composition
    print("5. Demonstrating function composition...")
    
    # Compose functions to create a simple pipeline
    def create_simple_pipeline(data_path: str, config_path: str):
        """Compose functions into a pipeline"""
        def pipeline():
            data = load_resume_data(data_path)
            config = load_config_data(config_path)
            styles = create_all_styles(config)
            return data, config, styles
        return pipeline
    
    # Create and run pipeline
    pipeline = create_simple_pipeline(
        "inputs/dheeraj_chand_software_engineer/resume_data.json",
        "inputs/dheeraj_chand_software_engineer/config.json"
    )
    
    try:
        data, config, styles = pipeline()
        print(f"   ✅ Pipeline executed successfully")
        print(f"   Data: {data.personal_info['name']}")
        print(f"   Config: {len(config.colors)} colors")
        print(f"   Styles: {len(styles)} styles")
    except Exception as e:
        print(f"   ❌ Pipeline error: {e}")
        return False
    
    print("\n🎉 Functional approach demonstration completed successfully!")
    return True


def compare_approaches():
    """Compare OOP vs Functional approaches"""
    print("\n📊 OOP vs Functional Comparison")
    print("=" * 40)
    
    print("Object-Oriented Approach:")
    print("  ❌ Monolithic classes (662+ lines)")
    print("  ❌ Mutable state management")
    print("  ❌ Tight coupling between components")
    print("  ❌ Difficult to test individual parts")
    print("  ❌ Side effects scattered throughout")
    
    print("\nFunctional Approach:")
    print("  ✅ Pure functions (no side effects)")
    print("  ✅ Immutable data structures")
    print("  ✅ Loose coupling via function composition")
    print("  ✅ Easy to test individual functions")
    print("  ✅ Clear data flow")
    print("  ✅ Reusable and composable")
    
    print("\nBenefits of Functional Approach:")
    print("  • Better testability - each function can be tested in isolation")
    print("  • Improved maintainability - functions are small and focused")
    print("  • Enhanced reusability - functions can be composed differently")
    print("  • Easier debugging - no hidden state changes")
    print("  • Better performance - no object instantiation overhead")
    print("  • Clearer code - each function has a single responsibility")


def main():
    """Main function"""
    success = demonstrate_functional_approach()
    compare_approaches()
    
    if success:
        print("\n✅ Functional approach is working correctly!")
        print("Next steps:")
        print("  1. Implement content_builder.py")
        print("  2. Implement generators/pdf_generator.py")
        print("  3. Create pipeline composition functions")
        print("  4. Add comprehensive tests")
        print("  5. Migrate existing code gradually")
    else:
        print("\n❌ Functional approach needs debugging")
    
    return success


if __name__ == "__main__":
    main()
