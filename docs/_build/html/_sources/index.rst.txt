Bienvenue sur la documentation de KISS GAME ENGINE!
===================================================

https://github.com/Fredkiss3/kge


**KISS GAME ENGINE**, alias kge, est le **premier moteur de jeu 2D** complet optimisé pour la création de jeux-vidéos avec le langage Python. Etant donné la lenteur de l'interprêteur python, le moteur a été optimisé en interne pour lancer vos jeux quelque soit leur taille. Ce moteur de jeu est basé sur un moteur de Jeu **PPB** créé par `Piper Thunstrom`_.

.. _Piper Thunstrom: https://github.com/ppb/pursuedpybear


Une Bibliothèque optimisée et facile à utiliser
-----------------------------------------------

L'API du moteur utilise les *best practices* de la programmation orientée objet en python, avec une interface simple facile et à comprendre. Le moteur utilise un système d'évènements pour l'implémentation de la logique du jeu, des collisions, des évènements personnalisés, la liste complète des évènements se trouve dans le module ``kge.core.events``. Le système utilise aussi une architecture d' `Entité Composant`_ afin de pouvoir facilement ajouter des comportements personnalisés (Exemple: ``Archer``, ``Magicien``, ``Goblin`` ).

.. _Entité Composant: https://en.wikipedia.org/wiki/Entity_component_system

Vous verrez vos jeux prendre vie en quelques lignes de code, la preuve :

.. code:: python

    import kge

    def setup(scene):
        scene.add(kge.Sprite(image=kge.Image('player.png')))

    kge.run(setup)


Résultat :

.. image:: screenshot.png
   :height: 400
   :alt: Screen Shot 1

Nous plongeons dans le contenu de ce code dans les sections suivantes, j'espère que ce petit bout de code vous a mis l'eau à la bouche.


.. toctree::
	:maxdepth: 2
	:caption: Contenu:

	getting-started
	user_guide/index
	ref/index
