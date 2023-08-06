# MonsterGen

## Installation
```shell script
$ pip install MonsterGen
```

## Monster Class
```python
from MonsterGen import Monster

print(Monster(10))
```

```
Name: Displacer Beast
CR: 10
Hit Points: 217
Armor Class: 17
Attack Bonus: 7
Typical Damage: 63 - 68
Save DC: 16
XP Value: 5900
```

## Alternate Calling Signatures
```python
from MonsterGen import Monster, CR

monster_cr = CR.party_adapter(average_level=10, num_players=3, difficulty=0)
print(Monster(monster_cr))
```

```
Name: Wyvern
CR: 10
Hit Points: 214
Armor Class: 18
Attack Bonus: 6
Typical Damage: 63 - 68
Save DC: 16
XP Value: 5900
```

```python
from MonsterGen import Monster, CR

monster_cr = CR(10)
print(Monster(monster_cr))
```

```
Name: Wraith
CR: 10
Hit Points: 217
Armor Class: 15
Attack Bonus: 9
Typical Damage: 63 - 68
Save DC: 16
XP Value: 5900
```

## CR Class
`CR(cr: int)`

The CR class is a numeric system representing the relative power of a monster in D&D 5e.
This system is a bit funky with values below 1, be careful... here be dragons!
CR less than 1 are printed as fractions but valued mathematically as integers [-3, 0]. See below:

#### CR Mapping

```python
from MonsterGen import CR

print(f"CR: {CR(-3)}")
print(f"CR: {CR(-2)}")
print(f"CR: {CR(-1)}")
print(f"CR: {CR(0)}")
print(f"CR: {CR(1)}")
print(f"CR: {CR(2)}")
print(f"CR: {CR(3)}")
print('...')
print(f"CR: {CR(30)}")
```

```
CR: 1/16
CR: 1/8
CR: 1/4
CR: 1/2
CR: 1
CR: 2
CR: 3
...
CR: 30
```

### Party Adapter Method (Factory Function)
`CR.player_adapter(average_level: int, num_players: int, difficulty: int) -> CR`

Class method for computing CR from party composition and difficulty setting.

#### Average Character Level (rounded down)
Required Integer, 1 to 20 clamped

#### Number of Player Characters
Optional Integer, 1 to 9 clamped, default 5

#### Difficulty Rating
Optional Integer, -5 to 5 clamped, default 0

    Stupid Easy    Easy    Norm    Epic    Legendary
          -5        -3      0       3          5
