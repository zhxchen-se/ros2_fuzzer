from setuptools import setup

setup(
    name='ros2_fuzzer',
    version='1.0.0',
    packages=['ros2_fuzzer'],
    url='https://www.aliasrobotics.com',
    license='GPLv3',
    author='Alias Robotics',
    author_email='contact@aliasrobotics.com',
    description='A ROS2 fuzzing tool for ROS2 systems',
    keywords=['network', 'fuzzing', 'ros', 'ros2'],
    entry_points={
        'console_scripts': [
            'ros2_fuzzer=ros2_fuzzer.ros_fuzzer:main',
            'ros2_generate_random_data=ros2_fuzzer.generate_random_data_by_service:main',
            'ros2_generate_random_service_data=ros2_fuzzer.generate_random_data_by_service:main',
            'ros2_generate_random_topic_data=ros2_fuzzer.generate_random_data_by_topic:main',
        ],
    },
    install_requires=[
        'hypothesis>=6.0.0',
        'attrs>=22.2.0',
        'numpy>=1.16.3',
    ],
    include_package_data=True,
    python_requires='>=3'
)
