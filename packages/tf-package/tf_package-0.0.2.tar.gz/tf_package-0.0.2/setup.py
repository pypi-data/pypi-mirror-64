# coding: utf-8

from setuptools import setup

setup(
    name='tf_package',  # 项目的名称,pip3 install get-time
    version='0.0.2',  # 项目版本
    author='YuHe',  # 项目作者
    author_email='yuhe20170108@gmail.com',  # 作者email
    url='https://github.com/yuhe-tf/tf_package',  # 项目代码仓库
    description='增加TensorFlow没有的功能函数',  # 项目描述
    packages=['tf_package'],  # 包名
    install_requires=[],
    entry_points={
        'console_scripts': [
            '',
        ]
    }
)
