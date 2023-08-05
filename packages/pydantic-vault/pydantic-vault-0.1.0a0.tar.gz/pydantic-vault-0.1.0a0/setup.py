# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydantic_vault']

package_data = \
{'': ['*']}

install_requires = \
['hvac>=0.10.0,<0.11.0', 'pydantic>=1.0,<2.0']

setup_kwargs = {
    'name': 'pydantic-vault',
    'version': '0.1.0a0',
    'description': 'A simple extension to Pydantic BaseSettings that can retrieve secrets from Hashicorp Vault',
    'long_description': '# Pydantic-Vault\n\n![Check code](https://github.com/nymous/pydantic-vault/workflows/Check%20code/badge.svg)\n\nA simple extension to [Pydantic][pydantic] [BaseSettings][pydantic-basesettings] that can retrieve secrets from a [KV v2 secrets engine][vault-kv-v2] in Hashicorp [Vault][vault]\n\n## Getting started\n\nSame as with the Pydantic `BaseSettings`, create a class that inherits from `pydantic_vault.VaultBaseSettings`, then define your fields and configure the settings with\n\n```python\nimport os\n\nfrom pydantic import SecretStr, Field\nfrom pydantic_vault import VaultBaseSettings\n\nclass Settings(VaultBaseSettings):\n    username: str = Field(..., vault_secret_path="path/to/secret", vault_secret_key="my_user")\n    password: SecretStr = Field(..., vault_secret_path="path/to/secret", vault_secret_key="my_password")\n\n    class Config:\n        vault_url: str = "https://vault.tld"\n        vault_token: SecretStr = os.environ["VAULT_TOKEN"]\n        vault_namespace: str = "your/namespace"  # Optional, pydantic-vault supports Vault namespaces (for Vault Enterprise)\n        vault_secret_mount_point: str = "secrets"  # Optional, if your KV v2 secrets engine is not available at the default "secret" mount point\n\nsettings = Settings()\n# These variables will come from the Vault secret you configured\nsettings.username\nsettings.password.get_secret_value()\n\n\n# Now let\'s pretend we have already set the USERNAME in an environment variable\n# (see the Pydantic documentation for more information and to know how to configure it)\n# Its value will override the Vault secret\nos.environ["USERNAME"] = "my user"\n\nsettings = Settings()\nsettings.username  # "my user", defined in the environment variable\nsettings.password.get_secret_value()  # the value set in Vault\n```\n\n## Documentation\n\n### `Field` additional parameters\n\nYou might have noticed that we import `Field` directly from Pydantic. Pydantic-Vault doesn\'t add any custom logic to it, which means you can still use everything you know and love from Pydantic.\n\nThe additional parameters Pydantic-Vault uses are:\n\n| Parameter name              | Required | Description |\n|-----------------------------|----------|-------------|\n| `vault_secret_path`         | **Yes**  | The path to your secret in Vault |\n| `vault_secret_key`          | **Yes**  | The key to use in the secret |\n\nFor example, if you create a secret `database/prod` with a key `password` and a value of `a secret password`, you would use\n\n```python\npassword: SecretStr = Field(..., vault_secret_path="database/prod", vault_secret_key="password")\n```\n\n### Authentication\n\nFor now Pydantic-Vault only supports direct token authentication, that is you must authenticate using your method of choice then pass the resulting Vault token to your `Settings` class.\n\nSupport is planned for Approle and Kubernetes authentication methods.\n\n### Configuration\n\nIn your `Settings.Config` class you can configure the following elements:\n\n| Settings name              | Required | Description |\n|----------------------------|----------|-------------|\n| `vault_url`                | **Yes**  | Your Vault URL |\n| `vault_token`              | **Yes**  | A token allowing to connect to Vault (retrieve it with any auth method you want) |\n| `vault_namespace`          | No       | Your Vault namespace (if you use one, requires Vault Enterprise) |\n| `vault_secret_mount_point` | No       | The mount point of the KV v2 secrets engine, if different from the default `"secret"` mount point |\n\nYou can also configure everything available in the original Pydantic `BaseSettings` class.\n\n### Order of priority\n\nSettings values are determined as follows (in descending order of priority):\n  - arguments passed to the `Settings` class initializer\n  - environment variables\n  - Vault variables\n  - the default field values for the `Settings` model\n\nIt\'s the [same order][pydantic-basesettings-priority] as with the original `BaseSettings`, but with Vault just before the default values.\n\n\n## License\n\nPydantic-Vault is available under the [MIT license](./LICENSE).\n\n[pydantic]: https://pydantic-docs.helpmanual.io/\n[pydantic-basesettings]: https://pydantic-docs.helpmanual.io/usage/settings/\n[pydantic-basesettings-priority]: https://pydantic-docs.helpmanual.io/usage/settings/#field-value-priority\n[vault]: https://www.vaultproject.io/\n[vault-kv-v2]: https://www.vaultproject.io/docs/secrets/kv/kv-v2/\n',
    'author': 'Thomas Gaudin',
    'author_email': 'thomas.gaudin@centraliens-lille.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nymous/pydantic-vault',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
