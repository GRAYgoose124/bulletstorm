### Features
- [x] simple in game HUD with imgui (Hp, Damage)
- [x] Player shooting (projectiles)
- [x] Screen wrapping and scrolling modes
- [x] Game Over restart option
- [x] turn based battle core (lol)
- [x] "Agents" Multi-entity subgraphs with specialized graph forces. 
- [ ] anchor entity feature
- [ ] shadow casting needs to work in various modes, cone, circle, etc. for flashlight and glowstick / entity graph lights.
### Fixes
 - collision handlers (pre/post/etc)
 - Player damage scaling
    - this partially works, when asteroids impact the player, but seems not all the player collision handlers are added correctly to handle it's own collision into an asteroid.
 - Rather than removing all angular velocity, we should subtract the turning from it.
 - Projectiles need to be particles, not entities.
 - Explosions need to be a shader, not particles
 - shocklines probably need to be drawn with a shader.
### Gamplay
- [ ] Damage scaling based on impact force/velocity 
(Discourage far towing, see fixes)
- [/] Tow mechanic  
    - [ ] an ability to prune leaf nodes from the towed graph. 
        (This is actually not necessary - in-game we can retarget a leaf node and then prune it from the graph.)
    - [ ] an ability to disable graph-growing except on towed nodes, which also should be toggleable.
- [ ] Limited fuel (Encourage towing)
- [/] Agents
    - [ ] Brain/controller
    - types
        - [/] Catcher - baseball glove-like entity that can catch foreign entities. 
### Cleanup 
- [ ] need to api-ify many things. unify shader usage, make views+their mixins more generic/standardized, decouple level/manager/view more, etc.
### Research
# TODO: research physics layers: https://stackoverflow.com/questions/14081949/pymunk-chipmunk-how-to-turn-off-physics-collisions-temporarily-for-concrete

