use raylib::prelude::*;
use crate::player::Effect;
use crate::{WINDOW_HEIGHT, WINDOW_WIDTH};

#[derive(Clone, Copy)]
pub enum BulletType {
    Enemy,
    Player,
}

pub struct Bullet {
    pub position: Vector2,
    pub velocity: Vector2,
    pub radius: f32,
    pub bullet_type: BulletType,
    pub effect: Effect,
}

impl Bullet {
    pub fn new(position: Vector2, velocity: Vector2, bullet_type: BulletType, effect: Effect) -> Self {
        Bullet {
            position,
            velocity,
            radius: 5.0,
            bullet_type,
            effect,
        }
    }

    pub fn update(&mut self) {
        self.position += self.velocity;
    }

    pub fn draw(&self, d: &mut RaylibDrawHandle) {
        let color = match self.bullet_type {
            BulletType::Enemy => Color::YELLOW,
            BulletType::Player => Color::GREEN,
        };
        d.draw_circle_v(self.position, self.radius, color);
    }

    pub fn is_out_of_bounds(&self) -> bool {
        self.position.x < 0.0
            || self.position.x > WINDOW_WIDTH as f32
            || self.position.y < 0.0
            || self.position.y > WINDOW_HEIGHT as f32
    }
}