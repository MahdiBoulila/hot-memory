#!/usr/bin/env python3
"""
Convert Rekordbox memory cues to hot cues.

Usage:
    python memory_to_hot.py --input memory.xml --output hot.xml
"""

import argparse
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import List


@dataclass
class MemoryCue:
    position: int  # in milliseconds
    name: str
    number: int


@dataclass
class HotCue:
    position: int  # in milliseconds
    number: int
    name: str
    color: str = "000000"  # default black
    enabled: bool = True


def parse_memory_cues(xml_path: str) -> List[MemoryCue]:
    """Parse memory cues from Rekordbox XML export."""
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    cues = []
    # Rekordbox XML structure varies - this is a simplified parser
    # You may need to adjust based on your XML structure
    for track in root.findall('.//Track'):
        cue_points = track.find('.//CuePoints')
        if cue_points is not None:
            for cue in cue_points.findall('.//Cue'):
                cue_type = cue.get('Type', '1')  # 1 = memory cue
                if cue_type == '1':
                    position = int(cue.get('Position', 0))
                    name = cue.get('Name', f'Memory {len(cues)}')
                    number = int(cue.get('Number', len(cues) + 1))
                    cues.append(MemoryCue(position, name, number))
    
    return cues


def convert_to_hot_cues(memory_cues: List[MemoryCue]) -> List[HotCue]:
    """Convert memory cues to hot cues."""
    hot_cues = []
    for i, memory in enumerate(memory_cues):
        hot_cues.append(HotCue(
            position=memory.position,
            number=i + 1,  # Hot cues are numbered sequentially
            name=memory.name,
            color="FF0000"  # Red for hot cues
        ))
    return hot_cues


def export_hot_cues_xml(hot_cues: List[HotCue], output_path: str):
    """Export hot cues in Rekordbox XML format."""
    # This would generate the proper XML structure
    # Implementation depends on your specific Rekordbox version
    print(f"Exporting {len(hot_cues)} hot cues to {output_path}")
    # TODO: Implement proper XML generation


def main():
    parser = argparse.ArgumentParser(description='Convert Rekordbox memory cues to hot cues')
    parser.add_argument('--input', '-i', required=True, help='Input Rekordbox XML file')
    parser.add_argument('--output', '-o', required=True, help='Output file path')
    
    args = parser.parse_args()
    
    print("Parsing memory cues...")
    memory_cues = parse_memory_cues(args.input)
    print(f"Found {len(memory_cues)} memory cues")
    
    print("Converting to hot cues...")
    hot_cues = convert_to_hot_cues(memory_cues)
    print(f"Created {len(hot_cues)} hot cues")
    
    export_hot_cues_xml(hot_cues, args.output)
    print("Done!")


if __name__ == '__main__':
    main()
