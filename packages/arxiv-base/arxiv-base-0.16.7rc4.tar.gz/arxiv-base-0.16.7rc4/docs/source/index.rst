arXiv Base Documentation
========================

This project provides a base Flask application and base Docker image for
arXiv-NG services.

Each component of this project **must** meet all of the following criteria:

1. It is likely that the component will be utilized in many or all arXiv
   services.
2. Once stable, it is unlikely to change often.
3. It is unlikely that implementing new features in specific services
   would require changes to the component.
4. When a component does change, it **must** change in the same way for all of
   the services that use it.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   arxiv/modules.rst
   arxiv/metadocs.rst
