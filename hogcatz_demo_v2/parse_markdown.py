import re
import json

def parse_markdown_to_json(markdown_text):
    nodes = []
    links = []
    dad_id = ""
    mom_id = ""

    # 解析 Markdown
    for line in markdown_text.split("\n"):
        if line.startswith("##"):  # 爸爸
            dad_id = re.sub(r"##\s*", "", line).strip().split("（")[0]
            nodes.append({
                "id": dad_id,
                "name": dad_id,
                "type": "cat",
                "gender": "male",
                "photo": f"./photos/{dad_id}.jpg",
                "IDcardPhoto": f"./IDcard/{dad_id}.jpg",
                "link": ""
            })
        elif line.startswith("###"):  # 妈妈
            mom_id = re.sub(r"###\s*", "", line).strip().split("（")[0]
            nodes.append({
                "id": mom_id,
                "name": mom_id,
                "type": "cat",
                "gender": "female",
                "photo": f"./photos/{mom_id}.jpg",
                "IDcardPhoto": f"./IDcard/{mom_id}.jpg",
                "link": ""
            })
        elif line.startswith("-"):  # 窝次
            litter_date = re.sub(r"-?\s*", "", line).strip()
            litter_id = f"窝_{litter_date.replace('/', '_')}"
            nodes.append({
                "id": litter_id,
                "name": f"{litter_date} 窝次",
                "type": "litter"
            })
            links.append({
                "source": dad_id,
                "target": litter_id,
                "type": "mate",
                "mate_line_color": 0xFFC0CB,
                "thickness": 3
            })
            links.append({
                "source": mom_id,
                "target": litter_id,
                "type": "mate",
                "mate_line_color": 0xFFC0CB,
                "thickness": 3
            })
        elif line.startswith("\t-"):  # 孩子
            child_info = re.sub(r"\t-\s*", "", line).strip()
            child_name, gender = child_info.split("，")
            child_link = ""
            if "[" in child_name and "]" in child_name:
                child_name, child_link = re.findall(r"\[(.*?)\]\((.*?)\)", child_name)[0]
            child_id = child_name.strip()
            nodes.append({
                "id": child_id,
                "name": child_id,
                "type": "cat",
                "gender": "male" if "男孩" in gender else "female",
                "photo": f"./photos/{child_id}.jpg",
                "IDcardPhoto": f"./IDcard/{child_id}.jpg",
                "link": child_link
            })
            links.append({
                "source": litter_id,
                "target": child_id,
                "type": "child",
                "child_line_color": 0xADD8E6,
                "thickness": 0.8
            })

    return {"nodes": nodes, "links": links}

# 主程序
if __name__ == "__main__":
    # 读取 Markdown 文件
    try:
        with open("family_tree.md", "r", encoding="utf-8") as file:
            markdown_data = file.read()
    except FileNotFoundError:
        print("Error: Markdown 文件 'family_tree.md' 未找到，请确保文件存在。")
        exit(1)
    except Exception as e:
        print(f"Error: 读取 Markdown 文件时发生错误：{e}")
        exit(1)

    # 调用解析函数
    json_data = parse_markdown_to_json(markdown_data)

    # 保存 JSON 数据到文件
    try:
        with open("output.json", "w", encoding="utf-8") as json_file:
            json.dump(json_data, json_file, ensure_ascii=False, indent=4)
        print("JSON 数据已成功保存到 output.json 文件中。")
    except Exception as e:
        print(f"Error: 保存 JSON 数据时发生错误：{e}")
