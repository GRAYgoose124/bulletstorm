use raylib::prelude::*;
use rand::{thread_rng, Rng};

use crate::player::Player;
use crate::enemy::{Enemy, EnemyType};
use crate::bullet::{Bullet, BulletType};
use crate::{WINDOW_WIDTH};

pub struct Game {
    pub player: Player,
    pub enemies: Vec<Enemy>,
    pub bullets: Vec<Bullet>,
    pub wave: u32,
    pub enemies_killed: u32,
    pub spawn_timer: f32,
}

impl Game {
    pub fn new() -> Self {
        Game {
            player: Player::new(),
            enemies: Vec::new(),
            bullets: Vec::new(),
            wave: 0,
            enemies_killed: 0,
            spawn_timer: 0.0,
        }
    }

    pub fn update(&mut self, rl: &RaylibHandle) {
        let delta_time = rl.get_frame_time();

        self.player.update(rl, delta_time);

        // Spawn new wave if all enemies are defeated
        if self.enemies.is_empty() {
            self.wave += 1;
            self.spawn_wave();
        }

        // Update enemies and their bullets
        for enemy in &mut self.enemies {
            let new_bullets = enemy.update(delta_time, self.player.position);
            self.bullets.extend(new_bullets);
        }

        // Player shooting
        if rl.is_mouse_button_down(MouseButton::MOUSE_BUTTON_LEFT) {
            if let Some(bullet) = self.player.shoot(rl.get_mouse_position().into()) {
                self.bullets.push(bullet);
            }
        }

        // Update bullets
        for bullet in &mut self.bullets {
            bullet.update();
        }

        // Check for collisions
        self.handle_collisions();

        // Remove out-of-bounds bullets
        self.bullets.retain(|bullet| !bullet.is_out_of_bounds());

        // Spawn new enemies
        self.spawn_timer += delta_time;
        if self.spawn_timer >= 5.0 && self.enemies.len() < (self.wave * 2).try_into().unwrap() {
            self.spawn_enemy();
            self.spawn_timer = 0.0;
        }
    }

    fn spawn_wave(&mut self) {
        for _ in 0..self.wave {
            self.spawn_enemy();
        }
    }

    fn spawn_enemy(&mut self) {
        let mut rng = thread_rng();

        let enemy_type = match rng.gen_range(0 .. 3) {
            0 => EnemyType::Basic,
            1 => EnemyType::Sniper,
            _ => EnemyType::Shotgun,
        };
        self.enemies.push(Enemy::new(enemy_type));
    }

    fn handle_collisions(&mut self) {
        let mut bullets_to_remove = Vec::new();
        let mut enemies_to_remove = Vec::new();

        for (bullet_index, bullet) in self.bullets.iter().enumerate() {
            match bullet.bullet_type {
                BulletType::Enemy => {
                    if self.player.position.distance_to(bullet.position) < self.player.size + bullet.radius {
                        self.player.apply_effect(bullet.effect);
                        self.player.health -= 10.0;
                        bullets_to_remove.push(bullet_index);
                    }
                }
                BulletType::Player => {
                    for (enemy_index, enemy) in self.enemies.iter_mut().enumerate() {
                        if enemy.position.distance_to(bullet.position) < enemy.size + bullet.radius {
                            if enemy.take_damage(self.player.damage) {
                                enemies_to_remove.push(enemy_index);
                                self.enemies_killed += 1;
                            }
                            bullets_to_remove.push(bullet_index);
                            break;
                        }
                    }
                }
            }
        }

        // Remove collided bullets and enemies
        for index in bullets_to_remove.iter().rev() {
            self.bullets.swap_remove(*index);
        }
        for index in enemies_to_remove.iter().rev() {
            self.enemies.swap_remove(*index);
        }
    }

    pub fn draw(&self, d: &mut RaylibDrawHandle) {
        d.clear_background(Color::BLACK);

        for bullet in &self.bullets {
            bullet.draw(d);
        }

        self.player.draw(d);

        for enemy in &self.enemies {
            enemy.draw(d);
        }

        d.draw_text(&format!("Health: {:.0}", self.player.health), 10, 10, 20, Color::WHITE);
        d.draw_text(&format!("Wave: {}", self.wave), 10, 40, 20, Color::WHITE);
        d.draw_text(&format!("Enemies Killed: {}", self.enemies_killed), 10, 70, 20, Color::WHITE);
        d.draw_fps(WINDOW_WIDTH - 100, 10);
    }

    pub fn is_game_over(&self) -> bool {
        self.player.health <= 0.0
    }

    pub fn reset(&mut self) {
        self.player = Player::new();
        self.enemies.clear();
        self.bullets.clear();
        self.wave = 0;
        self.enemies_killed = 0;
        self.spawn_timer = 0.0;
    }
}
