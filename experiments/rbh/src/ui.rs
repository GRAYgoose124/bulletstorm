use raylib::prelude::*;
use crate::game::Game;
use crate::player::Player;
use crate::stats::GameStats;

use crate::WINDOW_HEIGHT;
use crate::WINDOW_WIDTH;

pub struct UI {
    wave: u32,
    enemies_killed: u32,
}

impl UI {
    pub fn new() -> Self {
        UI {
            wave: 0,
            enemies_killed: 0,
        }
    }

    pub fn update(&mut self, stats: GameStats) {
        self.wave = stats.wave;
        self.enemies_killed = stats.enemies_killed;
    }

    pub fn draw(&self, d: &mut RaylibDrawHandle, player: &Player) {
        // Draw health bar
        let health_width = (player.health / player.stats.max_health * 200.0) as i32;
        d.draw_rectangle(10, WINDOW_HEIGHT - 30, health_width, 20, Color::GREEN);
        d.draw_rectangle_lines(10, WINDOW_HEIGHT - 30, 200, 20, Color::WHITE);

        // Draw active effects
        let mut effect_y = 10;
        for (effect_type, effect) in &player.active_effects {
            let effect_text = format!("{:?}: {:.1}s", effect_type, effect.duration);
            d.draw_text(&effect_text, 10, effect_y, 20, Color::WHITE);
            effect_y += 25;
        }

        // Draw game stats
        d.draw_text(&format!("Wave: {}", self.wave), WINDOW_WIDTH - 150, 10, 20, Color::WHITE);
        d.draw_text(&format!("Enemies: {}", self.enemies_killed), WINDOW_WIDTH - 150, 35, 20, Color::WHITE);
    }
}