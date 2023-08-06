Pyser
======
.. image:: https://badge.fury.io/py/pyser.svg
    :target: https://badge.fury.io/py/pyser
    :alt: PySer page on the Python Package Index
.. image:: https://github.com/jonnekaunisto/pyser/workflows/Python%20package/badge.svg
  :target: https://github.com/jonnekaunisto/pyser/actions
.. image:: https://codecov.io/gh/jonnekaunisto/pyser/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/jonnekaunisto/pyser

PySer(full documentation_) is a library for serializing and deserializing data in different data formats through intuitive mappings in defined inside a Python class.

Current formats supported are JSON and config files, with more coming later on.

Examples
--------

Class mappings for serializing and deserializing in JSON

.. code:: python

   from pyser import JSONBase, SerializeField, DeserializeField
   class FruitBasket(JSONBase):
        def __init__(self):
            super().__init__()
            self.name =           DeserializeField()
            self.fruit =          DeserializeField()
            self.iD =             DeserializeField(name='ref', kind=int)
            self.intString =      DeserializeField(kind=int)
            self.optionalString = DeserializeField(kind=str, optional=True)
            self.items =          DeserializeField(repeated=True)
            self.init_deserialize_json()

            self.name =           SerializeField()
            self.fruit =          SerializeField()
            self.iD =             SerializeField(name='ref', kind=int)
            self.intString =      SerializeField(kind=int)
            self.optionalString = SerializeField(optional=True)
            self.items =          SerializeField(repeated=True)
            self.register =       SerializeField(parent_keys=['checkout'], kind=int)
            self.amount =         SerializeField(parent_keys=['checkout'], kind=int)
            self.init_serialize_json()
            
            self.name =           'basket'
            self.fruit =          'banana'
            self.iD =             '123'
            self.intString =      '12345'
            self.optionalString = None
            self.items =          ['paper', 'rock']
            self.register =       '1'
            self.amount =         '10'


Serializing to a JSON file

.. code:: python

    basket = FruitBasket()
    basket.to_json(filename="basket.json")

File contents of basket.json after serializing:

.. code:: json

    {
        "name": "basket",
        "fruit": "banana",
        "ref": 123,
        "intString": 12345,
        "items": [
            "paper",
            "rock"
        ],
        "checkout": {
            "register": 1,
            "amount": 10
        }
    }

Similarly deserialization from a json file:

.. code:: Python

    basket = FruitBasket()
    basket.from_json(raw_json=raw_json)

Installation
------------

**Installation by hand:** you can download the source files from PyPi or Github:

.. code:: bash

    $ (sudo) python setup.py install

**Installation with pip:** make sure that you have ``pip`` installed, type this in a terminal:

.. code:: bash

    $ (sudo) pip install pyser

Documentation
-------------

Running `build_docs` has additional dependencies that require installation.

.. code:: bash

    $ (sudo) pip install pyser[docs]

The documentation can be generated and viewed via:

.. code:: bash

    $ python setup.py build_docs

You can pass additional arguments to the documentation build, such as clean build:

.. code:: bash

    $ python setup.py build_docs -E

More information is available from the `Sphinx`_ documentation.

Running Tests
-------------
Run the python command

.. code:: bash 

   python setup.py test

Contribute
----------
1. Fork the repository from Github
2. Clone your fork 

.. code:: bash 

   git clone https://github.com/yourname/pyser.git

3. Add the main repository as a remote

.. code:: bash

    git remote add upstream https://github.com/jonnekaunisto/pyser.git

4. Create a pull request and follow the guidelines


Maintainers
-----------
- jonnekaunisto_ (owner)


.. PySer links
.. _documentation: https://pyser.readthedocs.io/en/latest/

.. Software, Tools, Libraries
.. _`Sphinx`: https://www.sphinx-doc.org/en/master/setuptools.html

.. People
.. _jonnekaunisto: https://github.com/jonnekaunisto


