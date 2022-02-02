
Программа для парсинга курса выбранной валюты с сайта ЦБ.

Особенности проекта:
1. Согласно заданию парсинг выполняется без использования API сайта ЦБ.
2. Программа имеет пользовательский интерфейс
3. Мультипоточность отсутствует, т.к. парсинг и запись данных не занимают много времени, то и "подвисание" интерфейса происходит всего на несколько секунд. При необходимости проект может быть легко переписан под мультипоточный
4. Для парсинга используются библиотеки requests и Beautifulsoap
5. Для хранения полученных и обработанных данных используется база данных sqlite. Таблица с данными удаляется и пересоздается при каждой попытке сохранения данных, поэтому хранит данные только о последней валюте
6. Запуск программы - main.py
7. В базе данных сохраняются поля: Дата, Единиц, Курс 