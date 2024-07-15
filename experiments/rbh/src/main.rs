mod player;
mod enemy;
mod bullet; 
mod game;

use game::Game;

const WINDOW_WIDTH: i32 = 800;
const WINDOW_HEIGHT: i32 = 600;


fn main() {
    let (mut rl, thread) = raylib::init()
        .size(WINDOW_WIDTH, WINDOW_HEIGHT)
        .title("Improved Bullet Hell Game")
        .build();

    let mut game = Game::new();

    rl.set_target_fps(144);

    while !rl.window_should_close() {
        game.update(&rl);

        if game.is_game_over() {
            game.reset();
        }

        let mut d = rl.begin_drawing(&thread);
        game.draw(&mut d);
    }
}