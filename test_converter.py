#!/usr/bin/env python3
"""
Test the memory cue converter with sample data.
"""

import sys
from memory_to_hot import parse_memory_cues, convert_to_hot_cues

# Sample Rekordbox XML content for testing
SAMPLE_XML = """<?xml version="1.0" encoding="UTF-8"?>
<ROOT>
    <Track>
        <Position>120000</Position>
        <CuePoints>
            <Cue Type="1" Name="Intro" Position="0" Number="1"/>
            <Cue Type="1" Name="Drop" Position="60000" Number="2"/>
            <Cue Type="1" Name="Break" Position="120000" Number="3"/>
        </CuePoints>
    </Track>
</ROOT>
"""


def test_parse():
    """Test parsing memory cues from XML."""
    print("Test 1: Parse sample XML")
    
    # Write sample to temp file
    with open('/tmp/test_memory.xml', 'w') as f:
        f.write(SAMPLE_XML)
    
    cues = parse_memory_cues('/tmp/test_memory.xml')
    print(f"  Parsed {len(cues)} memory cues:")
    for cue in cues:
        print(f"    - {cue.name}: {cue.position}ms (#{cue.number})")
    
    assert len(cues) == 3, "Should parse 3 cues"
    assert cues[0].name == "Intro", "First cue should be Intro"
    assert cues[1].position == 60000, "Second cue should be at 60s"
    print("  ✓ Passed")


def test_conversion():
    """Test conversion to hot cues."""
    print("\nTest 2: Convert to hot cues")
    
    from memory_to_hot import MemoryCue, HotCue
    
    memory_cues = [
        MemoryCue(0, "Intro", 1),
        MemoryCue(60000, "Drop", 2),
        MemoryCue(120000, "Break", 3),
    ]
    
    hot_cues = convert_to_hot_cues(memory_cues)
    
    print(f"  Converted {len(hot_cues)} hot cues:")
    for cue in hot_cues:
        print(f"    - {cue.name}: {cue.position}ms (#{cue.number}, color: {cue.color})")
    
    assert len(hot_cues) == 3, "Should have 3 hot cues"
    assert hot_cues[0].color == "FF0000", "Hot cues should be red"
    assert hot_cues[0].number == 1, "First hot cue should be #1"
    print("  ✓ Passed")


def run_all_tests():
    """Run all tests."""
    print("Running tests for Hot Memory Converter\n")
    
    try:
        test_parse()
        test_conversion()
        print("\n✅ All tests passed!")
        return True
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
