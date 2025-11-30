import re
import os

# ====================== 配置项（无需修改，适配你的路径） ======================
links_file_path = r"C:\Users\未来可期\Desktop\音频\m4a_播放链接.txt"  # 音频链接文件路径
readme_path = r"C:\Users\未来可期\Desktop\音频\README.md"            # README 文件路径
repo_owner = "qyxay"                                                # GitHub 用户名
repo_name = "m4a"                                                   # GitHub 仓库名
branch = "main"                                                     # 仓库分支

# ====================== 核心逻辑 ======================
def extract_episode_info(link):
    """从链接中提取集名和集数（用于排序）"""
    # 从链接末尾提取文件名（如：%E7%AC%AC31%E9%9B%86.m4a → 第31集.m4a）
    filename = link.split("/")[-1]
    # 解码 URL 编码的文件名（处理中文）
    try:
        from urllib.parse import unquote
        filename = unquote(filename)
    except:
        pass  # 解码失败则用原文件名
    
    # 提取集名（核心：匹配“第X集”，保留完整集名）
    episode_match = re.search(r"第(\d+)集[^.]*", filename)
    if episode_match:
        episode_num = episode_match.group(1)  # 集数（数字，用于排序）
        episode_name = episode_match.group(0) # 集名（如：第31集）
    else:
        episode_num = "999"  # 无集数的放最后
        episode_name = "未知集数"
    
    return {
        "link": link,
        "episode_num": episode_num,
        "episode_name": episode_name
    }

def generate_audio_player_html(audio_info):
    """生成带集名的音频播放器 HTML 代码"""
    link = audio_info["link"]
    episode_name = audio_info["episode_name"]
    # 生成播放器代码（保留集名显示，播放器可直接播放）
    html = f"""
### {episode_name}
<audio controls preload="metadata">
  <source src="{link}" type="audio/mp4">
  您的浏览器不支持音频播放，请点击 <a href="{link}">下载音频</a>
</audio>
---
"""
    return html

# ====================== 执行流程 ======================
if __name__ == "__main__":
    # 1. 读取所有音频链接
    if not os.path.exists(links_file_path):
        print(f"❌ 错误：未找到链接文件 {links_file_path}")
        exit()
    
    audio_links = []
    with open(links_file_path, "r", encoding="utf-8") as f:
        for line in f.readlines():
            line = line.strip()
            if line and "m4a" in line:  # 过滤空行和非音频链接
                audio_links.append(line)
    print(f"✅ 成功读取 {len(audio_links)} 个音频链接")

    # 2. 提取集名+集数，按集数排序
    audio_info_list = [extract_episode_info(link) for link in audio_links]
    # 按集数从小到大排序（数字排序）
    audio_info_list.sort(key=lambda x: int(x["episode_num"]))

    # 3. 批量生成带集名的音频播放器代码
    markdown_content = "\n# 阴阳行者篇 音频播放列表\n\n"  # 标题
    for audio_info in audio_info_list:
        markdown_content += generate_audio_player_html(audio_info)

    # 4. 写入 README.md（覆盖原有内容，确保格式统一）
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)
    
    print(f"✅ 已成功生成带集名的音频播放器！")
    print(f"📁 结果已写入：{readme_path}")
    print("\n🔍 效果预览：")
    print(generate_audio_player_html(audio_info_list[0]))  # 打印第一个播放器示例