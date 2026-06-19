from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

setup(
	name="foodshare_hub",
	version="1.0.0",
	description="FoodShare Hub - Leftover Food Sharing Platform",
	author="FoodShare Hub",
	author_email="admin@foodsharehub.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires,
)
