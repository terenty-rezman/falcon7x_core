from setuptools import setup, find_packages

print("PACKAGES")
for p in find_packages():
    print(p)
print("END PACKAGES")

setup(
   name='falcon7x_core',
   version='1.0',
   description='A useful module',
   author='terenty rezman',
   author_email='terenty.rezman@gmail.com',
   packages=find_packages(),
#    install_requires=['wheel', 'bar', 'greek'], #external packages as dependencies
)
