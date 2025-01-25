# README

## 简介 / Introduction

`collect_files` 是一个 Python 工具方法。输入一个路径后，方法会递归遍历该路径及其子目录，收集所有符合条件的文件并返回它们的绝对路径列表。同时支持通过类似 `.gitignore` 的方式，使用自定义忽略文件动态排除某些文件或目录。  
`collect_files` is a Python utility function. Given a directory path, it recursively traverses the directory and its subdirectories, collecting all matching files and returning their absolute paths. It also supports dynamically excluding files or directories using custom ignore files, similar to `.gitignore`.


## 方法 / Method

### `collect_files(directory)`

- **参数 / Parameters**:
    - `directory` (str): 要遍历的目标目录路径。  
      The target directory path to search.

- **返回值 / Returns**:
    - (list): 收集到的文件绝对路径列表。  
      A list of absolute paths to the collected files.

- **功能描述 / Description**:
    - 递归遍历指定目录及其子目录。  
      Recursively traverses the specified directory and its subdirectories.
    - 根据配置文件中的扩展名规则收集文件。  
      Collects files based on file extension rules.
    - 通过忽略文件中的规则过滤文件。  
      Filters files based on rules specified in custom ignore files.



## 配置文件 / Configuration File

1. 创建一个名为 `config.txt` 的文件，放置在脚本的同目录下。  
   Create a file named `config.txt` and place it in the same directory as the script.

2. 配置文件格式示例 / Example configuration format:
   ```txt  
   # 要收集的文件类型扩展名（例如图片文件类型）  
   # File types to collect (e.g., image file types)  
   EXTENSIONS:.png,.jpg,.jpeg  

   # 自定义忽略文件的扩展名  
   # Custom ignore file extensions  
   CUSTOM_IGNORE_EXT:.pnpignore  
   ```  



## 自定义忽略文件规则 / Custom Ignore File Rules

您可以在自定义忽略文件（如 `.pnpignore`）中定义以下规则来动态排除文件或目录：  
You can define the following rules in custom ignore files (e.g., `.pnpignore`) to dynamically exclude files or directories:

1. **忽略特定文件 / Ignore specific files**  
   使用绝对路径或相对路径指定文件，例如：  
   Use absolute or relative paths to specify files, e.g.:
   ```txt  
   /absolute/path/to/ignored_file.png  
   relative/path/to/ignored_file.jpg  
   ```  

2. **忽略整个目录中的所有文件 / Ignore all files in a directory**  
   使用通配符 `*`，例如：  
   使用 `*` 符号来忽略整个目录下的所有文件，请确保该符号正确放置，例如：  
   **不要忘记使用 `*` 来匹配所有文件！**  
   Use the `*` symbol to ignore all files in a directory. Make sure to place the symbol correctly, e.g.:  
   **Don’t forget to use `*` to match all files!**
   ```txt  
   directory/*  
   ```  

3. **注释 / Comments**  
   使用 `#` 开头的行表示注释，例如：  
   Use lines starting with `#` for comments, e.g.:
   ```txt  
   # 忽略规则示例 / Example ignore rules  
   ```  

### 匹配策略实现位置 / Location of Matching Strategy

忽略文件的匹配策略通过 `fnmatch` 模块实现，位于 `should_ignore` 方法中。如果需要修改匹配逻辑，可以编辑该方法。  
The matching strategy for ignore files is implemented using `fnmatch` in the `should_ignore` method. To modify the matching logic, you can edit this method.

```python  
def should_ignore(file_path, ignore_patterns):  
    file_path = normalize_path(file_path)  
    for pattern in ignore_patterns:  
        if fnmatch.fnmatch(file_path.lower(), pattern.lower()):  
            return True  
    return False  
```



## 示例 / Example

假设以下文件结构：  
Given the following file structure:
```
example_directory/  
├── file1.png  
├── file2.jpg  
├── ignore_this.jpeg  
├── .pnpignore  
└── subfolder/  
    ├── file3.jpeg  
    ├── file4.png  
    └── another.pnpignore  
```  

配置文件 `config.txt` 的内容为：  
The `config.txt` file contains:
```txt  
EXTENSIONS:.png,.jpg,.jpeg  
CUSTOM_IGNORE_EXT:.pnpignore  
```  


`.pnpignore` 文件内容为：  
The `.pnpignore` file contains:

```python 
# 绝对路径忽略特定文件 / Ignore specific files by absolute path
example_directory/ignore_this.jpeg  

# 相对路径忽略整个目录中的所有文件 / Ignore all files in a directory by relative path
subfolder/*
```  

运行以下代码：  
Running the following code:
```python  
valid_files = collect_files("example_directory")  
print(valid_files)
```  

输出结果可能为：  
The output may be:
```
['example_directory/file1.png', 'example_directory/file2.jpg']  
```  



## License

此代码基于 MIT 协议发布，您可以自由使用、修改和分发。  
This code is released under the MIT license, and you are free to use, modify, and distribute it.
