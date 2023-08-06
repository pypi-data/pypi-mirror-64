# Client Python pour la banque Crédit agricole - Particuliers

Ce client Python est à destination des particuliers souhaitant récupérer ses opérations bancaires stockées par le Crédit Agricole.

## Installation

```python
pip install creditagricole_particuliers
```
  
## Authentification

```python
from creditagricole_particuliers import Authenticator, Operations

session = Authenticator(username="<n° de compte bancaire>",
                        password=[1, 2, 3, 4, 5, 6])
```
                
## Récupération des opérations bancaires

```python
operations = Operations(session=session,
                        date_start="2020-02-21",
                        date_stop="2020-02-21")
print(operations.list)
[ 
    { 
        'dateOperation': 'Feb 21, 2020 12:00:00 AM',
        'dateValeur': 'Feb 21, 2020 12:00:00 AM',
        'typeOperation': '11',
        'codeTypeOperation': '52',
        'familleTypeOperation': '11',
        'libelleOperation': 'CARTE LEROY MERLIN',
        'libelleTypeOperation': 'PAIEMENT PAR CARTE',
        'montant': -3.75,
        'idDevise': 'EUR',
        'libelleDevise': '€',
        'libelleComplementaire': '', 
        'referenceMandat': '',
        'idCreancier': '', 
        'libelleCash1': '',
        'libelleCash2': '', 
        'idCarte': '',
        'indexCarte': -1,
        'referenceClient': '', 
        'pictogrammeCSS': 'npc-card',
        'fitid': '5799800129718'
    }
]
```

## Itérer sur les opérations bancaires

```python
operations = Operations(session=session,
                        date_start="2020-02-21",
                        date_stop="2020-02-21")
for op in operations:
    print(op)
```
