import os
import json
import pandas as pd
import time
import requests
import argparse
import tempfile
import shutil
import subprocess
import urllib3
from typing import Dict, List, Any
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class SVNConfigTableConverter:
    def __init__(self, svn_url: str, svn_username: str = None, svn_password: str = None):
        self.supported_formats = ['.xlsx', '.xls']
        self.svn_url = svn_url.rstrip('/')

        # 保存认证信息
        self.svn_username = svn_username
        self.svn_password = svn_password

        # 创建临时工作目录
        self.temp_dir = tempfile.mkdtemp(prefix="svn_config_")
        print(f"临时工作目录: {self.temp_dir}")

        # 检出SVN仓库到临时目录
        self._svn_checkout()

    def _run_svn_command(self, args: List[str]) -> bool:
        """运行SVN命令"""
        try:
            cmd = ['svn'] + args

            if self.svn_username and self.svn_password:
                cmd.extend(['--username', self.svn_username, '--password', self.svn_password, '--non-interactive'])

            result = subprocess.run(cmd, check=True, capture_output=True, text=True, cwd=self.temp_dir)
            return True
        except subprocess.CalledProcessError as e:
            print(f"SVN命令失败: {' '.join(cmd)}")
            print(f"错误输出: {e.stderr}")
            return False
        except Exception as e:
            print(f"执行SVN命令时出错: {e}")
            return False

    def _svn_checkout(self):
        """检出SVN仓库到临时目录"""
        try:
            print(f"正在检出SVN仓库: {self.svn_url}")
            if not self._run_svn_command(['checkout', self.svn_url, '.']):
                raise Exception("SVN检出失败")
            print("SVN检出完成")
        except Exception as e:
            print(f"SVN检出失败: {e}")
            raise

    def _svn_add(self, file_path: str):
        """添加文件到SVN"""
        try:
            if self._is_path_in_svn(file_path):
                return
            if not self._run_svn_command(['add', file_path]):
                print(f"SVN添加文件失败: {file_path}")
            else:
                print(f"已添加文件到SVN: {file_path}")
        except Exception as e:
            print(f"SVN添加文件失败 {file_path}: {e}")

    def _svn_commit(self, message: str):
        """提交更改到SVN"""
        try:
            if not self._run_svn_command(['commit', '-m', message]):
                raise Exception("SVN提交失败")
            print(f"已提交更改到SVN: {message}")
        except Exception as e:
            print(f"SVN提交失败: {e}")
            raise

    def _svn_update(self):
        """更新SVN工作副本"""
        try:
            if not self._run_svn_command(['update']):
                raise Exception("SVN更新失败")
            print("SVN更新完成")
        except Exception as e:
            print(f"SVN更新失败: {e}")

    # 从这里开始，以下所有代码都保持原样，没有任何修改
    def get_svn_file_path(self, relative_path: str) -> str:
        """获取SVN工作副本中的文件完整路径"""
        return os.path.join(self.temp_dir, relative_path.lstrip('/'))

    def parse_config_table(self, svn_relative_path: str) -> Dict[str, Any]:
        """从SVN解析配置表格式"""
        try:
            # 先更新确保是最新版本
            self._svn_update()

            file_path = self.get_svn_file_path(svn_relative_path)

            # 检查文件是否存在且可读
            if not os.path.exists(file_path):
                return {"error": f"SVN文件不存在: {svn_relative_path}"}

            if not os.access(file_path, os.R_OK):
                return {"error": f"SVN文件不可读: {svn_relative_path}"}

            # 等待文件完全写入（如果文件正在被其他进程写入）
            file_size = -1
            for _ in range(5):  # 最多尝试5次
                current_size = os.path.getsize(file_path)
                if current_size == file_size:
                    break
                file_size = current_size
                time.sleep(0.1)

            # 读取Excel文件
            try:
                df = pd.read_excel(file_path, header=None, engine='openpyxl')
            except:
                df = pd.read_excel(file_path, header=None, engine='xlrd')

            # 检查数据是否足够
            if len(df) < 5:
                return {"error": f"文件行数不足，至少需要5行，实际只有{len(df)}行"}

            # 提取关键信息（保持原有逻辑不变）
            data_type_row = df.iloc[0]  # 类型行
            platform_row = df.iloc[1]  # 平台行
            desc_row = df.iloc[2]  # 描述行
            field_name_row = df.iloc[3]  # 字段名行
            data_rows = df.iloc[4:]  # 数据行

            # 构建表结构信息
            table_info = {
                "file_name": os.path.basename(file_path),
                "svn_path": svn_relative_path,
                "columns": [],
                "data": []
            }

            # 处理列信息
            for i, (data_type, platform, desc, field_name) in enumerate(zip(
                    data_type_row, platform_row, desc_row, field_name_row
            )):
                table_info["columns"].append({
                    "index": i,
                    "field_name": str(field_name).strip(),
                    "data_type": str(data_type).strip() if pd.notna(data_type) else "string",
                    "platform": str(platform).strip() if pd.notna(platform) else "Both",
                    "description": str(desc).strip() if pd.notna(desc) else ""
                })

            # 如果没有找到有效列，返回错误
            if not table_info["columns"]:
                return {"error": "未找到有效的列定义"}

            # 处理数据行
            for row_idx, row in data_rows.iterrows():
                # 检查第一列是否为空（通常是ID列）
                item = {}
                for col_info in table_info["columns"]:
                    idx = col_info["index"]
                    if idx < len(row):
                        value = row.iloc[idx] if pd.notna(row.iloc[idx]) else None
                        item[col_info["field_name"]] = self._convert_value(value, col_info["data_type"])
                    else:
                        item[col_info["field_name"]] = self._get_default_value(col_info["data_type"])
                table_info["data"].append(item)

            print(
                f"成功解析SVN文件: {svn_relative_path}, 找到 {len(table_info['columns'])} 列, {len(table_info['data'])} 行数据")
            return table_info

        except Exception as e:
            return {"error": f"解析表格失败: {str(e)}"}

    def _convert_value(self, value, data_type: str) -> Any:
        """根据数据类型转换值"""
        if value is None or value == '':
            return self._get_default_value(data_type)

        try:
            data_type = data_type.lower().strip()
            str_value = str(value).strip()

            if data_type == 'int':
                return int(float(str_value)) if str_value else 0
            elif data_type == 'float':
                return float(str_value) if str_value else 0.0
            elif data_type == 'bool':
                if isinstance(str_value, str):
                    return str_value.lower() in ('true', '1', 'yes', '是', 't')
                return bool(str_value)
            elif data_type == 'string':
                return str_value
            elif data_type == "array_string":
                return str_value.split("|") if str_value and str_value != "" else []
            elif data_type == "array_int" or data_type == "array_ulong":
                return [int(x) for x in str_value.split("|")] if str_value and str_value != "" else []
            elif data_type == "array_float":
                return [float(x) for x in str_value.split("|")] if str_value and str_value != "" else []
            else:
                # 处理复杂类型如 "1:1,2:0,3:0"
                return str_value
        except (ValueError, TypeError) as e:
            print(f"值转换警告: 将值 '{value}' 转换为类型 '{data_type}' 时出错: {e}")
            return str(value)

    def _get_default_value(self, data_type: str) -> Any:
        data_type = data_type.lower().strip()
        if data_type in ['int', 'long', 'ulong']:
            return 0
        elif data_type == 'float':
            return 0.0
        elif data_type == 'bool':
            return False
        elif data_type == 'string':
            return ""
        elif data_type.startswith('array'):
            return []  # 所有数组类型默认返回空列表
        else:
            return ""

    def _map_to_programming_type(self, data_type: str, language: str) -> str:
        """映射到编程语言类型"""
        type_mappings = {
            'python': {
                'int': 'int',
                'float': 'float',
                'bool': 'bool',
                'string': 'str',
                "array_string": "list",
                "array_ulong": "list",
                "array_int": "list",
                "array_float": "list"
            },
            'java': {
                'int': 'int',
                'float': 'float',
                'bool': 'boolean',
                'string': 'String',
                "array_string": "List<String>",
                "array_ulong": "List<Long>",
                "array_int": "List<Integer>",
                "array_float": "List<Float>"
            },
            'csharp': {
                'int': 'int',
                'float': 'float',
                'bool': 'bool',
                'string': 'string',
                "array_string": "List<string>",
                "array_ulong": "List<ulong>",
                "array_int": "List<int>",
                "array_float": "List<float>"
            }
        }

        base_type = data_type.lower()
        mapping = type_mappings.get(language, type_mappings['python'])
        return mapping.get(base_type, mapping['string'])

    def generate_python_class(self, class_name: str, columns: List[Dict]) -> str:
        """生成Python类"""
        class_code = f"class {class_name}:\n"
        class_code += '    """配置表数据类"""\n\n'

        # 添加构造函数
        init_params = []
        for col in columns:
            py_type = self._map_to_programming_type(col["data_type"], "python")
            default_value = self._get_default_value(col["data_type"])
            if py_type == 'str':
                default_value = f'"{default_value}"'
            elif py_type == 'bool':
                default_value = 'False' if not default_value else 'True'
            init_params.append(f"{col['field_name']}: {py_type} = {default_value}")

        class_code += f"    def __init__(self, {', '.join(init_params)}):\n"

        # 添加属性赋值和注释
        for col in columns:
            comment = f"  # {col['description']} ({col['platform']})"
            class_code += f"        self.{col['field_name']} = {col['field_name']}{comment}\n"

        # 添加to_dict方法
        class_code += "\n    def to_dict(self) -> dict:\n"
        class_code += "        \"\"\"转换为字典\"\"\"\n"
        class_code += "        return {\n"
        for col in columns:
            class_code += f"            '{col['field_name']}': self.{col['field_name']},\n"
        class_code += "        }\n"

        # 添加from_dict方法
        class_code += "\n    @classmethod\n"
        class_code += f"    def from_dict(cls, data: dict) -> '{class_name}':\n"
        class_code += "        \"\"\"从字典创建实例\"\"\"\n"
        class_code += "        return cls(\n"
        for col in columns:
            class_code += f"            {col['field_name']}=data.get('{col['field_name']}', {self._get_default_value(col['data_type'])}),\n"
        class_code += "        )\n"

        # 添加__str__方法
        class_code += "\n    def __str__(self) -> str:\n"
        # 尝试找到ID和Name字段
        id_field = next((col for col in columns if 'id' in col['field_name'].lower()), columns[0])
        name_field = next((col for col in columns if 'name' in col['field_name'].lower()),
                          columns[1] if len(columns) > 1 else columns[0])
        class_code += f'        return f"{class_name}({id_field["field_name"]}={{self.{id_field["field_name"]}}}, {name_field["field_name"]}={{self.{name_field["field_name"]}}})"\n'

        return class_code

    def generate_java_class(self, class_name: str, columns: List[Dict]) -> str:
        """生成Java类"""
        class_code = f"public class {class_name} {{\n\n"

        # 添加字段
        for col in columns:
            java_type = self._map_to_programming_type(col["data_type"], "java")
            comment = f"// {col['description']} ({col['platform']})"
            if col['field_name'] == "字段名" or col['field_name'].lower() == "id":
                continue
            if col['platform'] == "Client":
                continue
            class_code += f"    private {java_type} {col['field_name']}; {comment}\n"
        class_code += "    }\n"

        return class_code

    def generate_csharp_class(self, class_name: str, columns: List[Dict]) -> str:
        """生成C#类"""
        class_code = f"using System.Collections.Generic;\n\n"
        class_code += f"public class {class_name}:BaseWebTable \n{{\n"

        # 添加属性
        for col in columns:
            csharp_type = self._map_to_programming_type(col["data_type"], "csharp")
            prop_name = col['field_name'][0].upper() + col['field_name'][1:]
            if prop_name == "字段名" or col['field_name'].lower() == "id":
                continue
            if col['platform'] == "Server":
                continue
            comment = f"// {col['description']} ({col['platform']})"
            class_code += f"    public {csharp_type} {prop_name} {{ get; set; }} {comment}\n"

        class_code += "}"
        return class_code

    def generate_data_manager(self, class_name: str, table_info: Dict) -> str:
        """生成数据管理类（Python版本）"""
        manager_code = f"class {class_name}Manager:\n"
        manager_code += f'    """{class_name}配置表数据管理器"""\n\n'
        manager_code += "    def __init__(self):\n"
        manager_code += "        self._data_dict = {}\n"
        manager_code += "        self._load_data()\n\n"

        manager_code += "    def _load_data(self):\n"
        manager_code += "        \"\"\"加载数据\"\"\"\n"
        manager_code += "        # 这里应该从JSON文件或数据库加载数据\n"
        manager_code += "        # 示例数据\n"
        manager_code += "        raw_data = [\n"

        # 添加一些示例数据
        if table_info["data"]:
            for i, item in enumerate(table_info["data"][:2]):  # 只显示前2个作为示例
                manager_code += f"            {item},\n"
        manager_code += "        ]\n\n"

        manager_code += "        for item_data in raw_data:\n"
        manager_code += f"            item = {class_name}.from_dict(item_data)\n"
        # 假设第一个字段是ID
        id_field = table_info["columns"][0]["field_name"]
        manager_code += f"            self._data_dict[item.{id_field}] = item\n\n"

        manager_code += f"    def get_by_id(self, item_id: int) -> {class_name}:\n"
        manager_code += f"        \"\"\"根据ID获取{class_name}\"\"\"\n"
        manager_code += "        return self._data_dict.get(item_id)\n\n"

        manager_code += f"    def get_all(self) -> list[{class_name}]:\n"
        manager_code += f"        \"\"\"获取所有{class_name}\"\"\"\n"
        manager_code += "        return list(self._data_dict.values())\n\n"

        manager_code += f"    def get_by_condition(self, condition_func) -> list[{class_name}]:\n"
        manager_code += f"        \"\"\"根据条件筛选{class_name}\"\"\"\n"
        manager_code += "        return [item for item in self._data_dict.values() if condition_func(item)]\n\n"

        # 创建单例实例
        manager_code += f"\n# 全局数据管理器实例\n{class_name.lower()}_manager = {class_name}Manager()\n"

        return manager_code

    def _is_path_in_svn(self, path: str) -> bool:
        """检查路径是否已经在SVN版本控制下"""
        try:
            # 使用svn status命令检查
            result = subprocess.run(
                ['svn', 'status', path],
                capture_output=True,
                text=True,
                cwd=self.temp_dir
            )
            # 如果路径在SVN控制下，status命令会有特定输出
            # 如果路径不在SVN控制下，通常会有"?"标记
            return "?" not in result.stdout
        except:
            return False
    def upload_to_baota(self, table_name: str, data: List[Dict]) -> bool:
        try:
            # 宝塔API配置 - 请根据您的宝塔面板配置修改这些参数
            baota_base_url = "https://192.140.167.88:16598"  # 宝塔面板基础地址
            baota_path = "/2d4be7b7"  # 宝塔面板路径前缀
            api_key = "QPfx0tToX96wJfcUDO8LE4wcIBsjZtXr"  # 宝塔API密钥
            site_name = "192.140.167.88"  # 网站名称
            upload_path = "/www/wwwroot/RedMoon_3/GameTableConfig"  # 上传路径

            # 构建请求数据
            json_data = json.dumps(data, ensure_ascii=False, indent=2)
            
            import hashlib
            import time
            
            # 生成宝塔API认证参数
            request_time = str(int(time.time()))
            request_token = hashlib.md5((request_time + hashlib.md5(api_key.encode()).hexdigest()).encode()).hexdigest()

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'
            }

            # 正确的宝塔API端点 - 使用文件上传接口
            api_endpoint = f"{baota_base_url}{baota_path}/files?action=upload"
            
            print(f"正在上传到宝塔API: {api_endpoint}")
            print(f"目标路径: {upload_path}/{table_name}.json")

            # 准备文件数据
            file_content = json_data.encode('utf-8')
            file_size = len(file_content)

            # 上传数据到宝塔
            response = requests.post(
                api_endpoint,
                headers=headers,
                data={
                    'f_path': upload_path,
                    'f_name': f'{table_name}.json',
                    'f_size': str(file_size),
                    'f_start': '0',
                    'request_time': request_time,
                    'request_token': request_token
                },
                files={'blob': (f'{table_name}.json', file_content, 'application/json')},
                verify=False,
                timeout=30
            )

            print(f"宝塔API响应状态码: {response.status_code}")
            print(f"宝塔API响应内容: {response.text}")

            if response.status_code == 200:
                result = response.json()
                if result.get('status') == True:
                    print(f"成功上传 {table_name}.json 到宝塔")
                    return True
                else:
                    print(f"宝塔API返回错误: {result.get('msg', '未知错误')}")
                    return False
            else:
                print(f"宝塔API返回错误: {response.status_code} - {response.text}")
                return False

        except requests.exceptions.RequestException as e:
            print(f"宝塔API网络请求失败: {e}")
            return False
        except json.JSONDecodeError as e:
            print(f"宝塔API响应JSON解析失败: {e}")
            return False
        except Exception as e:
            print(f"上传到宝塔失败: {e}")
            return False

    def process_svn_folder(self, svn_relative_folder: str, output_csharp_dir: str = "output_csharp", output_java_dir: str = "output_java",
                           target_language: str = "all", generate_manager: bool = True,
                           commit_message: str = "Auto-generated config files") -> Dict[str, Any]:
        """处理SVN文件夹中的所有配置表文件"""
        results = {}

        # 获取SVN中的完整路径
        svn_input_dir = self.get_svn_file_path(svn_relative_folder)
        svn_output_csharp = self.get_svn_file_path(output_csharp_dir)
        svn_output_java = self.get_svn_file_path(output_java_dir)
        self._svn_add(svn_output_csharp)
        self._svn_add(svn_output_java)

        # 检查输入文件夹是否存在
        if not os.path.exists(svn_input_dir):
            print(f"错误: SVN输入文件夹不存在 - {svn_relative_folder}")
            return results

        # 创建输出目录
        os.makedirs(svn_output_csharp, exist_ok=True)
        os.makedirs(svn_output_java, exist_ok=True)

        # 确保输出目录被添加到SVN（关键修复）
        try:
            # 先检查输出目录是否已经在SVN控制下
            if not self._is_path_in_svn(svn_output_csharp):
                # 如果不在SVN控制下，先添加整个输出目录
                print(f"添加输出目录到SVN: {svn_output_csharp}")
                self._run_svn_command(['add', svn_output_csharp])
            if not self._is_path_in_svn(svn_output_java):
                # 如果不在SVN控制下，先添加整个输出目录
                print(f"添加输出目录到SVN: {svn_output_java}")
                self._run_svn_command(['add', svn_output_java])
        except Exception as e:
            print(f"添加输出目录到SVN失败: {e}")

        # 遍历SVN文件夹
        file_count = 0
        for filename in os.listdir(svn_input_dir):
            file_path = os.path.join(svn_input_dir, filename)
            svn_relative_path = os.path.join(svn_relative_folder, filename)

            if os.path.isfile(file_path) and any(filename.lower().endswith(ext) for ext in self.supported_formats):
                print(f"\n正在处理SVN文件: {svn_relative_path}")
                file_count += 1

                # 解析配置表
                table_info = self.parse_config_table(svn_relative_path)

                if "error" in table_info:
                    print(f"解析失败: {table_info['error']}")
                    results[filename] = {"error": table_info["error"]}
                    continue

                # 生成类名（基于文件名）
                class_name = os.path.splitext(filename)[0]

                file_results = {
                    "table_info": table_info,
                    "generated_files": []
                }

                # 生成类文件
                try:
                    # # Python类
                    # if target_language in ['all', 'python']:
                    #     py_code = self.generate_python_class(class_name, table_info["columns"])
                    #     py_file = os.path.join(svn_output_dir, f"{class_name}.py")
                    #     with open(py_file, 'w', encoding='utf-8') as f:
                    #         f.write(py_code)
                    #     self._svn_add(py_file)
                    #     file_results["generated_files"].append(py_file)
                    #     print(f"生成Python类: {py_file}")
                    #
                    #     # 生成数据管理器
                    #     if generate_manager:
                    #         manager_code = self.generate_data_manager(class_name, table_info)
                    #         manager_file = os.path.join(svn_output_dir, f"{class_name.lower()}_manager.py")
                    #         with open(manager_file, 'w', encoding='utf-8') as f:
                    #             f.write(manager_code)
                    #         self._svn_add(manager_file)
                    #         file_results["generated_files"].append(manager_file)
                    #         print(f"生成数据管理器: {manager_file}")

                    # Java类
                    if target_language in ['all', 'java']:
                        java_code = self.generate_java_class(class_name, table_info["columns"])
                        java_file = os.path.join(svn_output_java, f"{class_name}.java")
                        with open(java_file, 'w', encoding='utf-8') as f:
                            f.write(java_code)
                        self._svn_add(java_file)
                        file_results["generated_files"].append(java_file)
                        print(f"生成Java类: {java_file}")

                    # C#类
                    if target_language in ['all', 'csharp']:
                        csharp_code = self.generate_csharp_class(class_name, table_info["columns"])
                        csharp_file = os.path.join(svn_output_csharp, f"{class_name}.cs")
                        with open(csharp_file, 'w', encoding='utf-8') as f:
                            f.write(csharp_code)
                        self._svn_add(csharp_file)
                        file_results["generated_files"].append(csharp_file)
                        print(f"生成C#类: {csharp_file}")

                    # 生成JSON数据文件
                    try:
                        # 准备要上传的数据
                        filtered_data = [{
                            key: value for key, value in item.items() if key != "字段名"
                        } for item in table_info["data"] if item.get("字段名") != "#"]

                        # 上传到宝塔
                        if self.upload_to_baota(class_name, filtered_data):
                            print(f"成功上传数据到宝塔: {class_name}")
                            file_results["generated_files"].append(f"宝塔:{class_name}.json")
                        else:
                            print(f"上传数据到宝塔失败: {class_name}")
                    except Exception as e:
                        print(f"上传数据到宝塔时出错: {e}")

                except Exception as e:
                    print(f"生成文件时出错: {e}")
                    file_results["error"] = str(e)

                results[filename] = file_results

        # 提交所有更改到SVN
        if file_count > 0:
            try:
                self._svn_commit(commit_message)
                print(f"已提交所有更改到SVN: {commit_message}")
            except Exception as e:
                print(f"提交到SVN失败: {e}")

        if file_count == 0:
            print(f"在SVN文件夹 {svn_relative_folder} 中未找到支持的Excel文件")

        return results

    def __del__(self):
        """清理临时目录"""
        if hasattr(self, 'temp_dir') and os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
                print(f"已清理临时目录: {self.temp_dir}")
            except Exception as e:
                print(f"清理临时目录时出错: {e}")


