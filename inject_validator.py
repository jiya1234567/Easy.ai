"""inject_validator.py -- run once to wire manual_validator into Discovery Dashboard tab"""
lines = open('streamlit_app.py', encoding='utf-8').readlines()
inject = '    from manual_validator import validation_upload_panel; validation_upload_panel(get_harness_v2()["reality"], get_harness_v2()["calibration"])\n'
lines.insert(2068, inject)
open('streamlit_app.py', 'w', encoding='utf-8').writelines(lines)
print('Injected at line 2069')
