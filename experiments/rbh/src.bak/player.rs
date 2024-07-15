use raylib::prelude::*;
use crate::bullet::{Bullet, BulletType};
use crate::item::{Item, ItemType};
use crate::physics::Collidable;
use crate::{WINDOW_HEIGHT, WINDOW_WIDTH};

pub struct Player {
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
    pub dash_cooldown: f32,
    pub dash_timer: f32,
    pub invincibility_timer: f32,
    pub experience: u32,
    pub level: u32,
}

impl Player {
    pub fn new() -> Self {
        Player {
            position: Vector2::new(WINDOW_WIDTH as f32 / 2.0, WINDOW_HEIGHT as f32 - 50.0),
            velocity: Vector2::zero(),
            size: 20.0,
            hp: 100,
            max_hp: 100,
            attack: 10,
            defense: 5,
            speed: 5.0,
            fire_rate: 0.1,
            fire_timer: 0.0,
            dash_cooldown: 1.0,
            dash_timer: 0.0,
            invincibility_timer: 0.0,
            experience: 0,
            level: 1,
        }
    }

    pub fn update(&mut self, rl: &RaylibHandle, delta_time: f32) -> Vec<Bullet> {
        self.handle_movement(rl, delta_time);
        self.handle_dash(rl, delta_time);
        self.update_timers(delta_time);
        self.handle_shooting(rl, delta_time)
    }

    fn handle_movement(&mut self, rl: &RaylibHandle, delta_time: f32) {
        let mut direction = Vector2::zero();
        if rl.is_key_down(KeyboardKey::KEY_W) { direction.y -= 1.0; }
        if rl.is_key_down(KeyboardKey::KEY_S) { direction.y += 1.0; }
        if rl.is_key_down(KeyboardKey::KEY_A) { direction.x -= 1.0; }
        if rl.is_key_down(KeyboardKey::KEY_D) { direction.x += 1.0; }

        if direction != Vector2::zero() {
            direction = direction.normalized();
        }

        self.velocity = direction * self.speed;
        self.position += self.velocity * delta_time;
        self.position.x = self.position.x.clamp(self.size, WINDOW_WIDTH as f32 - self.size);
        self.position.y = self.position.y.clamp(self.size, WINDOW_HEIGHT as f32 - self.size);
    }

    fn handle_dash(&mut self, rl: &RaylibHandle, delta_time: f32) {
        if rl.is_key_pressed(KeyboardKey::KEY_SPACE) && self.dash_timer <= 0.0 {
            self.velocity *= 5.0;
            self.dash_timer = self.dash_cooldown;
            self.invincibility_timer = 0.5;
        }
    }

    fn update_timers(&mut self, delta_time: f32) {
        self.fire_timer -= delta_time;
        self.dash_timer -= delta_time;
        self.invincibility_timer -= delta_time;
    }

    fn handle_shooting(&mut self, rl: &RaylibHandle, delta_time: f32) -> Vec<Bullet> {
        let mut new_bullets = Vec::new();
        if rl.is_mouse_button_down(MouseButton::MOUSE_LEFT_BUTTON) && self.fire_timer <= 0.0 {
            let mouse_pos = rl.get_mouse_position();
            let direction = (mouse_pos - self.position).normalized();
            new_bullets.push(Bullet::new(
                self.position,
                direction * 10.0,
                BulletType::Player,
                self.attack as f32,
                true,
            ));
            self.fire_timer = self.fire_rate;
        }
        new_bullets
    }

    pub fn take_damage(&mut self, damage: f32) {
        if self.invincibility_timer <= 0.0 {
            let actual_damage = (damage - self.defense).max(1);
            self.hp -= actual_damage;
            self.invincibility_timer = 1.0;
        }
    }

    pub fn collect_item(&mut self, item: &Item) {
        match item.item_type {
            ItemType::HealthPotion => self.hp = (self.hp + 20).min(self.max_hp),
            ItemType::AttackBoost => self.attack += 1,
            ItemType::DefenseBoost => self.defense += 1,
            ItemType::SpeedBoost => self.speed += 0.2,
            ItemType::ExperienceOrb => self.gain_experience(50),
        }
    }

    pub fn gain_experience(&mut self, amount: u32) {
        self.experience += amount;
        while self.experience >= self.experience_to_next_level() {
            self.level_up();
        }
    }

    fn experience_to_next_level(&self) -> u32 {
        100 * self.level + 50 * (self.level - 1).pow(2)
    }

    fn level_up(&mut self) {
        self.level += 1;
        self.max_hp += 10;
        self.hp = self.max_hp;
        self.attack += 2;
        self.defense += 1;
        self.speed += 0.1;
    }

    pub fn is_dead(&self) -> bool {
        self.hp <= 0
    }

    pub fn collides_with<T: Collidable>(&self, other: &T) -> bool {
        other.collides_with_circle(self.position, self.size)
    }
}

impl Collidable for Player {
    fn collides_with_circle(&self, center: Vector2, radius: f32) -> bool {
        self.position.distance_to(center) < self.size + radius
    }
}
