# run yara rules on a file with terminal
import subprocess


def apply_rule(file_path, rules_path):
    file_name = file_path.split('/')[-1]
    print(file_path)
    print(rules_path)
    result = subprocess.run(['yara64', '-r', rules_path, file_path], capture_output=True, text=True)
    print([result.stdout.replace(file_name, '').strip()])


apply_rule('bad.txt', 'rules/mimikatz.yara')
