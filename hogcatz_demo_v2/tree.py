import json
import re

def parse_markdown(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    data = []
    current_father = None
    current_mother = None

    for line in lines:
        line = line.strip()

        # 判断父亲
        if line.startswith('## '):
            current_father = {
                'name': line[3:].strip(),
                'mothers': []
            }
            data.append(current_father)

        # 判断母亲
        elif line.startswith('### '):
            current_mother = {
                'name': line[4:].strip(),
                'litters': []
            }
            if current_father:
                current_father['mothers'].append(current_mother)

        # 判断窝次日期+名
        elif re.match(r'^- \d{4}/\d{1,2}/\d{1,2}', line):
            date_name = re.sub(r'^- ', '', line)
            current_litter = {
                'date': date_name,
                'children': []
            }
            if current_mother:
                current_mother['litters'].append(current_litter)

        # 判断孩子
        elif line.startswith('- ') or line.startswith('\t- ') or line.startswith('    - '):
            match = re.match(r'- \[(.*?)\]\((.*?)\)，(.*?)$', line) or \
                    re.match(r'- (.*?)，(.*?)$', line)
            if match:
                if len(match.groups()) == 3:
                    name, link, gender = match.groups()
                else:
                    name, gender = match.groups()
                    link = None
                child = {
                    'name': name.strip(),
                    'gender': gender.strip(),
                    'link': link,
                    'self_kept': '自留' in name or '自留' in gender
                }
                current_litter['children'].append(child)

    return data

# 示例调用
parsed_data = parse_markdown('family_tree.md')
with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(parsed_data, f, ensure_ascii=False, indent=2)

