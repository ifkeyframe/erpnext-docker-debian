from setuptools import setup, find_packages

setup(
    name="printbiz_custom",
    version="0.1.0",
    description="Custom app for PrintBiz warehouse and production management",
    author="PrintBiz",
    author_email="admin@printbiz.local",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[],
)
