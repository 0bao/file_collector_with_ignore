import os
import fnmatch

def collect_files_with_extensions(directory, extensions):
    """
    遍历指定目录及其子目录，收集具有指定扩展名的文件。
    Collect files with specific extensions in a directory and its subdirectories.

    :param directory: 要遍历的目录 / Directory to search
    :param extensions: 文件扩展名列表 / List of file extensions
    :return: 匹配文件的路径列表 / List of matching file paths
    """
    filtered_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(tuple(extensions)):
                filtered_files.append(os.path.join(root, file))
    return filtered_files

def parse_ignore_file(ignore_file):
    """
    解析单个 ignore 文件，生成完整路径模式列表。
    Parse a single ignore file to generate a list of full path patterns.

    :param ignore_file: ignore 文件路径 / Path to the ignore file
    :return: 路径模式列表 / List of path patterns
    """
    patterns = []

    if not os.path.exists(ignore_file):
        raise FileNotFoundError(f"Ignore file not found: {ignore_file}")

    base_dir = os.path.dirname(os.path.abspath(ignore_file))

    with open(ignore_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if os.path.isabs(line):
                patterns.append(line)
            else:
                full_path_pattern = os.path.join(base_dir, line)
                full_path_pattern = os.path.normpath(full_path_pattern)
                patterns.append(full_path_pattern)

    return patterns

def load_ignore_patterns(ignore_files):
    """
    加载多个 ignore 文件的规则，并合并为一个列表。
    Load rules from multiple ignore files and merge into a single list.

    :param ignore_files: ignore 文件路径列表 / List of ignore file paths
    :return: 合并后的路径模式列表 / Merged list of path patterns
    """
    all_patterns = []

    for ignore_file in ignore_files:
        patterns = parse_ignore_file(ignore_file)
        all_patterns.extend(patterns)

    return all_patterns

def get_files_by_extensions(directory, extensions):
    """
    递归获取目录及其子目录中指定扩展名的所有文件。
    Recursively get all files with specified extensions in a directory.

    :param directory: 目标目录 / Target directory
    :param extensions: 文件扩展名列表 / List of file extensions
    :return: 匹配的文件路径列表 / List of matching file paths
    """
    collected_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(tuple(extensions)):
                collected_files.append(os.path.join(root, file))
    return collected_files

def load_config():
    """
    从配置文件加载配置信息。
    Load configuration from a configuration file.

    :return: 配置字典 / Configuration dictionary
    """

    config = {"extensions": [], "custom_ignore_ext": []}
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(script_dir, "config.txt")

    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith("#") or not line:
                    continue
                if line.startswith("EXTENSIONS:"):
                    extensions = line.replace("EXTENSIONS:", "").split(",")
                    config["extensions"] = [ext.strip().lower() for ext in extensions]
                elif line.startswith("CUSTOM_IGNORE_EXT:"):
                    extensions = line.replace("CUSTOM_IGNORE_EXT:", "").split(",")
                    config["custom_ignore_ext"] = [ext.strip().lower() for ext in extensions]
    return config

def normalize_path(path):
    """
    标准化路径，以统一正反斜杠和大小写。
    Normalize the path to handle slashes and case insensitivity.

    :param path: 文件路径 / File path
    :return: 标准化后的路径 / Normalized path
    """
    return os.path.normpath(path).lower()

def should_ignore(file_path, ignore_patterns):
    """
    检查文件是否需要忽略。
    Check if a file should be ignored based on ignore patterns.

    :param file_path: 文件路径 / File path to check
    :param ignore_patterns: 忽略规则列表 / List of ignore patterns
    :return: 是否忽略该文件 / True if the file should be ignored, else False
    """
    file_path = normalize_path(file_path)

    for pattern in ignore_patterns:
        if fnmatch.fnmatch(file_path.lower(), pattern.lower()):
            return True
    return False

def filter_files(file_paths, ignore_patterns):
    """
    根据忽略规则过滤文件路径，返回未被忽略的文件。
    Filter file paths based on ignore patterns and return unignored files.

    :param file_paths: 文件路径列表 / List of file paths
    :param ignore_patterns: 忽略规则列表 / List of ignore patterns
    :return: 未忽略文件的路径列表 / List of unignored file paths
    """
    filtered_files = []
    for file_path in file_paths:
        if not should_ignore(file_path, ignore_patterns):
            filtered_files.append(file_path)
    return filtered_files

def collect_files(directory):
    """
    根据配置和忽略规则收集目录中的有效文件。
    Collect valid files from a directory based on config and ignore rules.

    :param directory: 目标目录 / Target directory
    :return: 符合条件的文件路径列表 / List of valid file paths
    """
    config = load_config()

    custom_ignore_ext = config.get("custom_ignore_ext", [])
    custom_ignore_files = collect_files_with_extensions(directory, custom_ignore_ext)

    ignore_patterns = load_ignore_patterns(custom_ignore_files)

    extensions = config.get("extensions", [])
    file_paths = collect_files_with_extensions(directory, extensions)

    filtered_files = filter_files(file_paths, ignore_patterns)

    return filtered_files

# imgs_path = input("Enter the path to the images folder: ").strip().strip('"')
# for img in collect_files(imgs_path):
#     print(img)
