import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='pylogflow',  
     version='0.2.0',
     author="Jacob Maldonado",
     author_email="jacobmaldonado99@gmail.com",
     description="Dialogflow Webhook utility package",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/JacobMaldonado/pylogflow.git",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
