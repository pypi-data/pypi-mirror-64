# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['drf_yasg_examples']
install_requires = \
['drf-yasg>=1.17.1,<2.0.0']

setup_kwargs = {
    'name': 'drf-yasg-examples',
    'version': '0.1.1',
    'description': 'Inspector for add example in drf-yasg docs',
    'long_description': "drf-yasg-examples\n-----------------\n\nAdd example value on your swagger documentation!\n\n\nRequirements\n============\n\n1. Python 3.6.1 or higher\n2. drf-yasg based code base\n\n\nInstall\n=======\n\nWith pip\n++++++++\n\n.. code-block:: sh\n\n   pip install drf-yasg-examples\n\n\nWith Poetry\n+++++++++++\n\n.. code-block:: sh\n\n   poetry add drf-yasg-examples\n\n\nConfiguration\n=============\n\nEdit your django config file.\n\n.. code-block:: py\n\n   SWAGGER_SETTINGS = {\n       'DEFAULT_AUTO_SCHEMA_CLASS': 'drf_yasg_examples.SwaggerAutoSchema',\n   }\n\nNote: If you use ``SwaggerAutoSchema`` class other codes, replace them together\n\n\nUsage\n=====\n\nChoiceField\n+++++++++++\n\nJust write verbose text like this in your models.\n\n.. code-block:: py\n\n   class Product(models.Model):\n\n       CATEGORY = [\n           ('F', 'Food'),\n           ('L', 'Living Item'),\n       ]\n\n       category = models.CharField(\n           verbose_name='Category',\n           max_length=1,\n           choices=CATEGORY,\n       )\n\n\nAnd ModelSerializer might set this field as ChoiceField, and this package\nwrite down enum k-v list on your documentation automatically.\n\n\nOthers\n++++++\n\nWrite example value in your serializer class like this.\n\n.. code-block:: py\n\n   class ProductSerializer(serializers.ModelSerializer):\n\n       class Meta:\n           model = Product\n           fields = '__all__'\n           example = {\n               'name': 'Apple',\n               'amount': 6,\n               'price': '10.00',\n           }\n\n\nThen drf-yasg will add example on your docs automatically.\n\n\nLICENSE\n=======\n\nMIT\n",
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
