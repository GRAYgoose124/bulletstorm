### Features
- [x] simple in game HUD with imgui (Hp, Damage)
- [x] Player shooting (projectiles)
- [x] Screen wrapping and scrolling modes
- [x] Game Over restart option
- [x] turn based battle core (lol)
- [ ] "Agents" Multi-entity subgraphs with specialized graph forces. 
    - [ ] Catcher - baseball glove-like entity that can catch foreign entities. 
### Fixes
 - Player collision handler? Fix comparing with sprite list.
 - Rather than removing all angular velocity, we should subtract the turning from it.
 - Projectiles need to be particles, not entities.
 - Explosions need to be a shader, not particles
 - shocklines probably need to be drawn with a shader.

 ### Research
 # TODO: research physics layers: https://stackoverflow.com/questions/14081949/pymunk-chipmunk-how-to-turn-off-physics-collisions-temporarily-for-concrete

