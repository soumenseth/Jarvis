SCRIPT_EXTENSION = {
    "win32": ".cmd",
    "ubuntu": ".sh"
}

SCRIPT_COMMAND = {
    "win32": {
        "open_terminal": "start powershell.exe",
        "open_projects": "start C:\\Users\\SOUMEN\\Projects",
        "create_folder": "mkdir"
    },
    "ubuntu": {
        "open_terminal": ""
    }
}

KEYWORDS_SUBJECT = {
    "terminal": ["terminal", "power shell", "powershell", "bash"],
    "projects": ["projects", "project"],
    "folder": ["folder"]
}

KEYWORDS_COMMAND = {
    "open": ["open", "start"],
    "create": ["create"],
    "delete": ["delete"],
    "cut": ["cut"],
    "copy": ["copy"],
    "paste": ["paste"]
}