def main():
    parser = argparse.ArgumentParser(description='SVN游戏配置表转换工具')
    parser.add_argument('svn_url', help='SVN仓库URL')
    parser.add_argument('svn_folder', help='SVN中配置表文件夹的相对路径')
    parser.add_argument('-oc', '--output_csharp', default='output_csharp', help='SVN中输出csharp的相对路径')
    parser.add_argument('-oj', '--output_java', default='output_java', help='SVN中输出java的相对路径')
    parser.add_argument('-l', '--language', choices=['python', 'java', 'csharp', 'all'],
                        default='all', help='目标编程语言')
    parser.add_argument('--no-manager', action='store_true', help='不生成数据管理器')
    parser.add_argument('--username', help='SVN用户名')
    parser.add_argument('--password', help='SVN密码')
    parser.add_argument('--commit-message', default='Auto-generated config files',
                        help='SVN提交消息')

    test_args = [
        'http://192.168.9.115:8080/svn/RedMoon3/RedMoon/',  # svn_url
        './Config',  # svn_folder
        '-oc', './Client/Assets/ClientGame/Scripts/DataTable/Web/',  # output_csharp
        '-oj', './Server/common/common-core/src/main/java/com/iohao/redmoon/common/entity/',  # output_csharp
        '-l', 'all',  # language
        '--username', 'shizejiang',
        '--password', '123456',
        '--commit-message', "配表生成"
    ]

    args = parser.parse_args(test_args)

    converter = SVNConfigTableConverter(
        svn_url=args.svn_url,
        svn_username=args.username,
        svn_password=args.password
    )

    results = converter.process_svn_folder(
        svn_relative_folder=args.svn_folder,
        output_csharp_dir=args.output_csharp,
        output_java_dir=args.output_java,
        target_language=args.language,
        generate_manager=not args.no_manager,
        commit_message=args.commit_message
    )

    print(f"\n处理完成！共处理 {len(results)} 个文件")
    print(f"SVN输出目录: {args.output_csharp}, {args.output_java}")

    # 显示处理结果摘要
    success_count = sum(1 for r in results.values() if "error" not in r)
    error_count = len(results) - success_count

    print(f"成功: {success_count}, 失败: {error_count}")


if __name__ == "__main__":
    main()