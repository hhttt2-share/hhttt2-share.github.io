#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix SVG file by moving image element before pattern definition"""

import re

# Read the SVG file
with open('fitTemp/1 챗지피티.svg', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the image element (it should be on a single line or multiple lines)
# Pattern: <image id="image0_1_4" ... />
image_pattern = r'<image id="image0_1_4"[^>]*>.*?</image>'
image_match = re.search(image_pattern, content, re.DOTALL)

if not image_match:
    # Try self-closing tag
    image_pattern = r'<image id="image0_1_4"[^>]*/>'
    image_match = re.search(image_pattern, content, re.DOTALL)

if image_match:
    image_element = image_match.group(0)
    print(f"Found image element (length: {len(image_element)})")
    
    # Remove the image element from its current position
    content_without_image = content[:image_match.start()] + content[image_match.end():]
    
    # Find <defs> tag
    defs_match = re.search(r'<defs>', content_without_image)
    if defs_match:
        # Find the position after <defs> and before <pattern>
        defs_end = defs_match.end()
        pattern_match = re.search(r'<pattern id="pattern0_1_4"', content_without_image)
        
        if pattern_match:
            # Insert image element after <defs> and before <pattern>
            insert_pos = pattern_match.start()
            new_content = (
                content_without_image[:defs_end] + 
                '\n' + image_element + '\n' +
                content_without_image[defs_end:insert_pos] +
                content_without_image[insert_pos:]
            )
            
            # Write the fixed content
            with open('fitTemp/1 챗지피티.svg', 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print("SVG file fixed successfully!")
            print(f"Image element moved before pattern definition")
        else:
            print("Error: Could not find pattern definition")
    else:
        print("Error: Could not find <defs> tag")
else:
    print("Error: Could not find image element")

