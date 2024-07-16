use raylib::prelude::*;

use crate::player::{Effect, EffectType};
use crate::{WINDOW_HEIGHT, WINDOW_WIDTH};

#[derive(Clone, Copy)]
pub enum BulletType {
    Enemy,
    Player,
}

// TODO: damage
pub struct Bullet {
    pub position: Vector2,
    pub velocity: Vector2,
    pub radius: f32,
    pub bullet_type: BulletType,
    pub effect: Option<Effect>,
    pub color: Color,
    pub lifetime: f32,
}

impl Bullet {
    pub fn new(position: Vector2, velocity: Vector2, bullet_type: BulletType, effect: Option<Effect>) -> Self {
        let (color, lifetime) = match bullet_type {
            BulletType::Player => (Color::GREEN, 2.0),
            BulletType::Enemy => {
                match effect {
                    Some(Effect { effect_type, .. }) => match effect_type {
                        EffectType::Weak => (Color::YELLOW, 1.5),
                        EffectType::Paralyzed => (Color::PURPLE, 1.0),
                        EffectType::Sick => (Color::LIME, 1.5),
                        EffectType::Burning => (Color::RED, 1.5),
                        EffectType::Freezing => (Color::SKYBLUE, 1.5),
                        EffectType::None => (Color::WHITE, 1.5),
                    },
                    None => (Color::WHITE, 1.5),
                }
            }
        };

        Bullet {
            position,
            velocity,
            radius: 5.0,
            bullet_type,
            effect,
            color,
            lifetime,
        }
    }

    pub fn update(&mut self, delta_time: f32) {
        self.position += self.velocity * delta_time;
        self.lifetime -= delta_time;
    }

    pub fn draw(&self, d: &mut RaylibDrawHandle) {
        d.draw_circle_v(self.position, self.radius, self.color);
    }

    pub fn is_out_of_bounds(&self) -> bool {
        self.position.x < 0.0
            || self.position.x > WINDOW_WIDTH as f32
            || self.position.y < 0.0
            || self.position.y > WINDOW_HEIGHT as f32
    }

    pub fn is_expired(&self) -> bool {
        self.lifetime <= 0.0
    }
}