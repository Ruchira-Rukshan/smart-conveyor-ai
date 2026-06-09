import os
import sys
import streamlit.web.cli as stcli

if __name__ == '__main__':
    # Determine path of the executable
    if getattr(sys, 'frozen', False):
        dir_path = sys._MEIPASS
    else:
        dir_path = os.path.dirname(os.path.abspath(__file__))
    
    # Path to the actual app.py inside the package
    app_path = os.path.join(dir_path, "app.py")
    
    # Run streamlit server targeting app.py
    sys.argv = ["streamlit", "run", app_path, "--global.developmentMode=false"]
    sys.exit(stcli.main())
