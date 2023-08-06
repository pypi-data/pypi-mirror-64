# Tests

## Lancement de tous les tests

    nosetests -v tests

## Lancement d'un test sans capture

    nosetests -v --nocapture tests/test_aci.py 

# Publication

    rm -rf dist/*
    python setup.py sdist bdist_wheel
    twine upload dist/*