use raylib::prelude::*;
use rand::{thread_rng, Rng};
use rayon::prelude::*;

use crate::player::Player;
use crate::enemy::{Enemy, EnemyType};
use crate::bullet::{Bullet, BulletType};
use crate::{ui::UI};
use crate::stats::GameStats;

pub struct Game {
    pub player: Player,
    pub enemies: Vec<Enemy>,
    pub bullets: Vec<Bullet>,
    pub stats: GameStats,
    pub ui: UI,
}

impl Game {
    pub fn new() -> Self {
        Game {
            player: Player::new(),
            enemies: Vec::new(),
            bullets: Vec::new(),
            stats: GameStats::default(),
            ui: UI::new(),
        }
    }

    pub fn update(&mut self, rl: &RaylibHandle) {
        let delta_time = rl.get_frame_time();

        self.player.update(rl, delta_time);

        if self.enemies.is_empty() {
            self.stats.wave += 1;
            self.spawn_wave();
        }

        for enemy in &mut self.enemies {
            let new_bullets = enemy.update(delta_time, self.player.position);
            self.bullets.extend(new_bullets);
        }

        if rl.is_mouse_button_down(MouseButton::MOUSE_BUTTON_LEFT) {
            let new_bullets = self.player.shoot(rl.get_mouse_position().into());
            self.bullets.extend(new_bullets);
        }

        self.update_bullets(delta_time);
        self.handle_collisions();
        self.spawn_enemies(delta_time);

        let game_stats = self.stats.clone();
        self.ui.update(game_stats);
    }

    fn update_bullets(&mut self, delta_time: f32) {
        // TODO dedicate thread?
        let indices_to_remove: Vec<usize> = self.bullets.par_iter_mut()
            .enumerate()
            .filter_map(|(index, bullet)| {
                bullet.update(delta_time);
                if bullet.is_expired() || bullet.is_out_of_bounds() {
                    Some(index)
                } else {
                    None
                }
            })
            .collect();
        
        // Remove bullets in reverse order to maintain correct indices
        for &index in indices_to_remove.iter().rev() {
            self.bullets.swap_remove(index);
        }
          
    }

    fn handle_collisions(&mut self) {
        let mut player_hit = false;
        let mut enemies_to_remove = Vec::new();
        let mut bullets_to_remove = Vec::new();

        for (bullet_idx, bullet) in self.bullets.iter().enumerate() {
            match bullet.bullet_type {
                BulletType::Enemy => {
                    if !player_hit && self.player.position.distance_to(bullet.position) < self.player.size + bullet.radius {
                        if let Some(effect) = &bullet.effect {
                            self.player.apply_effect(effect.clone());
                        }
                        self.player.health -= 10.0;
                        bullets_to_remove.push(bullet_idx);
                        player_hit = true;
                    }
                }
                BulletType::Player => {
                    for (enemy_idx, enemy) in self.enemies.iter_mut().enumerate() {
                        if enemy.position.distance_to(bullet.position) < enemy.size + bullet.radius {
                            if enemy.take_damage(self.player.stats.damage * self.player.stats.damage_multiplier) {
                                enemies_to_remove.push(enemy_idx);
                                self.stats.enemies_killed += 1;
                            }
                            bullets_to_remove.push(bullet_idx);
                            break;
                        }
                    }
                }
            }
        }

        for idx in bullets_to_remove.into_iter().rev() {
            self.bullets.swap_remove(idx);
        }

        for idx in enemies_to_remove.into_iter().rev() {
            self.enemies.swap_remove(idx);
        }
    }

    fn spawn_wave(&mut self) {
        for _ in 0..self.stats.wave {
            self.spawn_enemy();
        }
    }

    fn spawn_enemy(&mut self) {
        let mut rng = thread_rng();
        let enemy_type = match rng.gen_range(0..=3) {
            0 => EnemyType::Basic,
            1 => EnemyType::Sniper,
            2 => EnemyType::Shotgun,
            3 => EnemyType::Boss,
            _ => unreachable!(),
        };
        self.enemies.push(Enemy::new(enemy_type));
    }

    fn spawn_enemies(&mut self, delta_time: f32) {
        self.stats.spawn_timer += delta_time;
        if self.stats.spawn_timer >= 5.0 && self.enemies.len() < self.stats.wave as usize * 2 {
            self.spawn_enemy();
            self.stats.spawn_timer = 0.0;
        }
    }

    pub fn draw(&self, d: &mut RaylibDrawHandle) {
        d.clear_background(Color::BLACK);

        for bullet in &self.bullets {
            bullet.draw(d);
        }

        for enemy in &self.enemies {
            enemy.draw(d);
        }

        self.player.draw(d);
        self.ui.draw(d, &self.player, &self.bullets);
    }

    pub fn is_game_over(&self) -> bool {
        self.player.health <= 0.0
    }

    pub fn reset(&mut self) {
        self.player = Player::new();
        self.enemies.clear();
        self.bullets.clear();
        self.stats.wave = 0;
        self.stats.enemies_killed = 0;
        self.stats.spawn_timer = 0.0;
    }
}
