# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gcs_aio_mapper']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0',
 'gcloud-aio-storage>=5.2.2,<6.0.0',
 'google-cloud-storage>=1.26.0,<2.0.0',
 'pylint>=2.4.4,<3.0.0']

setup_kwargs = {
    'name': 'gcs-aio-mapper',
    'version': '0.1.0',
    'description': 'An mutable mapping interface to GCS leveraging asyncio',
    'long_description': 'Async GCS Mapper\n================\n\nExample::\n\n    import zarr\n    from gcs_aio_mapper import GCSMapperAio\n    from gcsfs import GCSMap\n    import logging\n\n    logging.basicConfig(level=logging.DEBUG)\n    n = 25\n\n    def build_gs_async():\n        store = GCSMapperAio("gs://bucket/tmp/test.zarr", cache_size=n)\n        g = zarr.open_array(store, shape=(n,), chunks=(3,), mode="w")\n        for i in range(n):\n            g[i] = i\n        store.flush()\n\n\n    def build_gs():\n        store = GCSMap("gs://bucket/tmp/test.zarr")\n        g = zarr.open_array(store, shape=(n,), chunks=(3,), mode="w")\n        for i in range(n):\n            g[i] = i\n',
    'author': 'Noah D. Brenowitz',
    'author_email': 'nbren12@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nbren12/gcs_aio_mapper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
