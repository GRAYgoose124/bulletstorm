use std::env;
use game::Game;
use network::NetworkManager;

mod player;
mod enemy;
mod bullet;
mod game;
mod ui;
mod inventory;
mod item;
mod stats;
mod network;

const WINDOW_WIDTH: i32 = 1280;
const WINDOW_HEIGHT: i32 = 720;

fn main() {
    let args: Vec<String> = env::args().collect();
    let is_multiplayer = args.contains(&"--multiplayer".to_string());

    let (mut rl, thread) = raylib::init()
        .size(WINDOW_WIDTH, WINDOW_HEIGHT)
        .title("Bullet Hell Game")
        .build();

    let mut game = Game::new(is_multiplayer);
    let mut network_manager = if is_multiplayer {
        Some(NetworkManager::new("127.0.0.1:8080"))
    } else {
        None
    };

    rl.set_target_fps(60);
    while !rl.window_should_close() {
        if let Some(ref mut nm) = network_manager {
            nm.send_player_state(&game.local_player.borrow());
            nm.receive_game_state(&mut game);
        }

        game.update(&rl);

        if game.is_game_over() {
            game.reset();
        }

        let mut d = rl.begin_drawing(&thread);
        game.draw(&mut d);
    }
}
