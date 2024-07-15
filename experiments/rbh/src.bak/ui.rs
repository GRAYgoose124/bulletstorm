use raylib::prelude::*;
use crate::game_state::GameState;

pub struct UserInterface;

impl UserInterface {
    pub fn new() -> Self {
        UserInterface
    }

    pub fn update_main_menu(&self, rl: &mut RaylibHandle, thread: &RaylibThread) -> bool {
        rl.is_key_pressed(KeyboardKey::KEY_ENTER)
    }

    pub fn update_game_over(&self, rl: &mut RaylibHandle, thread: &RaylibThread, score: u32) -> bool {
        rl.is_key_pressed(KeyboardKey::KEY_ENTER)
    }

    pub fn draw_main_menu(&self, d: &mut RaylibDrawHandle) {
        d.draw_text("ROGUELITE BULLET HELL", 100, 100, 40, Color::WHITE);
        d.draw_text("Press ENTER to start", 100, 200, 20, Color::GRAY);
    }

    pub fn draw_game_over(&self, d: &mut RaylibDrawHandle, score: u32) {
        d.draw_text("GAME OVER", 100, 100, 40, Color::WHITE);
        d.draw_text(&format!("Score: {}", score), 100, 200, 30, Color::WHITE);
        d.draw_text("Press ENTER to restart", 100, 300, 20, Color::GRAY);
    }

    pub fn draw_hud(&self, d: &mut RaylibDrawHandle, game_state: &GameState) {
        d.draw_text(&format!("Score: {}", game_state.score), 10, 10, 20, Color::WHITE);
        d.draw_text(&format!("Level: {}", game_state.level.level_number), 10, 40, 20, Color::WHITE);
        d.draw_text(&format!("Wave: {}/{}", game_state.level.wave_number, game_state.level.waves.len()), 10, 70, 20, Color::WHITE);
    }
}