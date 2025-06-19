import json
import re

# 输入的 Markdown 文件路径
INPUT_MD = 'family_tree.md'
# 输出的 JSON 文件路径
OUTPUT_JSON = 'graphData.json'

# 初始化数据结构
graph_data = {
    "nodes": [],
    "links": []
}
# 辅助字典用于去重
nodes_index = {}

# 关系色值
MATE_COLOR = 0xFFC0CB  # 粉色
CHILD_COLOR = 0xADD8E6  # 浅蓝色

# 当前上下文变量
current_father = None
current_mother = None
current_litter_id = None
litter_count = 1

# 正则模式
father_pattern = re.compile(r'^##\s+(.+?)')
mother_pattern = re.compile(r'^###\s+(.+?)')
litter_pattern = re.compile(r'^-\s*(?:\[.*?\]\(.+?\)|\d{4}/\d{1,2}/\d{1,2}.*)')
child_pattern = re.compile(r'^\s*[-*]\s*(?:\[(?P<name1>[^\]]+)\]\((?P<link>[^)]+)\)|(?P<name2>[^，\[]+))，?(?P<gender>男孩|女孩)?')

# 函数：添加节点
def add_node(node):
    key = (node['id'], node.get('type', ''))
    if key not in nodes_index:
        graph_data['nodes'].append(node)
        nodes_index[key] = True

# 添加猫咪节点
def add_cat(name, gender='', link=''):
    name = name.strip()
    node = {
        'id': name,
        'name': name,
        'photo': f'{name}.jpg',
        'IDcardPhoto': f'{name}.jpg',
        'link': link or '',
        'type': 'cat',
        'gender': 'male' if '男' in gender else 'female' if '女' in gender else ''
    }
    add_node(node)

# 添加窝次节点
def add_litter(display_name):
    global litter_count
    litter_id = f'窝_{display_name.replace("/","_")}'
    node = {
        'id': litter_id,
        'name': display_name + ' 窝次',
        'type': 'litter'
    }
    add_node(node)
    return litter_id

# 添加链接
def add_link(src, tgt, rel_type):
    link = {'source': src, 'target': tgt, 'type': rel_type}
    if rel_type == 'mate':
        link['mate_line_color'] = MATE_COLOR
        link['thickness'] = 3
    else:
        link['child_line_color'] = CHILD_COLOR
        link['thickness'] = 0.8
    graph_data['links'].append(link)

# 读取 Markdown 并解析
with open(INPUT_MD, encoding='utf-8') as f:
    for raw in f:
        line = raw.rstrip()  # 保留缩进空格
        # 爸爸
        m = father_pattern.match(line)
        if m:
            current_father = m.group(1)
            add_cat(current_father, gender='男')
            continue
        # 妈妈
        m = mother_pattern.match(line)
        if m:
            current_mother = m.group(1)
            add_cat(current_mother, gender='女')
            continue
        # 窝次
        if litter_pattern.match(line) and not line.startswith('    '):
            # 提取窝次显示文字
            display = line.lstrip('- ').split()[0]
            current_litter_id = add_litter(display)
            # 父母到窝次mate关系
            if current_father and current_mother:
                add_link(current_father, current_litter_id, 'mate')
                add_link(current_mother, current_litter_id, 'mate')
            continue
        # 孩子
        m = child_pattern.match(line)
        if m and current_litter_id:
            name = m.group('name1') or m.group('name2')
            link = m.group('link') or ''
            gender = m.group('gender') or ''
            name = name.strip()
            add_cat(name, gender=gender, link=link)
            add_link(current_litter_id, name, 'child')
            # 如果孩子名字中含“自留”，下次成为父或母
            if '自留' in name:
                # 会在后续标题中处理
                pass

# 导出 JSON 文件
with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
    json.dump(graph_data, f, ensure_ascii=False, indent=2)

print(f'✅ 已生成 {OUTPUT_JSON}')

