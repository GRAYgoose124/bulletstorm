use raylib::prelude::*;
use rand::{thread_rng, Rng};
use raylib::math::Vector2;
use std::rc::Rc;
use std::cell::RefCell;
use rand::prelude::SliceRandom;

use crate::{WINDOW_WIDTH, WINDOW_HEIGHT, bullet::{Bullet, BulletType}};
use crate::player::Player;
use crate::player::Effect;
use crate::player::EffectType;

#[derive(Clone, Copy)]
pub enum EnemyType {
    Basic,
    Sniper,
    Shotgun,
    Boss,
}

pub struct Enemy {
    pub position: Vector2,
    pub velocity: Vector2,
    pub size: f32,
    pub shoot_timer: f32,
    pub health: f32,
    pub enemy_type: EnemyType,
    pub shot_pattern: ShotPattern,
    player: Rc<RefCell<Player>>,
}

impl Enemy {
    pub fn new(enemy_type: EnemyType, player: Rc<RefCell<Player>>) -> Self {
        let mut rng = thread_rng();

        let (size, health, shot_pattern) = match enemy_type {
            EnemyType::Basic => (30.0, 50.0, ShotPattern::Single),
            EnemyType::Sniper => (25.0, 30.0, ShotPattern::Precise),
            EnemyType::Shotgun => (35.0, 70.0, ShotPattern::Spread(5)),
            EnemyType::Boss => (50.0, 200.0, ShotPattern::Circular(8)),
        };

        Enemy {
            position: Vector2::new(rng.gen_range(50.0..WINDOW_WIDTH as f32 - 50.0), 50.0),
            velocity: Vector2::new(rng.gen_range(-1.0..1.0), rng.gen_range(0.5..1.0)),
            size,
            shoot_timer: 0.0,
            health,
            enemy_type,
            shot_pattern,
            player,
        }
    }

    pub fn update(&mut self, delta_time: f32) -> Vec<Bullet> {
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
            EnemyType::Shotgun => 0.5,
            EnemyType::Boss => 0.15,
        };

        if self.shoot_timer >= shoot_interval {
            self.shoot_timer = 0.0;
            self.shoot()
        } else {
            Vec::new()
        }
    }

    pub fn shoot(&self) -> Vec<Bullet> {
        let player_position = self.player.borrow().position;
        let direction = (player_position - self.position).normalized();
        let effect_type = self.random_effect_type();

        self.shot_pattern.create_bullets(self.position, direction, BulletType::Enemy, Some(effect_type))
    }

    pub fn draw(&self, d: &mut RaylibDrawHandle) {
        let color = match self.enemy_type {
            EnemyType::Basic => Color::RED,
            EnemyType::Sniper => Color::PURPLE,
            EnemyType::Shotgun => Color::ORANGE,
            EnemyType::Boss => Color::MAROON,
        };
        d.draw_circle_v(self.position, self.size, color);
    }

    pub fn take_damage(&mut self, damage: f32) -> bool {
        self.health -= damage;
        self.health <= 0.0
    }

    fn random_effect_type(&self) -> Effect {
        let mut rng = thread_rng();
        let effect_type = match self.enemy_type {
            EnemyType::Basic => vec![EffectType::Weak, EffectType::Paralyzed, EffectType::Sick, EffectType::Burning, EffectType::Freezing],
            EnemyType::Sniper => vec![EffectType::Weak, EffectType::Sick, EffectType::Burning, EffectType::Freezing],
            EnemyType::Shotgun => vec![EffectType::Weak, EffectType::Sick, EffectType::Burning, EffectType::Freezing],
            EnemyType::Boss => vec![EffectType::Weak, EffectType::Sick, EffectType::Burning, EffectType::Freezing],
        };
        Effect {
            effect_type: *effect_type.choose(&mut rng).unwrap(),
            duration: rng.gen_range(1.0..5.0),
        }
    }
}

#[derive(Clone, Copy)]
pub enum ShotPattern {
    Single,
    Precise,
    Spread(u32),
    Circular(u32),
}

impl ShotPattern {
    pub fn create_bullets(&self, position: Vector2, direction: Vector2, bullet_type: BulletType, effect: Option<Effect>) -> Vec<Bullet> {
        match self {
            ShotPattern::Single => vec![Bullet::new(position, direction * 300.0, bullet_type, effect)],
            ShotPattern::Precise => vec![Bullet::new(position, direction * 500.0, bullet_type, effect)],
            ShotPattern::Spread(count) => {
                let mut bullets = Vec::new();
                for i in 0..*count {
                    let angle = (i as f32 - (*count as f32 - 1.0) / 2.0) * 0.2;
                    let mut rotated_direction = direction;
                    rotated_direction.rotate(angle);
                    bullets.push(Bullet::new(position, rotated_direction * 250.0, bullet_type, effect.clone()));
                }
                bullets
            },
            ShotPattern::Circular(count) => {
                let mut bullets = Vec::new();
                for i in 0..*count {
                    let angle = (i as f32 / *count as f32) * 2.0 * std::f32::consts::PI;
                    let rotated_direction = Vector2::new(angle.cos(), angle.sin());
                    bullets.push(Bullet::new(position, rotated_direction * 300.0, bullet_type, effect.clone()));
                }
                bullets
            },
        }
    }
}