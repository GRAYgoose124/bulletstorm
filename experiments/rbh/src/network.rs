use std::net::TcpStream;
use std::io::{Read, Write};
use serde::{Serialize, Deserialize};
use serde_json;
use crate::player::Player;
use crate::game::Game;

pub struct NetworkManager {
    stream: TcpStream,
}

#[derive(Serialize, Deserialize)]
pub struct PlayerState {
    pub id: u32,
    pub position: (f32, f32),
    pub health: f32,
}

#[derive(Serialize, Deserialize)]
pub struct BulletState {
    pub position: (f32, f32),
    pub velocity: (f32, f32),
    pub bullet_type: String,
}

#[derive(Serialize, Deserialize)]
pub struct EnemyState {
    pub id: u32,
    pub position: (f32, f32),
    pub enemy_type: String,
    pub health: f32,
}

#[derive(Serialize, Deserialize)]
pub struct GameState {
    pub players: Vec<PlayerState>,
    pub enemies: Vec<EnemyState>,
    pub bullets: Vec<BulletState>,
    pub wave: u32,
}

impl NetworkManager {
    pub fn new(address: &str) -> Self {
        let stream = TcpStream::connect(address).unwrap();
        NetworkManager { stream }
    }

    pub fn send_player_state(&mut self, player: &Player) {
        let state = PlayerState {
            id: player.id,
            position: (player.position.x, player.position.y),
            health: player.health,
        };
        let serialized = serde_json::to_string(&state).unwrap();
        self.stream.write_all(serialized.as_bytes()).unwrap();
    }

    pub fn receive_game_state(&mut self, game: &mut Game) {
        let mut buffer = [0; 4096];
        match self.stream.read(&mut buffer) {
            Ok(n) => {
                if n > 0 {
                    let serialized = String::from_utf8_lossy(&buffer[..n]);
                    if let Ok(game_state) = serde_json::from_str::<GameState>(&serialized) {
                        game.update_from_network(game_state);
                    }
                }
            }
            Err(e) => eprintln!("Failed to receive game state: {}", e),
        }
    }
}