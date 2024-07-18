use raylib::prelude::*;
use std::rc::Rc;
use std::cell::RefCell;
use std::collections::HashMap;
use rand::{thread_rng, Rng};

use crate::player::Player;
use crate::enemy::{Enemy, EnemyType};
use crate::bullet::{Bullet, BulletType};
use crate::ui::UI;
use crate::stats::GameStats;
use crate::network::{GameState, NetworkManager, PlayerAction, Vector2 as NetworkVector2};
use crate::item::ItemSlot;
use crate::WINDOW_WIDTH;

pub struct Game {
    pub local_player: Rc<RefCell<Player>>,
    pub other_players: HashMap<u32, Rc<RefCell<Player>>>,
    pub enemies: Vec<Enemy>,
    pub bullets: Vec<Bullet>,
    pub stats: GameStats,
    pub ui: UI,
    pub is_multiplayer: bool,
    pub network_manager: Option<NetworkManager>,
}

impl Game {
    pub fn new(is_multiplayer: bool) -> Self {
        let local_player = Rc::new(RefCell::new(Player::new(0)));
        let network_manager = if is_multiplayer {
            match NetworkManager::new("127.0.0.1:8080") {
                Ok(nm) => Some(nm),
                Err(e) => {
                    eprintln!("Failed to create NetworkManager: {}", e);
                    None
                }
            }
        } else {
            None
        };

        Game {
            local_player: local_player.clone(),
            other_players: HashMap::new(),
            enemies: Vec::new(),
            bullets: Vec::new(),
            stats: GameStats::default(),
            ui: UI::new(),
            is_multiplayer,
            network_manager,
        }
    }

    pub fn update(&mut self, rl: &RaylibHandle) {
        let delta_time = rl.get_frame_time();

        self.local_player.borrow_mut().update(rl, delta_time);

        if let Some(ref mut network_manager) = self.network_manager {
            let player_position = self.local_player.borrow().position;
            let move_action = PlayerAction::Move(NetworkVector2::from(player_position));
            if let Err(e) = network_manager.send_player_action(move_action) {
                eprintln!("Failed to send player position: {}", e);
            }

            if rl.is_mouse_button_pressed(MouseButton::MOUSE_BUTTON_LEFT) {
                let mouse_position = rl.get_mouse_position();
                let direction = (mouse_position - player_position).normalized();
                let shoot_action = PlayerAction::Shoot(NetworkVector2::from(direction));
                if let Err(e) = network_manager.send_player_action(shoot_action) {
                    eprintln!("Failed to send player shoot action: {}", e);
                }
            }

            match network_manager.receive_game_state() {
                Ok(game_state) => self.update_from_network(game_state),
                Err(e) => eprintln!("Failed to receive game state: {}", e),
            }
        } else {
            if self.enemies.is_empty() {
                self.stats.wave += 1;
                self.spawn_wave();
            }

            let mut new_bullets = Vec::new();
            for enemy in &mut self.enemies {
                new_bullets.extend(enemy.update(delta_time));
            }
            self.bullets.extend(new_bullets);

            self.spawn_enemies(delta_time);
            self.update_bullets(delta_time);
            self.handle_collisions();
        }

        // Update UI
        self.ui.update(self.stats);
    }

    pub fn draw(&mut self, d: &mut RaylibDrawHandle) {
        d.clear_background(Color::BLACK);

        for bullet in &self.bullets {
            bullet.draw(d);
        }

        for enemy in &self.enemies {
            enemy.draw(d);
        }

        self.local_player.borrow().draw(d);

        for player in self.other_players.values() {
            player.borrow().draw(d);
        }

        self.ui.draw(d, &mut self.local_player.borrow_mut(), &self.other_players, &self.bullets);
    }

    pub fn is_game_over(&self) -> bool {
        self.local_player.borrow().health <= 0.0
    }

    pub fn reset(&mut self) {
        *self.local_player.borrow_mut() = Player::new(0);
        self.enemies.clear();
        self.bullets.clear();
        self.stats.wave = 0;
        self.stats.enemies_killed = 0;
        self.stats.spawn_timer = 0.0;
    }

