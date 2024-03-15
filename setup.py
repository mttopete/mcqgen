from setuptools import find_packages, setup

setup(
    name='mcqgenerator',
    version='0.0.1',
    author='mateo topete',
    author_email='mateotopete@gmail.com',
    install_requires=["openai","langchain","streamlit","python-dotevn","PyPDF2"],
    packages=find_packages()
)