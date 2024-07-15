use raylib::prelude::*;
use std::collections::HashMap;
use crate::{WINDOW_HEIGHT, WINDOW_WIDTH, bullet::{Bullet, BulletType}, stats::Stats, item::Item};

#[derive(Clone, Copy, PartialEq, Eq, Hash, Debug)]
pub enum EffectType {
    None,
    Weak,
    Paralyzed,
    Sick,
    Burning,
    Freezing,
}

#[derive(Clone, Copy)]
pub struct Effect {
    pub effect_type: EffectType,
    pub duration: f32,
}

pub struct Player {
    pub position: Vector2,
    pub size: f32,
    pub health: f32,
    pub active_effects: HashMap<EffectType, Effect>,
    pub stats: Stats,
    pub equipped_item: Option<Item>,
    pub shoot_timer: f32,
}

impl Player {
    pub fn new() -> Self {
        Player {
            position: Vector2::new(WINDOW_WIDTH as f32 / 2.0, WINDOW_HEIGHT as f32 - 50.0),
            size: 20.0,
            health: 100.0,
            active_effects: HashMap::new(),
            stats: Stats::default(),
            equipped_item: None,
            shoot_timer: 0.0,
        }
    }

    pub fn update(&mut self, rl: &RaylibHandle, delta_time: f32) {
        self.update_effects(delta_time);
        self.move_player(rl);
        self.shoot_timer -= delta_time;
        self.health = self.health.clamp(0.0, self.stats.max_health);
    }

    fn update_effects(&mut self, delta_time: f32) {
        let mut effects_to_remove = Vec::new();
        
        for (effect_type, effect) in self.active_effects.iter_mut() {
            effect.duration -= delta_time;
            
            if effect.duration <= 0.0 {
                effects_to_remove.push(*effect_type);
            } else {
                match effect_type {
                    EffectType::Weak => self.stats.damage_multiplier = 0.5,
                    EffectType::Sick => self.health -= 1.0 * delta_time,
                    EffectType::Burning => self.health -= 2.0 * delta_time,
                    EffectType::Freezing => self.stats.speed_multiplier = 0.5,
                    _ => {}
                }
            }
        }

        for effect_type in effects_to_remove {
            self.active_effects.remove(&effect_type);
        }
    }

    fn move_player(&mut self, rl: &RaylibHandle) {
        let mut movement = Vector2::zero();

        // paralyze effect - probably want to handle by setting speed to 0
        if self.active_effects.contains_key(&EffectType::Paralyzed) {
            return;
        }

        if rl.is_key_down(KeyboardKey::KEY_LEFT) || rl.is_key_down(KeyboardKey::KEY_A) {
            movement.x -= 1.0;
        }
        if rl.is_key_down(KeyboardKey::KEY_RIGHT) || rl.is_key_down(KeyboardKey::KEY_D) {
            movement.x += 1.0;
        }
        if rl.is_key_down(KeyboardKey::KEY_UP) || rl.is_key_down(KeyboardKey::KEY_W) {
            movement.y -= 1.0;
        }
        if rl.is_key_down(KeyboardKey::KEY_DOWN) || rl.is_key_down(KeyboardKey::KEY_S) {
            movement.y += 1.0;
        }

        if movement != Vector2::zero() {
            movement = movement.normalized() * self.stats.speed * self.stats.speed_multiplier;
            self.position += movement;
        }

        self.position.x = self.position.x.clamp(self.size, WINDOW_WIDTH as f32 - self.size);
        self.position.y = self.position.y.clamp(self.size, WINDOW_HEIGHT as f32 - self.size);
    }

    pub fn draw(&self, d: &mut RaylibDrawHandle) {
        d.draw_circle_v(self.position, self.size, Color::BLUE);
    }

    pub fn apply_effect(&mut self, effect: Effect) {
        self.active_effects.insert(effect.effect_type, effect);
    }

    pub fn shoot(&mut self, mouse_position: Vector2) -> Vec<Bullet> {
        if self.shoot_timer <= 0.0 {
            self.shoot_timer = self.stats.fire_rate;
            let direction = (mouse_position - self.position).normalized();
            
            match &self.equipped_item {
                Some(Item::Weapon(weapon)) => weapon.shoot(self.position, direction),
                _ => vec![Bullet::new(self.position, direction * 10.0, BulletType::Player, None)],
            }
        } else {
            Vec::new()
        }
    }
}