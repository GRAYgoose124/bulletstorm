use raylib::prelude::*;
//use std::f32::consts::PI;

use crate::player::Effect;
use crate::bullet::{Bullet, BulletType};
use crate::{WINDOW_WIDTH, WINDOW_HEIGHT};
use rand::{thread_rng, Rng};

#[derive(Clone, Copy)]
pub enum EnemyType {
    Basic,
    Sniper,
    Shotgun,
}

pub struct Enemy {
    pub position: Vector2,
    pub velocity: Vector2,
    pub size: f32,
    pub shoot_timer: f32,
    pub health: f32,
    pub enemy_type: EnemyType,
}

impl Enemy {
    pub fn new(enemy_type: EnemyType) -> Self {
        let mut rng = thread_rng();

        let (size, health) = match enemy_type {
            EnemyType::Basic => (30.0, 50.0),
            EnemyType::Sniper => (25.0, 30.0),
            EnemyType::Shotgun => (35.0, 70.0),
        };
        Enemy {
            position: Vector2::new(rng.gen_range(50.0..WINDOW_WIDTH as f32 - 50.0), 50.0),
            velocity: Vector2::new(rng.gen_range(-1.0..1.0), rng.gen_range(0.5..1.0)),
            size,
            shoot_timer: 0.0,
            health,
            enemy_type,
        }
    }

    pub fn update(&mut self, delta_time: f32, player_position: Vector2) -> Vec<Bullet> {
        self.position += self.velocity * delta_time * 60.0;

        if self.position.x <= self.size || self.position.x >= WINDOW_WIDTH as f32 - self.size {
            self.velocity.x *= -1.0;
        }
        if self.position.y <= self.size || self.position.y >= WINDOW_HEIGHT as f32 / 2.0 {
            self.velocity.y *= -1.0;
        }

        self.shoot_timer += delta_time;
        let shoot_interval = match self.enemy_type {
            EnemyType::Basic => 1.0,
            EnemyType::Sniper => 2.0,
            EnemyType::Shotgun => 1.5,
        };

        if self.shoot_timer >= shoot_interval {
            self.shoot_timer = 0.0;
            self.shoot(player_position)
        } else {
            Vec::new()
        }
    }

    pub fn shoot(&self, player_position: Vector2) -> Vec<Bullet> {
        match self.enemy_type {
            EnemyType::Basic => {
                let direction = (player_position - self.position).normalized();
                vec![Bullet::new(self.position, direction * 3.0, BulletType::Enemy, Effect::Weak(3.0))]
            }
            EnemyType::Sniper => {
                let direction = (player_position - self.position).normalized();
                vec![Bullet::new(self.position, direction * 5.0, BulletType::Enemy, Effect::Paralyzed(2.0))]
            }
            EnemyType::Shotgun => {
                let mut bullets = Vec::new();
                for i in 0..5 {
                    let angle = (i as f32 - 2.0) * 0.2;
                    let direction = player_position - self.position;
                    direction.normalized().rotate(angle);
                    bullets.push(Bullet::new(self.position, direction * 2.5, BulletType::Enemy, Effect::Sick(5.0)));
                }
                bullets
            }
        }
    }

    pub fn draw(&self, d: &mut RaylibDrawHandle) {
        let color = match self.enemy_type {
            EnemyType::Basic => Color::RED,
            EnemyType::Sniper => Color::PURPLE,
            EnemyType::Shotgun => Color::ORANGE,
        };
        d.draw_circle_v(self.position, self.size, color);
    }

    pub fn take_damage(&mut self, damage: f32) -> bool {
        self.health -= damage;
        self.health <= 0.0
    }
}