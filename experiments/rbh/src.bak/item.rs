use raylib::prelude::*;
use rand::Rng;
use crate::physics::Collidable;

pub enum ItemType {
    HealthPotion,
    AttackBoost,
    DefenseBoost,
    SpeedBoost,
    ExperienceOrb,
}

impl ItemType {
    pub fn random() -> Self {
        let mut rng = rand::thread_rng();
        match rng.gen_range(0..5) {
            0 => ItemType::HealthPotion,
            1 => ItemType::AttackBoost,
            2 => ItemType::DefenseBoost,
            3 => ItemType::SpeedBoost,
            _ => ItemType::ExperienceOrb,
        }
    }
}

pub struct Item {
    pub position: Vector2,
    pub item_type: ItemType,
    pub size: f32,
    velocity: Vector2,
    collected: bool,
}

impl Item {
    pub fn new(position: Vector2, item_type: ItemType) -> Self {
        Item {
            position,
            item_type,
            size: 15.0,
            velocity: Vector2::new(0.0, 50.0),
            collected: false,
        }
    }

    pub fn update(&mut self, delta_time: f32) {
        self.position += self.velocity * delta_time;
    }

    pub fn is_collected(&self) -> bool {
        self.collected
    }

    pub fn collect(&mut self) {
        self.collected = true;
    }
}

impl Collidable for Item {
    fn collides_with_circle(&self, center: Vector2, radius: f32) -> bool {
        self.position.distance_to(center) < self.size + radius
    }
}