with open('index.html','r',encoding='utf-8') as f:
    lines = f.readlines()

def find_line(substr, start=0):
    for i in range(start, len(lines)):
        if substr in lines[i]:
            return i
    return -1

arch_comment = find_line('==================== ARCHITECTURE ====================')
arch_end = find_line('</script>', arch_comment) + 1
tools_comment = find_line('==================== TOOLS ====================')
tools_end = find_line('</section>', tools_comment) + 1

arch_block = lines[arch_comment:arch_end]
tools_block = lines[tools_comment:tools_end]

new_lines = lines[:arch_comment] + tools_block + lines[arch_end:tools_comment] + arch_block + lines[tools_end:]

with open('index.html','w',encoding='utf-8') as f:
    f.writelines(new_lines)

print('Swapped. New section positions:')
for i,l in enumerate(new_lines):
    if 'id="architecture"' in l or 'id="tools"' in l:
        print(' line', i+1, l.strip())