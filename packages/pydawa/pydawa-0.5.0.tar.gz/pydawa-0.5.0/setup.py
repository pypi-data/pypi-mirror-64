# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydawa']

package_data = \
{'': ['*']}

install_requires = \
['openpyxl>=3.0.3,<4.0.0',
 'pandas>=1.0.3,<2.0.0',
 'requests>=2.23.0,<3.0.0',
 'xlrd>=1.2.0,<2.0.0']

setup_kwargs = {
    'name': 'pydawa',
    'version': '0.5.0',
    'description': 'En API wrapper omkring Danmarks Adressers Web API',
    'long_description': 'PyDawa\n======\nEn simple API wrapper omkring Danmarks Adressers Web API (DAWA).\n\nFormålet med dette modul er at give nem adgang til DAWA i Python. Grunden til, at jeg begyndte at arbejde på dette modul er, at jeg havde skrevet et par scripts i python, der brugte API\'et, men der var ingen "nem" adgang til det. Plus, jeg var nysgerrig over, om jeg kunne skrive et modul og uploade til pypi.\n\nDet her projekt er et "work in progress", så jeg kommer til at tilføje funktionalitet, når jeg har brug for den. Jeg håber, at folk har lyst til at hjælpe med det.\n\nAfhængigheder\n* Requests\n\nInstallation\n----\nInstaller med pip:\n\n```$ pip install pydawa```\n\nBrug\n-----\n\nIndtil videre, består modulet kun af tre classer:\n\n1. Adressesoeg\n2. Adresseopslag\n3. Adressevasker\n\n### Adressesoeg()\nSøg efter en adresse med vejnavn, husnr og postnummer.\n\n```python\nimport pydawa\n\nadresse = pydawa.Adressesoeg(vejnavn=\'Dronning Dagmars vej\', husnr=\'200\', postnr=\'3650\')\nresponse = adresse.info()\n```\n`info()` metoden henter data fra dawa api\'et og returnerer en dictionary med respons.\n\nMan kan også søge med en tekststring.\n```python\nimport pydawa\n\nadresse = pydawa.Adressesoeg(q=\'Dronning Dagmars Vej 200, 3650 Ølstykke\')\nresponse = adresse.info()\n```\n\n### Adresseopslag\nSøg efter en adresse med adressens unikke id.\n\n```python\nimport pydawa\n\nadresse = pydawa.Adresseopslag(id=id)\nresponse = adresse.info()\n```\n`info()` metoden henter data fra dawa api\'et og returnerer en dictionary med respons.\n\n### Adressevasker\nDatavask af adressebetegnelse. Modtager en adressebetegnelse og returnerer en eller flere adresser, der bedst matcher.\n\n```python\nimport pydawa\n\nadresse = pydawa.Adressevasker(betegnelse=adressebetegnelse)\nresponse = adresse.info()\n```\n\n### Koordinater for adresser\nMan kan hente koordinater for en given adresse ved at bruge _get_koordinater_ metoden fra _adresse_ variablen i examplerne ovenfor.\n\n```python\nimport pydawa\n\nadresse = pydawa.Adresseopslag(id=id)\nresponse = adresse.info()\n\nkoordinater = adresse.get_koordinater(response[0])\n```\nDen metode tager et json object. Indtil videre se returner både _Adressesoeg_ og _Adresseopslag_ en liste, så derfor bruger man _response[0]_ som input. \nMan kan kun hente koordinater fra _Adressesoeg_ og _ Adresseopslag_, fordi _Adressevasker_ returnerer ikke koordinater.\n\n### Reverse geokodning\nHvis man har koordinater og gerne vil finde den nærmeste adresse.\n\n```python\nimport pydawa\n\nkoordinater = (12.18, 55.78)\n\nadresse = pydawa.Reverse(koordinater=koordinater)\nresponse = adresse.info()\n```\n\nGeokoder\n=========\nHvis man har en csv eller xlsx fil, som indeholder adresser, som skal geokodes, så kan man bruge den her. Peg på filen og gem resultatet enten som en Pandas dataframe, hvis du skal bearbejde data mere, eller i en fil i samme mappe.\n\n```python\nimport pydawa\n\ngeokoder = pydawa.Geokoder(\'c:/users/brugernavn/adresser.csv\')\n\n# Gem data i en dataframe\ndf = geokoder.geokod_file(cols=[\'adresse\', \'postnr\', \'By\'])\n\n# Gem data i en fil\ngeokoder.geokod_file(save=True, cols=[\'adresse\', \'postnr\', \'By\'])\n\n```\n',
    'author': 'Daníel Örn Árnason',
    'author_email': 'danielarnason85@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/danielarnason/pydawa.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
