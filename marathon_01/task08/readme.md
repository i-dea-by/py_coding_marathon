**Кодинг-марафон. Задача № 8.**

Эта задача основана на игре «Сапёр».

Создайте функцию, которая принимает сетку из «#» и «-». В этой сетке каждая решетка (#) представляет мину, а каждое тире (-) — место без мин.

Верните список, в котором каждое тире заменено цифрой, обозначающей количество мин, непосредственно примыкающих к тире (по горизонтали, вертикали и диагоналям).

Пример:
```
num_grid ([
  [«-», «-», «-», «-», «-»],
  [«-», «-», «-», «-», «-»],
  [«-», «-», «#», «-», «-»],
  [«-», «-», «-», «-», «-»],
  [«-», «-», «-», «-», «-»]
]) ➞ [
  [«0», «0», «0», «0», «0»],
  [«0», «1», «1», «1», «0»],
  [«0», «1», «#», «1», «0»],
  [«0», «1», «1», «1», «0»],
  [«0», «0», «0», «0», «0»]
]
```

