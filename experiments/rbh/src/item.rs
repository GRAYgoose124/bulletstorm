use raylib::prelude::*;
use crate::bullet::Bullet;
use crate::player::Effect;
use crate::enemy::ShotPattern;

pub enum Item {
    Weapon(Weapon),
    Armor(Armor),
    Consumable(Consumable),
}

pub struct Weapon {
    pub name: String,
    pub damage: f32,
    pub fire_rate: f32,
    pub shot_pattern: ShotPattern,
}

impl Weapon {
    pub fn shoot(&self, position: Vector2, direction: Vector2) -> Vec<Bullet> {
        self.shot_pattern.create_bullets(position, direction) // TODO: pass damage
    }
}

pub struct Armor {
    pub name: String,
    pub defense: f32,
}

pub struct Consumable {
    pub name: String,
    pub effect: Effect,
}
