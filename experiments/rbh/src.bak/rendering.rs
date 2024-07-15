use raylib::prelude::*;
use crate::game_state::GameState;
use crate::item::{Item, ItemType};
use crate::player::Player;
use crate::bullet::Bullet;
use crate::enemy::{Enemy, EnemyType};
use crate::{WINDOW_WIDTH, WINDOW_HEIGHT};


pub struct Renderer {
    camera: Camera2D,
    pub handle: Option<RaylibDrawHandle>,
}

impl Renderer {
    pub fn new(rl: &mut RaylibHandle, thread: &RaylibThread) -> Self {
        Renderer {
            camera: Camera2D {
                offset: Vector2::new(WINDOW_WIDTH as f32 / 2.0, WINDOW_HEIGHT as f32 / 2.0),
                target: Vector2::zero(),
                rotation: 0.0,
                zoom: 1.0,
            },
            handle: None,
        }
    }

    pub fn begin(&mut self, rl: &'static mut RaylibHandle, thread: &RaylibThread) {
        let mut d = rl.begin_drawing(thread);
        d.clear_background(Color::BLACK);
        d.begin_mode2D(self.camera);
        self.handle = Some(d);
    }

    pub fn end(&mut self, rl: &mut RaylibHandle, thread: &RaylibThread) {
        self.handle = None;
        d.end_mode2D();
    }

    pub fn draw_game(&mut self, game_state: &GameState) {
        self.draw_background(&mut self.handle.unwrap());
        self.draw_bullets(&mut self.handle.unwrap(), &game_state.bullets);
        self.draw_enemies(&mut self.handle, &game_state.enemies);
        self.draw_items(&mut self.handle.unwrap(), &game_state.items);
        self.draw_player(&mut self.handle.unwrap(), &game_state.player);
    }

    fn draw_background(&self, d: &mut RaylibDrawHandle) {
        for i in 0..20 {
            for j in 0..15 {
                let color = if (i + j) % 2 == 0 {
                    Color::new(10, 10, 40, 255)
                } else {
                    Color::new(20, 20, 50, 255)
                };
                d.draw_rectangle(
                    i * 64,
                    j * 64,
                    64,
                    64,
                    color,
                );
            }
        }
    }

    fn draw_player(&self, d: &mut RaylibDrawHandle, player: &Player) {
        d.draw_circle_v(player.position, player.size, Color::BLUE);
        let health_bar_width = player.size * 2.0;
        let health_percentage = player.hp as f32 / player.max_hp as f32;
        d.draw_rectangle_v(
            Vector2::new(player.position.x - health_bar_width / 2.0, player.position.y - player.size - 10.0),
            Vector2::new(health_bar_width, 5.0),
            Color::RED,
        );
        d.draw_rectangle_v(
            Vector2::new(player.position.x - health_bar_width / 2.0, player.position.y - player.size - 10.0),
            Vector2::new(health_bar_width * health_percentage, 5.0),
            Color::GREEN,
        );
    }
    
    fn draw_enemies(&self, d: &mut RaylibDrawHandle, enemies: &Vec<Enemy>) {
        for enemy in enemies {
            let color = match enemy.enemy_type {
                EnemyType::Basic => Color::RED,
                EnemyType::Sniper => Color::ORANGE,
                EnemyType::Shotgun => Color::PURPLE,
                EnemyType::Sine => Color::PINK,
                EnemyType::Boss => Color::MAROON,
            };
            d.draw_circle_v(enemy.position, enemy.size, color);
            let health_bar_width = enemy.size * 2.0;
            let health_percentage = enemy.hp as f32 / enemy.max_hp as f32;
            d.draw_rectangle_v(
                Vector2::new(enemy.position.x - health_bar_width / 2.0, enemy.position.y - enemy.size - 10.0),
                Vector2::new(health_bar_width, 5.0),
                Color::RED,
            );
            d.draw_rectangle_v(
                Vector2::new(enemy.position.x - health_bar_width / 2.0, enemy.position.y - enemy.size - 10.0),
                Vector2::new(health_bar_width * health_percentage, 5.0),
                Color::GREEN,
            );
        }
    }

    fn draw_bullets(&self, d: &mut RaylibDrawHandle, bullets: &Vec<Bullet>) {
        for bullet in bullets {
            let color = if bullet.is_player_bullet {
                Color::SKYBLUE
            } else {
                Color::ORANGE
            };
            d.draw_circle_v(bullet.position, bullet.radius, color);
        }
    }

    fn draw_items(&self, d: &mut RaylibDrawHandle, items: &Vec<Item>) {
        for item in items {
            let color = match item.item_type {
                ItemType::HealthPotion => Color::GREEN,
                ItemType::AttackBoost => Color::RED,
                ItemType::DefenseBoost => Color::BLUE,
                ItemType::SpeedBoost => Color::YELLOW,
                ItemType::ExperienceOrb => Color::PURPLE,
            };
            d.draw_circle_v(item.position, item.size, color);
        }
    }
}