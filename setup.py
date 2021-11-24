from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in hot_recharge_app/__init__.py
from hot_recharge_app import __version__ as version

setup(
	name="hot_recharge_app",
	version=version,
	description="Hot Recharge App in Frappe ERPNEXT",
	author="DonnC Lab",
	author_email="donnclab@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
