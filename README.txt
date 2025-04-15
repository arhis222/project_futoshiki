Remarque :Si vous avez des erreurs sur l'interpréteur python comme " Invalid Python SDK ", 
"No Python at 'C:\Users\Arhan\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.7_qbz5n2kfra8p0\python.exe'"

Vous pourriez devoir choisir comme interpréteur python le vôtre et ensuite télécharger des packages manquants.


Notre projet est constitué de plusieurs fichiers de code distincts. Pour jouer au jeu, il vous suffit 
de cliquer sur futoshiki.exe. Si jamais cela ne fonctionne pas vous pouvez exécuter le fichier table.py via l'interpréteur Python. Cela lancera toutes
les interfaces graphiques nécessaires pour jouer au jeu Futoshiki, tant que la localisation et 
l'intégrité des fichiers restent intactes. 

L'apparition de l'interface graphique peut prendre long temps selon la difficulté et la taille du jeu.
Ça depend du solveur aussi. Surtout notre solveur a plus de diffculté que minisat pour chargement de l'écran.(En particulier pour les tailles 7,8,9 et modes moyen ou difficile)


Nous avons utilisé PyCharm en faisant notre projet. Pour voir l'éxécution de la partie DIMACS,
si vous utilisez PyCharm aussi, n'oubliez pas de changer la configuration à mode_dimacs. (Cf. l'image nommé 'config')

Dans le fichier "mode_dimacs.py" vous pouvez voir des blocs de code en commentaires, ce sont nos tests. Si vous voulez tester les transformations vers les formats SAT ou DIMACS vous pouvez faire des tests en décommentant ces blocs qui sont séparés via des sous-titres Test 1 et Test 2.

Si jamais vous rencontrez des difficultés au sujet d'inclusion de packages dans les fichiers "jeu.py" et "table.py" veuillez regarder la partie "NOTE IMPORTANTE" des deux fichiers.

