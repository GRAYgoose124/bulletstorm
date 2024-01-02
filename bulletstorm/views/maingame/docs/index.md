# Entity vs Agent

## Entity

An entity is a game which represents a physical object in the game world. It has a position, a velocity, and a sprite. It can be collided with, and it can collide with other entities. 

## Agent

An Agent is a collection of entities which are controlled by an agent AI which can adapt edge forces or react to collision handlers. The agent AI is a graph of forces which are applied to the entities. The agent forces exists as subgraphs in a global entity_graph, which maintains all the graph interactions in the game. 