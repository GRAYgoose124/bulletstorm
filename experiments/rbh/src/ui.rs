use raylib::prelude::*;
use std::ffi::CString;
use std::rc::Rc;
use std::cell::RefCell;

use crate::player::Player;
use crate::bullet::Bullet;
use crate::stats::GameStats;
use crate::item::{Item, ItemSlot};

use crate::WINDOW_HEIGHT;
use crate::WINDOW_WIDTH;

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

    pub fn draw(&mut self, d: &mut RaylibDrawHandle, player: &Rc<RefCell<Player>>, bullets: &Vec<Bullet>) {
        
        // Draw health bar
        let health_width = (player.borrow().health / player.borrow().stats.max_health * 200.0) as i32;
        d.draw_rectangle(10, WINDOW_HEIGHT - 30, health_width, 20, Color::GREEN);
        d.draw_rectangle_lines(10, WINDOW_HEIGHT - 30, 200, 20, Color::WHITE);

        // Draw active effects
        let mut effect_y = 10;
        for (effect_type, effect) in player.borrow().active_effects.clone() {
            let effect_text = format!("{:?}: {:.1}s", effect_type, effect.duration);
            d.draw_text(&effect_text, 10, effect_y, 20, Color::WHITE);
            effect_y += 25;
        }

        // Draw game stats
        d.draw_text(&format!("Wave: {}", self.wave), WINDOW_WIDTH - 150, 10, 20, Color::WHITE);
        d.draw_text(&format!("Enemies: {}", self.enemies_killed), WINDOW_WIDTH - 150, 35, 20, Color::WHITE);
        
        // draw n bullets
        d.draw_text(&format!("Bullets: {}", bullets.len()), WINDOW_WIDTH - 150, 60, 20, Color::WHITE);
        
        d.draw_fps(10, 10);

        // Draw inventory button
        if d.gui_button(Rectangle::new(WINDOW_WIDTH as f32 - 110.0, WINDOW_HEIGHT as f32 - 40.0, 100.0, 30.0), Some(CString::new("Inventory").unwrap().as_c_str())) {
            self.inventory_open = !self.inventory_open;
        }

        // Draw inventory and gear board if open
        if self.inventory_open {
            let mouse_position = d.get_mouse_position();
            self.draw_inventory(d, player, mouse_position);
            self.draw_gear_board(d, player);
        }
    }

    fn draw_inventory(&self, d: &mut RaylibDrawHandle, player: &Rc<RefCell<Player>>, mouse_position: Vector2) {
        let inventory_bg = Rectangle::new(10.0, 10.0, 200.0, WINDOW_HEIGHT as f32 - 20.0);
        d.draw_rectangle_rec(inventory_bg, Color::new(0, 0, 0, 200));
        d.draw_rectangle_lines_ex(inventory_bg, 2.0, Color::WHITE);

        for (i, item) in player.borrow_mut().inventory.get_items().iter().enumerate() {
            let item_rect = Rectangle::new(20.0, 20.0 + i as f32 * 30.0, 180.0, 25.0);
            d.draw_rectangle_rec(item_rect, Color::GRAY);
            d.draw_text(&item.name, 25, 25 + i as i32 * 30, 20, Color::WHITE);

            // Draw tooltip if mouse is over the item
            if item_rect.check_collision_point_rec(mouse_position) {
                self.draw_item_tooltip(d, item, mouse_position.x as i32, mouse_position.y as i32);
            }
        }
    }

    fn draw_gear_board(&self, d: &mut RaylibDrawHandle, player: &Rc<RefCell<Player>>) {
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

            if let Some(item) = player.borrow().equipped_items.get(&slot) {
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
}
    