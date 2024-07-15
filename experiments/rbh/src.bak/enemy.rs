use raylib::prelude::*;
use std::f32::consts::PI;
use crate::bullet::{Bullet, BulletType};
use crate::physics::Collidable;
use crate::{WINDOW_HEIGHT, WINDOW_WIDTH};

pub enum EnemyType {
    Basic,
    Sniper,
    Shotgun,
    Sine,
    Boss,
}

pub struct Enemy {
    pub position: Vector2,
    pub velocity: Vector2,
    pub size: f32,
    pub hp: i32,
    pub max_hp: i32,
    pub attack: i32,
    pub defense: i32,
    pub speed: f32,
    pub fire_rate: f32,
    pub fire_timer: f32,
    pub enemy_type: EnemyType,
    pub score_value: u32,
    pub contact_damage: i32,
    movement_timer: f32,
}

impl Enemy {
    pub fn new(enemy_type: EnemyType, difficulty: f32) -> Self {
        let (hp, attack, defense, speed, fire_rate, size, score_value) = match enemy_type {
            EnemyType::Basic => (50, 5, 0, 2.0, 1.0, 20.0, 10),
            EnemyType::Sniper => (30, 15, 0, 1.5, 2.0, 15.0, 20),
            EnemyType::Shotgun => (80, 3, 2, 1.0, 1.5, 25.0, 30),
            EnemyType::Sine => (40, 7, 1, 3.0, 0.8, 18.0, 25),
            EnemyType::Boss => (500, 20, 10, 1.0, 0.5, 50.0, 1000),
        };

        Enemy {
            position: Vector2::new(rand::random::<f32>() * WINDOW_WIDTH as f32, -50.0),
            velocity: Vector2::zero(),
            size,
            hp: (hp as f32 * difficulty) as i32,
            max_hp: (hp as f32 * difficulty) as i32,
            attack: (attack as f32 * difficulty.sqrt()) as i32,
            defense: defense,
            speed: speed * difficulty.sqrt(),
            fire_rate: fire_rate / difficulty.sqrt(),
            fire_timer: 0.0,
            enemy_type,
            score_value: (score_value as f32 * difficulty) as u32,
            contact_damage: (attack as f32 * 0.5 * difficulty.sqrt()) as i32,
            movement_timer: 0.0,
        }
    }

    pub fn update(&mut self, delta_time: f32, player_pos: &Vector2, difficulty: f32) -> Vec<Bullet> {
        self.movement_timer += delta_time;
        self.fire_timer -= delta_time;

        match self.enemy_type {
            EnemyType::Basic => self.basic_movement(delta_time),
            EnemyType::Sniper => self.sniper_movement(delta_time, player_pos),
            EnemyType::Shotgun => self.shotgun_movement(delta_time),
            EnemyType::Sine => self.sine_movement(delta_time),
            EnemyType::Boss => self.boss_movement(delta_time, player_pos),
        }

        self.position += self.velocity * delta_time;
        self.position.x = self.position.x.clamp(self.size, WINDOW_WIDTH as f32 - self.size);

        if self.fire_timer <= 0.0 {
            self.fire_timer = self.fire_rate;
            self.shoot(player_pos, difficulty)
        } else {
            Vec::new()
        }
    }

    fn basic_movement(&mut self, delta_time: f32) {
        self.velocity = Vector2::new(0.0, self.speed);
    }

    fn sniper_movement(&mut self, delta_time: f32, player_pos: &Vector2) {
        let direction = (*player_pos - self.position).normalized();
        self.velocity = direction * self.speed * 0.5;
    }

    fn shotgun_movement(&mut self, delta_time: f32) {
        self.velocity = Vector2::new((self.movement_timer * 2.0).sin() * self.speed, self.speed * 0.5);
    }

    fn sine_movement(&mut self, delta_time: f32) {
        self.velocity = Vector2::new((self.movement_timer * 3.0).sin() * self.speed * 2.0, self.speed);
    }

    fn boss_movement(&mut self, delta_time: f32, player_pos: &Vector2) {
        let direction = (*player_pos - self.position).normalized();
        self.velocity = direction * self.speed * (0.5 + 0.5 * (self.movement_timer * 0.5).sin());
    }

    fn shoot(&self, player_pos: &Vector2, difficulty: f32) -> Vec<Bullet> {
        match self.enemy_type {
            EnemyType::Basic => vec![self.create_bullet(player_pos, 0.0, difficulty)],
            EnemyType::Sniper => vec![self.create_bullet(player_pos, 0.0, difficulty * 1.5)],
            EnemyType::Shotgun => (-1..=1)
                .map(|i| self.create_bullet(player_pos, i as f32 * PI / 6.0, difficulty * 0.8))
                .collect(),
            EnemyType::Sine => (0..2)
                .map(|i| self.create_bullet(player_pos, (i as f32 - 0.5) * PI / 8.0, difficulty))
                .collect(),
            EnemyType::Boss => (0..5)
                .map(|i| self.create_bullet(player_pos, (i as f32 - 2.0) * PI / 10.0, difficulty * 1.2))
                .collect(),
        }
    }

    fn create_bullet(&self, player_pos: &Vector2, angle_offset: f32, difficulty: f32) -> Bullet {
        let direction = *player_pos - self.position;
        direction.normalized().rotate(angle_offset);
        Bullet::new(
            self.position,
            direction * 5.0 * difficulty.sqrt(),
            BulletType::Enemy,
            self.attack as f32,
            false,
        )
    }

    pub fn take_damage(&mut self, damage: i32) {
        let actual_damage = (damage - self.defense).max(1);
        self.hp -= actual_damage;
    }

    pub fn is_dead(&self) -> bool {
        self.hp <= 0
    }
}

impl Collidable for Enemy {
    fn collides_with_circle(&self, center: Vector2, radius: f32) -> bool {
        self.position.distance_to(center) < self.size + radius
    }
}