### Features
- [x] simple in game HUD with imgui (Hp, Damage)
- [x] Player shooting (projectiles)
- [x] Screen wrapping and scrolling modes
- [x] Game Over restart option
- [x] turn based battle core (lol)
- [x] "Agents" Multi-entity subgraphs with specialized graph forces. 
### Fixes
 - Player collision handler? Fix comparing with sprite list.
 - Rather than removing all angular velocity, we should subtract the turning from it.
 - Projectiles need to be particles, not entities.
 - Explosions need to be a shader, not particles
 - shocklines probably need to be drawn with a shader.

### Gampleay

- [ ] Damage scaling based on impact force/velocity (Discourage far towing)
- [/] Tow mechanic  
    - [ ] an ability to prune leaf nodes from the towed graph. 
        (This is actually not necessary - in-game we can retarget a leaf node and then prune it from the graph.)
    - [ ] an ability to disable graph-growing except on towed nodes, which also should be toggleable.
- [ ] Limited fuel (Encourage towing)
- [/] Agents
    - [ ] Brain/controller
    - types
        - [/] Catcher - baseball glove-like entity that can catch foreign entities. 

 ### Research
 # TODO: research physics layers: https://stackoverflow.com/questions/14081949/pymunk-chipmunk-how-to-turn-off-physics-collisions-temporarily-for-concrete

