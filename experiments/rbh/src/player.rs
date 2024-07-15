use raylib::prelude::*;

use crate::{WINDOW_HEIGHT, WINDOW_WIDTH};
use crate::bullet::{Bullet, BulletType};


#[derive(Clone, Copy)]
pub enum Effect {
    None,
    Weak(f32),
    Paralyzed(f32),
    Sick(f32),
}

pub struct Player {
    pub position: Vector2,
    pub speed: f32,
    pub size: f32,
    pub health: f32,
    pub max_health: f32,
    pub damage: f32,
    pub base_damage: f32,
    pub effect: Effect,
    pub shoot_timer: f32,
}

impl Player {
    pub fn new() -> Self {
        Player {
            position: Vector2::new(WINDOW_WIDTH as f32 / 2.0, WINDOW_HEIGHT as f32 - 50.0),
            speed: 5.0,
            size: 20.0,
            health: 100.0,
            max_health: 100.0,
            damage: 10.0,
            base_damage: 10.0,
            effect: Effect::None,
            shoot_timer: 0.0,
        }
    }

    pub fn update(&mut self, rl: &RaylibHandle, delta_time: f32) {
        match self.effect {
            Effect::None => self.move_player(rl),
            Effect::Weak(duration) => {
                self.move_player(rl);
                let new_duration = duration - delta_time;
                if new_duration <= 0.0 {
                    self.effect = Effect::None;
                    self.damage = self.base_damage;
                } else {
                    self.effect = Effect::Weak(new_duration);
                }
            }
            Effect::Paralyzed(duration) => {
                let new_duration = duration - delta_time;
                if new_duration <= 0.0 {
                    self.effect = Effect::None;
                } else {
                    self.effect = Effect::Paralyzed(new_duration);
                }
            }
            Effect::Sick(duration) => {
                self.move_player(rl);
                let new_duration = duration - delta_time;
                if new_duration <= 0.0 {
                    self.effect = Effect::None;
                } else {
                    self.effect = Effect::Sick(new_duration);
                    self.health -= 1.0 * delta_time;
                }
            }
        }

        self.health = self.health.clamp(0.0, self.max_health);
        self.shoot_timer -= delta_time;
    }

    pub fn move_player(&mut self, rl: &RaylibHandle) {
        if rl.is_key_down(KeyboardKey::KEY_LEFT) || rl.is_key_down(KeyboardKey::KEY_A) {
            self.position.x -= self.speed;
        }
        if rl.is_key_down(KeyboardKey::KEY_RIGHT) || rl.is_key_down(KeyboardKey::KEY_D) {
            self.position.x += self.speed;
        }
        if rl.is_key_down(KeyboardKey::KEY_UP) || rl.is_key_down(KeyboardKey::KEY_W) {
            self.position.y -= self.speed;
        }
        if rl.is_key_down(KeyboardKey::KEY_DOWN) || rl.is_key_down(KeyboardKey::KEY_S) {
            self.position.y += self.speed;
        }

        self.position.x = self.position.x.clamp(self.size, WINDOW_WIDTH as f32 - self.size);
        self.position.y = self.position.y.clamp(self.size, WINDOW_HEIGHT as f32 - self.size);
    }

    pub fn draw(&self, d: &mut RaylibDrawHandle) {
        d.draw_circle_v(self.position, self.size, Color::BLUE);
        d.draw_rectangle(10, WINDOW_HEIGHT - 30, (self.health / self.max_health * 200.0) as i32, 20, Color::GREEN);
        d.draw_rectangle_lines(10, WINDOW_HEIGHT - 30, 200, 20, Color::WHITE);
    }

    pub fn apply_effect(&mut self, effect: Effect) {
        match effect {
            Effect::Weak(_) => self.damage = self.base_damage * 0.5,
            Effect::Paralyzed(_) => {},
            Effect::Sick(_) => {},
            Effect::None => {},
        }
        self.effect = effect;
    }

    pub fn shoot(&mut self, mouse_position: Vector2) -> Option<Bullet> {
        if self.shoot_timer <= 0.0 {
            self.shoot_timer = 0.2; // Cooldown between shots
            let direction = (mouse_position - self.position).normalized();
            let velocity = direction * 10.0;
            Some(Bullet::new(self.position, velocity, BulletType::Player, Effect::None))
        } else {
            None
        }
    }
}