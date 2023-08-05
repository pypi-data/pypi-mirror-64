import setuptools 

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()
   
setuptools.setup(
    name="jingjue",
    version="1.0",
    author="Ken Tang",
    author_email="kinyeah@gmail.com",
    install_requires=[            
      ],
	description= "Jingjue is an ancient Chinese divination method similar as ichingshifa found from a bunch of bamboo slips relics collected by Peking University",
	long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kentang2017/jingjue",
	packages=setuptools.find_packages(),
	package_data = {'jingjue': ['gua_dict.py']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)