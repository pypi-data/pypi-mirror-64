import setuptools

setuptools.setup(name='sparse-pendulum',
    version='0.0.6',
    author="Christoper Glenn Wulur",
    packages=[package for package in setuptools.find_packages() if package.startswith('sparse_pendulum')],
    zip_safe=False,
    author_email="christoper.glennwu@gmail.com",
    description="Open AI gym Pendulum Env with sparse rewards",
    install_requires=['gym']#And any other dependencies required
)
