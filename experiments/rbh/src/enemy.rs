use raylib::prelude::*;
use rand::{thread_rng, Rng};
use crate::{WINDOW_WIDTH, WINDOW_HEIGHT, bullet::{Bullet, BulletType}, player::Effect};

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
}

impl Enemy {
    pub fn new(enemy_type: EnemyType) -> Self {
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
            EnemyType::Shotgun => 0.5,
            EnemyType::Boss => 0.8,
        };

        if self.shoot_timer >= shoot_interval {
            self.shoot_timer = 0.0;
            self.shoot(player_position)
        } else {
            Vec::new()
        }
    }

    pub fn shoot(&self, player_position: Vector2) -> Vec<Bullet> {
        let direction = (player_position - self.position).normalized();
        self.shot_pattern.create_bullets(self.position, direction)
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
}

pub enum ShotPattern {
    Single,
    Precise,
    Spread(u32),
    Circular(u32),
}

impl ShotPattern {
    pub fn create_bullets(&self, position: Vector2, direction: Vector2) -> Vec<Bullet> {
        match self {
            ShotPattern::Single => vec![Bullet::new(position, direction * 300.0, BulletType::Enemy, Some(Effect { effect_type: crate::player::EffectType::Weak, duration: 3.0 }))],
            ShotPattern::Precise => vec![Bullet::new(position, direction * 500.0, BulletType::Enemy, Some(Effect { effect_type: crate::player::EffectType::Paralyzed, duration: 1.5 }))],
            ShotPattern::Spread(count) => {
                let mut bullets = Vec::new();
                for i in 0..*count {
                    let angle = (i as f32 - (*count as f32 - 1.0) / 2.0) * 0.2;
                    let mut rotated_direction = direction;
                    rotated_direction.rotate(angle);
                    bullets.push(Bullet::new(position, rotated_direction * 25., BulletType::Enemy, Some(Effect { effect_type: crate::player::EffectType::Sick, duration: 5.0 })));
                }
                bullets
            },
            ShotPattern::Circular(count) => {
                let mut bullets = Vec::new();
                for i in 0..*count {
                    let angle = (i as f32 / *count as f32) * 2.0 * std::f32::consts::PI;
                    let rotated_direction = Vector2::new(angle.cos(), angle.sin());
                    bullets.push(Bullet::new(position, rotated_direction * 300.0, BulletType::Enemy, Some(Effect { effect_type: crate::player::EffectType::Burning, duration: 3.0 })));
                }
                bullets
            },
        }
    }
}