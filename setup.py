from setuptools import setup, find_packages

pkj_name = 'redirects'

setup(
    name='django-ok-redirects',
    version='0.1',
    long_description_content_type='text/x-rst',
    packages=[pkj_name] + [pkj_name + '.' + x for x in find_packages(pkj_name)],
    include_package_data=True,
)