    pub fn update_from_network(&mut self, game_state: GameState) {
        // Update other players
        for player_state in &game_state.players {
            if player_state.id != self.local_player.borrow().id {
                if let Some(player) = self.other_players.get_mut(&player_state.id) {
                    let mut player = player.borrow_mut();
                    player.position = player_state.position.clone().into(); // Convert NetworkVector2 to raylib Vector2
                    player.health = player_state.health;
                } else {
                    let new_player = Rc::new(RefCell::new(Player::new(player_state.id)));
                    new_player.borrow_mut().position = player_state.position.clone().into(); // Convert NetworkVector2 to raylib Vector2
                    new_player.borrow_mut().health = player_state.health;
                    self.other_players.insert(player_state.id, new_player);
                }
            }
        }

        // Remove disconnected players
        self.other_players.retain(|&id, _| game_state.players.iter().any(|p| p.id == id));

        // Update enemies
        self.enemies = game_state.enemies.into_iter().map(Enemy::from_state).collect();

        // Update bullets
        self.bullets = game_state.bullets.into_iter().map(Bullet::from_state).collect();

        // Update wave
        self.stats.wave = game_state.wave;
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
        let id = self.enemies.len() as u32;
        self.enemies.push(Enemy::new(id, enemy_type, self.local_player.clone()));
    }

    fn spawn_enemies(&mut self, delta_time: f32) {
        self.stats.spawn_timer += delta_time;
        if self.stats.spawn_timer >= 5.0 && self.enemies.len() < self.stats.wave as usize * 3 {
            self.spawn_enemy();
            self.stats.spawn_timer = 0.0;
        }
    }

    fn create_player_bullets(&self, mouse_position: Vector2) -> Vec<Bullet> {
        let player = self.local_player.borrow();
        let direction = (mouse_position - player.position).normalized();
        let bullet_speed = 10.0; // Adjust this value to control bullet speed
        
        vec![Bullet::new(player.position, direction, bullet_speed, BulletType::Player, None)]
    }

    fn update_bullets(&mut self, delta_time: f32) {
        self.bullets.retain_mut(|bullet| {
            bullet.update(delta_time);
            !bullet.is_expired() && !bullet.is_out_of_bounds()
        });
    }

    fn handle_collisions(&mut self) {
        let mut player_hit = false;
        let mut enemies_to_remove = Vec::new();
        let mut bullets_to_remove = Vec::new();

        // Check bullet collisions
        for (bullet_idx, bullet) in self.bullets.iter().enumerate() {
            match bullet.bullet_type {
                BulletType::Enemy => {
                    let mut player = self.local_player.borrow_mut();
                    if !player_hit && player.position.distance_to(bullet.position) < player.size + bullet.radius {
                        if let Some(effect) = &bullet.effect {
                            player.apply_effect(effect.clone());
                        }
                        player.health -= 1.0;
                        bullets_to_remove.push(bullet_idx);
                        player_hit = true;
                    }
                }
                BulletType::Player => {
                    for (enemy_idx, enemy) in self.enemies.iter_mut().enumerate() {
                        if enemy.position.distance_to(bullet.position) < enemy.size + bullet.radius {
                            if enemy.take_damage(self.local_player.borrow().stats.damage * self.local_player.borrow().stats.damage_multiplier) {
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

        // Remove bullets and enemies safely
        bullets_to_remove.sort_unstable_by(|a, b| b.cmp(a));
        for &idx in bullets_to_remove.iter() {
            if idx < self.bullets.len() {
                self.bullets.remove(idx);
            }
        }

        enemies_to_remove.sort_unstable_by(|a, b| b.cmp(a));
        for &idx in enemies_to_remove.iter() {
            if idx < self.enemies.len() {
                self.enemies.remove(idx);
            }
        }
    }

    pub fn equip_item(&mut self, inventory_index: usize) {
        let mut player = self.local_player.borrow_mut();
        if let Some(item) = player.inventory.remove_item(inventory_index) {
            player.equip_item(item);
        }
    }

    pub fn handle_inventory_interactions(&mut self, rl: &RaylibHandle) {
        let mouse_position = rl.get_mouse_position();

        let items_count = self.local_player.borrow().inventory.get_items().len();
        for i in 0..items_count {
            let item_rect = Rectangle::new(20.0, 20.0 + i as f32 * 30.0, 180.0, 25.0);
            if item_rect.check_collision_point_rec(mouse_position) && rl.is_mouse_button_pressed(MouseButton::MOUSE_BUTTON_LEFT) {
                self.equip_item(i);
                break;
            }
        }

        let slots: Vec<ItemSlot> = vec![
            ItemSlot::Helmet,
            ItemSlot::Chest,
            ItemSlot::Gloves,
            ItemSlot::Boots,
            ItemSlot::Weapon,
            ItemSlot::Ring1,
            ItemSlot::Ring2,
            ItemSlot::Amulet,
        ];

        for (i, slot) in slots.iter().enumerate() {
            let slot_rect = Rectangle::new(WINDOW_WIDTH as f32 - 200.0, 20.0 + i as f32 * 40.0, 180.0, 35.0);
            if slot_rect.check_collision_point_rec(mouse_position) && rl.is_mouse_button_pressed(MouseButton::MOUSE_BUTTON_LEFT) {
                self.local_player.borrow_mut().unequip_item(slot.clone());
                break;
            }
        }
    }
}