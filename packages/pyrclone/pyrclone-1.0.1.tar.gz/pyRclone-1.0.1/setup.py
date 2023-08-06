# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyrclone']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyrclone',
    'version': '1.0.1',
    'description': 'A typed interface for rclone.',
    'long_description': '# pyRclone\n\nA typed rClone interface for python.\n\nWritten to more easily express awkward logic, that would be a pain or not\n(easily) possible on the command line.\n\nA short example, to tidy up and half the number of backups is shown below.\nThe logic can be trivially expanded to instead say, parse the time stamp of\nthe backup out of the folder name, to allow different logic to be applied\ndepending on the age of a backup (do nothing if 1 month old, half is 2 months\nold, remove every other after a year old etc).\n\n```py\nimport json\nimport logging\nimport os\nimport sys\n\nfrom pyrclone import Rclone, RcloneError\n\n\ndef main():\n\n    # Setup rclone runner, and have it run in verbose and dry run mode.\n    rclone: Rclone = Rclone()\n    rclone.verbose_mode = True\n    rclone.dry_run_mode = True\n\n    # Attach a logger, for more immediate output, rather than just on command completion.\n    rclone.logger.setLevel(logging.DEBUG)\n    handler: logging.StreamHandler = logging.StreamHandler(sys.stdout)\n    handler.setLevel(logging.DEBUG)\n    formatter: logging.Formatter = logging.Formatter(\n        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"\n    )\n    handler.setFormatter(formatter)\n    rclone.logger.addHandler(handler)\n\n    # List all folders in backup directory to iterate over them.\n    remote_path: str = "drive:PC/Backups"\n    output = rclone.lsd(remote_path)\n\n    # If we failed to run, stop.\n    if output.return_code is not RcloneError.SUCCESS:\n        print(output.error)\n        return\n\n    # lsd (and all other ls commands) will default to using lsjson.\n    # Lets decode the JSON, and get a list of all our folders.\n    backup_folders = []\n    for folder in json.loads("".join(files)):\n        backup_folders.append(f"{remote_path}/{folder[\'Path\']}")\n\n    # With our list of folders, lets delete every other folder, excluding these\n    # useful ones.\n    #\n    # This could also be more indepth logic, such as using the modified timestamp\n    # or the timestamp in the folder name to do logic to different backups of\n    # varying age. This is allows the ease of scripting in Python to help, versus\n    # confusing/verbose command line options and shell scripts.\n    ignore_list = [\n        "drive:PC/Backups/2017-09-18_WindowsUpdate",\n        "drive:PC/Backups/2019-07-30_FlatMove",\n        "drive:PC/Backups/2019-08-12_HDD-Swap",\n    ]\n\n    # Iterate over every other folder and delete if not in the ignore.\n    #\n    # Of course, right now we are in dry_run mode, so this won\'t do anything\n    # except list what it would have done.\n    for folder in backup_folders[1::2]:\n        if folder in ignore_list:\n            continue\n        rclone.delete(folder)\n\n\nif __name__ == "__main__":\n    main()\n\n```',
    'author': 'Ryan C',
    'author_email': 'r.cross@lancaster.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
