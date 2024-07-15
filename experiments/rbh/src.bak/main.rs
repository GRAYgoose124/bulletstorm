#![allow(unused_variables)]
#![allow(unused_imports)]

use raylib::prelude::*;

mod game_state;
mod player;
mod enemy;
mod bullet;
mod item;
mod level;
mod rendering;
mod audio;
mod ui;
mod physics;

use game_state::{GameState, Screen, GameEvent};
use rendering::Renderer;
use audio::{AudioManager, MusicTrack, SoundEffect};
use ui::UserInterface;

const WINDOW_WIDTH: i32 = 1280;
const WINDOW_HEIGHT: i32 = 720;

fn main() {
    let (mut rl, thread) = raylib::init()
        .size(WINDOW_WIDTH, WINDOW_HEIGHT)
        .title("Roguelite Bullet Hell")
        .vsync()
        .msaa_4x()
        .build();

    let mut game_state = GameState::new();
    let mut renderer = Renderer::new(&mut rl, &thread);
    let mut audio_manager = AudioManager::new(&mut rl);
    let ui = UserInterface::new();

    audio_manager.play_music(MusicTrack::MainMenu);

    rl.set_target_fps(60);

    while !rl.window_should_close() {
        let delta_time = rl.get_frame_time();

        match game_state.current_screen {
            Screen::MainMenu => {
                if ui.update_main_menu(&mut rl, &thread) {
                    game_state.start_new_game();
                    audio_manager.play_music(MusicTrack::GamePlay);
                }
            }
            Screen::GamePlay => {
                game_state.update(&mut rl, delta_time);
                
                if game_state.player.is_dead() {
                    game_state.current_screen = Screen::GameOver;
                    audio_manager.play_sound(SoundEffect::GameOver);
                    audio_manager.play_music(MusicTrack::MainMenu);
                }

                // Handle sound effects
                for event in game_state.events.drain(..) {
                    match event {
                        GameEvent::PlayerShoot => audio_manager.play_sound(SoundEffect::PlayerShoot),
                        GameEvent::EnemyShoot => audio_manager.play_sound(SoundEffect::EnemyShoot),
                        GameEvent::PlayerHit => audio_manager.play_sound(SoundEffect::PlayerHit),
                        GameEvent::EnemyDeath => audio_manager.play_sound(SoundEffect::EnemyDeath),
                        GameEvent::ItemPickup => audio_manager.play_sound(SoundEffect::ItemPickup),
                        GameEvent::LevelUp => audio_manager.play_sound(SoundEffect::LevelUp),
                    }
                }

                if game_state.level.is_boss_wave() && game_state.current_music != MusicTrack::Boss {
                    audio_manager.play_music(MusicTrack::Boss);
                } else if !game_state.level.is_boss_wave() && game_state.current_music != MusicTrack::GamePlay {
                    audio_manager.play_music(MusicTrack::GamePlay);
                }
            }
            Screen::GameOver => {
                if ui.update_game_over(&mut rl, &thread, game_state.score) {
                    game_state = GameState::new();
                    audio_manager.play_music(MusicTrack::MainMenu);
                }
            }
        }

        renderer.begin(&mut rl, &thread);
        match game_state.current_screen {
            Screen::MainMenu => ui.draw_main_menu(&mut renderer.handle.unwrap()),
            Screen::GamePlay => {
                renderer.draw_game(&game_state);
                ui.draw_hud(&mut renderer.handle.unwrap(), &game_state);
            }
            Screen::GameOver => ui.draw_game_over(&mut renderer.handle.unwrap(), game_state.score),
        }

        audio_manager.update();
    }
}