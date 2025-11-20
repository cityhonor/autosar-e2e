import json
import argparse
from datetime import datetime

def load_json_config(config_path):
    """加载JSON配置文件"""
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"错误：配置文件 {config_path} 未找到")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"错误：解析JSON配置失败 - {e}")
        exit(1)

def generate_header_guard(filename):
    """生成头文件保护宏"""
    return f"_{filename.upper().replace('.', '_')}_"

def generate_c_code(config):
    """根据配置生成C代码"""
    code = []
    
    # 生成文件头部注释
    code.append(f"/*")
    code.append(f" * 自动生成的C代码")
    code.append(f" * 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    code.append(f" * 配置文件: {config.get('config_file', 'unknown')}")
    code.append(f" */")
    code.append("")
    
    # 生成头文件包含
    includes = config.get('includes', [])
    for include in includes:
        if include.startswith('<'):
            code.append(f"#include {include}")
        else:
            code.append(f'#include "{include}"')
    if includes:
        code.append("")
    
    # 生成宏定义
    defines = config.get('defines', {})
    for name, value in defines.items():
        code.append(f"#define {name} {value}")
    if defines:
        code.append("")
    
    # 生成类型定义
    typedefs = config.get('typedefs', [])
    for typedef in typedefs:
        code.append(f"typedef {typedef['type']} {typedef['name']};")
    if typedefs:
        code.append("")
    
    # 生成结构体定义
    structs = config.get('structs', [])
    for struct in structs:
        code.append(f"typedef struct {struct['name']} {{")
        for member in struct['members']:
            code.append(f"    {member['type']} {member['name']};")
        code.append(f"}} {struct['name']};")
        code.append("")
    
    # 生成枚举定义
    enums = config.get('enums', [])
    for enum in enums:
        code.append(f"typedef enum {enum['name']} {{")
        for member in enum['members']:
            if 'value' in member:
                code.append(f"    {member['name']} = {member['value']},")
            else:
                code.append(f"    {member['name']},")
        code.append(f"}} {enum['name']};")
        code.append("")
    
    # 生成函数原型
    functions = config.get('functions', [])
    for func in functions:
        return_type = func.get('return_type', 'void')
        params = ', '.join([f"{p['type']} {p['name']}" for p in func.get('params', [])])
        code.append(f"{return_type} {func['name']}({params});")
    if functions:
        code.append("")
    
    # 生成函数实现
    implementations = config.get('implementations', [])
    for impl in implementations:
        return_type = impl.get('return_type', 'void')
        params = ', '.join([f"{p['type']} {p['name']}" for p in impl.get('params', [])])
        code.append(f"{return_type} {impl['name']}({params}) {{")
        
        # 添加函数体内容
        body = impl.get('body', [])
        for line in body:
            code.append(f"    {line}")
        
        # 如果有返回值，添加默认返回
        if return_type != 'void' and not any(line.startswith('return') for line in body):
            if return_type in ['int', 'long', 'float', 'double']:
                code.append(f"    return 0;")
            elif return_type.endswith('*'):
                code.append(f"    return NULL;")
        
        code.append("}")
        code.append("")
    
    return '\n'.join(code)

def generate_header_file(config):
    """生成头文件内容"""
    header_code = []
    
    # 生成头文件保护
    header_filename = config.get('header_filename', 'generated.h')
    guard = generate_header_guard(header_filename)
    header_code.append(f"#ifndef {guard}")
    header_code.append(f"#define {guard}")
    header_code.append("")
    
    # 添加头文件包含
    includes = config.get('header_includes', [])
    for include in includes:
        if include.startswith('<'):
            header_code.append(f"#include {include}")
        else:
            header_code.append(f'#include "{include}"')
    if includes:
        header_code.append("")
    
    # 添加类型定义、结构体、枚举
    # 这些内容通常同时出现在头文件和源文件中
    typedefs = config.get('typedefs', [])
    for typedef in typedefs:
        header_code.append(f"typedef {typedef['type']} {typedef['name']};")
    if typedefs:
        header_code.append("")
    
    structs = config.get('structs', [])
    for struct in structs:
        header_code.append(f"typedef struct {struct['name']} {{")
        for member in struct['members']:
            header_code.append(f"    {member['type']} {member['name']};")
        header_code.append(f"}} {struct['name']};")
        header_code.append("")
    
    enums = config.get('enums', [])
    for enum in enums:
        header_code.append(f"typedef enum {enum['name']} {{")
        for member in enum['members']:
            if 'value' in member:
                header_code.append(f"    {member['name']} = {member['value']},")
            else:
                header_code.append(f"    {member['name']},")
        header_code.append(f"}} {enum['name']};")
        header_code.append("")
    
    # 添加函数原型
    functions = config.get('functions', [])
    for func in functions:
        return_type = func.get('return_type', 'void')
        params = ', '.join([f"{p['type']} {p['name']}" for p in func.get('params', [])])
        header_code.append(f"{return_type} {func['name']}({params});")
    if functions:
        header_code.append("")
    
    header_code.append(f"#endif // {guard}")
    
    return '\n'.join(header_code)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='根据JSON配置生成C代码')
    parser.add_argument('config', help='JSON配置文件路径')
    parser.add_argument('--output', help='输出C文件路径', default='generated.c')
    parser.add_argument('--header', help='输出头文件路径', default='generated.h')
    args = parser.parse_args()
    
    # 加载配置
    config = load_json_config(args.config)
    config['config_file'] = args.config
    
    # 生成C代码
    c_code = generate_c_code(config)
    with open(args.output, 'w') as f:
        f.write(c_code)
    print(f"C代码已生成: {args.output}")
    
    # 生成头文件
    header_code = generate_header_file(config)
    with open(args.header, 'w') as f:
        f.write(header_code)
    print(f"头文件已生成: {args.header}")

if __name__ == "__main__":
    main()