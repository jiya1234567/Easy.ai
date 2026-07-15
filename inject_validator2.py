"""inject_validator2.py -- injects validation_upload_panel before COMMAND CENTER tab"""
lines = open('streamlit_app.py', encoding='utf-8').readlines()

# Find the correct injection point - line before # 2. COMMAND CENTER
target = None
for i, line in enumerate(lines):
    if '# 2. COMMAND CENTER' in line or ('COMMAND CENTER' in line and line.strip().startswith('#')):
        target = i
        break

if target is None:
    print('Could not find COMMAND CENTER comment - searching for active_tab COMMAND CENTER')
    for i, line in enumerate(lines):
        if 'active_tab ==' in line and 'COMMAND CENTER' in line:
            target = i - 1
            break

if target is None:
    print('ERROR: Could not find injection point')
else:
    inject = [
        '\n',
        '    from manual_validator import validation_upload_panel\n',
        '    validation_upload_panel(get_harness_v2()["reality"], get_harness_v2()["calibration"])\n',
        '\n',
    ]
    for j, line in enumerate(inject):
        lines.insert(target + j, line)
    open('streamlit_app.py', 'w', encoding='utf-8').writelines(lines)
    print(f'Injected at line {target+1}')
