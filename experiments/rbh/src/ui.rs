// ui.rs
use raylib::prelude::*;
use std::rc::Rc;
use std::cell::RefCell;
use std::collections::HashMap;
use cstr::cstr;

use crate::player::Player;
use crate::bullet::Bullet;
use crate::stats::GameStats;
use crate::item::{Item, ItemSlot};
use crate::{WINDOW_HEIGHT, WINDOW_WIDTH};

pub struct UI {
    wave: u32,
    enemies_killed: u32,
    pub inventory_open: bool,
}

impl UI {
    pub fn new() -> Self {
        UI {
            wave: 0,
            enemies_killed: 0,
            inventory_open: false,
        }
    }

    pub fn update(&mut self, stats: GameStats) {
        self.wave = stats.wave;
        self.enemies_killed = stats.enemies_killed;
    }

    pub fn draw(&mut self, d: &mut RaylibDrawHandle, local_player: &mut Player, other_players: &HashMap<u32, Rc<RefCell<Player>>>, bullets: &[Bullet]) {
        self.draw_player_hud(d, local_player);
        self.draw_other_players_info(d, other_players);
        self.draw_game_stats(d);
        self.draw_bullet_count(d, bullets);
        
        if d.gui_button(Rectangle::new(WINDOW_WIDTH as f32 - 110.0, WINDOW_HEIGHT as f32 - 40.0, 100.0, 30.0), Some(cstr!("Inventory"))) {
            self.inventory_open = !self.inventory_open;
        }
        
        if self.inventory_open {
            self.draw_inventory(d, local_player);
        }

        d.draw_fps(10, 10);
    }

    fn draw_player_hud(&self, d: &mut RaylibDrawHandle, player: &Player) {
        // Draw health bar
        let health_width = (player.health / player.stats.max_health * 200.0) as i32;
        d.draw_rectangle(10, WINDOW_HEIGHT - 30, health_width, 20, Color::GREEN);
        d.draw_rectangle_lines(10, WINDOW_HEIGHT - 30, 200, 20, Color::WHITE);

        // Draw active effects
        let mut effect_y = WINDOW_HEIGHT - 60;
        for (effect_type, effect) in &player.active_effects {
            let effect_text = format!("{:?}: {:.1}s", effect_type, effect.duration);
            d.draw_text(&effect_text, 10, effect_y, 15, Color::YELLOW);
            effect_y -= 20;
        }
    }

    fn draw_other_players_info(&self, d: &mut RaylibDrawHandle, other_players: &HashMap<u32, Rc<RefCell<Player>>>) {
        for (i, player) in other_players.values().enumerate() {
            let player = player.borrow();
            let y_offset = i as i32 * 25;
            d.draw_text(&format!("Player {}: {:.0} HP", player.id, player.health), 10, 40 + y_offset, 20, Color::WHITE);
        }
    }

    fn draw_game_stats(&self, d: &mut RaylibDrawHandle) {
        d.draw_text(&format!("Wave: {}", self.wave), WINDOW_WIDTH - 150, 10, 20, Color::WHITE);
        d.draw_text(&format!("Enemies: {}", self.enemies_killed), WINDOW_WIDTH - 150, 35, 20, Color::WHITE);
    }

    fn draw_bullet_count(&self, d: &mut RaylibDrawHandle, bullets: &[Bullet]) {
        d.draw_text(&format!("Bullets: {}", bullets.len()), WINDOW_WIDTH - 150, 60, 20, Color::WHITE);
    }

    fn draw_inventory(&self, d: &mut RaylibDrawHandle, player: &mut Player) {
        let inventory_bg = Rectangle::new(10.0, 10.0, 200.0, WINDOW_HEIGHT as f32 - 20.0);
        d.draw_rectangle_rec(inventory_bg, Color::new(0, 0, 0, 200));
        d.draw_rectangle_lines_ex(inventory_bg, 2.0, Color::WHITE);
        self.draw_gear_board(d, player);

        for (i, item) in player.inventory.clone().get_items().iter().enumerate() {
            let item_rect = Rectangle::new(20.0, 20.0 + i as f32 * 30.0, 180.0, 25.0);
            d.draw_rectangle_rec(item_rect, Color::GRAY);
            d.draw_text(&item.name, 25, 25 + i as i32 * 30, 20, Color::WHITE);

            // Draw tooltip if mouse is over the item
            let mouse_position = d.get_mouse_position();
            if item_rect.check_collision_point_rec(mouse_position) {
                self.draw_item_tooltip(d, item, mouse_position.x as i32, mouse_position.y as i32);
            }
            
            // Equip item on left click
            if item_rect.check_collision_point_rec(mouse_position) && d.is_mouse_button_pressed(MouseButton::MOUSE_BUTTON_LEFT) {
                player.equip_item(item.clone());
            }
        }

    }

    fn draw_gear_board(&self, d: &mut RaylibDrawHandle, player: &Player) {
        let gear_bg = Rectangle::new(WINDOW_WIDTH as f32 - 210.0, 10.0, 200.0, WINDOW_HEIGHT as f32 - 20.0);
        d.draw_rectangle_rec(gear_bg, Color::new(0, 0, 0, 200));
        d.draw_rectangle_lines_ex(gear_bg, 2.0, Color::WHITE);

        let slots = vec![
            (ItemSlot::Helmet, "Helmet"),
            (ItemSlot::Chest, "Chest"),
            (ItemSlot::Gloves, "Gloves"),
            (ItemSlot::Boots, "Boots"),
            (ItemSlot::Weapon, "Weapon"),
            (ItemSlot::Ring1, "Ring 1"),
            (ItemSlot::Ring2, "Ring 2"),
            (ItemSlot::Amulet, "Amulet"),
        ];

        for (i, (slot, name)) in slots.into_iter().enumerate() {
            let slot_rect = Rectangle::new(WINDOW_WIDTH as f32 - 200.0, 20.0 + i as f32 * 40.0, 180.0, 35.0);
            d.draw_rectangle_rec(slot_rect, Color::DARKGRAY);
            d.draw_text(name, WINDOW_WIDTH - 195, 25 + i as i32 * 40, 20, Color::WHITE);

            if let Some(item) = player.equipped_items.get(&slot) {
                d.draw_text(&item.name, WINDOW_WIDTH - 190, 45 + i as i32 * 40, 16, Color::YELLOW);
            }
        }
    }

    fn draw_item_tooltip(&self, d: &mut RaylibDrawHandle, item: &Item, x: i32, y: i32) {
        let tooltip_text = format!(
            "{}
Slot: {:?}
Damage: {}
Max Health: {}
Speed: {}
Fire Rate: {}",
            item.name, item.slot, item.stats.damage, item.stats.max_health, item.stats.speed, item.stats.fire_rate
        );

        let text_size = 16;
        let padding = 5;
        let line_count = tooltip_text.lines().count() as i32;
        let rect_height = line_count * text_size + 2 * padding;

        d.draw_rectangle(x, y, 200, rect_height, Color::new(0, 0, 0, 200));
        d.draw_rectangle_lines(x, y, 200, rect_height, Color::WHITE);

        for (i, line) in tooltip_text.lines().enumerate() {
            d.draw_text(line, x + padding, y + padding + i as i32 * text_size, text_size, Color::WHITE);
        }
    }

    pub fn toggle_inventory(&mut self) {
        self.inventory_open = !self.inventory_open;
    }
}