- [What is it ?](#what-is-it)
- [What do I need ?](#what-do-i-need)
- [How to use it ?](#how-to-use-it)
- [What the configuration file should look like ?](#what-the-configuration-file-should-look-like)
- [Does it always work ?](#does-it-always-work)
  - [Short Answer](#short-answer)
  - [Longer Answer](#longer-answer)


# What is it ?

A simple script for making gift for christmas.

# What do I need ?

Only [Python3](https://python.org)

# How to use it ?

1. clone this repo (at least copy the `scrumble.py`)
2. Create a configuration file
3. launch the command `python3 scrumble.py conf.json`

# What the configuration file should look like ?

```json
{
  "couple" : [
    ["couple_a_person_aa", "couple_a_person_ab"],
    ["couple_b_person_ba", "couple_b_person_bb"],
    ["couple_c_person_ca", "couple_c_person_cb"],
    ["couple_d_person_da", "couple_d_person_db"]
  ]
}
```

# Does it always work ?

## Short Answer

Nope.

The following configuration file have no solution and the current program will loop for ever.

```json
{
  "couple" : [
    ["a", "b"],
    ["c"]
  ]
}
```

Indeed we have the situation:

```
a -> c
c -> b
b -> a  # <- but it's forbiden to make a gift in the couple
```

## Longer Answer

This problem could be resume has _one person must have only one gift and make one gift to anybody but his familly_.

Now if we represent it with a graph with those suppositions:
* vertex represent a person
* oriented edges represent to who you can make a gift

The following configuration file:

```json
{
  "couple" : [
    ["a", "b"],
    ["c", "d"]
  ]
}
```

Would make the graph:

```
a --> c
a --> d
b --> c
b --> d
c --> a
c --> b
d --> a
d --> d
```

And it growth in complexity! (In fact it is a [Complete graph](https://en.wikipedia.org/wiki/Complete_graph) minus familly edges).

In graph theory this could be modeled as finding an [Hamiltonian path](https://en.wikipedia.org/wiki/Hamiltonian_path).
And this is a [NP-Complet](https://en.wikipedia.org/wiki/NP-completeness) problem.

Ok, the general problem is hard, but in our case, we have many edges to walk to (aka we can make a gift to anybody), so most of the time we can find a solution fearly easely.

My implementation here is:

1. init a map of person who make a gift and to who 
1. take a random person who are not making a gift,
2. select a random person who do not receive a gift AND is not in the familly,
3. if you can't find anybody start again (1.)
4. if nobody left, so everybody have a gift AND everybody is making a gift, you have a solution
5. merry christmas !