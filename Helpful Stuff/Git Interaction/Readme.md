This is just a remind of popular git commands:


git init 

###---Повторяем для всех загружаемых файлов---###
git add <filename>
git commit -m "Комментарий к добавленному файлу"
###---Повторяем для всех загружаемых файлов---###
# или можно добавить все сразу командой git add .

git branch master				 				# удостоверимся что мы находимся не в ветках
git remote add origin https://github.com/hse-mlearn/ha-01-danyanyam.git 	# добавляем alias для дальнейшего удобного обращения к ссылке
git push -u origin master							# по алиасу загружаем все измененные файлы

# Удаляем лишние файлы в репозитории
git rm <filename>
git commit -m "Deleted file"
git push -u origin master
