use raylib::prelude::*;
use crate::physics::Collidable;
use crate::{WINDOW_HEIGHT, WINDOW_WIDTH};

pub enum BulletType {
    Player,
    Enemy,
}

pub struct Bullet {
    pub position: Vector2,
    pub velocity: Vector2,
    pub bullet_type: BulletType,
    pub damage: f32,
    pub radius: f32,
    pub is_player_bullet: bool,
}

impl Bullet {
    pub fn new(position: Vector2, velocity: Vector2, bullet_type: BulletType, damage: f32, is_player_bullet: bool) -> Self {
        Bullet {
            position,
            velocity,
            bullet_type,
            damage,
            radius: 5.0,
            is_player_bullet,
        }
    }

    pub fn update(&mut self, delta_time: f32) {
        self.position += self.velocity * delta_time;
    }

    pub fn is_out_of_bounds(&self) -> bool {
        self.position.x < -50.0
            || self.position.x > WINDOW_WIDTH as f32 + 50.0
            || self.position.y < -50.0
            || self.position.y > WINDOW_HEIGHT as f32 + 50.0
    }
}


impl Collidable for Bullet {
    fn collides_with_circle(&self, center: Vector2, radius: f32) -> bool {
        self.position.distance_to(center) < self.radius + radius
    }
}