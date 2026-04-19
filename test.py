import os

def create_init_files():
    # Paths based on the project structure in README.md
    # The root folder is gym_site, containing apps and config
    structure = [
        'gym_site',                 # Root project folder
        'gym_site/gym_site',        # Project configuration folder
        'gym_site/accounts',        # accounts app
        'gym_site/accounts/services',
        'gym_site/templates'        # global templates
    ]

    # Directories that should be Python packages (contain __init__.py)
    package_paths = [
        'gym_site/gym_site',
        'gym_site/accounts',
        'gym_site/accounts/services'
    ]

    for path in structure:
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"Created directory: {path}")

        if path in package_paths:
            init_file = os.path.join(path, '__init__.py')
            if not os.path.exists(init_file):
                with open(init_file, 'w') as f:
                    pass
                print(f"Created: {init_file}")
            else:
                print(f"Already exists: {init_file}")

if __name__ == "__main__":
    create_init_files()
