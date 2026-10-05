import re
import os

files_to_merge = ["data.js", "data2.js", "data3.js", "data4.js", "data5.js"]
combined_content = ""

for idx, file in enumerate(files_to_merge):
    with open(file, "r", encoding="utf-8") as f:
        content = f.read()

        if idx == 0:
            # data.js
            # Find the start of the array and the end
            # It looks like `var IDIOMS = [\n  {...}\n];`
            match = re.search(r'var IDIOMS = \[', content)
            if match:
                # Remove the closing brackets from the end
                content = re.sub(r'\];$', ',', content.strip())
                combined_content += content + "\n"
        else:
            # data2.js, etc.
            # IDIOMS = IDIOMS.concat([
            # ...
            # ]);
            content = re.sub(r'IDIOMS = IDIOMS.concat\(\[', '', content)
            content = re.sub(r'\]\);$', ',', content.strip())
            # Remove comments at the top like // 扩充成语库 ...
            content = re.sub(r'^//.*?\n', '', content, flags=re.MULTILINE)
            combined_content += content + "\n"

# Replace the last comma with closing brackets
combined_content = combined_content.strip()
if combined_content.endswith(','):
    combined_content = combined_content[:-1]
combined_content += "\n];\n"

with open("data.js", "w", encoding="utf-8") as f:
    f.write(combined_content)
