use raylib::prelude::*;
use std::collections::VecDeque;

mod player;
mod enemy;
mod bullet;
mod item;
mod level;

use crate::player::Player;
use crate::enemy::{Enemy, EnemyType};
use crate::bullet::Bullet;
use crate::item::{Item, ItemType};
use crate::level::Level;

pub enum Screen {
    MainMenu,
    GamePlay,
    GameOver,
}

pub enum GameEvent {
    PlayerShoot,
    EnemyShoot,
    PlayerHit,
    EnemyDeath,
    ItemPickup,
    LevelUp,
}

pub struct GameState {
    pub current_screen: Screen,
    pub player: Player,
    pub enemies: Vec<Enemy>,
    pub bullets: Vec<Bullet>,
    pub items: Vec<Item>,
    pub score: u32,
    pub level: Level,
    pub difficulty: f32,
    pub spawn_queue: VecDeque<(EnemyType, f32)>,
    pub events: Vec<GameEvent>,
    pub current_music: Option<MusicTrack>,
    spawn_timer: f32,
}

impl GameState {
    pub fn new() -> Self {
        GameState {
            current_screen: Screen::MainMenu,
            player: Player::new(),
            enemies: Vec::new(),
            bullets: Vec::new(),
            items: Vec::new(),
            score: 0,
            level: Level::new(1),
            difficulty: 1.0,
            spawn_queue: VecDeque::new(),
            events: Vec::new(),
            spawn_timer: 0.0,
            current_music: None,
        }
    }

    pub fn start_new_game(&mut self) {
        self.current_screen = Screen::GamePlay;
        self.player = Player::new();
        self.enemies.clear();
        self.bullets.clear();
        self.items.clear();
        self.score = 0;
        self.level = Level::new(1);
        self.difficulty = 1.0;
        self.spawn_queue.clear();
        self.events.clear();
        self.spawn_timer = 0.0;
        self.current_music = None;
    }

    pub fn update(&mut self, rl: &RaylibHandle, delta_time: f32) {
        self.events.clear();
        let player_bullets = self.player.update(rl, delta_time);
        if !player_bullets.is_empty() {
            self.events.push(GameEvent::PlayerShoot);
        }
        self.bullets.extend(player_bullets);
        
        self.update_enemies(delta_time);
        self.update_bullets(delta_time);
        self.update_items(delta_time);
        self.check_collisions();
        self.spawn_enemies(delta_time);
        self.update_difficulty();
    }

    fn update_enemies(&mut self, delta_time: f32) {
        for enemy in &mut self.enemies {
            let new_bullets = enemy.update(delta_time, &self.player.position, self.difficulty);
            if !new_bullets.is_empty() {
                self.events.push(GameEvent::EnemyShoot);
            }
            self.bullets.extend(new_bullets);
        }
        self.enemies.retain(|enemy| !enemy.is_dead());
    }

    fn update_bullets(&mut self, delta_time: f32) {
        for bullet in &mut self.bullets {
            bullet.update(delta_time);
        }
        self.bullets.retain(|bullet| !bullet.is_out_of_bounds());
    }

    fn update_items(&mut self, delta_time: f32) {
        for item in &mut self.items {
            item.update(delta_time);
        }
        self.items.retain(|item| !item.is_collected());
    }

    fn check_collisions(&mut self) {
        // Player-Bullet collisions
        self.bullets.retain(|bullet| {
            if !bullet.is_player_bullet && self.player.collides_with(bullet) {
                self.player.take_damage(bullet.damage);
                self.events.push(GameEvent::PlayerHit);
                false
            } else {
                true
            }
        });

        // Player-Item collisions
        self.items.retain(|item| {
            if self.player.collides_with(item) {
                self.player.collect_item(item);
                self.events.push(GameEvent::ItemPickup);
                false
            } else {
                true
            }
        });

        // Player-Enemy collisions
        for enemy in &mut self.enemies {
            if self.player.collides_with(enemy) {
                self.player.take_damage(enemy.contact_damage);
                self.events.push(GameEvent::PlayerHit);
            }
        }

        // Bullet-Enemy collisions
        for enemy in &mut self.enemies {
            self.bullets.retain(|bullet| {
                if bullet.is_player_bullet && enemy.collides_with(bullet) {
                    enemy.take_damage(bullet.damage);
                    if enemy.is_dead() {
                        self.score += enemy.score_value;
                        self.events.push(GameEvent::EnemyDeath);
                        if rand::random::<f32>() < 0.1 {
                            self.items.push(Item::new(enemy.position, ItemType::random()));
                        }
                    }
                    false
                } else {
                    true
                }
            });
        }
    }

    fn spawn_enemies(&mut self, delta_time: f32) {
        self.spawn_timer += delta_time;
        while let Some((enemy_type, spawn_time)) = self.spawn_queue.front() {
            if self.spawn_timer >= *spawn_time {
                self.enemies.push(Enemy::new(*enemy_type, self.difficulty));
                self.spawn_queue.pop_front();
            } else {
                break;
            }
        }

        if self.spawn_queue.is_empty() {
            if self.level.next_wave() {
                self.events.push(GameEvent::LevelUp);
            }
            self.spawn_queue = self.level.generate_spawn_queue(self.difficulty);
        }
    }

    fn update_difficulty(&mut self) {
        self.difficulty += 0.01;
    }
}