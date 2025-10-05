#!/usr/bin/env python3
"""Simple validation script for the Gemini AI integration."""

import sys
import os

# Add the project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all new modules can be imported."""
    print("Testing imports...")
    
    try:
        from client_whisper.ai_config import AIConfigManager
        print("  ✓ AIConfigManager imported successfully")
    except Exception as e:
        print(f"  ✗ Failed to import AIConfigManager: {e}")
        return False
    
    try:
        from client_whisper.gemini_service import GeminiService
        print("  ✓ GeminiService imported successfully")
    except Exception as e:
        print(f"  ✗ Failed to import GeminiService: {e}")
        return False
    
    try:
        from client_whisper.ui.settings_dialog import SettingsDialog
        print("  ✓ SettingsDialog imported successfully")
    except Exception as e:
        print(f"  ✗ Failed to import SettingsDialog: {e}")
        return False
    
    return True

def test_ai_config():
    """Test AI configuration manager basic functionality."""
    print("\nTesting AI configuration manager...")
    
    from client_whisper.ai_config import AIConfigManager
    import tempfile
    import shutil
    
    # Create a temporary directory for testing
    test_dir = tempfile.mkdtemp()
    original_home = os.environ.get('HOME')
    os.environ['HOME'] = test_dir
    
    try:
        manager = AIConfigManager()
        
        # Test default config
        config = manager.load_config()
        assert 'api_keys' in config, "Config should have api_keys"
        assert 'current_model' in config, "Config should have current_model"
        print("  ✓ Default configuration loaded")
        
        # Test adding API key
        manager.add_api_key("test_key_12345", "Test Key")
        keys = manager.get_api_keys()
        assert len(keys) == 1, "Should have 1 key after adding"
        print("  ✓ API key addition works")
        
        # Test getting active key
        active = manager.get_active_api_key()
        assert active == "test_key_12345", "Active key should match added key"
        print("  ✓ Active key retrieval works")
        
        # Test model management
        models = manager.get_available_models()
        assert len(models) > 0, "Should have available models"
        print(f"  ✓ {len(models)} models available")
        
        # Test setting model
        manager.set_current_model("gemini-1.5-pro")
        current = manager.get_current_model()
        assert current == "gemini-1.5-pro", "Model should be updated"
        print("  ✓ Model selection works")
        
        # Test usage recording
        manager.record_api_usage("test_key_12345", success=True)
        keys = manager.get_api_keys()
        assert keys[0]['requests_count'] == 1, "Request count should be 1"
        print("  ✓ Usage recording works")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Cleanup
        if original_home:
            os.environ['HOME'] = original_home
        shutil.rmtree(test_dir, ignore_errors=True)

def test_gemini_service():
    """Test Gemini service basic functionality."""
    print("\nTesting Gemini service...")
    
    from client_whisper.gemini_service import GeminiService
    
    try:
        service = GeminiService()
        print("  ✓ GeminiService instantiation works")
        
        # Note: We can't test actual API calls without a real key
        # but we can test the structure
        assert hasattr(service, 'config_manager'), "Should have config_manager"
        assert hasattr(service, 'process_with_ai'), "Should have process_with_ai method"
        print("  ✓ GeminiService has required attributes")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all validation tests."""
    print("=" * 60)
    print("VorkVoice - Gemini AI Integration Validation")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Imports", test_imports()))
    results.append(("AI Configuration", test_ai_config()))
    results.append(("Gemini Service", test_gemini_service()))
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All validations passed! The integration is ready to use.")
        return 0
    else:
        print("\n⚠️ Some validations failed. Please review the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
