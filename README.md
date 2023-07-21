# cas_to_cramer

Данное приложение написано на Питоне.
Если на вход скормить файл csv (разделитель ";") - с колонкой CAS,приложение запрашивает через PubChemAPI формулу в виде SMILE,
которыми кормит установленное приложение Toxtree, (обычно расположен C:\Ideaconsult\Toxtree-v3.1.0.1851\Toxtree) получая данные по классу Cramer,
вывод в csv файл при выполнении в начальной папке создаются файлы result.csv - данные по SMILE,toxout.csv - обработка Toxtree"

Обработка делается при помощи ПО https://sourceforge.net/projects/toxtree/files/toxtree/Toxtree-v.3.1.0/
https://toxtree.sourceforge.net/


Cramer Class       Description                      TTC (µg/day*)
I               Substances of simple chemical       1,800 (30 µg/kg bw/d)
                structure with known metabolic 
                 pathways and innocuous end 
                 products which suggest a low 
                  order of oral toxicity.

II              Substances that are intermediate.    540 (9 µg/kg bw/d)
                They possess structures that are 
                less innocuous than those in 
                Class 1 but they do not contain 
                structural features that are 
                 suggestive of toxicity like those
                  in Class 3.

III              Substances with chemical structures  90 (1.5 µg/kg bw/d)
                 that permit no strong initial 
                 impression of safety and may even 
                  suggest a significant toxicity.

