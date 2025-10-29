Для запуска локальной сети hardhat 

Инициализацися проекта
```
npx hardhat --init
```
Перед повторным запуском сети, её нужно всегда чистить
```
npx hardhat clean
```
Запуск сети
```
npx hardhat node
```

В другом терминале:

Компиляция
```
npx hardhat compile
```
Деплой - специальный скрипт 
```
npx hardhat run --network localhost scripts/deploy.js
```