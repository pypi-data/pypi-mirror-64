import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='oss_policy_sign',
     version='1.2',
     author="wyh",
     author_email="samuel.yh.wu@gmail.com",
     description="A django rest framework (DRF) policy sign for aliyun oss",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/wyh/oss-policy-sign",
     packages=setuptools.find_packages(),
     include_package_data=True,
     test_suite='nose.collector',
     tests_require=['nose'],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: Apache Software License",
         "Operating System :: OS Independent",
     ],
 )
