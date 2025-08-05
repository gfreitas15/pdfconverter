import PyInstaller.__main__

PyInstaller.__main__.run([
    'rename.py',
    '--onefile',
    '--windowed',
    '--name=MonitorPDF',
    '--icon=icon.ico',
    '--add-data=requirements.txt;.',
    '--add-data=icon.ico;.'
]) 