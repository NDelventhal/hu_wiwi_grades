import setuptools

setuptools.setup(
    name="hu_wiwi_grades",
    version="0.1.0",
    license='MIT',  
    url="https://github.com/NDelventhal/hu_wiwi_grades",
    author="Niall Delventhal",
    author_email="ni.delventhal@gmail.com",
    description="hu_wiwi_grades is a Python library for searching, viewing and scraping published students' grading of the Faculty of Economics and Business Administration of the Humboldt University of Berlin",
    long_description=open('README.md').read(),
    download_url = 'https://github.com/NDelventhal/hu_wiwi_grades/archive/v_010.tar.gz',
    packages=setuptools.find_packages(),
    'Intended Audience :: Researchers',
    'License :: OSI Approved :: MIT License', 
    'Development Status :: 3 - Alpha', 
    install_requires=['tabula','pandas','numpy','requests','beautifulsoup4'],
    classifiers=[
     #   'Programming Language :: Python',
         'Programming Language :: Python :: 3',
         'Programming Language :: Python :: 3.6',],
)