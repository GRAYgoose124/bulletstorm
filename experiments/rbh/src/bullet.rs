use raylib::prelude::*;

use crate::player::{Effect, EffectType};
use crate::network::BulletState;
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
    pub path: BulletPath,
    initial_position: Vector2,
}

pub enum BulletPath {
    Linear,
    Sinusoidal { amplitude: f32, frequency: f32 },
    Parametric { t: f32, x_func: fn(f32) -> f32, y_func: fn(f32) -> f32 },
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
            path: BulletPath::Linear,
            initial_position: position,
        }
    }

    pub fn update(&mut self, delta_time: f32) {
        match self.path {
            BulletPath::Linear => {
                self.position += self.velocity * delta_time;
            },
            BulletPath::Sinusoidal { amplitude, frequency } => {
                let distance = self.velocity.length() * delta_time;
                let angle = (self.position - self.initial_position).angle_to(self.velocity);
                let x = distance * angle.cos();
                let y = distance * angle.sin() + amplitude * (frequency * self.lifetime).sin();
                self.position = self.initial_position + Vector2::new(x, y);
            },
            BulletPath::Parametric { ref mut t, x_func, y_func } => {
                *t += delta_time;
                self.position.x = self.initial_position.x + x_func(*t);
                self.position.y = self.initial_position.y + y_func(*t);
            },
        }
        self.lifetime -= delta_time;
    }

    pub fn from_state(state: BulletState) -> Self {
        Bullet::new(
            Vector2::new(state.position.0, state.position.1),
            Vector2::new(state.velocity.0, state.velocity.1),
            match state.bullet_type.as_str() {
                "Player" => BulletType::Player,
                "Enemy" => BulletType::Enemy,
                _ => BulletType::Enemy,
            },
            None,
        )
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