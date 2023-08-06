"""Setup file"""
import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="django-i18n",
  version="1.0.4",
  author="Golden M",
  author_email="support@goldenmcorp.com",
  description="Lightweight i18n for Django framework",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://gitlab.com/goldenm-software/open-source-libraries/django-i18n",
  packages=setuptools.find_packages(),
  python_requires='>=3.6',
  install_requires=[
      'pyyaml',
  ],
)
